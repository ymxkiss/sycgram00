from core import command
from pyrogram import Client
from pyrogram.types import Message
from tools.helpers import execute
from pyrogram.enums import ParseMode 

@Client.on_message(command('pingdc'))
async def pingdc(_: Client, msg: Message):
    """到各个DC区的延时"""
    DCs = {
        1: "149.154.175.50",
        2: "149.154.167.51",
        3: "149.154.175.100",
        4: "149.154.167.91",
        5: "91.108.56.130",
        6: "138.2.86.251",
        7: "168.138.191.11",
        8: "150.230.105.147",
        9: "150.230.109.14",
        10: "152.67.210.242",
        11: "140.238.16.235",
        12: "193.123.64.206",
        13: "152.69.195.140",
        14: "144.21.53.196",
        15: "140.238.204.248"
    }
    data = []
    for dc in range(1, 6):
        result = await execute(f"ping -c 1 {DCs[dc]} | awk -F '/' " + "'END {print $5}'")
        output = result.get('output')
        data.append(output.replace('\n', '') if output else '-1')

    await msg.edit_text(
        f"🇺🇸 DC1(迈阿密): `{data[0]}ms`\n"
        f"🇳🇱 DC2(阿姆斯特丹): `{data[1]}ms`\n"
        f"🇺🇸 DC3(迈阿密): `{data[2]}ms`\n"
        f"🇳🇱 DC4(阿姆斯特丹): `{data[3]}ms`\n"
        f"🇸🇬 DC5(新加坡): `{data[4]}`\n"
        f"🇸🇬 ORACLE(新加坡1): `{data[5]}`\n"
        f"🇸🇬 ORACLE(新加坡2): `{data[6]}`\n"
        f"🇯🇵 ORACLE(东京1): `{data[7]}`\n"
        f"🇯🇵 ORACLE(东京2): `{data[8]}`\n"
        f"🇰🇷 ORACLE(春川1): `{data[9]}`\n"
        f"🇰🇷 ORACLE(首尔1): `{data[10]}`\n"
        f"🇦🇪 ORACLE(迪拜1): `{data[11]}`\n"
        f"🇯🇵 ORACLE(大阪1): `{data[12]}`\n"
        f"🇬🇧 ORACLE(伦敦1): `{data[13]}`\n"
        f"🇦🇺 ORACLE(悉尼1): `{data[14]}ms`", ParseMode.MARKDOWN
    )
