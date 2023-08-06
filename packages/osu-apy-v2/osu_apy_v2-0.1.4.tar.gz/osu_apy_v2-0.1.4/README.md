handles refreshing the access_token and stores a mapping of known osu player names and ids in a sqlite database.\
read the [osu!api v2 Docs](https://osu.ppy.sh/docs/index.html)

```console
pip install osu-apy-v2
```

```py
from osu_apy_v2 import OsuApiV2

api = OsuApiV2(application_id, application_secret)
user_id = api.get_user_id("whitecat")
res = api.get(f"/users/{user_id}/scores/best?mode=osu&limit=1")
print(res.json())
```
