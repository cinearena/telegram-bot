from http.server import BaseHTTPRequestHandler
import json
import os
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import threading

# Get token from environment variable
TOKEN = os.getenv("BOT_TOKEN", "8410891252:AAEDNVXneNwzziQTubfr3Px9ngjyrakVX2o")
WEBSITE_URL = "https://cinearena.live"

# Store bot application globally
bot_app = None
bot_thread = None

def init_bot():
    """Initialize the Telegram bot"""
    global bot_app
    
    bot_app = Application.builder().token(TOKEN).build()
    
    async def start(update: Update, context: CallbackContext) -> None:
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        keyboard = [[InlineKeyboardButton("🎬 Visit CineArena Live", url=WEBSITE_URL)]]
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
    
    async def handle_message(update: Update, context: CallbackContext) -> None:
        if update.message.text and update.message.text.startswith('/'):
            return
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        keyboard = [[InlineKeyboardButton("🎬 Visit CineArena Live Now", url=WEBSITE_URL)]]
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
    
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", start))
    bot_app.add_handler(CommandHandler("link", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

def run_bot():
    """Run the bot in polling mode"""
    global bot_app
    if bot_app:
        bot_app.run_polling(drop_pending_updates=True)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for webhook setup or status check"""
        if self.path == '/api/bot':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "online",
                "message": "CineArena Live Bot",
                "website": WEBSITE_URL,
                "endpoints": {
                    "webhook": "/api/bot/webhook",
                    "status": "/api/bot/status"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/api/bot/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "running",
                "bot": "CineArena Live Bot",
                "timestamp": "2024-01-01T00:00:00Z"
            }
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """Handle POST requests for webhook"""
        if self.path == '/api/bot/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Process webhook update
            try:
                update_data = json.loads(post_data.decode('utf-8'))
                print(f"Received update: {update_data}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "received"}).encode())
            except:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid data"}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
