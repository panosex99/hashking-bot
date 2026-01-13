from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8586452239:AAFGxPETSbKcqmquaWHrVpPUAnple5jzjdo"

users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {"hash": 100, "btc": 0.0, "vip": False}
    return users[uid]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⛏ Mine", callback_data="mine")],
        [InlineKeyboardButton("🚀 Upgrade", callback_data="up")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip")]
    ]
    await update.message.reply_text(
        "👑 Welcome to HashKing\n⛏ Start mining BTC!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = get_user(query.from_user.id)

    if query.data == "mine":
        gain = user["hash"] * 0.00000001
        if user["vip"]:
            gain *= 2
        user["btc"] += gain
        await query.edit_message_text(f"⛏ You mined {gain:.8f} BTC\nTotal: {user['btc']:.8f}")

    elif query.data == "up":
        user["hash"] += 50
        await query.edit_message_text(f"🚀 Hash Power: {user['hash']} GH/s")

    elif query.data == "vip":
        user["vip"] = True
        await query.edit_message_text("💎 VIP Activated! Earnings x2")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.run_polling()
