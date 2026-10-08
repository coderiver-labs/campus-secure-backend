import requests
from decouple import config
import logging
logger = logging.getLogger(__name__)


# Create Services

# class SentryWebhookService:

#     @staticmethod
#     def handle(payload: dict, request):
#         resource = request.headers.get("Sentry-Hook-Resource")
#         action = payload.get("action")

#         # We only care about newly created error events.
#         if resource != "error" or action != "created":
#             return

#         data = payload.get("data") or {}
#         error = data.get("error") or {}

#         event_id = error.get("event_id") or "N/A"
#         transaction = error.get("transaction") or "N/A"
#         level = error.get("level") or "error"
#         title = error.get("title") or payload.get("title") or "N/A"

#         environment = (
#             error.get("environment")
#             or data.get("environment")
#             or "N/A"
#         )

#         project = (
#             data.get("project")
#             or error.get("project")
#             or "N/A"
#         )
#         web_url = error.get("web_url") or ""

#         notification = (
#             "------- SENTRY ERROR -------\n\n"
#             f"Level: {level.upper()}\n\n"
#             f"Transaction (Path):----- \n{transaction}\n\n"
#             f"Error:-----\n{title}\n\n"
#             f"Environment: {environment}\n\n"
#             f"Project: {project}\n\n"
#             f"url: {web_url}\n\n"
#             f"Event ID: {event_id}\n\n"
#         )
#         TelegramNotificationService.send(message=notification)




# class TelegramNotificationService:

#     @staticmethod
#     def send(message: str) -> bool:
#         token = config("TELEGRAM_BOT_TOKEN", default="")
#         chat_id = config("TELEGRAM_CHAT_ID", default="")

#         if not token or not chat_id:
#             logger.error("Telegram bot token or chat_id is missing.")
#             return False

#         url = f"https://api.telegram.org/bot{token}/sendMessage"

#         payload = {
#             "chat_id": chat_id,
#             "text": message,
#             "disable_web_page_preview": True,
#         }

#         try:
#             response = requests.post(url, json=payload, timeout=5,)
#             if not response.ok:
#                 logger.error(
#                     "Telegram API returned status=%s response=%s",
#                     response.status_code,
#                     response.text,
#                 )
#                 return False
#             return True
#         except requests.exceptions.RequestException:
#             logger.exception("Telegram request failed.")
#             return False
        




import html


class SentryWebhookService:

    LEVEL_EMOJI = {
        "error": "🔴",
        "warning": "🟡",
        "info": "🔵",
        "debug": "⚪",
    }

    @staticmethod
    def handle(payload: dict, request):
        resource = request.headers.get("Sentry-Hook-Resource")
        action = payload.get("action")

        # We only care about newly created error events.
        if resource != "error" or action != "created":
            return

        data = payload.get("data") or {}
        error = data.get("error") or {}

        event_id = error.get("event_id") or "N/A"
        transaction = error.get("transaction") or "N/A"
        level = (error.get("level") or "error").lower()
        title = error.get("title") or payload.get("title") or "N/A"

        environment = (
            error.get("environment")
            or data.get("environment")
            or "N/A"
        )

        project = (
            data.get("project")
            or error.get("project")
            or "N/A"
        )
        web_url = error.get("web_url") or ""

        emoji = SentryWebhookService.LEVEL_EMOJI.get(level, "❗")

        notification = (
            f"{emoji} <b>SENTRY {level.upper()}</b>\n\n"
            f"<b>Project:</b> {html.escape(str(project))}\n"
            f"<b>Environment:</b> {html.escape(str(environment))}\n"
            f"<b>Transaction:</b> <code>{html.escape(str(transaction))}</code>\n\n"
            f"<b>Error:</b>\n{html.escape(str(title))}\n\n"
            f"<b>Event ID:</b> <code>{html.escape(str(event_id))}</code>\n\n"
            f'\n<a href="{html.escape(web_url)}">🔗 View in Sentry</a>'
        )


        TelegramNotificationService.send(message=notification)


class TelegramNotificationService:

    @staticmethod
    def send(message: str) -> bool:
        token = config("TELEGRAM_BOT_TOKEN", default="")
        chat_id = config("TELEGRAM_CHAT_ID", default="")

        if not token or not chat_id:
            logger.error("Telegram bot token or chat_id is missing.")
            return False

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if not response.ok:
                logger.error(
                    "Telegram API returned status=%s response=%s",
                    response.status_code,
                    response.text,
                )
                return False
            return True
        except requests.exceptions.RequestException:
            logger.exception("Telegram request failed.")
            return False