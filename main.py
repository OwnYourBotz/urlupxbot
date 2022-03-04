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


