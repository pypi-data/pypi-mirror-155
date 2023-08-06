import os
from pathlib import Path
from typing import Literal
import requests
import yaml

from osu_apy_v2.database import Database
from osu_apy_v2.exceptions import ApiError, NotFound

BASE_URL = "https://osu.ppy.sh/api/v2"


class OsuApiV2:
    def __init__(self, client_id: int, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret

        self._config_yaml = Path("./osupy_storage/access_token.yaml").resolve()
        os.makedirs(self._config_yaml.parent, exist_ok=True)

        if not self._config_yaml.exists():
            with open(self._config_yaml, "+x") as f:
                yaml.dump({"token": ""}, f)

        with open(self._config_yaml) as f:
            cfg: dict = yaml.safe_load(f)

        if access_token := cfg.get("token", None):
            self._access_token = access_token
        else:
            self._access_token = self._refresh_access_token()

    def _refresh_access_token(self) -> str:
        data = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "client_credentials",
            "scope": "public",
        }
        res = requests.post("https://osu.ppy.sh/oauth/token", json=data)
        self._access_token = res.json()["access_token"]

        with open(self._config_yaml) as f:
            cfg: dict = yaml.safe_load(f)
        with open(self._config_yaml, "w") as f:
            cfg.update({"token": self._access_token})
            yaml.safe_dump(cfg, f)

        return self._access_token

    def get(self, endpoint: str) -> requests.Response:
        """performs a get request to the osu api v2 `enpoint`
        and handles refreshing the `access_token` automatically"""

        def do_get():
            return requests.get(
                BASE_URL + endpoint,
                headers={"Authorization": f"Bearer {self._access_token}"},
            )

        res = do_get()
        if not res.ok:
            self._refresh_access_token()
            res = do_get()
        if not res.ok:
            raise ApiError()
        return res

    def get_user_id(self, username: str) -> int:
        """returns the osu user id from local storage or via the osu api"""
        with Database() as db:
            if id := db.get_user_id(username):
                return id

        res = self.get(f"/search?mode=user&query={username}")
        for user in res.json()["user"]["data"]:
            if user["username"].lower() == username.lower():
                with Database() as db:
                    db.upsert_known_user(user["username"], user["id"])
                return user["id"]

        raise NotFound(username)

    def get_user_scores(
        self,
        user: "int | str",
        type_: Literal["best", "firsts", "recent"] = "best",
        include_fails: bool = False,
        mode: Literal["osu", "fruits", "mania", "taiko"] = "osu",
        limit: int = 1,
        offset: int = 0,
    ) -> requests.Response:
        if isinstance(user, str):
            user = self.get_user_id(user)
        return self.get(
            f"/users/{user}/scores/{type_}?include_fails={int(include_fails)}&mode={mode}&limit={limit}&offset={offset}"
        )

    def lookup_beatmap(self, id: int = None, checksum: str = None, filename: str = None) -> requests.Response:
        """https://osu.ppy.sh/docs/index.html?bash#lookup-beatmap"""
        query = "/beatmaps/lookup?"
        if c := checksum:
            query += f"checksum={c}&"
        if f := filename:
            query += f"filename={f}&"
        if id:
            query += f"id={id}"

        return self.get(query.rstrip("?&"))

    def get_beatmap(self, id: int) -> requests.Response:
        return self.get(f"/beatmaps/{id}")

    def get_user_beatmap_score(
        self, user: "str | int", beatmap: int, mode: Literal["osu", "fruits", "mania", "taiko"] = "osu", mods=None
    ):
        if isinstance(user, str):
            user = self.get_user_id(user)
        return self.get(f"/beatmaps/{beatmap}/scores/users/{user}?mode={mode}{f'&mods={mods}' if mods else ''}")

    def get_user_beatmap_scores(
        self, user: "str | int", beatmap: int, mode: Literal["osu", "fruits", "mania", "taiko"] = "osu"
    ):
        if isinstance(user, str):
            user = self.get_user_id(user)
        return self.get(f"/beatmaps/{beatmap}/scores/users/{user}/all?mode={mode}")
