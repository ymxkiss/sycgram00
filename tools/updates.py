import re
from typing import Any, Dict

import yaml

from .constants import CMD_YML_REMOTE, COMMAND_YML
from .sessions import session


def update_cmd_yml(cmd_yml: Dict[str, Any]):
    with open(COMMAND_YML, 'w', encoding='utf-8') as f:
        yaml.dump(cmd_yml, f, allow_unicode=True)


def modify_cmd_prefix(pfx: str) -> Dict[str, Any]:
    with open(COMMAND_YML, "rb") as f:
        cmd_yml: Dict[str, Any] = yaml.full_load(f)
        old_pfx = cmd_yml['help']['all_prefixes']
        cmd_yml['help']['all_prefixes'] = pfx
        # 读取每个指令的kv
        for every_cmd in cmd_yml.values():
            get_cmd = every_cmd['cmd']
            old_cmd = rf"[{old_pfx}]{get_cmd}"
            new_cmd = f"{pfx}{get_cmd}"
            every_cmd['format'] = re.sub(old_cmd, new_cmd, every_cmd['format'])

    # 返回已修改过所有指令前缀的一个大字典
    return cmd_yml


def update_cmd_prefix(pfx: str) -> None:
    try:
        cmd_yml = modify_cmd_prefix(pfx)
    except Exception as e:
        raise e
    else:
        update_cmd_yml(cmd_yml=cmd_yml)


def modify_cmd_alias(source: str, new_cmd: str) -> Dict[str, Any]:
    with open(COMMAND_YML, "rb") as f:
        cmd_yml: Dict[str, Any] = yaml.full_load(f)
        if not cmd_yml.get(source):
            raise ValueError(f"The {source} Command Not Found")
        pfx = cmd_yml.get('help').get('all_prefixes')
        old_cmd = cmd_yml[source]['cmd']
        old_fmt = rf"[{pfx}]{old_cmd}"
        new_fmt = f"{pfx}{new_cmd}"

        cmd_yml[source]['cmd'] = new_cmd
        cmd_yml[source]['format'] = re.sub(
            old_fmt, new_fmt, cmd_yml[source]['format'])
        return cmd_yml


def update_cmd_alias(source: str, new_cmd: str) -> None:
    try:
        cmd_yml = modify_cmd_alias(source, new_cmd)
    except Exception as e:
        raise e
    else:
        update_cmd_yml(cmd_yml=cmd_yml)


def reset_cmd_alias(source: str) -> None:
    try:
        cmd_yml = modify_cmd_alias(source, new_cmd=source)
    except Exception as e:
        raise e
    else:
        update_cmd_yml(cmd_yml=cmd_yml)


def get_alias_of_cmds() -> str:
    with open(COMMAND_YML, "rb") as f:
        cmd_yml: Dict[str, Dict[str, str]] = yaml.full_load(f)
        tmp = ''.join(
            f"`{k}` | `{v.get('cmd')}`\n" for k, v in cmd_yml.items()
        )
        return f"**⭐️ 指令别名：**\n**源名** | **别名**\n{tmp}"


async def pull_and_update_command_yml() -> None:
    # 读取远程command.yml
    async with session.get(
        CMD_YML_REMOTE, timeout=9.9,
    ) as resp:
        if resp.status == 200:
            data = yaml.full_load(await resp.text())
            with open(COMMAND_YML, "rb") as f:
                cmd_yml: Dict[str, Dict[str, str]] = yaml.full_load(f)
                data.update(cmd_yml)
            # 合并到本地，以本地为主
            update_cmd_yml(data)
        resp.raise_for_status()
