from fastapi import FastAPI, Request
from telegram import Update
import os
from app.webhook import application


app = FastAPI()





@app.on_event("startup")
async def startup():
    await application.initialize()

    render_url = os.getenv("RENDER_EXTERNAL_URL")

    if render_url:
        await application.bot.set_webhook(
            url=f"{render_url}/webhook"
        )


@app.on_event("shutdown")
async def shutdown():
    await application.shutdown()


@app.get("/")
async def health_check():
    return {
        "status": "online",
        "service": "Telegram Assistant"
    }


@app.post("/webhook")
async def telegram_webhook(request: Request):

    data = await request.json()

    update = Update.de_json(
        data,
        application.bot
    )

    await application.process_update(update)

    return {"ok": True}