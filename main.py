import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, Updater, MessageHandler, CommandHandler, CallbackQueryHandler
from random import shuffle

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# def start(update, context):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text("Hello, I am Jarvis.")
#
#
# def help(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Available commands:\n\n/id')
#
#
# def id(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text(update.effective_chat.id)


def welcome(update, context):
    try:
        for new_member in update.message.new_chat_members:
            callback_id = str(new_member.id)
            context.bot.restrict_chat_member(
                int(os.environ['CHAT_ID']),
                new_member.id,
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )

            keyboard_items = [
                InlineKeyboardButton("🥩", callback_data=callback_id + ',steak'),
                InlineKeyboardButton("🥝", callback_data=callback_id + ',kiwi'),
                InlineKeyboardButton("🥛", callback_data=callback_id + ',milk'),
                InlineKeyboardButton("🥓", callback_data=callback_id + ',bacon'),
                InlineKeyboardButton("🥥", callback_data=callback_id + ',coconut'),
                InlineKeyboardButton("🍩", callback_data=callback_id + ',donut'),
                InlineKeyboardButton("🌮", callback_data=callback_id + ',taco'),
                InlineKeyboardButton("🍕", callback_data=callback_id + ',pizza'),
                InlineKeyboardButton("🥗", callback_data=callback_id + ',salad'),
                InlineKeyboardButton("🍌", callback_data=callback_id + ',banana'),
                InlineKeyboardButton("🌰", callback_data=callback_id + ',chestnut'),
                InlineKeyboardButton("🍭", callback_data=callback_id + ',lollipop'),
                InlineKeyboardButton("🥑", callback_data=callback_id + ',avocado'),
                InlineKeyboardButton("🍗", callback_data=callback_id + ',chicken'),
                InlineKeyboardButton("🥪", callback_data=callback_id + ',sandwich'),
                InlineKeyboardButton("🥒", callback_data=callback_id + ',cucumber')
            ]

            shuffle(keyboard_items)
            keyboard = []

            counter = 0
            for i in range(4):  # create a list with nested lists
                keyboard.append([])
                for n in range(4):
                    keyboard_item = keyboard_items[counter]
                    keyboard[i].append(keyboard_item)  # fills nested lists with data
                    counter += 1

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(
                'Hello, ' +
                new_member.first_name +
                ' and welcome to Code for Cause. We are a community of developers with various levels of experience, who are here to help each other out and grow together.\n\nI\'m Jarvis, a loyal servant of this community. To verify if you\'re not a bot, please select milk from the options below.',
                reply_markup=reply_markup
            )
    except AttributeError:
        pass


def button(update, context):
    query = update.callback_query
    person_who_pushed_the_button = int(query.data.split(",")[0])
    print("Query user: " + str(query.from_user))
    print("Query data: " + str(query.data))

    if query.from_user.id == person_who_pushed_the_button:
        if 'milk' in query.data:
            context.bot.delete_message(
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id
            )
            context.bot.restrict_chat_member(
                int(os.environ['CHAT_ID']),
                person_who_pushed_the_button,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        else:
            query.edit_message_text(text="🚨 A robot suspect was just put on hold! 🚨")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(str(os.environ['TOKEN']), use_context=True)
    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("id", id))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
