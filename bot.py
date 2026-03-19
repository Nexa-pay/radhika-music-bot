from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION

bot = Client("radhika_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call = PyTgCalls(assistant)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("🎵 Radhika Music Bot is alive!")

@bot.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Give a song name")

    query = " ".join(message.command[1:])
    msg = await message.reply("🔎 Searching...")

    ydl_opts = {"format": "bestaudio"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        url = info["url"]
        title = info["title"]

    await msg.edit(f"▶️ Playing: {title}")

    chat_id = message.chat.id

    try:
        await call.join_group_call(
            chat_id,
            AudioPiped(url)
        )
    except Exception as e:
        await message.reply(f"Error: {e}")

@bot.on_message(filters.command("stop"))
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏹ Stopped")

async def main():
    await bot.start()
    await assistant.start()
    await call.start()
    print("Radhika Music Bot Started")
    await idle()

from pyrogram import idle
asyncio.run(main())
