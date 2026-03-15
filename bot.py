import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ==============================
# API KEYS (यहाँ अपनी keys डालना)
# ==============================

TELEGRAM_TOKEN = "PASTE_TELEGRAM_TOKEN"
GROQ_API_KEY = "PASTE_GROQ_KEY"
OPENWEATHER_KEY = "PASTE_OPENWEATHER_KEY"

# ==============================
# AI FARMING EXPERT
# ==============================

def ask_ai(question):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are KisanGPT, an expert farming assistant helping farmers with crops, fertilizer, pests, and irrigation."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    r = requests.post(url, headers=headers, json=payload)

    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "AI error. Try again."

# ==============================
# START COMMAND
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🌾 Welcome to KisanGPT

Commands:

/weather city
/crop cropname
/pest cropname
/fertilizer crop acre
/price crop

Or ask any farming question.
"""

    await update.message.reply_text(text)

# ==============================
# WEATHER SYSTEM
# ==============================

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = " ".join(context.args)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"

    r = requests.get(url).json()

    try:

        temp = r["main"]["temp"]
        humidity = r["main"]["humidity"]
        wind = r["wind"]["speed"]
        desc = r["weather"][0]["description"]

        msg = f"""
🌦 Weather in {city}

Temperature: {temp}°C
Humidity: {humidity}%
Wind: {wind} m/s
Condition: {desc}
"""

        await update.message.reply_text(msg)

    except:

        await update.message.reply_text("City not found.")

# ==============================
# CROP GUIDE
# ==============================

async def crop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cropname = " ".join(context.args)

    q = f"Give farming guide for {cropname} including sowing time fertilizer irrigation and harvest"

    ans = ask_ai(q)

    await update.message.reply_text(ans)

# ==============================
# PEST CONTROL
# ==============================

async def pest(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cropname = " ".join(context.args)

    q = f"What pests attack {cropname} crop and what pesticide should farmers use"

    ans = ask_ai(q)

    await update.message.reply_text(ans)

# ==============================
# FERTILIZER CALCULATOR
# ==============================

async def fertilizer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cropname = context.args[0]
    acre = context.args[1]

    q = f"How much fertilizer for {cropname} crop in {acre} acre land"

    ans = ask_ai(q)

    await update.message.reply_text(ans)

# ==============================
# MANDI PRICE
# ==============================

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cropname = " ".join(context.args)

    msg = f"Checking mandi price for {cropname}..."

    await update.message.reply_text(msg)

    q = f"Average mandi price of {cropname} in India today"

    ans = ask_ai(q)

    await update.message.reply_text(ans)

# ==============================
# CHAT AI
# ==============================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    ans = ask_ai(user_text)

    await update.message.reply_text(ans)

# ==============================
# BOT SETUP
# ==============================

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("crop", crop))
app.add_handler(CommandHandler("pest", pest))
app.add_handler(CommandHandler("fertilizer", fertilizer))
app.add_handler(CommandHandler("price", price))

app.add_handler(MessageHandler(filters.TEXT, chat))

print("KisanGPT Bot Running...")

app.run_polling()
