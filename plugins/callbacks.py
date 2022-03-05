# © Shrimadhav Uk | @Tellybots

import os

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from pyrogram.errors import FloodWait, MessageNotModified

from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back
from translation import Translation
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ForceReply
from plugins.database.database import db
import asyncio
import time
import psutil
import shutil
import string
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified


@Client.on_callback_query()
async def button(bot, update):
    if "|" in update.data:
        await youtube_dl_call_back(bot, update)
    elif "=" in update.data:
        await ddl_call_back(bot, update)
    elif update.data == "home":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=Translation.ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


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



