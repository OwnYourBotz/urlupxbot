@RenameBot.on_message(filters.private & filters.command("settings"))
async def settings_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    editable = await event.reply_text(
        text="**👀 Processing...**"
    )
    await OpenSettings(editable, user_id=event.from_user.id)
