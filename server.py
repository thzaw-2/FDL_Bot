import uvicorn
from fastapi import FastAPI, HTTPException, Response
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID

app = FastAPI(title="FDL API")

bot_client = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_event("startup")
async def startup():
    await bot_client.start()

@app.on_event("shutdown")
async def shutdown():
    await bot_client.stop()

@app.get("/dl/{file_id}")
async def download_file(file_id: int, code: str):
    try:
        msg = await bot_client.get_messages(LOG_CHANNEL_ID, file_id)
        file = await bot_client.download_media(msg, in_memory=True)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        filename = None
        mime = "application/octet-stream"
        if msg.document:
            filename = msg.document.file_name
            mime = msg.document.mime_type
        elif msg.video:
            filename = msg.video.file_name or "video.mp4"
            mime = msg.video.mime_type
        elif msg.audio:
            filename = msg.audio.file_name or "audio.mp3"
            mime = msg.audio.mime_type
        else:
            filename = "file.bin"

        return Response(
            content=file.getbuffer(),
            media_type=mime,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream/{file_id}")
async def stream_file(file_id: int, code: str):
    try:
        msg = await bot_client.get_messages(LOG_CHANNEL_ID, file_id)
        file = await bot_client.download_media(msg, in_memory=True)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        mime = "application/octet-stream"
        if msg.video:
            mime = msg.video.mime_type
        elif msg.audio:
            mime = msg.audio.mime_type

        return Response(content=file.getbuffer(), media_type=mime)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
