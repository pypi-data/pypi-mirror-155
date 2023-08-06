import requests
import json
import logging
import base64
import hashlib
from typing import Text, List, Dict


class WebComRobot(object):
    def __init__(
            self,
            key: Text = None,
            content: Text = None,
            markdown: bool = False,
            image: Text = None,
            articles: List = None,
            file: Text = None,
            at_all: bool = False,
            mentioned_mobile_list: List[Text] = None):
        self.webhook = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
        self.upload_hook = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
        self.markdown = markdown
        self.headers = {
            "Content-Type": "application/json;text/plain;charset=UTF-8",
            "Accept": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.79 Safari/537.36 "
            }
        self.content = content
        self.image = image
        self.articles = articles
        self.file = file
        self.at_all = at_all
        self.mentioned_mobile_list = mentioned_mobile_list
        self.log = logging.getLogger("WebComRobot")

        elem_types = sum([e is None for e in [content, image, articles, file]])

        if elem_types > 1:
            self.log.warning(
                (
                    "You provide different types of messages to send, "
                    "robot can only send one type message each time! \n"
                    "Message type priority is: [red]markdown > message > image > articles > file[/]"
                )
                , extra={"markup": True})

        if markdown:
            self.payload = self.__messages_md()
        elif content:
            self.payload = self.__messages()
        elif image:
            self.payload = self.__image()
        elif articles:
            self.payload = self.__news()
        elif file:
            self.payload = self.__file()
        else:
            self.payload = {}

    def __messages(self) -> Dict:
        payload = {
            "msgtype": "text",
            "text": {
                "mentioned_mobile_list": ["@all"] if self.at_all else (
                        self.mentioned_mobile_list if self.mentioned_mobile_list else []),
                "content": self.content
                }
            }
        return payload

    def __messages_md(self) -> Dict:
        """Send messages in markdown format."""
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": self.content
                }
            }
        return payload

    def __image(self) -> Dict:
        """Send an image"""
        with open(self.image, "rb") as img:
            img_ = img.read()
            base64_ = str(base64.b64encode(img_), encoding='utf-8')
            md = hashlib.md5()
            md.update(img_)
            md5_ = md.hexdigest()

        payload = {
            "msgtype": "image",
            "image": {
                "base64": base64_,
                "md5": md5_,
                }
            }

        return payload

    def __news(self) -> Dict:
        """Send news with links"""
        payload = {
            "msgtype": "news",
            "news": {
                "articles": self.articles
                }
            }

        return payload

    def __file(self) -> Dict:
        """Send a file"""
        def _upload_file():
            with open(self.file, "rb") as fp:
                data = {"file": fp}
                res = requests.post(self.upload_hook, files=data)
                media_id = res.json()["media_id"]

                return media_id

        media_id = _upload_file()
        payload = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        return payload

    def send(self) -> bool:
        res = requests.post(self.webhook, json=self.payload, headers=self.headers, verify=False)

        if json.loads(res.text)["errmsg"] == "ok":
            self.log.info("WebComRobot send message [green]successfully[/]", extra={"markup": True})
            return True
        else:
            self.log.info("WebComRobot send message [red]failed[/]", extra={"markup": True})
            return False


def send_messages(
        key: Text = None,
        content: Text = None,
        at_all: bool = False,
        mentioned_mobile_list: List[Text] = None
        ):
    robot = WebComRobot(key=key, content=content, at_all=at_all, mentioned_mobile_list=mentioned_mobile_list)
    robot.send()


def send_messages_md(key: Text = None, content: Text = None):
    robot = WebComRobot(key=key, content=content, markdown=True)
    robot.send()


def send_image(key: Text = None, image: Text = None):
    robot = WebComRobot(key=key, image=image)
    robot.send()


def send_images(key: Text = None, images: List[Text] = None):
    for image in images:
        send_image(key=key, image=image)


def send_news(key: Text = None, articles: List = None):
    robot = WebComRobot(key=key, articles=articles)
    robot.send()


def send_file(key: Text = None, file: Text = None):
    robot = WebComRobot(key=key, file=file)
    robot.send()


def send_files(key: Text = None, files: List[Text] = None):
    for file in files:
        send_file(key=key, file=file)
