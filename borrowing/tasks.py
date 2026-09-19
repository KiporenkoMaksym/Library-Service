import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone


def send_telegram_message(message_text: str):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not bot_token or not chat_id:
        print("Telegram token or Chat ID is not configured!")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")


@shared_task
def send_telegram_notification_task(message_text: str):
    send_telegram_message(message_text)


@shared_task
def check_overdue_borrowings():

    from borrowing.models import Borrowing

    today = timezone.now().date()

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=today,
        actual_return_date__isnull=True
    ).select_related("user", "book")

    if not overdue_borrowings.exists():
        send_telegram_message("✅ <b>Overdue Check:</b> No overdue borrowings today!")
        return

    message = f"⚠️ <b>Attention! Overdue Borrowings ({overdue_borrowings.count()}):</b>\n\n"
    for b in overdue_borrowings:
        message += (
            f"• <b>User:</b> {b.user.email}\n"
            f"  <b>Book:</b> {b.book.title}\n"
            f"  <b>Due date:</b> {b.expected_return_date}\n\n"
        )

    send_telegram_message(message)
