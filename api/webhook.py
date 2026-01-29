from http.server import BaseHTTPRequestHandler
import json
import os
import hmac
import hashlib
from telegram import Bot, Update
import asyncio

TOKEN = os.getenv("BOT_TOKEN", "8410891252:AAEDNVXneNwzziQTubfr3Px9ngjyrakVX2o")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")
WEBSITE_URL = "https://cinearena.live"

bot = Bot(token=TOKEN)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for status and setup"""
        if self.path == '/api/webhook/setup':
            # Set webhook URL
            webhook_url = f"https://{self.headers.get('Host')}/api/webhook"
            asyncio.run(self.set_webhook(webhook_url))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "webhook_set",
                "url": webhook_url,
                "message": "Webhook configured successfully"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/webhook/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "online",
                "bot": "CineArena Live Bot",
                "website": WEBSITE_URL
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """Handle Telegram webhook updates"""
        if self.path == '/api/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                update_data = json.loads(post_data.decode('utf-8'))
                update = Update.de_json(update_data, bot)
                
                # Process update asynchronously
                asyncio.run(self.process_update(update))
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode())
                
            except Exception as e:
                print(f"Error processing update: {e}")
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    async def set_webhook(self, url):
        """Set webhook URL on Telegram"""
        await bot.set_webhook(url=url)
    
    async def process_update(self, update: Update):
        """Process incoming Telegram update"""
        if update.message:
            if update.message.text:
                text = update.message.text.lower()
                
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                
                keyboard = [[InlineKeyboardButton("🎬 Visit CineArena Live", url=WEBSITE_URL)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                if text.startswith('/start') or text.startswith('/help'):
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
                
                else:
                    message_text = """
                    🎬 *CineArena Live*
                    
                    📌 *Click below:*
                    
                    Watch movies and TV shows for FREE!
                    No registration required.
                    Updated daily with new content.
                    
                    Enjoy your streaming! 🍿🎥
                    """
                    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
