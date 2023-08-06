# coding: utf8
import re
import time
import logging
import pandas as pd
from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
from typing import Dict, Text, List
from impala.hiveserver2 import HiveServer2Connection, HiveServer2Cursor
from impala.dbapi import connect
from impala.util import as_pandas
from wukong.decorators import retry, progressbar


class ImpalaRunner(object):
    def __init__(
            self,
            db_config: Dict = None,
            sql_file: Text = None,
            context: Dict = None,
            verbose: bool = True,
            retry_times: int = 5,
            sleep_time: int = 60
            ) -> None:
        self.db_config = db_config
        self.sql_file = sql_file
        self.context = context
        self.verbose = verbose
        self.retry_times = retry_times
        self.sleep_time = sleep_time
        self.log = logging.getLogger("Impala")
        self.console = Console()
        self.conn = self.__create_conn()
        self.sqls = self.__parse_sqlfile() if sql_file else {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close_conn()
        self.log.info("Impala Connection has been closed!")

    def __create_conn(self) -> HiveServer2Connection:
        """Create a connection for Impala database according to db_config"""
        @retry(retry_times=self.retry_times, sleep_time=self.sleep_time)
        def _create_conn():
            host = self.db_config["host"]
            port = self.db_config["port"]
            user = self.db_config["user"]
            password = self.db_config["password"]
            auth_mechanism = self.db_config["auth_mechanism"]

            conn = None

            if isinstance(host, Text):
                conn = connect(
                            host=host,
                            port=port,
                            user=user,
                            password=password,
                            auth_mechanism=auth_mechanism,
                            timeout=60)
            elif isinstance(host, List):
                for h in host:
                    try:
                        conn = connect(
                                    host=h,
                                    port=port,
                                    user=user,
                                    password=password,
                                    auth_mechanism=auth_mechanism,
                                    timeout=60)
                        break
                    except Exception as e:
                        self.logging.err(e)
            else:
                self.log.exception("[bold green]`host`[/] type must be [red]str[/] or [red]list[/]",
                                extra={"markup": True})

            if conn is None:
                self.log.Exception("Can not connect Impala Database with db_config")

            return conn

        return _create_conn()

    def __close_conn(self):
        self.conn.close()

    def __check_sqlfile_health(self):
        with open(self.sql_file, "r", encoding="utf8") as f:
            file_content = f.read().replace("${", "{")

        titles = re.findall("--\[(.*?)\]", file_content)

        if len(titles) == 0:
            self.log.warning(f"[bold red]{self.sql_file}[/] contains no title!", extra={"markup": True})
            return 0

        elif 'end' not in titles:
            self.log.warning(
                (
                    f"[bold red]{self.sql_file}[/] contains {len(titles)} title, "
                    f"and use --\[title] format without --\[end]!"
                ), extra={"markup": True})
            return 1
        else:
            end_num = titles.count('end')
            title_num = len(titles) - end_num

            if title_num == end_num:
                self.log.info(
                    (
                        f"[bold red]{self.sql_file}[/] contains {title_num} titles, "
                        f"and contains {end_num} --\[end]!"
                    ), extra={"markup": True})
                return 2
            else:
                self.log.exception(
                    (
                        f"[bold red]{self.sql_file}[/] contains {title_num} titles, "
                        f"but contains {end_num} --\[end]. Please Check First!"
                    ), extra={"markup": True})
                raise Exception(f"--\[title] is not same size as --\[end]")

    def __parse_sqlfile(self):
        with open(self.sql_file, "r", encoding="utf8") as f:
            file_content = self.__format_sql(f.read())

        check_sqlfile_health = self.__check_sqlfile_health()

        if check_sqlfile_health == 0:
            file_content = re.sub('\n{2,}', '\n', re.sub('--.*?\n', '', file_content))
            sqls = {"exec_sql": file_content} if file_content != '\n' else {}

        elif check_sqlfile_health == 1:
            titles = re.findall("--\[(.*?)\]\n", file_content)
            blocks_sql = [re.sub('\n{2,}', '\n', re.sub('--.*?\n', '', s)) for s in re.split("--\[.*?\]\n", file_content) if s != ""]
            sqls = dict(zip(titles, blocks_sql))
        else:
            pat = r"--\[(.*?)\](.*?)\n--\[end\]"
            sqls = dict([(title, self.__format_sql(re.sub('\n{2,}', '\n', re.sub('--.*?\n', '', block_sql))))
                        for title, block_sql in re.findall(pat, file_content, re.S) if block_sql != ""])

        return sqls

    def get_sqls(self):
        pass

    def __format_sql(self, sql: Text = None, context: Dict = None) -> Text:
        """Formatted query sql with parameters in context.
        :param sql: str, Query SQL
        :return: str, Formatted SQL
        """
        def _upper_sql_keywords(sql: Text = None):
            keywords = [
                # phrases
                'alter table', 'anti join', 'add columns', 'as bigint', 'as float',  'as double',
                'as string', 'as tinyint', 'as decimal', 'as int',
                'create table', 'create external table', 'create database ', 'create view ',
                'compute stats ', 'change column ', 'case when',
                'describe formatted', 'drop database', 'drop table', 'drop schema ',
                'end as', 'escaped by',
                'fields terminated by',
                'group by ',
                'inner join', 'insert table', 'insert overwrite', 'insert overwrite into',
                'insert overwrite table', 'insert into ',  'insert into table',
                'if exists ', 'if not exists ', 'invalidate metadata ', 'is true', 'is false',
                'not like', 'not in', 'not exists',
                'left join', 'load data inpath ',
                'order by ',
                'partition by',
                'row format delimited', 'right join', 'row_number() over(', 'rename to ',
                'replace columns',
                'show tables', 'show databases', 'show partitions', 'show create table',
                'show stats', 'select user()', 'select current_database()', 'select current_timestamp()',
                'stored as', 'stored as textfile', 'stored as parquet', 'select version()',
                'set location ', 'set serdeproperties('
                'union all',
                'with serdeproperties',
                '= true', '= false', ', true, false)', ', false, , true)',
                ' int,', ' bigint,', ' float,', ' double,', '  tinyint,', ' timestamp,', ' date,', ' string,',

                # keywords
                ' as ', ' and ', ' between ', ' desc',  'explain ', 'else ', 'false', 'from ', 'null', 'not',
                'having ', ' in ', 'interval ', ' is ', ' like ', 'limit ', 'location ', ' or ', 'offset ', 'on ',
                'overwrite ', 'set ', 'truncate ', ' then ', 'use ', 'union ', 'update ', 'where ', 'with ',
                'select ', '[shuffle]', 'refresh ', 'rename ', 'role ', 'roles ', ' schema ', 'commit ',
                'distinct ', 'describe ', 'delete ',
                ' bigint', ' double', ' int', ' float',  ' tinyint', ' timestamp', 'date', ' string',
                ' numeric',' true', ' false'

                # functions
                'add(',  'avg(', 'add_months(', "adddate(", 'abs(', 'ascii(', 'btrim(',
                'cast(', 'ceil(',   'count(', 'cos(', 'ceiling(',  'concat(', 'concat_ws(', 'chr(', 'char_length(',
                'div(', 'decimal(', 'dense_rank(', 'date_add(', 'date_sub(', 'datediff(', 'day（', 'dayname(',
                'dayofmonth(', 'dayofweek(', 'dayofyear(', 'days_add(', 'days_sub(',
                'floor(', 'from_timestamp(', 'from_unixtime(', 'from_utctime(', 'group_concat(',
                'hour(', 'hours_add(', 'hours_sub(', 'if(', ' isnull(', 'ifnull(', 'isfalse(', 'istrue(', 'json_object(',
                'lead(', 'lag(', 'log(', 'length(', 'lower(', 'locate(', 'lcase(', 'lpad(', 'ltrim(',
                'max(', 'min(', 'month(', 'minute(', 'minutes_add(', 'minutes_sub(', 'microseconds_add(', 'microseconds_sub(',
                'millisecond(', 'millisecond_add(', 'millisecond_sub(', 'months_add(', 'months_sub(', 'months_between(', 'mod(',
                'ndv(', 'nullif(', 'nullifzero(', 'now()',
                'over(', 'to_date(', 'to_timestamp(', 'to_utc_timestamp(',
                'percent_rank(', 'partition(', 'power(', 'pow(', 'pid(', 'parse_url(', 'period(',
                'row_number(', 'regexp(', 'regexp_like(', 'regexp_replace(', 'regexp_extract(',
                'rank(', 'round(', 'random(', 'rand(', 'replace(', 'reverse(', 'rpad(', 'rtrim(',
                'sum(', 'second(', 'seconds_add(', 'seconds_sub(', 'subdate(', 'sqrt(', 'sign(', 'substr(', 'substring(',
                'split_part(', 'strleft(', 'strright(', 'timeofday(', 'trunc(', 'typeof(',
                'unix_timestamp(', 'utc_timestamp(', 'uuid(', 'upper(', 'ucase(', 'values(', 'value(',
                'weekofyear(', 'weaks_add(', 'weaks_sub(', 'year(', 'years_add(', 'years_sub(', 'zeroifnull(',
                ]

            for kw in keywords:
                sql = sql.replace(kw, kw.upper())

            return sql

        formatted_sql = _upper_sql_keywords(sql.strip().replace("${", "{").replace("  ", " "))

        if context:
            formatted_sql = formatted_sql.format_map(context)

        elif self.context:
            formatted_sql = formatted_sql.format_map(self.context)

        return formatted_sql

    @staticmethod
    def __verify_df(df: pd.DataFrame = None) -> pd.DataFrame:
        """Update Dataframe columns"""
        if df is None:
            raise Exception("Parameter `df` can not be None!")

        df.columns = [col.rsplit('.', 1)[-1] for col in df.columns]

        # update columns type
        for col in df.columns:
            series = df[col][df[col].notnull()]

            if not series.empty:
                if type(series.iloc[0]).__name__ == 'Decimal':
                    df[col] = df[col].astype(float)
                if type(series.iloc[0]).__name__ == 'Timestamp':
                    df[col] = df[col].astype(str)

        return df

    def __cursor_to_df(self, cursor: HiveServer2Cursor) -> pd.DataFrame:
        """Fetch all records with cursor."""
        data = cursor.description

        if data is not None and hasattr(data, '__iter__'):
            names = [metadata[0] for metadata in data]
            df = as_pandas(cursor)
            df.columns = names
        else:
            df = pd.DataFrame()

        df = self.__verify_df(df)

        return df

    @progressbar
    def __display_progress(self, cursor: HiveServer2Cursor) -> HiveServer2Cursor:

        p, total, state = 0, 100, False
        yield total

        while p < 90 or not state:
            state = True if cursor.status() == "FINISHED_STATE" else False
            p = int(re.findall(r"(\d+)%", cursor.get_log(), re.S)[0]) if cursor.get_log() != "" else 0
            time.sleep(0.05)
            yield p

        else:
            yield total

        return cursor

    def run_sql(self, sql: Text = None, context: Dict = None) -> pd.DataFrame:
        if context:
            sql = self.__format_sql(sql, context)

        @retry(retry_times=self.retry_times, sleep_time=self.sleep_time)
        def _run_sql() -> pd.DataFrame:
            """Execute One SQL"""
            cur = self.conn.cursor()

            if sql.replace(" ", "") == "":
                self.log.info("Executed sql is empty!")
                cur.close()
                return pd.DataFrame()

            else:
                self.log.info("Executing the following SQL...")
                executing_sql = Syntax(code=sql, lexer="mysql", line_numbers=True, indent_guides=True)
                self.console.print(executing_sql)

                if not self.verbose:
                    cur.execute(sql)
                else:
                    cur.execute_async(sql)
                    time.sleep(2)
                    self.__display_progress(cur)

            df = self.__cursor_to_df(cur)
            cur.close()

            return df
        return _run_sql()

    def run_sql_block(self, title: Text = None) -> pd.DataFrame:
        if len(self.sqls) == 0:
            self.log.warning(
                "You can not use [green]run_sql_block[/] function, because [red]sql_file[/] not provided or empty,"
                "\n and you can use [green]run_sql[/] function to just execute one sql!", extra={"markup": True})
            raise Exception(f"Please provide sql_file or use run_sql function!")
        if len(self.sqls) == 1:
            title = "exec_sql"

        @retry(retry_times=self.retry_times, sleep_time=self.sleep_time)
        def _run_sql_block() -> pd.DataFrame:
            if title is not None:
                exec_sqls = self.sqls.get(title)
                results = [self.run_sql(sql) for sql in exec_sqls.split(";")]
            else:
                results = []

                for exec_sqls in self.sqls.values():
                    results += [self.run_sql(sql) for sql in exec_sqls.split(";")]

            results = [res for res in results if not res.empty]
            df = results[-1] if results else None

            return df

        return _run_sql_block()


def impala_to_df(
        db_config: Dict = None,
        sql: Text = None,
        context: Dict = None,
        verbose: bool = True,
        retry_times: int = 5,
        sleep_time: int = 60) -> pd.DataFrame:
    log = logging.getLogger("impala_to_df")

    if not sql.strip().replace("\n", "").upper().startswith("SELECT"):
        log.warning(
            "This SQL is not a query, so you will not get a Dataframe, "
            "but this sql will be executed in fact!")

    with ImpalaRunner(
            db_config=db_config,
            verbose=verbose,
            retry_times=retry_times,
            sleep_time=sleep_time) as runner:
        df = runner.run_sql(sql, context)

    return df

def impala_run_sqlfile(
        db_config: Dict = None,
        sql_file: Text = None,
        context: Dict = None,
        titles: List = None,
        verbose: bool = True,
        retry_times: int = 5,
        sleep_time: int = 60) -> pd.DataFrame:

    with ImpalaRunner(
            db_config=db_config,
            sql_file=sql_file,
            context=context,
            verbose=verbose,
            retry_times=retry_times,
            sleep_time=sleep_time) as runner:

        for title in titles:
            df = runner.run_sql_block(title=title)

    return df


def df_to_impala():
    pass