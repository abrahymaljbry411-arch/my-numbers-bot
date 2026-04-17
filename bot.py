import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات المدير
TOKEN = "8684000990:AAGeHMFAnRpxEqrA5Q4ZAUu606CSvKnc2rk"
OWNER_ID = 8401353611  # معرفك الشخصي

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# قائمة الدول
COUNTRIES = [
    ("اليمن 🇾🇪", "967"), ("هولندا 🇳🇱", "31"), ("أمريكا 🇺🇸", "1"), ("فنزويلا 🇻🇪", "58"),
    ("فيتنام 🇻🇳", "84"), ("روسيا 🇷🇺", "7"), ("أذربيجان 🇦🇿", "994"), ("تركيا 🇹🇷", "90"),
    ("مصر 🇪🇬", "20"), ("السعودية 🇸🇦", "966"), ("المغرب 🇲🇦", "212"), ("فرنسا 🇫🇷", "33")
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # إذا كان المستخدم هو أنت، سيظهر له رصيد مليون
    balance = "1,000,000" if user.id == OWNER_ID else "0.00"
    
    msg = (
        f"<b>مرحباً بك يا {user.first_name} في نظام التفعيل ⚡</b>\n\n"
        f"💰 رصيدك الحالي: <b>{balance} نقطة</b>\n"
        "━━━━━━━━━━━━━━\n"
        "💡 اختر الخدمة المطلوبة:"
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 WhatsApp", callback_data='app_واتساب'), InlineKeyboardButton("✈️ Telegram", callback_data='app_تلجرام')],
        [InlineKeyboardButton("🔵 Facebook", callback_data='app_فيسبوك'), InlineKeyboardButton("📸 Instagram", callback_data='app_انستجرام')]
    ]
    
    # إضافة زر لوحة التحكم للمدير فقط
    if user.id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("⚙️ لوحة تحكم المدير (Admin)", callback_data='admin_panel')])
    
    keyboard.append([InlineKeyboardButton("👨‍💻 المطور", url=f"tg://user?id={OWNER_ID}")])
    
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    # لوحة تحكم المشرف
    if data == 'admin_panel' and user_id == OWNER_ID:
        admin_msg = (
            "<b>🛠 لوحة تحكم المدير</b>\n\n"
            "مرحباً سيادة المشرف، لديك الصلاحيات الكاملة:"
        )
        admin_keys = [
            [InlineKeyboardButton("🚫 حظر مستخدم", callback_data='admin_block'), InlineKeyboardButton("✅ فك حظر", callback_data='admin_unblock')],
            [InlineKeyboardButton("💰 تحويل رصيد", callback_data='admin_transfer')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='back')]
        ]
        await query.edit_message_text(admin_msg, reply_markup=InlineKeyboardMarkup(admin_keys), parse_mode='HTML')

    elif data.startswith('app_'):
        app = data.split('_')[1]
        keyboard = []
        for i in range(0, len(COUNTRIES), 2):
            row = [
                InlineKeyboardButton(COUNTRIES[i][0], callback_data=f"buy_{app}_{COUNTRIES[i][1]}"),
                InlineKeyboardButton(COUNTRIES[i+1][0], callback_data=f"buy_{app}_{COUNTRIES[i+1][1]}")
            ]
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data='back')])
        await query.edit_message_text(f"<b>قسم {app} ✅</b>\nاختر الدولة:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    elif data.startswith('buy_'):
        app, code = data.split('_')[1], data.split('_')[2]
        phone = f"+{code}" + "771234567"
        msg = (
            f"<b>تم شراء الرقم لـ {app} ✅</b>\n\n"
            f"📞 الرقم: <code>{phone}</code>\n"
            "⚠️ <i>اضغط للنسخ، واطلب الكود في التطبيق.</i>"
        )
        keys = [[InlineKeyboardButton("📩 طلب الكود", callback_data="wait")], [InlineKeyboardButton("🔙 رجوع", callback_data='back')]]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keys), parse_mode='HTML')

    elif data == 'back':
        # العودة للبداية
        user = query.from_user
        balance = "1,000,000" if user.id == OWNER_ID else "0.00"
        keyboard = [
            [InlineKeyboardButton("💬 WhatsApp", callback_data='app_واتساب'), InlineKeyboardButton("✈️ Telegram", callback_data='app_تلجرام')],
            [InlineKeyboardButton("🔵 Facebook", callback_data='app_فيسبوك'), InlineKeyboardButton("📸 Instagram", callback_data='app_انستجرام')]
        ]
        if user.id == OWNER_ID:
            keyboard.append([InlineKeyboardButton("⚙️ لوحة تحكم المدير (Admin)", callback_data='admin_panel')])
        await query.edit_message_text(f"💰 رصيدك: {balance} نقطة\nاختر الخدمة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith('admin_'):
        action = data.split('_')[1]
        await query.message.reply_text(f"⚙️ أداة [{action}] قيد التجهيز.. سيتم ربطها بقاعدة البيانات في التحديث القادم.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_buttons))
    application.run_polling()

if __name__ == '__main__':
    main()
    application.run_polling()

if __name__ == '__main__':
    main()

