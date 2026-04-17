import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# معلوماتك التي حفظتها
TOKEN = "8684000990:AAGeHMFAnRpxEqrA5Q4ZAUu606CSvKnc2rk"
OWNER_ID = 8401353611

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 أرقام أمريكية", callback_query='num')],
        [InlineKeyboardButton("🇾🇪 أرقام يمنية", callback_query='num')],
        [InlineKeyboardButton("👨‍💻 المطور", url=f"tg://user?id={OWNER_ID}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"مرحباً بك يا إبراهيم في بوت الأرقام المجاني الخاص بك!\n\nاختر الدولة:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="هذا الرقم مجاني حالياً: +12025550100\nانتظر الكود هنا...")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
