from aiogram import types
from loader import dp
from utils.db_api import DBS
from filters import IsAdmin

@dp.message_handler(IsAdmin(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def new_chat_member_bot(msg: types.Message):
    DBS.group_register(DBS, msg.chat.id)
    new_members = msg.new_chat_members
    for x in new_members:
        DBS.join_in_group(DBS, msg.from_id, x.id, msg.chat.id)
    await msg.answer("Hello")