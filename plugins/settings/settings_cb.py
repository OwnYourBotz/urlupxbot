@Tellybots.on_message(filters.private & filters.command("start"))
async def start_handler(bot: Client, event: Message, cb=False):
    await AddUserToDatabase(bot, event)
    if not cb:
        send_msg = await event.reply_text("**👀 Processing......**", quote=True)    
    await send_msg.edit(
      text=f"{Translation.START_TEXT}".format(event.from_user.mention), 
      reply_markup=Translation.START_BUTTONS, 
      disable_web_page_preview=True
       )
    if cb:
        return await event.message.edit(
                 text=f"{Translation.START_TEXT}".format(event.from_user.mention),
                 reply_markup=Translation.START_BUTTONS,
                 disable_web_page_preview=True
                     )
            
@Tellybots.on_message(filters.private & filters.command("help"))
async def start_handler(bot: Client, event: Message, cb=False):
    await AddUserToDatabase(bot, event)
    if not cb:
        send_msg = await event.reply_text("**👀 Processing......**", quote=True)    
    await send_msg.edit(
      text=f"{Translation.HELP_TEXT}".format(event.from_user.mention), 
      reply_markup=Translation.HELP_BUTTONS, 
      disable_web_page_preview=True
       )
    if cb:
        return await event.message.edit(
                 text=f"{Translation.HELP_TEXT}".format(event.from_user.mention),
                 reply_markup=Translation.HELP_BUTTONS,
                 disable_web_page_preview=True
                     )
            
@Tellybots.on_message(filters.private & filters.command("about"))
async def start_handler(bot: Client, event: Message, cb=False):
    await AddUserToDatabase(bot, event)
    if not cb:
        send_msg = await event.reply_text("**👀 Processing......**", quote=True)    
    await send_msg.edit(
      text=f"{Config.ABOUT_TEXT}", 
      reply_markup=ABOUT_BUTTONS, 
      disable_web_page_preview=True
       )
    if cb:
        return await event.message.edit(
                 text=f"{Config.ABOUT_TEXT}",
                 reply_markup=ABOUT_BUTTONS,
                 disable_web_page_preview=True
                     )


            #try:
                #os.remove(download_location)
              #  os.remove(thumb_image_path)
            #except:
                #pass

@Tellybots.on_message(filters.private & filters.command("settings"))
async def settings_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    editable = await event.reply_text(
        text="**👀 Processing...**"
    )
    await OpenSettings(editable, user_id=event.from_user.id)



@Tellybots.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    if "closeMeh" in cb.data:
        await cb.message.delete(True)
        await cb.message.reply_to_message.delete()
    elif "close" in cb.data:
        await cb.message.delete(True)
        await cb.message.reply_to_message.delete()
    elif "help" in cb.data:
        await cb.edit_message_text(
              text = f"{Translation.HELP_TEXT}".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = Translation.HELP_BUTTONS)
    elif "home" in cb.data:
        await cb.edit_message_text(
              text = f"{Translation.START_TEXT}".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = Translation.START_BUTTONS)
    elif "about" in cb.data:
        await cb.edit_message_text(
              text = f"{Translation.ABOUT_TEXT}".format(cb.from_user.mention),
              disable_web_page_preview = True,
              reply_markup = Translation.ABOUT_BUTTONS)
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
        await OpenSettings(cb.message, user_id=cb.from_user.id)
                )
        except TimeoutError:
            await cb.message.edit(
                text="**🤬 I can't wait more.... BYE 👋🏻**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔚 Go Back", callback_data="openSettings")]])
            )











