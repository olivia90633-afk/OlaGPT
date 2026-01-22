from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import os

# 🔐 KEYS
BOT_TOKEN = "8359897581:AAEUsBf_zOY_d7PxgGM-BgmnaxSFx_C-fvg"
OPENAI_KEY = "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"

openai.api_key = OPENAI_KEY

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am *OlaGPT* 🤖\nAn AI assistant.\nType anything!",
        parse_mode="Markdown"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/about - About OlaGPT\n\n"
        "Just type a message to chat with AI 🤖"
    )

# /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *OlaGPT*\n"
        "Powered by ChatGPT AI\n"
        "Created by Ola\n"
        "Smart • Fast • Friendly",
        parse_mode="Markdown"
    )

# AI Reply
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant called OlaGPT."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Error. Try again later.")

# BOT SETUP
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("about", about))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

print("🤖 OlaGPT AI is running...")
app.run_polling()
