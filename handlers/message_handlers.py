import logging
from config import SUPPORT_CHANNEL_ID, DISCUSSION_GROUP_ID
from utils.data_manager import load_tracking_data, save_tracking_data
from utils.utils import get_timestamp
from utils.data_manager import load_tracking_data, save_tracking_data, load_conversations_data, save_conversations_data
from utils.ticket_manager import notify_support_staff
from helper import logger

async def process_forwarded_message(client, message, forward_from_chat_id, forward_from_message_id):
    if forward_from_chat_id != SUPPORT_CHANNEL_ID:
        return False, "Message not forwarded from our support channel"
        
    logger.info(f"Processing forwarded message from channel to discussion group")
    logger.info(f"Original message ID: {forward_from_message_id}")
    logger.info(f"Discussion group message ID: {message.id}")

    tracking_data = load_tracking_data()

    channel_message_id = forward_from_message_id
    found_user_id = None

    for user_id, data in tracking_data.items():
        if data.get("channel_message_id") == channel_message_id:
            found_user_id = user_id
            break
    
    if not found_user_id:
        logger.warning(f"Could not find user associated with channel message ID {channel_message_id}")
        return False, "Could not find associated user"
 
    tracking_data[found_user_id].update({
        "discussion_group_id": DISCUSSION_GROUP_ID,
        "discussion_message_id": message.id,
        "status": "forwarded_to_discussion",
        "forward_timestamp": message.date.timestamp(),
        "forward_timestamp_utc7": get_timestamp(),
        "last_activity": get_timestamp()
    })

    save_tracking_data(tracking_data)
        
    logger.info(f"Updated tracking for user {found_user_id} with discussion group info")
    return True, found_user_id

async def process_user_message(client, message, is_reply=False):
    """Process a message from a user"""
    
    return await process_user_message(client, message, is_reply)

async def process_user_message(client, message, is_reply=False):
    user_id = message.from_user.id

    tracking_data = load_tracking_data()
    conversations_data = load_conversations_data()

    if str(user_id) not in tracking_data:
        await message.reply("You don't have an active ticket. Use /create_ticket to open a new ticket.")
        return False

    timestamp = get_timestamp()

    tracking_data[str(user_id)]["last_activity"] = timestamp
    save_tracking_data(tracking_data)

    ticket_data = tracking_data[str(user_id)]
    discussion_group_id = ticket_data.get("discussion_group_id", DISCUSSION_GROUP_ID)

    media_type = None
    media_file_id = None
    message_text = None
    
    if message.text:
        message_text = message.text
        logger.info(f"User {user_id} sent text: {message_text[:20]}...")
    elif message.photo:
        media_type = "photo"
        media_file_id = message.photo.file_id
        message_text = message.caption
        logger.info(f"User {user_id} sent photo with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.video:
        media_type = "video"
        media_file_id = message.video.file_id
        message_text = message.caption
        logger.info(f"User {user_id} sent video with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.document:
        media_type = "document"
        media_file_id = message.document.file_id
        message_text = message.caption
        logger.info(f"User {user_id} sent document with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.audio:
        media_type = "audio"
        media_file_id = message.audio.file_id
        message_text = message.caption
        logger.info(f"User {user_id} sent audio with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.voice:
        media_type = "voice"
        media_file_id = message.voice.file_id
        message_text = message.caption
        logger.info(f"User {user_id} sent voice with caption: {message_text[:20] if message_text else 'No caption'}")

    if str(user_id) not in conversations_data:
        conversations_data[str(user_id)] = []
    
    conversation_entry = {
        "sender": "user",
        "message_id": message.id,
        "text": message_text or "",
        "media_type": media_type,
        "media_file_id": media_file_id,
        "timestamp": message.date.timestamp(),
        "timestamp_utc7": timestamp,
    }

    if is_reply and message.reply_to_message:
        conversation_entry["reply_to_message_id"] = message.reply_to_message.id

        is_reply_to_staff = False
        staff_discussion_msg_id = None

        for msg in conversations_data.get(str(user_id), []):
            if msg.get("sender") == "staff" and msg.get("message_id") == message.reply_to_message.id:
                is_reply_to_staff = True
                staff_discussion_msg_id = msg.get("discussion_message_id")
                logger.info(f"User replying to staff message with ID {message.reply_to_message.id}")
                break
                
        conversation_entry["is_reply_to_staff"] = is_reply_to_staff
        
    conversations_data[str(user_id)].append(conversation_entry)
    
    user_info = f"👤 {message.from_user.first_name}"
    if message.from_user.username:
        user_info += f" (@{message.from_user.username})"

    if message_text:
        if is_reply:
            forward_text = f"{user_info} replied on {timestamp}:\n\n{message_text}"
        else:
            forward_text = f"{user_info} sent a message on {timestamp}:\n\n{message_text}"
    else:
        if is_reply:
            forward_text = f"{user_info} replied with media on {timestamp}."
        else:
            forward_text = f"{user_info} sent media on {timestamp}."

    reply_to_msg_id = None
    
    if is_reply and conversation_entry.get("is_reply_to_staff") and staff_discussion_msg_id:
        reply_to_msg_id = staff_discussion_msg_id
        logger.info(f"Will reply to staff message with ID {staff_discussion_msg_id} in discussion group")
    else:
        reply_to_msg_id = ticket_data.get("discussion_message_id")
        logger.info(f"Will reply to original message with ID {reply_to_msg_id} in discussion group")
    
    try:
        if media_type:
            if media_type == "photo":
                discussion_msg = await client.send_photo(
                    discussion_group_id,
                    photo=media_file_id,
                    caption=forward_text,
                    reply_to_message_id=reply_to_msg_id
                )
            elif media_type == "video":
                discussion_msg = await client.send_video(
                    discussion_group_id,
                    video=media_file_id,
                    caption=forward_text,
                    reply_to_message_id=reply_to_msg_id
                )
            elif media_type == "document":
                discussion_msg = await client.send_document(
                    discussion_group_id,
                    document=media_file_id,
                    caption=forward_text,
                    reply_to_message_id=reply_to_msg_id
                )
            elif media_type == "audio":
                discussion_msg = await client.send_audio(
                    discussion_group_id,
                    audio=media_file_id,
                    caption=forward_text,
                    reply_to_message_id=reply_to_msg_id
                )
            elif media_type == "voice":
                discussion_msg = await client.send_voice(
                    discussion_group_id,
                    voice=media_file_id,
                    caption=forward_text,
                    reply_to_message_id=reply_to_msg_id
                )
        else:
            discussion_msg = await client.send_message(
                discussion_group_id,
                forward_text,
                reply_to_message_id=reply_to_msg_id
            )

        conversations_data[str(user_id)][-1]["discussion_message_id"] = discussion_msg.id
        save_conversations_data(conversations_data)

        user_name = f"{message.from_user.first_name}"
        if message.from_user.username:
            user_name += f" (@{message.from_user.username})"
            
        await notify_support_staff(
            client, 
            user_id, 
            user_name, 
            message_text or "", 
            discussion_group_id,
            discussion_msg.id
        )
        
        logger.info(f"User message forwarded to discussion group - Message ID: {discussion_msg.id}")
        await message.reply("✅ Your message has been forwarded to our support team.", quote=True)
        return True
    except Exception as e:
        logger.error(f"Error processing user message: {e}")
        await message.reply("❌ An error occurred while processing your message. Please try again later.", quote=True)
        return False

async def process_staff_reply(client, message):
    replied_msg_id = message.reply_to_message.id
    logger.info(f"Staff replying to message ID {replied_msg_id} in discussion group")

    tracking_data = load_tracking_data()
    conversations_data = load_conversations_data()

    media_type = None
    media_file_id = None
    message_text = None
    
    if message.text:
        message_text = message.text
        logger.info(f"Staff sent text reply: {message_text[:20]}...")
    elif message.photo:
        media_type = "photo"
        media_file_id = message.photo.file_id
        message_text = message.caption
        logger.info(f"Staff sent photo reply with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.video:
        media_type = "video"
        media_file_id = message.video.file_id
        message_text = message.caption
        logger.info(f"Staff sent video reply with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.document:
        media_type = "document"
        media_file_id = message.document.file_id
        message_text = message.caption
        logger.info(f"Staff sent document reply with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.audio:
        media_type = "audio"
        media_file_id = message.audio.file_id
        message_text = message.caption
        logger.info(f"Staff sent audio reply with caption: {message_text[:20] if message_text else 'No caption'}")
    elif message.voice:
        media_type = "voice"
        media_file_id = message.voice.file_id
        message_text = message.caption
        logger.info(f"Staff sent voice reply with caption: {message_text[:20] if message_text else 'No caption'}")

    found_user_id = None
    original_user_message_id = None

    for user_id, data in tracking_data.items():
        if data.get("discussion_message_id") == replied_msg_id:
            found_user_id = user_id
            logger.info(f"Found user {user_id} - replying to original discussion message")
            break

    if not found_user_id:
        for user_id, messages in conversations_data.items():
            for msg in messages:
                if msg.get("discussion_message_id") == replied_msg_id:
                    found_user_id = user_id
                    original_user_message_id = msg.get("message_id")
                    logger.info(f"Found user {user_id} associated with message ID {replied_msg_id}")
                    break
            if found_user_id:
                break
    
    if found_user_id:
        user_id_int = int(found_user_id)
        logger.info(f"Staff replied to message in discussion group for user {found_user_id}")

        timestamp = get_timestamp()

        if found_user_id in tracking_data:
            tracking_data[found_user_id]["last_activity"] = timestamp
            save_tracking_data(tracking_data)

        if message_text:
            reply_text = f"💬 Reply from Support Staff:\n\n{message_text}"
        else:
            reply_text = f"💬 Reply from Support Staff:"
        
        try:
            if original_user_message_id:
                if media_type:
                    if media_type == "photo":
                        user_msg = await client.send_photo(
                            user_id_int,
                            photo=media_file_id,
                            caption=reply_text,
                            reply_to_message_id=original_user_message_id
                        )
                    elif media_type == "video":
                        user_msg = await client.send_video(
                            user_id_int,
                            video=media_file_id,
                            caption=reply_text,
                            reply_to_message_id=original_user_message_id
                        )
                    elif media_type == "document":
                        user_msg = await client.send_document(
                            user_id_int,
                            document=media_file_id,
                            caption=reply_text,
                            reply_to_message_id=original_user_message_id
                        )
                    elif media_type == "audio":
                        user_msg = await client.send_audio(
                            user_id_int,
                            audio=media_file_id,
                            caption=reply_text,
                            reply_to_message_id=original_user_message_id
                        )
                    elif media_type == "voice":
                        user_msg = await client.send_voice(
                            user_id_int,
                            voice=media_file_id,
                            caption=reply_text,
                            reply_to_message_id=original_user_message_id
                        )
                else:
                    user_msg = await client.send_message(
                        user_id_int, 
                        reply_text,
                        reply_to_message_id=original_user_message_id
                    )
                logger.info(f"Sent reply to user's message with ID {original_user_message_id}")
            else:
                if media_type:
                    if media_type == "photo":
                        user_msg = await client.send_photo(
                            user_id_int,
                            photo=media_file_id,
                            caption=reply_text
                        )
                    elif media_type == "video":
                        user_msg = await client.send_video(
                            user_id_int,
                            video=media_file_id,
                            caption=reply_text
                        )
                    elif media_type == "document":
                        user_msg = await client.send_document(
                            user_id_int,
                            document=media_file_id,
                            caption=reply_text
                        )
                    elif media_type == "audio":
                        user_msg = await client.send_audio(
                            user_id_int,
                            audio=media_file_id,
                            caption=reply_text
                        )
                    elif media_type == "voice":
                        user_msg = await client.send_voice(
                            user_id_int,
                            voice=media_file_id,
                            caption=reply_text
                        )
                else:
                    user_msg = await client.send_message(user_id_int, reply_text)
                logger.info(f"Sent message to user without reply")

            if found_user_id not in conversations_data:
                conversations_data[found_user_id] = []
                
            conversations_data[found_user_id].append({
                "sender": "staff",
                "message_id": user_msg.id,
                "text": message_text or "",
                "media_type": media_type,
                "media_file_id": media_file_id,
                "discussion_message_id": message.id,
                "replied_to_discussion_msg_id": replied_msg_id,
                "timestamp": message.date.timestamp(),
                "timestamp_utc7": timestamp
            })

            save_conversations_data(conversations_data)
                
            logger.info(f"Staff reply forwarded to user {found_user_id} - Message ID: {user_msg.id}")

            await message.reply("✅ Message has been forwarded to the user.", quote=True)
            return True
        except Exception as e:
            logger.error(f"Error sending staff reply to user: {e}")
            await message.reply(f"❌ Error sending message to the user: {e}", quote=True)
            return False
    else:
        logger.warning(f"Could not find user associated with replied message ID {replied_msg_id}")
        await message.reply("❓ Cannot find the user associated with this message.", quote=True)
        return False