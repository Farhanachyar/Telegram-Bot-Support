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

## 🚀 Quick Deployment

### ☁️ Deploy to Koyeb (Recommended)

The easiest way to deploy this bot is using Koyeb's one-click deployment:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=hyperbot-assist&repository=Xylence2%2FHyperBot-Assist&branch=main&regions=tyo)

1. Fork the repository to your GitHub account
2. Use the deploy button above to connect with Koyeb
3. Configure the environment variables (see below)
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

#### Step 4: Setup required IDs using ChatID_HyperBot

To get the required Channel ID, Group ID, and User IDs, you'll need to use [@ChatID_HyperBot](https://t.me/ChatID_HyperBot):

1. Start a chat with [@ChatID_HyperBot](https://t.me/ChatID_HyperBot)
2. Send a random message to the bot to get your User ID
3. Create a Telegram channel for support tickets
4. Link this channel with a discussion group for staff collaboration
5. Add the bot to your support channel and forward a message to get SUPPORT_CHANNEL_ID
6. Add the bot to your discussion group and forward a message to get DISCUSSION_GROUP_ID
7. Get the IDs of your support staff members the same way

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


> ⚠️ **Important**: After successfully deploying and starting your bot, send a random message to it right away to prevent "peer ID invalid" errors. This must be done after the bot is already active.

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
