import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token (Replace with your actual token)
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Sample website database (you can expand this)
WEBSITES = {
    "google": {"url": "https://www.google.com", "name": "Google Search"},
    "youtube": {"url": "https://www.youtube.com", "name": "YouTube"},
    "github": {"url": "https://www.github.com", "name": "GitHub"},
    "wikipedia": {"url": "https://www.wikipedia.org", "name": "Wikipedia"},
    "amazon": {"url": "https://www.amazon.com", "name": "Amazon"},
    "netflix": {"url": "https://www.netflix.com", "name": "Netflix"},
    "twitter": {"url": "https://twitter.com", "name": "Twitter"},
    "facebook": {"url": "https://www.facebook.com", "name": "Facebook"},
    "instagram": {"url": "https://www.instagram.com", "name": "Instagram"},
    "reddit": {"url": "https://www.reddit.com", "name": "Reddit"},
    "stackoverflow": {"url": "https://stackoverflow.com", "name": "Stack Overflow"},
    "linkedin": {"url": "https://www.linkedin.com", "name": "LinkedIn"},
}

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    welcome_text = """
    👋 *Welcome to Website Finder Bot!*
    
    *How to use:*
    1. Type any website name (e.g., google, youtube, github)
    2. I'll find the website link for you
    3. Click the button below to visit the website
    
    *Try typing:* google, youtube, github, wikipedia, etc.
    
    Or use /help for more information.
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message."""
    help_text = """
    *Help Guide*
    
    *Commands:*
    /start - Start the bot
    /help - Show this help message
    /websites - List all available websites
    
    *Simply type* any website name (like "google", "youtube") and I'll provide the link.
    
    *Example:* Type "google" to get Google's link.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def list_websites(update: Update, context: CallbackContext) -> None:
    """List all available websites."""
    websites_list = "*Available Websites:*\n\n"
    for key in sorted(WEBSITES.keys()):
        websites_list += f"• {key.capitalize()}\n"
    
    websites_list += "\nType any of these names to get the link!"
    await update.message.reply_text(websites_list, parse_mode='Markdown')

async def search_website(update: Update, context: CallbackContext) -> None:
    """Handle user search queries."""
    user_message = update.message.text.strip().lower()
    
    # Check if query matches any website
    found = False
    for key, info in WEBSITES.items():
        if key in user_message or user_message in key:
            # Create inline keyboard with website button
            keyboard = [
                [InlineKeyboardButton(f"🌐 Visit {info['name']}", url=info['url'])]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send message with link
            message_text = f"🔍 *{info['name']}*\n\n📌 *Click below to visit:*"
            await update.message.reply_text(
                message_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            found = True
            break
    
    # If no website found
    if not found:
        # Try fuzzy matching
        suggestions = []
        for key in WEBSITES.keys():
            if user_message in key or any(word in key for word in user_message.split()):
                suggestions.append(key)
        
        if suggestions:
            suggestion_text = "Did you mean:\n"
            for suggestion in suggestions[:5]:  # Limit to 5 suggestions
                suggestion_text += f"• {suggestion.capitalize()}\n"
            await update.message.reply_text(suggestion_text)
        else:
            await update.message.reply_text(
                "❌ Website not found in database.\n\n"
                "Try: google, youtube, github, wikipedia, amazon, etc.\n"
                "Or use /websites to see all available websites."
            )

async def handle_callback(update: Update, context: CallbackContext) -> None:
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("websites", list_websites))
    
    # Register callback handler for buttons
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Register message handler for search queries
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_website))

    # Start the bot
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
