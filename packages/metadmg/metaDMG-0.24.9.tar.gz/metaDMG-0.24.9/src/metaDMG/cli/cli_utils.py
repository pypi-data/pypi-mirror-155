from enum import Enum
from typing import Iterable

import typer
from click import Context, Group
from click_help_colors import HelpColorsCommand, HelpColorsGroup


#%%


class CustomHelpColorsCommand(HelpColorsCommand):
    """Colorful command line main help. Colors one of:
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "reset",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white"
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = "yellow"
        self.help_options_color = "blue"


class CustomHelpColorsGroup(HelpColorsGroup):
    # colorfull command line for subcommands
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = "yellow"
        self.help_options_color = "blue"


class ColorfulApp(typer.Typer):
    def __init__(self, *args, cls=CustomHelpColorsGroup, **kwargs) -> None:
        super().__init__(*args, cls=cls, **kwargs)

    def command(
        self, *args, cls=CustomHelpColorsCommand, **kwargs
    ) -> typer.Typer.command:
        return super().command(*args, cls=cls, **kwargs)


class OrderedCommands(Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        return self.commands.keys()


def get_cli_app():
    cli_app = ColorfulApp(cls=OrderedCommands)
    # cli_app = ColorfulApp(cls=OrderedCommands, chain=True)
    return cli_app


def version_callback(value: bool):
    from metaDMG.__version__ import __version__

    if value:
        typer.echo(f"metaDMG CLI, version: {__version__}")
        raise typer.Exit()


def is_in_range(x: float, val_min: float, val_max: float) -> float:
    """Confirms that x is val_min <= x <= val_max

    Parameters
    ----------
    x
        Value to check
    val_min
        Minimum
    val_max
        Maximum

    Returns
    -------
        Confirmed value

    Raises
    ------
    typer.BadParameter
        If x is outside bounds
    """

    if x < val_min or val_max < x:
        raise typer.BadParameter(
            f"x has to be between {val_min} and {val_max}. Got: {x}"
        )
    return x


#%%
class RANKS(str, Enum):
    "Ranks allowed in the LCA"

    family = "family"
    genus = "genus"
    species = "species"
    none = ""


class DAMAGE_MODE(str, Enum):
    "Damage mode allowed in the LCA"

    LCA = "lca"
    LOCAL = "local"
    GLOBAL = "global"


#%%
