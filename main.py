# © Shrimadhav Uk | @Tellybots

import os
import asyncio
import time
import psutil
import shutil
import string
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.database.database import db
from translation import Translation

async def OpenSettings(event: Message, user_id: int):
    try:
        await event.edit(
            text="**⚙ Configure My Behaviour**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"🔰 Upload as {'File 🗃️' if ((await db.get_upload_as_doc(user_id)) is True) else 'Video 🎥'}",
                                          callback_data="triggerUploadMode")],
                    [InlineKeyboardButton("🌆 Custom Thumbnail ", callback_data="triggerThumbnail")],
                    [InlineKeyboardButton("⛔ Close Settings", callback_data="close")]
                ]
            )
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await OpenSettings(event, user_id)
    except MessageNotModified:
        pass

@Client.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    if "oo" in cb.data:
        await cb.edit_message_text(
              text = f"✓ I Can't Upload File Size More Than 2GB".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = Translation.BUTTONS)
    elif "openSettings" in cb.data:
        await OpenSettings(cb.message, user_id=cb.from_user.id)
    elif "triggerUploadMode" in cb.data:
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc is True:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=True)
        await OpenSettings(cb.message, user_id=cb.from_user.id)

    elif "triggerThumbnail" in cb.data:
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if thumbnail is None:
            await cb.answer("No Thumbnail Found... ", show_alert=True)
        else:
            await cb.answer("Trying to send your thumbnail...", show_alert=True)
            try:
                await bot.send_photo(
                    chat_id=cb.message.chat.id,
                    photo=thumbnail,
                    text=f"**👆🏻 Your Custom Thumbnail...\n© @AVBotz**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="deleteThumbnail")]])
                )
            except Exception as err:
                try:
                    await bot.send_message(
                        chat_id=cb.message.chat.id,
                        text=f"**😐 Unable to send Thumbnail! Got an unexpected Error**",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⛔ Close", callback_data="closeMeh")],[InlineKeyboardButton("📮 Report issue", url="https://t.me/AVBotz_Support")]])
                    )
                except:
                    pass
    elif "deleteThumbnail" in cb.data:
        await db.set_thumbnail(cb.from_user.id, thumbnail=None)
        await cb.answer("Successfully Removed Custom Thumbnail!", show_alert=True)
        await cb.message.delete(True)
            
