from config import app
from pyrogram import idle

async def main():
    await app.start()
    print(app.me.full_name)
    await idle()

if __name__ == "__main__":
    app.run(main())
