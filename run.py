from app.bot import create_bot


def main():
    application = create_bot()

    print("🤖 Bot is starting...")

    application.run_polling()


if __name__ == "__main__":
    main()