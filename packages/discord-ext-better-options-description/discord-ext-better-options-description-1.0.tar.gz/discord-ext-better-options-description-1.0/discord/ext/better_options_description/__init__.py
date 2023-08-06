from yaml import safe_load
from discord.app_commands.commands import _populate_descriptions, Command

__all__ = ["parse_doc"]


def parse_doc(func):
    assert isinstance(func, Command)

    command_doc = safe_load(func.callback.__doc__)
    _populate_descriptions(func._params, command_doc)

