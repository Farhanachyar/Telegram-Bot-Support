import logging
from pyrogram.enums import ParseMode
from config import SUPPORT_CHANNEL_ID, SUPPORT_STAFF_IDS
from utils.data_manager import load_tracking_data, save_tracking_data, load_conversations_data, save_conversations_data
from utils.utils import get_timestamp, get_channel_message_url
from utils.ticket_manager import notify_support_staff_about_new_ticket, close_ticket
from helper import logger

async def process_issue_selection(client, user_id, issue_type, description, callback_query):
    logger.info(f"Processing issue selection for user {user_id}, type: {issue_type}")

    tracking_data = load_tracking_data()
    conversations_data = load_conversations_data()

    if str(user_id) not in conversations_data:
        conversations_data[str(user_id)] = []

    media_type = None
    media_file_id = None
    caption = None
    description_text = None
    
    if description.text:
        logger.info(f"User {user_id} provided text description: {description.text[:20]}...")
        description_text = description.text
    elif description.photo:
        media_type = "photo"
        media_file_id = description.photo.file_id
        caption = description.caption
        logger.info(f"User {user_id} provided photo description with caption: {caption[:20] if caption else 'No caption'}")
    elif description.video:
        media_type = "video"
        media_file_id = description.video.file_id
        caption = description.caption
        logger.info(f"User {user_id} provided video description with caption: {caption[:20] if caption else 'No caption'}")
    elif description.document:
        media_type = "document"
        media_file_id = description.document.file_id
        caption = description.caption
        logger.info(f"User {user_id} provided document description with caption: {caption[:20] if caption else 'No caption'}")
    elif description.audio:
        media_type = "audio"
        media_file_id = description.audio.file_id
        caption = description.caption
        logger.info(f"User {user_id} provided audio description with caption: {caption[:20] if caption else 'No caption'}")
    elif description.voice:
        media_type = "voice"
        media_file_id = description.voice.file_id
        caption = description.caption
        logger.info(f"User {user_id} provided voice description with caption: {caption[:20] if caption else 'No caption'}")
    else:
        logger.warning(f"User {user_id} provided an unsupported message type")
        return False, "Please provide either text or media content for your ticket."

    timestamp = get_timestamp()

    ticket_info = (
        f"🎫 NEW TICKET #{user_id}\n"
        f"👤 User: {callback_query.from_user.first_name} (@{callback_query.from_user.username or 'N/A'})\n"
        f"📝 Category: {issue_type.capitalize()}\n"
        f"⏰ Time: {timestamp}\n"
    )
    
    if description_text:
        ticket_info += f"🔍 Message:\n{description_text}"
    elif caption:
        ticket_info += f"🔍 Message:\n{caption}\n\n(Media attached)"
    else:
        ticket_info += "🔍 Message: (Media without text)"

    try:
        if media_type:
            if media_type == "photo":
                channel_message = await client.send_photo(
                    SUPPORT_CHANNEL_ID,
                    photo=media_file_id,
                    caption=ticket_info
                )
            elif media_type == "video":
                channel_message = await client.send_video(
                    SUPPORT_CHANNEL_ID,
                    video=media_file_id,
                    caption=ticket_info
                )
            elif media_type == "document":
                channel_message = await client.send_document(
                    SUPPORT_CHANNEL_ID,
                    document=media_file_id,
                    caption=ticket_info
                )
            elif media_type == "audio":
                channel_message = await client.send_audio(
                    SUPPORT_CHANNEL_ID,
                    audio=media_file_id,
                    caption=ticket_info
                )
            elif media_type == "voice":
                channel_message = await client.send_voice(
                    SUPPORT_CHANNEL_ID,
                    voice=media_file_id,
                    caption=ticket_info
                )
        else:
            channel_message = await client.send_message(SUPPORT_CHANNEL_ID, ticket_info)

        channel_message_url = get_channel_message_url(SUPPORT_CHANNEL_ID, channel_message.id)

        tracking_data[str(user_id)] = {
            "channel_id": SUPPORT_CHANNEL_ID,
            "channel_message_id": channel_message.id,
            "channel_message_url": channel_message_url,
            "user_id": user_id,
            "issue_type": issue_type,
            "status": "pending_discussion_forward",
            "timestamp": channel_message.date.timestamp(),
            "timestamp_utc7": timestamp,
            "media_type": media_type, 
            "last_activity": timestamp
        }

        conversations_data[str(user_id)].append({
            "sender": "user",
            "message_id": description.id,
            "text": description_text or caption or "",
            "media_type": media_type,
            "media_file_id": media_file_id,
            "timestamp": description.date.timestamp(),
            "timestamp_utc7": timestamp
        })

        save_tracking_data(tracking_data)

        save_conversations_data(conversations_data)
        
        logger.info(f"Ticket for user {user_id} created and forwarded to channel - Message ID: {channel_message.id}")
        logger.info(f"Channel message URL: {channel_message_url}")

        response_message = (
            "🎫 Your ticket has been created and forwarded to our support team.\n"
            "We will respond as soon as possible.\n"
            "You can close this ticket at any time with /close_ticket"
        )

        user_name = f"{callback_query.from_user.first_name}"
        if callback_query.from_user.username:
            user_name += f" (@{callback_query.from_user.username})"

        await notify_support_staff_about_new_ticket(
            client, 
            user_id, 
            user_name, 
            issue_type, 
            timestamp, 
            description_text or caption or "", 
            channel_message_url
        )
        
        return True, response_message
    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        return False, f"Error creating your ticket: {e}"

async def process_user_ticket_closure(client, user_id, message):
    """Process ticket closure initiated by a user"""
    logger.info(f"Processing ticket closure by user {user_id}")

    tracking_data = load_tracking_data()
    conversations_data = load_conversations_data()

    if str(user_id) not in tracking_data:
        return False, "You don't have an open ticket."

    user_name = f"{message.from_user.first_name}"
    if message.from_user.username:
        user_name += f" (@{message.from_user.username})"

    success, result = await close_ticket(client, tracking_data, conversations_data, user_id, user_name, is_staff=False)
    
    if success:
        if str(user_id) in conversations_data:
            del conversations_data[str(user_id)]
            save_conversations_data(conversations_data)
            logger.info(f"Removed conversation data for user {user_id}")
            
        if str(user_id) in tracking_data:
            del tracking_data[str(user_id)]
            save_tracking_data(tracking_data)
            logger.info(f"Removed tracking data for user {user_id}")
        
        # Create detailed notification
        channel_url = result.get("channel_url", "")
        timestamp = result.get("timestamp", "")
        issue_type = result.get("issue_type", "").capitalize()
        
        # Prepare user notification
        notification = (
            f"✅ Your ticket has been closed.\n\n"
            f"📝 Category: {issue_type}\n"
            f"⏰ Closed on: {timestamp}\n"
            f"👤 Closed by: You\n\n"
        )
                    
        notification += "Thank you for contacting us. If you have another question, please use /create_ticket to create a new ticket."

        staff_notification = (
            f"🔒 TICKET CLOSED\n\n"
            f"👤 User: {user_name} (ID: {user_id})\n"
            f"📝 Category: {issue_type}\n"
            f"⏰ Closed on: {timestamp}\n"
            f"✅ Closed by: User\n\n"
        )
        
        if channel_url:
            staff_notification += f"🔗 [View Ticket]({channel_url})"

        for staff_id in SUPPORT_STAFF_IDS:
            try:
                await client.send_message(
                    staff_id,
                    staff_notification,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"Notified support staff {staff_id} about ticket closure by user")
            except Exception as e:
                logger.error(f"Failed to notify support staff {staff_id} about ticket closure: {e}")
                
        return True, notification
    else:
        logger.error(f"Error in process_user_ticket_closure: {result}")
        return False, "An error occurred while closing the ticket. Please try again later or contact an administrator."