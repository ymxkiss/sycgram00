import asyncio
import sys

from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.constants import SYCGRAM, SYCGRAM_ERROR, SYCGRAM_INFO, SYCGRAM_WARNING, UPDATE_CMD
from tools.helpers import basher


@Client.on_message(command("restart"))
async def restart(_: Client, msg: Message):
    """重启容器"""
    text = f"**{SYCGRAM_INFO}**\n> # `The {SYCGRAM} is restarting......`"
    await msg.edit_text(text=text, parse_mode='md')
    sys.exit()


@Client.on_message(command("update"))
async def update(_: Client, msg: Message):
    """更新sycgram到主分支的最新版本"""
    text = f"**{SYCGRAM_INFO}**\n> # `It's updating container to the latest version......`"
    await msg.edit_text(text, parse_mode='md')
    try:
        _ = await basher(UPDATE_CMD, timeout=60)
    except asyncio.exceptions.TimeoutError:
        text = f"**{SYCGRAM_WARNING}**\n> # `Update Timeout！`"
    except Exception as e:
        text = f"**{SYCGRAM_ERROR}**\n> # `{e}`"
    else:
        text = f"**{SYCGRAM_INFO}**\n> # `Your {SYCGRAM} version is the latest.`"
    finally:
        await msg.edit_text(text, parse_mode='md')
