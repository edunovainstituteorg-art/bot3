import threading
from flask import Flask, request, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8320102746:AAEUwcmq6IlpeRvBRqt9ixdlAd05XhaXMUY"
AD_URL = "https://omg10.com/4/11066405"
BASE_URL = "https://web-production-09eb9.up.railway.app"


VIDEO_IDS = [
    "BAACAgUAAxkBAAMDahnnTA7wUgqFlZmMmGVU75r8A5QAAlcdAAIKlNBUhQsWx7UOATg7BA",
    "BAACAgUAAxkBAAMEahnnTCbrHZKEgPZ9a64M8K7UkeEAAksdAAIKlNBUnholzCn34vE7BA",
    "BAACAgUAAxkBAAMFahnnTEskqpOMQJGiiUHXL2x7YqQAAlEdAAIKlNBUVtTJjayY3eA7BA",
    "BAACAgUAAxkBAAMGahnnTHJsu9VpRt__UpKMWRXfMXcAAk0dAAIKlNBU_Oyw-nASNS47BA",
    "BAACAgUAAxkBAAMHahnnTH5rnAsGEYRkXL6p-fK2atwAAlsdAAIKlNBUiAfHBco6cLk7BA",
    "BAACAgUAAxkBAAMHahnnTH5rnAsGEYRkXL6p-fK2atwAAlsdAAIKlNBUiAfHBco6cLk7BA",
    "BAACAgUAAxkBAAMJahnnTG_FnWHHuOhvoy_6PuR3KtgAAkwdAAIKlNBUghjSgSAvB-k7BA",
    "BAACAgUAAxkBAAMKahnnTGVo5Mlkxp35S7Xj-NN0DmIAAk4dAAIKlNBUOo6DJAwgSZ07BA",
    "BAACAgUAAxkBAAMLahnnTP8ifOlmpoylcn7iWY4lVZcAAlgdAAIKlNBU5DbIeX0wskI7BA",
    "BAACAgUAAxkBAAMMahnnTJ5GPqzAB4qua8NMPwrwHcsAAlkdAAIKlNBUGOcuOD3Kz3Y7BA",
    "BAACAgUAAxkBAAMMahnnTJ5GPqzAB4qua8NMPwrwHcsAAlkdAAIKlNBUGOcuOD3Kz3Y7BA",
    "BAACAgUAAxkBAAMNahnnTHcjFKv9B9RTJylgqzxWNNMAAlIdAAIKlNBUS969JNDR7987BA",
    "BAACAgUAAxkBAAMOahnnTPLlB3pNUDTQms6m7_10qrAAAl4dAAIKlNBUaY2zfWo8aZI7BA",
    "BAACAgUAAxkBAAMPahnnTOX1HxvyTfnzd3KiPMwJEuMAAlMdAAIKlNBUNGQb4D6OrXM7BA",
    "BAACAgUAAxkBAAMQahnnTX-xiE-voR-uPmL7q4ION6oAAmAdAAIKlNBUuEGF9NC6cB87BA",
    "BAACAgUAAxkBAAMRahnnTVeIbL35K3LNrQkPOXtSYL4AAlwdAAIKlNBUQ5_F46cgYHA7BA",
    "BAACAgUAAxkBAAMRahnnTVeIbL35K3LNrQkPOXtSYL4AAlwdAAIKlNBUQ5_F46cgYHA7BA",
    "BAACAgUAAxkBAAMTahnnTffDoIoFSSZRddFoqTY4qLkAAlodAAIKlNBUhyTJosLoUUY7BA",
    "BAACAgUAAxkBAAMUahnnTWKVyl3V8biXd5s5p9tuvkcAAlQdAAIKlNBU4Rp9Z80ltzk7BA",    
    "BAACAgUAAxkBAAMYahnnTfjd7q-MWx2_Djjv3_LH07MAAlAdAAIKlNBULlWmBvfeyos7BA",  
    "BAACAgUAAxkBAAMXahnnTTloLsXedRuNjqSLp-Px5qEAAlYdAAIKlNBUqA7fiAMz4Ho7BA",  
    ]
    
visited_users = set()

flask_app = Flask(__name__)

@flask_app.route("/visit")
def visit():
    user_id = request.args.get("user_id")
    if user_id:
        visited_users.add(int(user_id))
    return redirect(AD_URL)

@flask_app.route("/")
def home():
    return "Bot is running!", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("Visit Link", url=f"{BASE_URL}/visit?user_id={user_id}")],
        [InlineKeyboardButton("Get My Videos", callback_data="send_video")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Tap Visit Link first, then tap Get My Videos!",
        reply_markup=reply_markup
    )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in visited_users:
        await query.answer("Please tap Visit Link first!", show_alert=True)
        return
    visited_users.discard(user_id)
    await query.answer("Sending your videos...")
    for video_id in VIDEO_IDS:
        await query.message.reply_video(
            video=video_id,
            caption="Enjoy!"
        )

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(send_video, pattern="^send_video$"))
    
    app.run_polling()