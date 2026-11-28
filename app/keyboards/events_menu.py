from telebot.types import ReplyKeyboardMarkup, KeyboardButton


ACTIVE_EVENTS = [
    "💻 سیری در جهان کامپیوتر | فصل دوم، جلسه چهارم",
    "🖼 بوتکمپ پردازش تصویر کاربردی",
]


def active_events_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for event_title in ACTIVE_EVENTS:
        keyboard.row(KeyboardButton(event_title))
    keyboard.row(KeyboardButton("🔙 منوی اصلی"))
    return keyboard
