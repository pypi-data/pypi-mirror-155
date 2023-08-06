import math
import re
import os
import time

import requests
import logging
import configparser
import asyncio
from pathlib import Path
from typing import Text, List, Optional
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table
from pyppeteer import launch
from pyppeteer_stealth import stealth
from wukong.decorators import progressbar
from rich.panel import Panel
from rich.progress import Progress, BarColumn, SpinnerColumn, TimeRemainingColumn, TimeElapsedColumn


class RichProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks), title="⌛ Progress Frame", expand=False)


class ObtainYuQueDocs(object):
    """Get urls of all public docs of special account"""
    def __init__(
            self,
            token: Text = None,
            uid: Text = None,
            ):
        self.headers = {"X-Auth-Token": token}
        self.uid = uid
        self.log = logging.getLogger("YuQue")

        if not self.__check():
            raise Exception("Please configure correct API token!")

    def __check(self):
        """Check API token can access YuQue"""
        url = "https://www.yuque.com/api/v2/hello"

        res = requests.get(url, headers=self.headers)

        if res.status_code == 200:
            self.log.info("[green]Your API Token access YuQue successfully![/]", extra={"markup": True})
            return True
        else:
            self.log.warning("[red]Your API Token can not access YuQue successfully![/]", extra={"markup": True})
            return False

    def __get_repos(self) -> List[Text]:
        """Get all public repos of special account"""
        repo_api = f"https://www.yuque.com/api/v2/users/{self.uid}/repos"
        res = requests.get(repo_api, headers=self.headers).json()

        if 'data' in res:
            repos = [repo['slug'] for repo in res['data'] if repo['public'] == 1]
        else:
            repos = []

        return repos

    def get_docs(self) -> List[Text]:
        docs = []
        repos = self.__get_repos()

        for idx, repo in enumerate(repos):
            docs_api = f"https://www.yuque.com/api/v2/repos/{self.uid}/{repo}/docs"
            doc_url = "https://www.yuque.com/{uid}/{repo}/{doc_url}"
            res = requests.get(docs_api, headers=self.headers).json()

            if 'data' in res:
                docs_repo = [doc_url.format(uid=self.uid, repo=repo, doc_url=doc['slug'])
                            for doc in res['data'] if doc['public'] == 1]
                docs += docs_repo

        return docs


def init(args):
    """Initialize a project named YuQueAssistant"""
    if not os.path.exists("YuQueAssistant"):
        os.mkdir("./YuQueAssistant")

    yq_cfg = "./YuQueAssistant/yuque.cfg"

    if not os.path.exists(yq_cfg):
        with open(Path(__file__).parent.parent.parent / 'yuque.cfg', 'r', encoding='utf8') as f:
            with open(yq_cfg, 'w', encoding='utf8') as fw:
                fw.write(f.read())

    if not os.path.exists("./YuQueAssistant/data"):
        os.mkdir("./YuQueAssistant/data")

    if not os.path.exists("./YuQueAssistant/logs"):
        os.mkdir("./YuQueAssistant/logs")


def load_checked_docs(user: Text) -> List[Text]:
    """Load checked documents this account"""
    if not os.path.exists(f"./logs/{user}.csv"):
        return []

    with open(f"./logs/{user}.csv", 'r', encoding="utf8") as f:
        checked_docs = [line.replace("\n", "") for line in f.readlines() if line != '\n']

        return checked_docs


def load_data(qtype: Text) -> List[Text]:
    """Load info in data directory"""
    if not os.path.exists(f"./data/{qtype}.csv"):
        return []

    with open(f"./data/{qtype}.csv", 'r', encoding="utf8") as f:
        results = [line.replace("\n", "").split(",")[0] for line in f.readlines() if line != '\n']
        return results


def display_table_yuque_accounts(users_info: List[List[Text]]):
    """Display a table of YuQue accounts"""
    table = Table(title="YuQue Thumbs Up Accounts")

    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Account", style="magenta")
    table.add_column("Comment", justify="right", style="green")
    table.add_column("CheckedDocs", justify="right", style="red")

    for i, user_info in enumerate(users_info):
        table.add_row(str(i + 1), user_info[0], user_info[2], str(len(load_checked_docs(user_info[0]))))

    console = Console()
    console.print(table)


async def _like(user: Text, password: Text, docs: List[Text], num: int = 100):
    login_url = "https://www.yuque.com/login"
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
        ]
    })
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })
    await page.goto(login_url, options={'timeout': 60 * 1000})
    await page.type(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > form > div:nth-child(1) > div > div > span > div > span > input',
        user)
    await asyncio.sleep(2)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > div.login-more-warp > div > div.switch-login-warp > div > span')
    await page.type('#password', password)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > div.lark-login-protocol > label > span.ant-checkbox > input')
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > form > div:nth-child(4) > div > div > span > button')
    await asyncio.sleep(2)

    failed_docs = []
    checked_docs = load_checked_docs(user)
    skipped_docs = load_data("skipped_docs")
    like_docs = [doc for doc in docs if doc not in checked_docs and doc not in skipped_docs][:num]

    print(f"🔔 {user}: 共计 {len(like_docs)} 个文档")

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🎯Loading"
        task = progress.add_task(description, total=len(like_docs))

        for p, doc in enumerate(like_docs):
            await page.goto(doc, options={'timeout': 120 * 1000})
            await asyncio.sleep(2)

            try:
                await page.click('#content > div.article-content-reward.index-module_reward_QafG4 > div > div.like-module_larkLikeBtn_uHsxq > span')
                await asyncio.sleep(2)

                with open(f"./logs/{user}.csv", 'a+', encoding="utf8") as fw:
                    fw.write(doc + '\n')
                    checked_docs.append(doc)

                progress.update(task, completed=p + 1, description=description)
            except Exception as e:
                skipped_docs.append(doc)
                failed_docs.append(doc)

        print(f"{len(like_docs) - len(failed_docs)} documents have been thumbed up👍")

        if len(failed_docs) > 0:
            print(f"{len(failed_docs)} have not been thumbed up unsuccessfully: ")
            print("\n".join(failed_docs))


def like(args):
    """Thumbs up docs by other YuQue accounts"""
    log = logging.getLogger("ThumbsUp")
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.token and args.uid:
        token, uid = args.token, args.uid
    elif yq_cfg:
        token = cfg.get("core", "token")
        uid = cfg.get("self", "uid")
    else:
        raise Exception("Parameters `token` and `uid` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    docs = ObtainYuQueDocs(token=token, uid=uid).get_docs()

    if args.like_user and args.like_password:
        like_user, like_password = args.like_user, args.like_password

    elif yq_cfg:
        users = [[cfg.get(u, 'user'), cfg.get(u, 'password'), cfg.get(u, 'comment')]
                 for u in cfg.sections() if u.startswith("u")]
        log.info(f"You have [red]{len(users)}[/] accounts in yuque.cfg, and you have to choose one.",
                 extra={"markup": True})
        display_table_yuque_accounts(users)
        like_account_idx = IntPrompt.ask("Please Choose One YuQue Account Index to Thumbs up",
                                         choices=[str(i) for i in list(range(1, len(users) + 1))],
                                         show_choices=False)
        like_user, like_password, like_comment = users[like_account_idx - 1]

    else:
        raise Exception("You do not provide other accounts to thumbs up documents, "
                        "\n and specify this info in the command line."
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    num = args.num if args.num else 100

    asyncio.run(_like(like_user, like_password, docs, num))


async def _follow(user: Text, password: Text, num: int = 50):
    # TODO: 用户不存在的情况 404
    # num 不起作用
    login_url = "https://www.yuque.com/login"
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
            ]
        })
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    await page.setViewport({
        "width": 1920,
        "height": 1080
        })
    await page.goto(login_url, options={'timeout': 60 * 1000})
    await page.type('#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > form > div:nth-child(1) > div > div > span > div > span > input', user)
    await asyncio.sleep(2)
    await page.click('#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > div.login-more-warp > div > div.switch-login-warp > div > span')
    await page.type('#password', password)
    await page.click('#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > div.lark-login-protocol > label > span.ant-checkbox > input')
    await page.click('#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > form > div:nth-child(4) > div > div > span > button')
    await asyncio.sleep(2)

    users = load_data("users_info")
    follow_checkpoint_result = load_data("checkpoint_follow")
    follow_checkpoint = users.index(follow_checkpoint_result[0]) if follow_checkpoint_result else 0
    users_follow = users[follow_checkpoint:][:num]
    users_followed = load_data("users_followed")
    users_not_exists = load_data("users_not_exists")

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🔎 Loading"
        task = progress.add_task(description, total=len(users_follow))

        for p, user_follow in enumerate(users_follow):
            user_homepage = f"https://www.yuque.com/{user_follow}"

            if user_follow in users_followed:
                continue

            with open('./data/checkpoint_follow.csv', 'w', encoding='utf-8') as fw:
                fw.write(user_follow + "\n")

            res = await page.goto(user_homepage, options={'timeout': 120 * 1000})

            if res.status == 404:
                if user_follow not in users_not_exists:
                    with open('./data/users_not_exists.csv', 'a+', encoding='utf-8') as fw:
                        fw.write(user_follow + "\n")

                    users_not_exists.append(user_follow)

                continue

            try:
                status = await page.querySelectorAllEval('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div.ant-card.ant-card-bordered.larkui-card.UserInfo-module_container_VLLyp > div > div.UserInfo-module_head_VQt2K > div.user-info-btn > button > span',
                                                         'nodes => nodes.map(node => node.innerText)')

            except Exception as e:
                with open('./data/users_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_follow + "\n")
                    users_not_exists.append(user_follow)

                continue

            if status[0] == "关注":
                await page.click('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div.ant-card.ant-card-bordered.larkui-card.UserInfo-module_container_VLLyp > div > div.UserInfo-module_head_VQt2K > div.user-info-btn > button')
                await asyncio.sleep(2)
                progress.update(task, completed=p + 1, description=description)

                with open('./data/users_followed.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_follow + "\n")

                users_followed.append(user_follow)

            await asyncio.sleep(2)


def follow(args):
    """Follow other yuque users"""
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.user and args.password:
        user, password = args.user, args.password
    elif yq_cfg:
        user = cfg.get("self", "user")
        password = cfg.get("self", "password")
    else:
        raise Exception("Parameters `user` and `password` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    num = args.num if args.num else 50

    asyncio.run(_follow(user, password, num))


async def _unfollow(user: Text, password: Text):
    login_url = "https://www.yuque.com/login"
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
        ]
    })
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })
    await page.goto(login_url, options={'timeout': 60 * 1000})
    await page.type(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > form > div:nth-child(1) > div > div > span > div > span > input',
        user)
    await asyncio.sleep(2)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > div.login-more-warp > div > div.switch-login-warp > div > span')
    await page.type('#password', password)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > div.lark-login-protocol > label > span.ant-checkbox > input')
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > form > div:nth-child(4) > div > div > span > button')
    await asyncio.sleep(2)

    users_followed = load_data("users_followed")
    users_unfollowed = load_data("users_unfollowed")
    unfollow_checkpoint_result = load_data("checkpoint_unfollow")
    unfollow_checkpoint = users_followed.index(unfollow_checkpoint_result[0]) if unfollow_checkpoint_result else 0
    users_unfollow = users_followed[unfollow_checkpoint:]
    users_not_exists = load_data("users_not_exists")

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🔎 Loading"
        task = progress.add_task(description, total=len(users_unfollow))

        for p, user_unfollow in enumerate(users_unfollow):
            user_homepage = f"https://www.yuque.com/{user_unfollow}"

            if user_unfollow in users_unfollowed:
                continue

            with open('./data/checkpoint_unfollow.csv', 'w', encoding='utf-8') as fw:
                fw.write(user_unfollow + "\n")

            res = await page.goto(user_homepage, options={'timeout': 120 * 1000})

            if res.status == 404 and user_unfollow not in users_not_exists:
                with open('./data/users_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_unfollow + "\n")

            try:
                status = await page.querySelectorAllEval('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div.ant-card.ant-card-bordered.larkui-card.UserInfo-module_container_VLLyp > div > div.UserInfo-module_head_VQt2K > div.user-info-btn > button > span',
                                                         'nodes => nodes.map(node => node.innerText)')
            except Exception as e:
                with open('./data/users_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_unfollow + "\n")
                continue

            if status[0] == "已关注":
                await page.click('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div > div > div.UserInfo-module_head_VQt2K > div.user-info-btn > button')
                progress.update(task, completed=p + 1, description=description)
                await asyncio.sleep(2)

                with open('./data/users_unfollowed.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_unfollow + "\n")

            await asyncio.sleep(2)


def unfollow(args):
    """Unfollow other yuque users"""
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.user and args.password:
        user, password = args.user, args.password
    elif yq_cfg:
        user = cfg.get("self", "user")
        password = cfg.get("self", "password")
    else:
        raise Exception("Parameters `user` and `password` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    asyncio.run(_unfollow(user, password))


async def _comment(user: Text, password: Text, num: int = 50):
    """Comment other docs, not your own docs"""
    login_url = "https://www.yuque.com/login"
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
        ]
    })
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })
    await page.goto(login_url, options={'timeout': 60 * 1000})
    await page.type(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > form > div:nth-child(1) > div > div > span > div > span > input',
        user)
    await asyncio.sleep(2)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > div.login-more-warp > div > div.switch-login-warp > div > span')
    await page.type('#password', password)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > div.lark-login-protocol > label > span.ant-checkbox > input')
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > form > div:nth-child(4) > div > div > span > button')
    await asyncio.sleep(2)

    docs = load_data("users_docs")
    comment_checkpoint_result = load_data("checkpoint_comment")
    comment_checkpoint = docs.index(comment_checkpoint_result[0]) if comment_checkpoint_result else 0
    docs_comment = docs[comment_checkpoint:][:num]
    docs_commented = load_data("docs_commented")
    docs_not_exists = load_data("docs_not_exists")
    cnt = 0

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🔎 Loading"
        task = progress.add_task(description, total=len(docs_comment))

        for p, doc in enumerate(docs_comment):
            if doc in docs_commented:
                continue

            with open('./data/checkpoint_comment.csv', 'w', encoding='utf-8') as fw:
                fw.write(doc + "\n")

            res = await page.goto(doc, options={'timeout': 120 * 1000})

            if res.status == 404 and doc not in docs_not_exists:
                with open('./data/docs_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(doc + "\n")
                    docs_not_exists.append(doc)

            try:
                await page.type("#lark-mini-editor > div > div.ne-editor-body > div.ne-editor-wrap > div.ne-editor-wrap-content > div > div > div.ne-editor-box > div > div", "写的不错，值得学习😁！")
                time.sleep(2)
                await asyncio.sleep(2)
                # await page.click("#commentFloorContainer > div.index-module_commentEditor_yI7Ow > div > div > div > div.comments-form-wrapper > div.action.clearfix > button")
                await page.click("#main > div > div > div:nth-child(1) > div.DocReader-module_comment_eDglS > div > div > div.ReaderComment-module_commentFloorContainer_hYRys > div > div.index-module_commentEditor_yI7Ow > div > div > div > div.comments-form-wrapper > div.action.clearfix > button")
                await asyncio.sleep(2)

                progress.update(task, completed=p + 1, description=description)

                with open("./data/docs_commented.csv", 'a+', encoding="utf8") as fw:
                    fw.write(doc + "\n")
                    docs_commented.append(doc)

                cnt += 1
            except Exception as e:
                with open('./data/docs_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(doc + "\n")
                    docs_not_exists.append(doc)

                continue

    print(f"{cnt} documents have been commented!")


def comment(args):
    """Review other docs, not your own docs"""
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.user and args.password:
        user, password = args.user, args.password
    elif yq_cfg:
        user = cfg.get("self", "user")
        password = cfg.get("self", "password")
    else:
        raise Exception("Parameters `user` and `password` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    num = args.num if args.num else 50

    asyncio.run(_comment(user, password, num))


async def _note(user: Text, password: Text, num: int = 33):
    login_url = "https://www.yuque.com/login"
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
        ]
    })
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })
    await page.goto(login_url, options={'timeout': 60 * 1000})
    await page.type(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > form > div:nth-child(1) > div > div > span > div > span > input',
        user)
    await asyncio.sleep(2)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > div.login-more-warp > div > div.switch-login-warp > div > span')
    await page.type('#password', password)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > div.lark-login-protocol > label > span.ant-checkbox > input')
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > form > div:nth-child(4) > div > div > span > button')
    await asyncio.sleep(2)

    note_url = "https://www.yuque.com/dashboard/notes"
    await page.goto(note_url, options={'timeout': 60 * 1000})
    await asyncio.sleep(2)

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🔎 Loading"
        task = progress.add_task(description, total=num)

        for i in range(1, num + 1):
            await page.type(r'#mynote-container > div > div.index-module_leftSide_hjt\+x > div > div > div.index-module_editor_357aJ.index-module_singleMode_iaWgk.note-editor > div.lakex-note-editor.ne-doc-note-editor.ne-ui-scrollbar-visible > div > div.ne-editor-body > div.ne-editor-wrap > div.ne-editor-wrap-content > div > div > div.ne-editor-box > div > div', str(i))
            await asyncio.sleep(1)
            await page.keyboard.down("Control")
            await page.keyboard.press("Enter")
            await page.keyboard.up("Control")
            await asyncio.sleep(1)
            await page.click(r"#mynote-container > div > div.index-module_leftSide_hjt\+x > div > div > div.index-module_buttons_qrTUQ.index-module_singleMode_iaWgk > span > span.index-module_addButton_cBRrG > button")
            await asyncio.sleep(1)
            progress.update(task, completed=i, description=description)
            await asyncio.sleep(1)


def note(args):
    """Make notes"""
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.user and args.password:
        user, password = args.user, args.password
    elif yq_cfg:
        user = cfg.get("self", "user")
        password = cfg.get("self", "password")
    else:
        raise Exception("Parameters `user` and `password` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    num = args.num if args.num else 33

    asyncio.run(_note(user, password, num))


async def _search_users(user: Text, password: Text, num: int, spec_user: Optional[Text] = None):
    login_url = "https://www.yuque.com/login"
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
        ]
    })
    page = await browser.newPage()
    await stealth(page)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })
    await page.goto(login_url, options={'timeout': 60 * 1000})
    await page.type(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > form > div:nth-child(1) > div > div > span > div > span > input',
        user)
    await asyncio.sleep(2)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > div.login-more-warp > div > div.switch-login-warp > div > span')
    await page.type('#password', password)
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div.account-login.form-pro > div.lark-login-protocol > label > span.ant-checkbox > input')
    await page.click(
        '#ReactApp > div > div.lark.page-account.lark-login > div > div > div > div > div.lark-form-content.form-pro > div > form > div:nth-child(4) > div > div > span > button')
    await asyncio.sleep(2)

    users = load_data("users_info")
    users_checked = load_data("checked_users")
    checkpoint_search_result = load_data("checkpoint_user")
    checkpoint_search = users.index(checkpoint_search_result[0]) if checkpoint_search_result else 0
    users_search = users[checkpoint_search:][:num]

    if spec_user:
        users.append(spec_user)

        with open('./data/users_info.csv', 'a+', encoding='utf-8') as fw:
            fw.write(spec_user + '\n')

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🔎 Loading"
        task = progress.add_task(description, total=len(users_search))

        for p, user_search in enumerate(users_search):
            if user_search in users_checked:
                continue

            with open('data/checkpoint_user.csv', 'w', encoding='utf-8') as fw:
                fw.write(user_search + "\n")

            user_followers = f"https://www.yuque.com/{user_search}?tab=followers"
            resp = await page.goto(user_followers, options={'timeout': 120 * 1000})
            await page.keyboard.press("ArrowDown")

            if resp.status == 404:
                with open('./data/users_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_search + "\n")
                continue

            try:
                followers_following_num = await page.querySelectorAllEval('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div.ant-card.ant-card-bordered.larkui-card.UserInfo-module_container_VLLyp > div > div.UserInfo-module_head_VQt2K > div.UserInfo-module_followInfo_kTr87 > a', 'nodes => nodes.map(node => node.innerText)')
                followers_num = int(re.findall(r'\d+', followers_following_num[0])[0])
                followings_num = int(re.findall(r'\d+', followers_following_num[1])[0])

            except Exception as e:
                with open('./data/users_not_exists.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_search + "\n")
                continue

            if followers_num >= 10000 or followings_num >= 10000:
                with open('./data/users_spec.csv', 'a+', encoding='utf-8') as fw:
                    fw.write(user_search + "\n")
                continue

            desc = await page.querySelectorAllEval('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div > div > div.UserInfo-module_head_VQt2K > div.UserInfo-module_info_mSJna > div',
                                                   'nodes => nodes.map(node => node.innerText)')
            desc = desc[1]

            addr_occ = await page.querySelectorAllEval('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div > div > div.UserInfo-module_detail_JtTf0 > p',
                                                       'nodes => nodes.map(node => node.innerText)')

            addr = "" if addr_occ[0] == "未填写" else addr_occ[0]
            occ = "" if len(addr_occ) <= 1 else addr_occ[0]

            docs_thumbsup_num = await page.querySelectorAllEval('#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-8.ant-col-md-7 > div > div > div.Social-module_social_jQI6Q > p',
                                                                'nodes => nodes.map(node => node.innerText)')

            docs_num, thumbsup_num = re.findall('\d+', docs_thumbsup_num[0])[0], re.findall('\d+', docs_thumbsup_num[1])[0]

            if followers_num != 0:
                if followers_num > 20:
                    loop1 = math.ceil((followers_num - 20) / 20)

                    loop1_ = 0
                    while loop1_ != loop1:
                        try:
                            await page.click("#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-17 > div > div.ant-card-body > div > div.larkui-list-block-more > a")
                            loop1_ += 1
                            await page.keyboard.press("PageDown")

                        except Exception:
                            await page.goto(user_followers.format(user=user), options={'timeout': 120 * 1000})
                            loop1_ = 0

                        await asyncio.sleep(2)

                followers_frame = await page.xpath('//*[@id="ReactApp"]/div[5]/div[2]/div/div/div[2]/div/div[2]/div/div/div/ul/li')

                # Get users who follow this YuQue user
                for follower_frame in followers_frame:
                    follower_content = await follower_frame.querySelectorAllEval('div > a', 'nodes => nodes.map(node => node.href)')
                    follower = follower_content[0].split("/")[-1]

                    if follower not in users:
                        users.append(follower)

                        with open('./data/users_info.csv', 'a+', encoding='utf-8') as fw:
                            fw.write(follower + "\n")

                    with open('./data/users_graph.csv', 'a+', encoding='utf-8') as fw:
                        fw.write(follower + "," + user_search + "\n")

                await asyncio.sleep(2)

            if followings_num != 0:
                user_followings = f"https://www.yuque.com/{user_search}?tab=following"
                await page.goto(user_followings, options={'timeout': 120 * 1000})
                await page.keyboard.press("ArrowDown")

                if followings_num > 20:
                    loop2 = math.ceil((followings_num - 20) / 20)

                    loop2_ = 0
                    while loop2_ != loop2:
                        try:
                            await page.click("#ReactApp > div.lark > div.main-wrapper > div > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-17 > div > div.ant-card-body > div > div.larkui-list-block-more > a")
                            loop2_ += 1
                            await page.keyboard.press("PageDown")
                        except Exception as e:
                            await page.goto(user_followings, options={'timeout': 120 * 1000})
                            loop2_ = 0

                        await asyncio.sleep(2)

                followings_frame = await page.xpath('//*[@id="ReactApp"]/div[5]/div[2]/div/div/div[2]/div/div[2]/div/div/div/ul/li')

                for following_frame in followings_frame:
                    following_content = await following_frame.querySelectorAllEval('div > a', 'nodes => nodes.map(node => node.href)')
                    following = following_content[0].split("/")[-1]

                    if following not in users:
                        users.append(following)

                        with open('./data/users_info.csv', 'a+', encoding='utf-8') as fw:
                            fw.write(following + "\n")

                    with open('./data/users_graph.csv', 'a+', encoding='utf-8') as fw:
                        fw.write(user_search + "," + following + "\n")

            with open('./data/checked_users.csv', 'a+', encoding='utf-8') as fw:
                line = ",".join([user, str(followers_num), str(followings_num), docs_num, thumbsup_num, addr, occ, desc])
                fw.write(line + "\n")

            progress.update(task, completed=p + 1, description=description)
            await asyncio.sleep(2)


def search_users(args):
    """Search YuQue users"""
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.user and args.password:
        user, password = args.user, args.password
    elif yq_cfg:
        user = cfg.get("self", "user")
        password = cfg.get("self", "password")
    else:
        raise Exception("Parameters `user` and `password` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    num = args.num if args.num else 1000

    asyncio.run(_search_users(user, password, num))


def search_docs(args):
    yq_cfg = os.path.exists("./yuque.cfg")
    cfg = configparser.ConfigParser()

    if yq_cfg:
        cfg.read("./yuque.cfg")

    if args.token and args.uid:
        token, uid = args.token, args.uid
    elif yq_cfg:
        token = cfg.get("core", "token")
    else:
        raise Exception("Parameters `token` and `uid` must be provided if you don't have yuque.cfg file. "
                        "\n You can also run `wukong yuque init` to generate a yuque.cfg, then complete it.")

    num = args.num if args.num else 1000

    users = load_data("users_info")
    users_searched = load_data("users_searched")
    checkpoint_search_result = load_data("checkpoint_search")
    checkpoint_search = users.index(checkpoint_search_result[0]) if checkpoint_search_result else 0
    users_search = users[checkpoint_search:][:num]

    with RichProgress(
            "[progress.description]{task.description}({task.completed}/{task.total})",
            SpinnerColumn(finished_text="🚀"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.2f}%",
            SpinnerColumn(spinner_name="clock", finished_text="🕐"),
            TimeElapsedColumn(),
            "⏳",
            TimeRemainingColumn()) as progress:

        description = "[red]🔎 Loading"
        task = progress.add_task(description, total=len(users_search))

        for p, user_search in enumerate(users_search):
            if user_search in users_searched:
                continue

            with open('./data/checkpoint_search.csv', 'w', encoding='utf-8') as fw:
                fw.write(user_search + "\n")

            docs = ObtainYuQueDocs(token, user_search).get_docs()

            with open('./data/users_searched.csv', 'a+', encoding='utf-8') as fw:
                fw.write(user_search + "\n")

            with open('./data/users_docs.csv', 'a+', encoding='utf-8') as fw:
                for doc in docs:
                    fw.write(doc + "\n")

            progress.update(task, completed=p + 1, description=description)
