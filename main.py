import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

BOT_TOKEN = os.getenv("8648028972:AAE9ej8GdJghkZCAArJB_NDBNCFjO7BsSUg")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your AI Telegram Bot. Send me any message."
    )

# AI reply function
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=300,
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Main app
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot is running...")
app.run_polling()
