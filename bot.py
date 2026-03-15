import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8597896381:AAH3Ubxxcn4A0k2TTbb-lqNDKLy9JecbuXA"
GROQ_API_KEY = "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"
OPENWEATHER_KEY = "cdef6473642acedcc9a9bbfe6284c956"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌾 नमस्ते किसान!\n\n"
        "मैं KisanGPT हूँ\n"
        "खेती से जुड़ा कोई भी सवाल पूछो\n\n"
        "Commands:\n"
        "/weather city"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text("Example: /weather Delhi")
        return

    city = " ".join(context.args)

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"

    r = requests.get(url).json()

    if "main" in r:

        temp = r["main"]["temp"]
        desc = r["weather"][0]["description"]

        msg = f"🌦 Weather in {city}\n\nTemperature: {temp}°C\nCondition: {desc}"

    else:

        msg = "City नहीं मिला"

    await update.message.reply_text(msg)

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):

    question = update.message.text

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an agriculture expert helping farmers."},
            {"role": "user", "content": question}
        ]
    }

    r = requests.post(url, headers=headers, json=data).json()

    answer = r["choices"][0]["message"]["content"]

    await update.message.reply_text(answer)

def main():

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai))

    print("KisanGPT running...")

    app.run_polling()

if __name__ == "__main__":
    main()
