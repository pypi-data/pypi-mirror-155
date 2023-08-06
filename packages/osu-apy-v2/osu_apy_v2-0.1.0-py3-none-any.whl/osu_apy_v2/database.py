import sqlite3


class Database:
    def __init__(self) -> None:
        self.con = sqlite3.connect("./osupy_storage/osu_apy.db")
        self.cur = self.con.cursor()

    def __enter__(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS known_user (
                id      INTEGER  PRIMARY KEY  AUTOINCREMENT,
                name    TEXT     NOT NULL     UNIQUE         COLLATE NOCASE,
                osu_id  INTEGER  NOT NULL     UNIQUE
            )
            """
        )
        self.con.commit()
        return self

    def __exit__(self, *_):
        self.con.close()

    def upsert_known_user(self, name: str, id: int):
        try:
            self.cur.execute(
                f"""
                INSERT INTO known_user(name, osu_id) 
                VALUES ('{name}', {id})
                ON CONFLICT (osu_id)
                DO UPDATE SET name = '{name}'
                """
            )
        except sqlite3.IntegrityError:
            print(f"{name}[{id}] already exists")
        self.con.commit()

    def get_user_id(self, name: str) -> "int | None":
        self.cur.execute(f"SELECT osu_id FROM known_user WHERE name = '{name}'")
        res = self.cur.fetchone()
        return None if not res else res[0]

    def get_user_name(self, id: int) -> "str | None":
        self.cur.execute(f"SELECT name FROM known_user WHERE osu_id = {id}")
        res = self.cur.fetchone()
        return None if not res else res[0]
