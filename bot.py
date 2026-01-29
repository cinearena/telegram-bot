import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, render_template_string, request
import threading
import asyncio

# ================= CONFIGURATION =================
TOKEN = os.getenv("BOT_TOKEN", "8410891252:AAEDNVXneNwzziQTubfr3Px9ngjyrakVX2o")
WEBSITE_URL = "https://cinearena.live"
PORT = int(os.getenv("PORT", 5000))

# ================= FLASK WEB APP =================
app = Flask(__name__)

@app.route('/')
def home():
    """Home page with bot status"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CineArena Live Telegram Bot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 800px;
                width: 100%;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .header h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .status {
                background: #f0f9ff;
                border-left: 5px solid #2196f3;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 8px;
            }
            
            .status.online {
                border-left-color: #4CAF50;
                background: #f1f8e9;
            }
            
            .card {
                background: #f8f9fa;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                border: 1px solid #e9ecef;
            }
            
            .card h3 {
                color: #333;
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            
            .button {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 28px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                font-size: 1.1em;
                transition: transform 0.3s, box-shadow 0.3s;
                border: none;
                cursor: pointer;
                margin: 10px 5px;
            }
            
            .button:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
                color: white;
                text-decoration: none;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 25px 0;
            }
            
            .stat-box {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
                border: 1px solid #e0e0e0;
            }
            
            .stat-box .number {
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 5px;
            }
            
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 0.9em;
                padding-top: 20px;
                border-top: 1px solid #eee;
            }
            
            .telegram-badge {
                display: inline-flex;
                align-items: center;
                background: #0088cc;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                text-decoration: none;
                margin: 10px 0;
            }
            
            .telegram-badge:hover {
                background: #0077b5;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎬 CineArena Live Bot</h1>
                <p>Telegram Bot for Free Movie Streaming</p>
            </div>
            
            <div class="status online">
                <strong>✅ Status: ONLINE</strong>
                <p>Bot is running 24/7 on server</p>
            </div>
            
            <div class="card">
                <h3>🤖 About This Bot</h3>
                <p>This Telegram bot provides instant access to CineArena Live - a free movie streaming platform.</p>
                <p>Simply message the bot on Telegram and it will reply with the streaming link!</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="number">24/7</div>
                    <div>Uptime</div>
                </div>
                <div class="stat-box">
                    <div class="number">🎥</div>
                    <div>Free Movies</div>
                </div>
                <div class="stat-box">
                    <div class="number">⚡</div>
                    <div>Instant Link</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🔗 Quick Links</h3>
                <p>
                    <a href="https://t.me/YourBotUsername" class="telegram-badge" target="_blank">
                        💬 Start Chatting with Bot
                    </a>
                </p>
                <p>
                    <a href="https://cinearena.live" class="button" target="_blank">
                        🎬 Visit CineArena Live
                    </a>
                    
                    <a href="https://github.com/yourusername/cinearena-bot" class="button" style="background: linear-gradient(135deg, #333 0%, #666 100%);" target="_blank">
                        📦 View Source Code
                    </a>
                </p>
            </div>
            
            <div class="card">
                <h3>📱 How to Use</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li>Open Telegram app</li>
                    <li>Search for @YourBotUsername</li>
                    <li>Click "Start" or send any message</li>
                    <li>Get instant link to CineArena Live</li>
                    <li>Enjoy free streaming!</li>
                </ol>
            </div>
            
            <div class="footer">
                <p>© 2024 CineArena Live Bot | Powered by Python & Telegram API</p>
                <p>Always free • No registration • HD Quality</p>
            </div>
        </div>
        
        <script>
            // Simple real-time update (optional)
            function updateTime() {
                const now = new Date();
                document.querySelector('.status p').innerHTML = 
                    `Bot is running 24/7 on server | Last checked: ${now.toLocaleTimeString()}`;
            }
            
            // Update every 30 seconds
            setInterval(updateTime, 30000);
            updateTime();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/bot-status')
def bot_status():
    """API endpoint to check bot status"""
    return {"status": "online", "website": WEBSITE_URL, "timestamp": "2024-01-01T00:00:00Z"}

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return "OK", 200

# ================= TELEGRAM BOT FUNCTIONS =================
async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
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
    
    *Web Dashboard:* https://your-domain.railway.app
    
    *Simply type anything to get the link!*
    """
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_all_messages(update: Update, context: CallbackContext) -> None:
    """Handle ALL text messages with the link."""
    if update.message.text and update.message.text.startswith('/'):
        return
    
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

# ================= MAIN FUNCTION =================
def run_flask():
    """Run Flask web server"""
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)

def run_telegram_bot():
    """Run Telegram bot"""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("link", start))
    
    # Register message handler for ALL text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

    print("🎬 CineArena Live Bot is running...")
    print(f"🌐 Web Dashboard: http://localhost:{PORT}")
    print(f"🤖 Bot will always reply with: {WEBSITE_URL}")
    
    application.run_polling(drop_pending_updates=True)

def main():
    """Run both Flask web server and Telegram bot"""
    print("🚀 Starting CineArena Live Bot with Web Interface...")
    
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print(f"✅ Flask server started on port {PORT}")
    
    # Run Telegram bot in main thread
    run_telegram_bot()

if __name__ == '__main__':
    main()
