from generators.no_bitches import NoBitchesGenerator
from outputs.image import BodyImageOutput

DISCORD_API_URL = "https://discord.com/api/v9"
DISCORD_CDN_URL = "https://cdn.discordapp.com"
PARAM_DELIMITER_GENERATOR_GROUPS = "."
PARAM_DELIMITER_GENERATOR_ARG = "-"

PRESETS = {
    "no-bitches": (NoBitchesGenerator, BodyImageOutput)
}
