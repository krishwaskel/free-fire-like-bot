import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8725080580:AAF_Wlx-fJe-IjiL_6cO33nztfOIc-ly0qk"

# --- API helpers ---
def check_ban(uid):
    """Check ban status using Garena's public endpoint."""
    url = f"https://ff.garena.com/api/antihack/check_banned?uid={uid}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data
    except Exception as e:
        return {"error": str(e)}

def get_player_info(uid):
    """Fetch player profile from a third-party API."""
    url = f"https://freefire-api-six.vercel.app/api/player?uid={uid}"
    try:
        resp = requests.get(url, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

# --- Command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Free Fire Info Bot\n\n"
        "Commands:\n"
        "/ban <UID> – Check ban status\n"
        "/player <UID> – Get player profile"
    )

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ban <UID>")
        return
    uid = context.args[0]
    result = check_ban(uid)
    if "error" in result:
        await update.message.reply_text(f"❌ Error: {result['error']}")
    else:
        status = "Banned" if result.get("is_banned") else "Not banned"
        await update.message.reply_text(f"🆔 UID: {uid}\n🚫 Status: {status}")

async def player_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /player <UID>")
        return
    uid = context.args[0]
    info = get_player_info(uid)
    if "error" in info:
        await update.message.reply_text(f"❌ Error: {info['error']}")
    else:
        # Adjust fields based on the API response
        name = info.get("nickname", "Unknown")
        level = info.get("level", "?")
        rank = info.get("rank", "?")
        await update.message.reply_text(
            f"🎮 Player Info\n"
            f"🆔 UID: {uid}\n"
            f"📛 Name: {name}\n"
            f"⭐ Level: {level}\n"
            f"🏆 Rank: {rank}"
        )

# --- Run the bot ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(CommandHandler("player", player_cmd))
    print("Bot is running...")
    app.run_polling()