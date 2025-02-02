import math
import time
from aiogram import types
from loader import dp
from utils.db_api import DBS
from aiogram.utils.exceptions import Throttled
from filters import IsAdmin

@dp.message_handler(IsAdmin(), content_types=[types.ContentType.ANY], chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def not_join_channel (msg: types.Message):
    get_chat = await dp.bot.get_chat_member(msg.chat.id, msg.from_id)
    status_list = ['administrator', 'creator']
    if get_chat.status not in status_list:
        channel_id = DBS.get_channel_id(DBS, msg.chat.id)
        if channel_id != False:
            get_status = await dp.bot.get_chat_member(channel_id, msg.from_id)
            get_data = await dp.bot.get_chat(channel_id)
            if get_status.status == 'left':
                await msg.delete()
                await msg.answer(
                    text=f"[{get_data.title}]({get_data.invite_link}) Kanalga agza bolmasan'iz gruppada jaza almaysiz", 
                    parse_mode="markdown",
                    disable_web_page_preview=True
                    )
                await dp.bot.restrict_chat_member(
                        chat_id=msg.chat.id,
                        user_id=msg.from_id,
                        until_date=math.floor(time.time()) + 5*60,
                        permissions=types.ChatPermissions(can_send_messages=False, can_invite_users=True)
                        )
        
        count_data = DBS.get_member_count(DBS, msg.chat.id)
        if count_data != False:
            if DBS.my_members(DBS, user_id=msg.from_id, group_id=msg.chat.id) < int(count_data):  
                await msg.delete()
                await msg.answer(
                        text=f"{count_data} adam qospasan'iz gruppada jaza almaysiz", 
                        parse_mode="markdown",
                        disable_web_page_preview=True
                        )
                await dp.bot.restrict_chat_member(
                            chat_id=msg.chat.id,
                            user_id=msg.from_id,
                            until_date=math.floor(time.time()) + 5*60,
                            permissions=types.ChatPermissions(can_send_messages=False, can_invite_users=True)
                        )
        
        get_chan_status = DBS.get_chan(DBS, msg.chat.id)
        if get_chan_status != False:
            if msg.sender_chat:
                await msg.delete()
                await msg.answer(
                        text="kanal atinnan gruppada jaza almaysiz", 
                        parse_mode="markdown",
                        disable_web_page_preview=True
                        )
                await dp.bot.restrict_chat_member(
                            chat_id=msg.chat.id,
                            user_id=msg.from_id,
                            until_date=math.floor(time.time()) + 5*60,
                            permissions=types.ChatPermissions(can_send_messages=False, can_invite_users=True)
                        )
        get_ads = DBS.get_ads(DBS, msg.chat.id)
        if get_ads != False:
            link_list = ['mention', 'url', 'text_link', 'text_mention']
            for x in msg.entities:
                if x.type in link_list:
                    await msg.delete()
                    try:
                        await dp.throttle(key='*', rate=10)
                        await msg.answer(f"<a href='tg://user?id={msg.from_id}'>{msg.from_user.full_name}</a> <b>реклама тарқатпаң!</b>")
                    except Throttled: pass
            else:
                for x in msg.caption_entities:
                    if x.type in link_list:
                        await msg.delete()
                        try:
                            await dp.throttle(key='*', rate=10)
                            await msg.answer(f"<a href='tg://user?id={msg.from_id}'>{msg.from_user.full_name}</a> реклама тарқатпаң!")
                        except Throttled: pass

                
        