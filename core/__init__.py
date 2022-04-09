from .custom import command, CMDS_DATA, CMDS_PREFIX
from pyrogram import Client

app = Client(
    "./data/app",
    config_file='./data/config.ini',
    plugins=dict(root="plugins")
)


__all__ = (
    'app',
    'command',
    'CMDS_DATA',
    'CMDS_PREFIX',
)
