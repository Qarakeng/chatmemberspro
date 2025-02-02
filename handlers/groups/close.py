from aiogram import types
from loader import dp
from utils.db_api import DBS
from filters import IsAdmin

@dp.message_handler(IsAdmin(), commands='close', chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_colse(msg: types.Message):
    group_data= await dp.bot.get_chat(msg.chat.id)
    DBS.set_group_premissions(DBS, msg.chat.id, group_data.permissions)
    chat_permissions = types.ChatPermissions(
        can_send_messages=False
    )
    await dp.bot.set_chat_permissions(
            chat_id=msg.chat.id,
            permissions=chat_permissions)
    await msg.answer("Gruppada jaziw waqtinshaliq sheklendi")

@dp.message_handler(IsAdmin(), commands='open', chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_open(msg: types.Message):
    permissions =  DBS.get_group_premissions(DBS, msg.chat.id)
    await dp.bot.set_chat_permissions(
        chat_id=msg.chat.id,
        permissions=permissions
    )
    await msg.answer("Gruppa ashildi")