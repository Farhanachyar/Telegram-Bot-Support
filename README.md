# 🤖 Telegram Support Bot

A powerful Telegram bot that helps manage support tickets between users and your support staff, with seamless media handling, collaborative discussion, and ticket management capabilities.

## ✨ Features

- 🎫 Create and manage support tickets
- 📨 Forward messages between users and support staff
- 🖼️ Process any media type (photos, videos, documents, etc.)
- 📣 Send notifications for new tickets, replies, and closed tickets
- 👥 Support for multiple staff members
- 💬 Open discussion format for staff to collaborate on tickets
- 🔄 Simple command interface with `/create_ticket` and `/close_ticket`

## 📋 Prerequisites

- Python 3.6 or higher
- Pyrogram library
- A Telegram account
- Bot token from [@BotFather](https://t.me/BotFather)

## 🔧 Telegram Channel & Group Setup

This bot requires:
1. A Telegram channel where support tickets will be posted
2. A discussion group linked to that channel where staff can collaborate
3. Your bot must be an admin in both the channel and discussion group

**How to link a discussion group to a channel:**
1. Go to your channel
2. Click on the channel name at the top
3. Select "Manage Channel"
4. Select "Discussion"
5. Choose an existing group or create a new one
6. Make sure your bot is an admin in both places

## 🚀 Quick Deployment

### ☁️ Deploy to Koyeb (Recommended)

The easiest way to deploy this bot is using Koyeb's one-click deployment:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=telegram-bot-support&repository=Farhanachyar%2FTelegram-Bot-Support&branch=main&builder=dockerfile&instance_type=free&instances_min=0&autoscaling_sleep_idle_delay=300)

1. Fork the repository to your GitHub account
2. Use the deploy button above to connect with Koyeb
3. **Important**: You must manually add all required environment variables in the Koyeb interface:
   - `API_ID` (from my.telegram.org)
   - `API_HASH` (from my.telegram.org)
   - `BOT_TOKEN` (from BotFather)
   - `SUPPORT_CHANNEL_ID` (from ChatID_HyperBot)
   - `DISCUSSION_GROUP_ID` (from ChatID_HyperBot)
   - `SUPPORT_STAFF_IDS` (comma-separated list of staff User IDs)
4. Deploy and enjoy your support bot!

### 🛠️ Manual Installation

#### Step 1: Clone the repository
```bash
git clone https://github.com/Farhanachyar/Telegram-Bot-Support.git
cd Telegram-Bot-Support
```

#### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Get your API credentials
1. **API ID & API Hash**:
   - Visit [my.telegram.org](https://my.telegram.org/auth)
   - Log in with your phone number
   - Click on "API Development tools"
   - Create a new application (fill in all required fields)
   - Your API ID and Hash will be displayed

2. **Bot Token**:
   - Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow the instructions
   - Choose a name and username for your bot
   - Once created, you'll receive a bot token

#### Step 4: Setup your channels and get required IDs

1. Create a Telegram channel for support tickets
2. Link this channel with a discussion group for staff collaboration
3. **Add your newly created bot as an admin** to both the channel and discussion group
4. Send a random message in your channel
5. Send a random message in your discussion group
6. Forward both messages to [@ChatID_HyperBot](https://t.me/ChatID_HyperBot)
7. ChatID_HyperBot will respond with the Chat IDs you need:
   - Use the channel message's Chat ID as your SUPPORT_CHANNEL_ID
   - Use the group message's Chat ID as your DISCUSSION_GROUP_ID
8. For SUPPORT_STAFF_IDS, have each staff member send a message to ChatID_HyperBot to get their User IDs

> ⚠️ **Important**: ChatID_HyperBot is only used to retrieve the necessary IDs. Your own support bot (not ChatID_HyperBot) must be added as an admin to both your channel and discussion group.

> ⚠️ **Important**: After successfully deploying and starting your bot, send a random message to it right away to prevent "peer ID invalid" errors. This must be done after the bot is already active.

#### Step 5: Configure environment variables

Create a `.env` file with the following variables:

```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
SUPPORT_CHANNEL_ID=your_channel_id
DISCUSSION_GROUP_ID=your_group_id
SUPPORT_STAFF_IDS=id1,id2,id3
```

#### Step 6: Run the bot
```bash
python main.py
```

## 🐳 Docker Deployment

This repository includes a Dockerfile for easy deployment.

```bash
# Build the Docker image
docker build -t telegram-support-bot .

# Run the container with environment variables
docker run -d \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e BOT_TOKEN=your_bot_token \
  -e SUPPORT_CHANNEL_ID=your_channel_id \
  -e DISCUSSION_GROUP_ID=your_group_id \
  -e SUPPORT_STAFF_IDS=id1,id2,id3 \
  telegram-support-bot
```

> ⚠️ **Note for Koyeb users**: The Dockerfile helps simplify deployment, but you must still manually add all the environment variables listed above in the Koyeb interface for your bot to function properly.

## 📝 Usage

### For Users:
1. Start a chat with your bot on Telegram
2. Send `/start` to begin
3. Use `/create_ticket` followed by your issue to open a support ticket
4. Wait for staff to respond to your ticket
5. Use `/close_ticket` when your issue has been resolved

### For Support Staff:
1. Ensure you're added to the SUPPORT_STAFF_IDS list
2. Monitor the support channel for new tickets
3. Reply to messages directly in the discussion section of the channel posts
4. All staff members can see and participate in the open discussion for each ticket
5. Use `/close_ticket` to close a resolved ticket

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## ⭐ Support

If you find this project helpful, please consider giving it a star on GitHub! It helps a lot.

<a href="https://github.com/Farhanachyar/Telegram-Bot-Support">
  <img src="https://img.shields.io/github/stars/Farhanachyar/Telegram-Bot-Support?style=social" alt="GitHub stars">
</a>

You can also:
- 💻 Check out my other projects on [GitHub](https://github.com/farhanachyar)

Your support motivates me to create more useful tools and projects!

---
Made with ❤️ by [Farhanachyar](https://github.com/farhanachyar)
