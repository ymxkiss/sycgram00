import asyncio
import sys

from core import command
from loguru import logger
from pyrogram import Client
from pyrogram.types import Message
from tools.constants import (SYCGRAM, SYCGRAM_ERROR, SYCGRAM_INFO,
                             SYCGRAM_WARNING, UPDATE_CMD)
from tools.helpers import Parameters, basher, get_cmd_error
from tools.updates import (get_alias_of_cmds, pull_and_update_command_yml,
                           reset_cmd_alias, update_cmd_alias,
                           update_cmd_prefix)


@Client.on_message(command("restart"))
async def restart(_: Client, msg: Message):
    """重启容器"""
    text = f"**{SYCGRAM_INFO}**\n> # `Restarting {SYCGRAM} ...`"
    await msg.edit_text(text=text, parse_mode='md')
    sys.exit()


@Client.on_message(command("update"))
async def update(_: Client, msg: Message):
    """更新sycgram到主分支的最新版本"""
    text = f"**{SYCGRAM_INFO}**\n> # `It's updating {SYCGRAM} ...`"
    await msg.edit_text(text, parse_mode='md')
    try:
        await pull_and_update_command_yml()
        _ = await basher(UPDATE_CMD, timeout=60)
    except asyncio.exceptions.TimeoutError:
        text = f"**{SYCGRAM_WARNING}**\n> # `Update Timeout！`"
    except Exception as e:
        text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
    else:
        text = f"**{SYCGRAM_INFO}**\n> # `{SYCGRAM.title()} is already the latest version.`"
    finally:
        await msg.edit_text(text, parse_mode='md')


@Client.on_message(command("prefix"))
async def prefix(_: Client, msg: Message):
    """更改所有指令的前缀"""
    _, pfx = Parameters.get(msg)
    punctuation = list("""!#$%&*+,-./:;=?@^~！？。，；·\\""")
    if len(pfx) == 0 or len(pfx) > 1 or pfx not in punctuation:
        text = f"**{SYCGRAM_WARNING}**\n> # `Prefix must be one of {' '.join(punctuation)}`"
        await msg.edit_text(text, parse_mode='md')
        return
    try:
        update_cmd_prefix(pfx)
    except Exception as e:
        text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
        logger.error(e)
        await msg.edit_text(text, parse_mode='md')
    else:
        text = f"**{SYCGRAM_INFO}**\n> # `Restarting {SYCGRAM} prefix of all commands.`"
        await msg.edit_text(text, parse_mode='md')
        sys.exit()


@Client.on_message(command("alias"))
async def alias(_: Client, msg: Message):
    """
    cmd: alias
    format: -alias <set> <source> <to> or -alias <reset> <source> or -alias <list>
    usage: 修改指令别名
    """
    cmd, args = Parameters.get_more(msg)
    if len(args) == 3 and args[0] == 'set':
        _, source, to = args
        try:
            update_cmd_alias(source, to)
        except Exception as e:
            text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
            logger.error(e)
            await msg.edit_text(text, parse_mode='md')
        else:
            text = f"**{SYCGRAM_INFO}**\n> # `Updating alias of <{source}> to <{to}> ...`"
            await msg.edit_text(text, parse_mode='md')
            sys.exit()

    elif len(args) == 2 and args[0] == 'reset':
        _, source = args
        try:
            reset_cmd_alias(source)
        except Exception as e:
            text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
            logger.error(e)
            await msg.edit_text(text, parse_mode='md')
        else:
            text = f"**{SYCGRAM_INFO}**\n> # `Reset alias of <{source}> ...`"
            await msg.edit_text(text, parse_mode='md')
            sys.exit()

    elif len(args) == 1 and args[0] == 'list':
        try:
            text = get_alias_of_cmds()
        except Exception as e:
            text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
            logger.error(e)
            await msg.edit_text(text, parse_mode='md')
        else:
            await msg.edit_text(text, parse_mode='md')

    else:
        await msg.edit_text(get_cmd_error(cmd))
