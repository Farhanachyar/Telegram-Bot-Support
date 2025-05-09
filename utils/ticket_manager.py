import logging
from pyrogram.enums import ParseMode
from config import SUPPORT_STAFF_IDS
from utils.data_manager import load_tracking_data
from utils.utils import get_channel_message_url
from helper import logger

async def notify_support_staff_about_new_ticket(client, user_id, user_name, issue_type, timestamp, description_text, channel_url=None):
    notification = (
        f"🎫 NEW TICKET\n\n"
        f"👤 From: {user_name} (ID: {user_id})\n"
        f"📝 Category: {issue_type.capitalize()}\n"
        f"⏰ Time: {timestamp}\n\n"
    )
    
    if description_text:
        notification += f"🔍 Description: {description_text[:100]}{'...' if len(description_text) > 100 else ''}\n\n"
    else:
        notification += "🔍 Description: [Media without text]\n\n"

    if channel_url:
        notification += f"📎 [View in Channel]({channel_url})"

    for staff_id in SUPPORT_STAFF_IDS:
        try:
            await client.send_message(
                staff_id,
                notification,
                disable_web_page_preview=True,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"Sent new ticket notification to support staff {staff_id}")
        except Exception as e:
            logger.error(f"Failed to notify support staff {staff_id}: {e}")

async def notify_support_staff(client, user_id, user_name, message_text, discussion_group_id, discussion_msg_id):

    notification = (
        f"🔔 New message from {user_name} (ID: {user_id})\n\n"
    )
    
    if message_text:
        notification += f"Message: {message_text[:100]}{'...' if len(message_text) > 100 else ''}\n\n"
    else:
        notification += "Message: [Media without text]\n\n"
 
    message_links = []

    if discussion_group_id and discussion_msg_id:
        discussion_url = get_channel_message_url(discussion_group_id, discussion_msg_id)
        message_links.append(f"📎 [View in Group]({discussion_url})")

    tracking_data = load_tracking_data()
    if str(user_id) in tracking_data and "channel_message_url" in tracking_data[str(user_id)]:
        channel_url = tracking_data[str(user_id)]["channel_message_url"]
        message_links.append(f"🔗 [View Ticket in Channel]({channel_url})")

    if message_links:
        notification += " | ".join(message_links)
 
    for staff_id in SUPPORT_STAFF_IDS:
        try:
            await client.send_message(
                staff_id,
                notification,
                disable_web_page_preview=True,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"Sent message notification to support staff {staff_id}")
        except Exception as e:
            logger.error(f"Failed to notify support staff {staff_id}: {e}")

async def close_ticket(client, tracking_data, conversations_data, user_id, closer_name, is_staff=False):
    try:
        user_id_str = str(user_id)

        if user_id_str not in tracking_data:
            return False, "No open ticket found."

        ticket_info = tracking_data[user_id_str]
        channel_id = ticket_info.get("channel_id")
        channel_msg_id = ticket_info.get("channel_message_id")
        channel_message_url = ticket_info.get("channel_message_url", "")
        issue_type = ticket_info.get("issue_type", "Unknown")

        from utils.utils import get_timestamp
        close_timestamp = get_timestamp()

        if channel_id and channel_msg_id:
            try:
                channel_message = await client.get_messages(channel_id, channel_msg_id)
                original_text = channel_message.text or channel_message.caption or ""
                
                if "TICKET CLOSED" not in original_text:
                    if is_staff:
                        closure_text = f"{original_text}\n\n🔒 TICKET CLOSED by staff {closer_name} on {close_timestamp}"
                    else:
                        closure_text = f"{original_text}\n\n🔒 TICKET CLOSED by user on {close_timestamp}"

                    if channel_message.media:
                        await client.edit_message_caption(
                            channel_id,
                            channel_msg_id,
                            caption=closure_text
                        )
                    else:
                        await client.edit_message_text(
                            channel_id,
                            channel_msg_id,
                            closure_text
                        )
                    logger.info(f"Edited channel message {channel_msg_id} to mark ticket as closed")
            except Exception as e:
                logger.error(f"Error editing channel message: {e}")

        return True, {
            "timestamp": close_timestamp,
            "channel_url": channel_message_url,
            "issue_type": issue_type,
            "closer_name": closer_name if is_staff else "user"
        }
    except Exception as e:
        logger.error(f"Error in close_ticket: {e}")
        return False, str(e)