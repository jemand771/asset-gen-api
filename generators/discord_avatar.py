import requests
from PIL.Image import Image

from generators.image_from_url import ImageFromUrl
from util.constants import DISCORD_API_URL, DISCORD_CDN_URL
from util.types import GeneratorInternalError, InvalidInputError
from util.util import get_env


class DiscordAvatar(ImageFromUrl):
    type = "discord"

    def __init__(self):
        super().__init__()
        self.discord_token = get_env("DISCORD_TOKEN")

    # noinspection PyShadowingBuiltins
    def run(self, id: str) -> Image:
        r = requests.get(
            f"{DISCORD_API_URL}/users/{id}",
            headers={
                "Authorization": f"Bot {self.discord_token}"
            }
        )
        if r.status_code == 404:
            raise InvalidInputError("user not found")
        if r.status_code != 200:
            raise GeneratorInternalError("unknown error while talking to discord")
        avatar_hash: str = r.json().get("avatar")
        if avatar_hash.startswith("a_"):
            raise InvalidInputError("animated avatars aren't currently supported")
        cdn_url = f"{DISCORD_CDN_URL}/avatars/{id}/{avatar_hash}.png?size=1024"
        return super().run(cdn_url)
