from aiogram import types
from loader import dp
from utils.db_api import DBS
from filters import IsAdmin

@dp.message_handler(IsAdmin(), commands="toplist", is_chat_admin=True, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_top_list(msg: types.Message):
    users = DBS.top_users(DBS, msg.chat.id)
    if len(users) == 0:
        await msg.answer("Группаға еле ҳешким адам қоспаған.")
    else: 
        text = "TOP 50\n\n"
        for x, i in zip(users, range(1, len(users)+1)):
            get_user = await dp.bot.get_chat(x[0])
            text  +=f'{i}. {get_user.full_name} {x[2]}\n'
        await msg.answer(text=text)