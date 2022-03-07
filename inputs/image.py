import requests
from PIL import Image

from util.types import InputBase, MediaType
from util.util import get_env
from util.constants import DISCORD_API_URL, DISCORD_CDN_URL


class ImageInput(InputBase):
    type = MediaType.image


class UrlImageInput(ImageInput):
    name = "url"
    params = ("url",)

    def run(self, url):
        r = requests.get(url, stream=True)
        img = Image.open(r.raw)
        return img


class DiscordImageInput(ImageInput):
    name = "discord"
    params = ("id",)

    def __init__(self):
        super().__init__()
        self.discord_token = get_env("DISCORD_TOKEN")

    # noinspection PyShadowingBuiltins
    def run(self, id):
        r = requests.get(
            f"{DISCORD_API_URL}/users/{id}",
            headers={
                "Authorization": f"Bot {self.discord_token}"
            }
        )
        assert r.status_code == 200  # TODO error handling
        avatar_hash: str = r.json().get("avatar")
        if avatar_hash.startswith("a_"):
            raise ValueError("animated avatars aren't currently supported")  # TODO pass exception on
        cdn_url = f"{DISCORD_CDN_URL}/avatars/{id}/{avatar_hash}.png?size=1024"
        return UrlImageInput().run(cdn_url)
