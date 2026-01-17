import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

verified_users = set()
user_emails = {}
user_state = {}

QUIZ_INSTRUCTIONS = """
📢 QUIZ INSTRUCTIONS – DHYAAN SE PADHE

📝 Total Questions: 30
⏱ Time: 20 Minutes
❌ Negative Marking: 1/3 Marks

🔐 Quiz Access Rule
• Quiz sirf 1 minute ad ke baad milega
• Ad GPLinks se compulsory hai

📧 Email Mandatory
• Winner ko contact karne ke liye email dena zaroori hai

📊 Results & Rewards
• Result: Quiz ke 10 min baad
• Leaderboard: Top ranks publish honge
• Prize: 1–2 hours ke andar

👇 Ad complete karne ke baad verify karo
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "🔓 1 Min Ad Dekh Kar Entry Lo",
            url="https://gplinks.in/YOUR_GPLINK"
        )
    ]]
    await update.message.reply_text(
        QUIZ_INSTRUCTIONS,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    verified_users.add(user_id)
    user_state[user_id] = "WAITING_EMAIL"

    await update.message.reply_text(
        "✅ Verification Successful!\n\n"
        "📧 Ab apni EMAIL ADDRESS bhejo (winner contact ke liye)"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in verified_users:
        await update.message.reply_text("❌ Pehle /start karo aur verify karo.")
        return

    if user_state.get(user_id) == "WAITING_EMAIL":
        if "@" not in text or "." not in text:
            await update.message.reply_text("❌ Valid email address bhejo.")
            return

        user_emails[user_id] = text
        user_state[user_id] = "DONE"

        await update.message.reply_text(
            "✅ Email save ho gayi!\n"
            "🧠 Quiz scheduled time par start hoga.\n"
            "📊 Result & leaderboard baad me milega."
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("verify", verify))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
