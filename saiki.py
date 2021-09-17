"""
Saiki Discord Bot

https://discord.com/api/oauth2/authorize?client_id=888164762532343819&permissions=274878204928&scope=bot%20applications.commands

© Anime no Sekai, 2021
"""

# IMPORTS

from io import BytesIO
from json import dumps
# NATIVE TO PYTHON
from re import compile
from traceback import print_exc

import discord  # to communicate with discord
from discord.ext import commands  # to get discord commands
from discord_slash import SlashCommand
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from config import (COMMAND_PREFIX, DEBUG_MODE, ROGER_REACTION,
                    SAIKI_BOT_VERSION, SAIKI_LLS_ENDPOINT)
from models.exercice import Exercice
from templates.botstats import BOTSTATS_TEMPLATE, POWERED_BY
from templates.help import HELP_TEMPLATE
from utils import exceptions
from utils.exceptions import ExerciceNotNumber, PageNotNumber, SaikiException
from utils.html import render
from utils.log import LogLevels, log
from utils.request import Request
from utils.sanitize import url_encode

# DEFINING CLIENT/BOT AND ITS PREFIX
client = commands.Bot(command_prefix=COMMAND_PREFIX, case_insensitive=True)
slash = SlashCommand(client, sync_commands=True)

# WHEN THE BOT IS UP


INT_REGEX = compile("\d+")


@client.event
async def on_ready():
    # GAME ACTIVITY
    await client.change_presence(activity=discord.Game(name='!saikihelp'))
    log("Saiki is ready", level=LogLevels.INFO)


def to_int_list(text: str) -> list[int]:
    if text is None or str(text).replace(" ", "") in ["", "*"]:
        return []
    results = [int(val) for val in INT_REGEX.findall(str(text))]
    results.sort()
    return results


async def get_lls(class_name: str, subject: str, pages: list[int], exercices: list[int] = None, style: str = "", width: int = 1920):
    log("Converting the pages to integers")
    for index, page in enumerate(list(pages)):
        try:
            pages[index] = int(page)
        except Exception:
            raise PageNotNumber(
                f"The {page} page does not seem to be an integer")

    if len(exercices) <= 0:
        exercices = None
    if exercices is not None:
        log("Converting the exercices to integers")
        for index, exercice in enumerate(list(exercices)):
            try:
                exercices[index] = int(exercice)
            except Exception:
                raise ExerciceNotNumber(
                    f"The {exercice} page does not seem to be an integer")
    r = Request(url=SAIKI_LLS_ENDPOINT.format(
        subject=url_encode(str(subject).strip()),
        class_name=url_encode(str(class_name).strip()),
        pages=url_encode(dumps(pages, ensure_ascii=False)),
    ))
    valid = 0
    results = ""
    for data in r.json:
        exercice = Exercice(data)
        if exercices is not None and not exercice.number in exercices:
            continue
        results += exercice.dump() + "<br><br>"
        valid += 1

    if valid <= 0:
        return BytesIO(render(f"<h1>Nous n'avons pas pu trouver de solution.<br>Livre: {subject}<br>Pages: {pages}<br>Exercices: {exercices}</h1>", width=800))

    return BytesIO(render(results, css=str(style), width=width))


async def error_handler(context, error):
    if DEBUG_MODE:
        print_exc()
    if isinstance(error, SaikiException):
        await context.send(error.SAFE_MESSAGE.format(mention=context.author.mention))
    else:
        log("An unknown error occured: {name} {error}".format(
            name=error.__class__.__name__, error=str(error)), level=LogLevels.ERROR)
        await context.send(exceptions.SaikiException.SAFE_MESSAGE.format(mention=context.author.mention))


@slash.slash(name="solution",
             description="Donne la solution d'un exercice",
             options=[
                 create_option(
                     name="classe",
                     description="Ta classe",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 ),
                 create_option(
                     name="matiere",
                     description="La matière (pour choisir le livre)",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 ),
                 create_option(
                     name="page",
                     description="La page (ou les pages)",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 ),
                 create_option(
                     name="exercice",
                     description="L'exercice (ou les exercices)",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 ),
                 create_option(
                     name="style",
                     description="Si t'es un developpeur et que veux rajouter du CSS à ton image :)",
                     option_type=SlashCommandOptionType.STRING,
                     required=False
                 ),
                 create_option(
                     name="width",
                     description="Pour définir la largeur de ton image",
                     option_type=SlashCommandOptionType.INTEGER,
                     required=False
                 )
             ])
async def solution(context: SlashContext, classe: str, matiere: str, page: str, exercice: str = None, style: str = "", width: int = 1920):
    try:
        log(
            f"→ '/solution' came from the server {context.guild} (user: {context.author})", level=LogLevels.INFO)
        log("Getting the responses from LLS")
        pages = to_int_list(page)
        exercices = to_int_list(exercice)
        await context.send(f"On cherche les solutions {context.author.mention}")
        async with context.channel.typing():
            response = await get_lls(class_name=classe, subject=matiere, pages=pages, exercices=exercices, style=style, width=width)
            log(f"Sending back the response for {context.interaction_id}")
            await context.channel.send(content=f"{context.author.mention} voici les solutions pour {matiere} (Page{'s' if len(pages) > 1 else ''}: {', '.join([str(p) for p in pages])}{'; Exercices: ' + ', '.join([str(e) for e in exercices]) if len(exercices) > 0 else ''}):", file=discord.File(response, filename="solutions.jpg"))
            log("← '/solution' for {user}".format(
                user=context.author), level=LogLevels.INFO)
    except Exception as err:
        await error_handler(context=context, error=err)


@client.command(pass_context=True, aliases=["saikihelps"])
async def saikihelp(context):
    try:
        async with context.typing():
            # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            # await context.message.add_reaction(ROGER_REACTION)

            log("→ '!saikihelp' came from the server {server} (user: {user})".format(
                server=context.guild, user=context.author), level=LogLevels.INFO)

            embed = discord.Embed(title='Saiki Help Center',
                                  colour=discord.Colour.blue())
            embed.add_field(name='Available Commands', value=HELP_TEMPLATE)
            embed.set_author(name=f"Requested by {context.author}")
            embed.set_footer(text="© Anime no Sekai — 2021")
            await context.send(embed=embed)

            log("← '!saikihelp' for {user}".format(
                user=context.author), level=LogLevels.INFO)

    except Exception as err:
        await error_handler(context=context, error=err)


@client.command(pass_context=True, aliases=["saikistat"])
async def saikistats(context):
    try:
        async with context.typing():
            # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND
            # await context.message.add_reaction(ROGER_REACTION)

            log("→ '!saikistats' came from the server {server} (user: {user})".format(
                server=context.guild, user=context.author), level=LogLevels.INFO)

            embed = discord.Embed(title='Saiki Bot Stats',
                                  colour=discord.Colour.blue())
            embed.add_field(name='Stats', value=BOTSTATS_TEMPLATE.format(
                version=SAIKI_BOT_VERSION,
                latency=round(client.latency * 1000, 2),
                servers=len(client.guilds),
                # users=len(client.users)
            ))
            embed.add_field(name='Powered by', value=POWERED_BY)

            await context.send(embed=embed)

            log("← '!saikistats' for {user}".format(
                user=context.author), level=LogLevels.INFO)

    except Exception as err:
        await error_handler(context=context, error=err)
