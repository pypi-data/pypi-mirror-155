# better-options-description 1.0
[![Downloads](https://pepy.tech/badge/discord-ext-better-options-description)](https://pepy.tech/project/discord-ext-better-options-description)
![PyPI - License](https://img.shields.io/pypi/l/discord-ext-better-options-description)

Discord.py extension to keep your slash commands options neat and tidy.

## Example Usage (Only for slash commands)
```py

# With discord-ext-better-options-description
...
from discord.ext.better_options_description import parse_doc

@parse_doc
@bot.tree.command(name="dice", description="Roll one or more dice.")
async def dice_commands(interaction: discord.Interaction, number: int,
                        sides: int = 6, bonus: int = 0):
    """
    number: "The number of dice to roll (max: 25)."
    sides: "The number of sides each die will have."
    bonus: "A fixed number to add to the total roll."
    """

    if number > 25:
        await interaction.response.send_message("No more than 25 dice can be rolled at once.")
        return

    if sides > 100:
        await interaction.response.send_message("The dice cannot have more than 100 sides.")
        return

    rolls = [random.randint(1, sides) for _ in range(number)]

    await interaction.response.send_message(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )


# Without discord-ext-better-options-description
...
from discord import app_commands

@app_commands.describe(number="The number of dice to roll (max: 25).", sides="The number of sides each die will have.",
                       bonus="A fixed number to add to the total roll.")
@bot.tree.command(name="dice", description="Roll one or more dice.")
async def dice_commands(interaction: discord.Interaction, number: int,
                        sides: int = 6, bonus: int = 0):
    if number > 25:
        await interaction.response.send_message("No more than 25 dice can be rolled at once.")
        return

    if sides > 100:
        await interaction.response.send_message("The dice cannot have more than 100 sides.")
        return

    rolls = [random.randint(1, sides) for _ in range(number)]

    await interaction.response.send_message(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )
```