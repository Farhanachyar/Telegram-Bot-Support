import logging
from pyrogram.enums import ParseMode
from config import SUPPORT_STAFF_IDS
from utils.data_manager import load_tracking_data, save_tracking_data, load_conversations_data, save_conversations_data
from utils.ticket_manager import close_ticket
from handlers.message_handlers import process_staff_reply as handler_process_staff_reply
from helper import logger

async def process_staff_ticket_closure(client, message, replied_msg_id):
    logger.info(f"Staff attempting to close ticket from message ID {replied_msg_id}")

    tracking_data = load_tracking_data()
    conversations_data = load_conversations_data()

    found_user_id = None

    for user_id, data in tracking_data.items():
        if data.get("discussion_message_id") == replied_msg_id:
            found_user_id = user_id
            break

        for msg in conversations_data.get(user_id, []):
            if msg.get("discussion_message_id") == replied_msg_id:
                found_user_id = user_id
                break
                
        if found_user_id:
            break
    
    if not found_user_id:
        return False, "Cannot find a ticket associated with this message."

    staff_name = "HyperBot Staff"
    if message.from_user:
        staff_name = message.from_user.first_name
        if message.from_user.username:
            staff_name += f" (@{message.from_user.username})"

    user_info = None
    try:
        user = await client.get_users(int(found_user_id))
        user_name = f"{user.first_name}"
        if user.username:
            user_name += f" (@{user.username})"
        user_info = user_name
    except:
        user_info = f"User (ID: {found_user_id})"

    success, result = await close_ticket(
        client, tracking_data, conversations_data, found_user_id, staff_name, is_staff=True
    )
    
    if not success:
        logger.error(f"Error in process_staff_ticket_closure: {result}")
        return False, f"An error occurred while closing the ticket: {result}"
    
    user_id_int = int(found_user_id)

    channel_url = result.get("channel_url", "")
    timestamp = result.get("timestamp", "")
    issue_type = result.get("issue_type", "").capitalize()

    if found_user_id in conversations_data:
        del conversations_data[found_user_id]
        save_conversations_data(conversations_data)
        logger.info(f"Removed conversation data for user {found_user_id}")
        
    if found_user_id in tracking_data:
        del tracking_data[found_user_id]
        save_tracking_data(tracking_data)
        logger.info(f"Removed tracking data for user {found_user_id}")

    notification = (
        f"🔒 Your ticket has been closed by our support staff.\n\n"
        f"📝 Category: {issue_type}\n"
        f"⏰ Closed on: {timestamp}\n"
        f"👤 Closed by: {staff_name}\n"
    )
            
    notification += "Thank you for contacting us. If you have another question, please use /create_ticket to create a new ticket."

    try:
        await client.send_message(
            user_id_int,
            notification,
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"Sent ticket closure notification to user {found_user_id}")
    except Exception as e:
        logger.error(f"Error sending closure notification to user: {e}")

    staff_confirmation = f"✅ Ticket for user ID {found_user_id} has been closed."
    if channel_url:
        staff_confirmation += f"\n🔗 [View Ticket]({channel_url})"

    staff_notification = (
        f"🔒 TICKET CLOSED\n\n"
        f"👤 User: {user_info} (ID: {found_user_id})\n"
        f"📝 Category: {issue_type}\n"
        f"⏰ Closed on: {timestamp}\n"
        f"✅ Closed by: {staff_name}\n"
    )
    
    if channel_url:
        staff_notification += f"🔗 [View Ticket]({channel_url})"

    closer_id = message.from_user.id if message.from_user else None
    
    for staff_id in SUPPORT_STAFF_IDS:
        if closer_id and staff_id == closer_id:
            continue
            
        try:
            await client.send_message(
                staff_id,
                staff_notification,
                disable_web_page_preview=True,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"Notified support staff {staff_id} about ticket closure by staff")
        except Exception as e:
            logger.error(f"Failed to notify support staff {staff_id} about ticket closure: {e}")
    
    return True, staff_confirmation

async def process_staff_reply(client, message, replied_msg_id):    
    return await handler_process_staff_reply(client, message)