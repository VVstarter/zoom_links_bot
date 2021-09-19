import os
from dotenv import load_dotenv
from zoom_links_resend_bot import ZoomLinksTelegramBot


load_dotenv()


if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    REDIRECT_TO_CHAT_ID = os.getenv('REDIRECT_TO_CHAT_ID')
    INTERVAL = float(os.getenv('INTERVAL'))

    tg_bot = ZoomLinksTelegramBot(
        token=TOKEN,
        redirect_to_chat_id=REDIRECT_TO_CHAT_ID,
    )
    tg_bot.run(interval=INTERVAL)
