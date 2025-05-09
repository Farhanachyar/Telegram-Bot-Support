from datetime import datetime, timezone, timedelta

def get_timestamp():
    """Get current timestamp in UTC+7 timezone"""
    utc7 = timezone(timedelta(hours=7))
    now = datetime.now(timezone.utc).astimezone(utc7)

    return now.strftime("%d-%m-%Y %H:%M:%S UTC+7")

def get_channel_message_url(channel_id, message_id):
    """Get URL for a message in a channel"""
    channel_id_str = str(channel_id)
    if channel_id_str.startswith('-100'):
        channel_id_for_url = channel_id_str[4:]
    else:
        channel_id_for_url = channel_id_str
        
    return f"https://t.me/c/{channel_id_for_url}/{message_id}"