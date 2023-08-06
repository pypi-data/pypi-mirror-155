from datetime import datetime
import sqlite3
from time import sleep
from typing import List, Tuple


class UnifiedBuffer:
    def __init__(self, db_path: str, env_name: str, n_workers: int):
        self.db_path = db_path
        self.env_name = env_name
        self.n_workers = n_workers
        # === Create Tables ===
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        # Phase: "node?_phase?" (? is from 0)
        create_actions_table_sql = '''CREATE TABLE IF NOT EXISTS Actions (
            Aid INTEGER primary key AUTOINCREMENT,    
            EnvName VARCHAR(100),
            NoUpdate INTEGER,
            Phase VARCHAR(100),
            GreenTime INTEGER,
            Time TIMESTAMP);'''
        create_updates_table_sql = '''CREATE TABLE IF NOT EXISTS Updates (
            Uid INTEGER primary key AUTOINCREMENT,    
            EnvName VARCHAR(100),
            No INTEGER,
            Time TIMESTAMP);'''
        cur.execute(create_actions_table_sql)
        cur.execute(create_updates_table_sql)
        conn.commit()
        cur.close()
        conn.close()

    def update(self, update_no, data: List[Tuple[str, int, str, int, datetime]]):
        """
        :param update_no:
        :param data: List of [env_name, update_no, phase_name, green_time, time]
        :return: None
        """
        assert len(data) > 0
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.executemany('INSERT INTO Actions(EnvName,NoUpdate,Phase,GreenTime,Time) VALUES(?,?,?,?,?);', data)
        c.execute('INSERT INTO Updates(EnvName, No, Time) VALUES(?,?,?);', (self.env_name, update_no, datetime.now()))
        conn.commit()
        conn.close()

    def get_last(self, n_latest_data: int) -> List:
        """

        :param n_latest_data:
        :return: List of (phase_name, green_time)
        """
        assert n_latest_data > 0
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT Phase,GreenTime FROM Actions ORDER BY Time DESC LIMIT ?;", (n_latest_data,))
        rows = c.fetchall()
        conn.commit()
        conn.close()
        return rows

    def get_by_update_no(self, update_no: int) -> List:
        """

        :param update_no:
        :return: List of (phase_name, green_time)
        """
        assert update_no >= 0
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT Phase,GreenTime FROM Actions WHERE NoUpdate=?", (update_no,))
        rows = c.fetchall()
        conn.commit()
        conn.close()
        return rows

    def wait(self, update_no, sleep_sec=0.5):
        while True:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "SELECT COUNT(DISTINCT EnvName) FROM Updates WHERE No=?;",
                (update_no,))
            ret_row = c.fetchone()
            assert ret_row is not None, f'There is no any row achieve this update no.'
            n_workers_achieve_this_update_no = ret_row[0]
            conn.commit()
            conn.close()
            if n_workers_achieve_this_update_no == self.n_workers:
                break
            sleep(sleep_sec)
