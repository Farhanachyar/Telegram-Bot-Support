# main.py
# Author: https://github.com/Farhanachyar
# Created: 2025-05-10
# Description: Telegram Bot Support With Media Compatible


from pyromod import listen
from pyrogram import Client, filters, idle
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import API_ID, API_HASH, BOT_TOKEN, SUPPORT_CHANNEL_ID, DISCUSSION_GROUP_ID
from handlers.ticket_handlers import process_issue_selection, process_user_ticket_closure
from handlers.staff_handlers import process_staff_ticket_closure, process_staff_reply
from handlers.message_handlers import process_forwarded_message, process_user_message
from helper import logger

app = Client(
    "sessions/Support_HyperBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    logger.info(f"User {message.from_user.id} started the bot")
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔗 Repository URL", url="https://github.com/Farhanachyar/Telegram-Bot-Support"),
                InlineKeyboardButton("👤 Author Profile", url="https://github.com/Farhanachyar")
            ]
        ]
    )
    
    await message.reply(
        "👋 Hello! I am a Support Bot. How can I help you today?\n\n"
        "Use /create_ticket to open a new support ticket\n"
        "Use /close_ticket to close an existing ticket",
        reply_markup=keyboard
    )

@app.on_message(filters.command("create_ticket"))
async def create_ticket_command(client, message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} is creating a ticket")

    from utils.data_manager import load_tracking_data
    tracking_data = load_tracking_data()
    
    if str(user_id) in tracking_data:
        await message.reply("You already have an open ticket! Please close it with /close_ticket first")
        return
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Technical Issue", callback_data="issue_technical")],
        [InlineKeyboardButton("Billing Question", callback_data="issue_billing")],
        [InlineKeyboardButton("Feature Request", callback_data="issue_feature")],
        [InlineKeyboardButton("General Question", callback_data="issue_general")]
    ])
    
    await message.reply(
        "Please select the category that best matches your issue:",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex(r"^issue_(.+)$"))
async def handle_issue_selection(client, callback_query):
    user_id = callback_query.from_user.id
    issue_type = callback_query.data.split("_")[1]
    
    logger.info(f"User {user_id} selected issue type: {issue_type}")
    
    await callback_query.message.delete()
    await callback_query.message.reply(
        f"You have selected: {issue_type.capitalize()}\n\n"
        "Please describe your issue in detail: (You can send text, photo, video, or document)"
    )

    try:
        description = await client.listen(user_id, timeout=300)
        
        success, message = await process_issue_selection(client, user_id, issue_type, description, callback_query)
        
        if success:
            await description.reply(message)
        else:
            await callback_query.message.reply(
                f"❌ {message}\n"
                "Please try again later or contact an administrator."
            )
        
    except TimeoutError:

        await callback_query.message.reply(
            "You did not provide a description within the time limit. Please use /create_ticket to start again."
        )

@app.on_message(filters.command("close_ticket"))
async def close_ticket_command(client, message):
    is_from_group = not message.chat.type.name.startswith("PRIVATE")
    
    if is_from_group:
        if not message.reply_to_message:
            await message.reply("This command must be used as a reply to a message from the ticket you want to close.")
            return

        await staff_close_ticket(client, message)
        return

    user_id = message.from_user.id
    logger.info(f"User {user_id} is trying to close their ticket")

    success, result_message = await process_user_ticket_closure(client, user_id, message)
    
    if success:
        await message.reply(
            result_message,
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        logger.error(f"Error in close_ticket_command: {result_message}")
        await message.reply(result_message)

@app.on_message(filters.chat(DISCUSSION_GROUP_ID) & filters.forwarded)
async def handle_forwarded_message(client, message):
    if message.forward_from_chat and message.forward_from_chat.id == SUPPORT_CHANNEL_ID:
        await process_forwarded_message(
            client, 
            message, 
            message.forward_from_chat.id, 
            message.forward_from_message_id
        )

@app.on_message(filters.chat(DISCUSSION_GROUP_ID) & filters.command("close"))
async def staff_close_ticket(client, message):
    if not message.reply_to_message:
        await message.reply("This command must be used as a reply to a message from the ticket you want to close.")
        return
    
    replied_msg_id = message.reply_to_message.id

    success, result_message = await process_staff_ticket_closure(client, message, replied_msg_id)
    
    if success:
        await message.reply(
            result_message,
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.reply(result_message)

@app.on_message(filters.chat(DISCUSSION_GROUP_ID) & filters.reply)
async def handle_discussion_reply(client, message):
    if message.text and message.text.startswith('/'):
        return
    await process_staff_reply(client, message, message.reply_to_message.id)

@app.on_message(filters.private)
async def handle_user_message(client, message):
    is_reply = message.reply_to_message is not None

    await process_user_message(client, message, is_reply)

if __name__ == "__main__":
    logger.critical("Starting the Support Bot...")
    logger.critical("Repository: https://github.com/Farhanachyar/Telegram-Bot-Support")
    logger.critical("Developer: https://github.com/Farhanachyar")
    app.start()
    logger.critical("Bot is running. Press Ctrl+C to stop.")
    idle()
    app.stop()