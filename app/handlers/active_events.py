from telebot import TeleBot

from app.keyboards.main_menu import main_menu
from app.keyboards.events_menu import active_events_menu


def register_active_events_handler(bot: TeleBot):

    @bot.message_handler(
        func=lambda message: (
            message.text is not None
            and message.text.strip() == "🟢 رویدادهای فعال"
        )
    )
    def show_active_events(message):
        bot.send_message(
            message.chat.id,
            "🟢 رویدادهای فعال انجمن\\n\\n"
            "لطفاً رویداد موردنظر خود را انتخاب کنید:",
            reply_markup=active_events_menu(),
        )

    @bot.message_handler(
        func=lambda message: (
            message.text is not None
            and message.text.strip() == "🔙 منوی اصلی"
        )
    )
    def back_to_main(message):
        bot.send_message(
            message.chat.id,
            "به منوی اصلی بازگشتید.",
            reply_markup=main_menu(),
        )
