import asyncio
import uvicorn
from main import start_bot

async def main():
    # Run bot and API server concurrently
    await asyncio.gather(
        start_bot(),
        asyncio.to_thread(uvicorn.run, "server:app", host="0.0.0.0", port=8000)
    )

if __name__ == "__main__":
    asyncio.run(main())
