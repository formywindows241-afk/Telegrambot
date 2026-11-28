from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("🟢 رویدادهای فعال"))
    keyboard.row(KeyboardButton("💡 پیشنهادات و انتقادات"))
    keyboard.row(KeyboardButton("🤝 همکاری با ما"))
    return keyboard
