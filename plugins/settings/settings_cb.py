import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from pyrogram import Client
from translation import Translation 
from plugins.settings.settings import OpenSettings
from plugins.database.database import db
from pyrogram import types
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes


@Client.on_callback_query()
async def cb_handlers(c: Client, cb: "types.CallbackQuery"):
    if cb.data == "OpenSettings":
        await cb.answer()
        await show_settings(cb.message)
    elif cb.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if not thumbnail:
            await cb.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await cb.answer()
            await c.send_photo(cb.message.chat.id, thumbnail, "Custom Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Delete Thumbnail",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif cb.data == "deleteThumbnail":
        await db.set_thumbnail(cb.from_user.id, None)
        await cb.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await cb.message.delete(True)
    elif cb.data == "setThumbnail":
        await cb.answer()
        await cb.message.edit("Send me any photo to set that as custom thumbnail.\n\n"
                              "Press /cancel to cancel process.")
        from_user_thumb: "types.Message" = await c.listen(cb.message.chat.id)
        if not from_user_thumb.photo:
            await cb.message.edit("Process Cancelled!")
            return await from_user_thumb.continue_propagation()
        else:
            await db.set_thumbnail(cb.from_user.id, from_user_thumb.photo.file_id)
            await cb.message.edit("Okay!\n"
                                  "Now I will apply this thumbnail to next uploads.",
                                  reply_markup=types.InlineKeyboardMarkup(
                                      [[types.InlineKeyboardButton("Show Settings",
                                                                   callback_data="OpenSettings")]]
                                  ))

    elif cb.data == "triggerUploadMode":
        await cb.answer()
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(cb.from_user.id, False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, True)
        await show_settings(cb.message)
    elif cb.data == "closeMessage":
        await cb.message.delete(True)

