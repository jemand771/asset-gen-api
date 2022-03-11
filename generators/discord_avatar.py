import requests

from util.constants import DISCORD_API_URL, DISCORD_CDN_URL
from util.types import GeneratorBase, MediaType
from util.util import get_env

from generators.image_from_url import ImageFromUrl


class DiscordAvatar(ImageFromUrl):
    input_params = {
        "id": MediaType.text
    }
    name = "discord"
    output_type = MediaType.image

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
        return super().run(cdn_url)
