from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.helpers import Parameters, show_cmd_tip, show_exception
from tools.sessions import session


@Client.on_message(command('ip'))
async def ip(_: Client, msg: Message):
    """查询ip信息"""
    cmd, address = Parameters.get(msg)
    if not address:
        return await show_cmd_tip(msg, cmd)
    elif address == "me":
        address = ''

    async def get_api(api: str) -> str:
        async with session.get(api) as resp:
            if resp.status == 200:
                data = await resp.json()
                tmp = '\n'.join(f"{k}：`{v}`" for k, v in data.items())
                return tmp if tmp else "😂 No Response ~"
            resp.raise_for_status()

    try:
        api = f"http://ip-api.com/json/{address}"
        text = await get_api(api)
    except Exception as e:
        return await show_exception(msg, e)
    else:
        await msg.edit_text(text)
