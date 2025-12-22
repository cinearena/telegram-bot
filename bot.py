import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token (Replace with your actual token)
TOKEN = "8410891252:AAEDNVXneNwzziQTubfr3Px9ngjyrakVX2o"

# The fixed link
WEBSITE_URL = "https://cinearena.live"
WEBSITE_NAME = "CineArena Live"

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    keyboard = [
        [InlineKeyboardButton("🎬 Visit CineArena Live", url=WEBSITE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
    🎬 *Welcome to CineArena Live Bot!*
    
    *Stream movies and TV shows for FREE!*
    
    📌 *Click below to visit:*
    {WEBSITE_URL}
    
    ⭐ *Features:*
    • HD Streaming
    • No Registration Required
    • Latest Movies & TV Shows
    • Free Access
    
    *Simply type anything to get the link!*
    """
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message."""
    keyboard = [
        [InlineKeyboardButton("🎬 Visit CineArena Live", url=WEBSITE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = f"""
    *🎬 CineArena Live Help*
    
    This bot provides the link to CineArena Live.
    
    *Commands:*
    /start - Start the bot
    /help - Show this message
    /link - Get the direct link
    
    *Simply type ANY message* to get the CineArena Live link!
    
    *Website:* {WEBSITE_URL}
    """
    await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

async def send_link(update: Update, context: CallbackContext) -> None:
    """Send the CineArena Live link."""
    keyboard = [
        [InlineKeyboardButton("🎬 Click to Visit CineArena Live", url=WEBSITE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # You received: {update.message.text}
    message_text = f"""
    🎬 *CineArena Live*
    
    📌 *Click below to visit:*
    
    🎥 Stream movies & TV shows FREE
    ⭐ HD Quality • No Registration
    🆓 Completely Free Access
    
    *Link:* {WEBSITE_URL}
    """
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def link_command(update: Update, context: CallbackContext) -> None:
    """Send only the link when /link command is used."""
    keyboard = [
        [InlineKeyboardButton("🎬 Direct Link to CineArena Live", url=WEBSITE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = "🎬 *CineArena Live*\n\n📌 *Click below:*"
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_all_messages(update: Update, context: CallbackContext) -> None:
    """Handle ALL text messages with the link."""
    # Check if it's a command (already handled)
    if update.message.text.startswith('/'):
        return
    
    # Send the link for ALL other messages
    keyboard = [
        [InlineKeyboardButton("🎬 Visit CineArena Live Now", url=WEBSITE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = """
    🎬 *CineArena Live*
    
    📌 *Click below:*
    
    Watch movies and TV shows for FREE!
    No registration required.
    Updated daily with new content.
    
    Enjoy your streaming! 🍿🎥
    """
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("link", link_command))
    
    # Register message handler for ALL text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

    # Start the bot
    print("🎬 CineArena Live Bot is running...")
    print("🤖 Bot will always reply with: https://cinearena.live")
    print("🛑 Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
