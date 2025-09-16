import asyncio
import uvicorn
from main import start_bot
from bot import SmartPyro

async def main():
    await SmartPyro.start()   # start Pyrogram
    try:
        await asyncio.gather(
            start_bot(),
            asyncio.to_thread(uvicorn.run, "server:app", host="0.0.0.0", port=8000)
        )
    finally:
        await SmartPyro.stop()  # graceful stop

if __name__ == "__main__":
    asyncio.run(main())
