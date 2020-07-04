from telegram.constants import MAX_MESSAGE_LENGTH
from telegram import ChatAction
import time


def send_long_message(update, context, lines, **kwargs):
    """
    Sends a message containing many lines in smaller bursts to avoid hitting Telegram's message length limit.

    Note that if one of the lines is longer than Telegram's length limit, you may still get an exception.
    """

    messages = _join_until(lines, MAX_MESSAGE_LENGTH, '\n')

    for message in messages[:-1]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, **kwargs)
        context.bot.send_chat_action(update.message.chat_id, ChatAction.TYPING)
        time.sleep(1)
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages[-1], **kwargs)


def _join_until(iterable, length_limit, joiner=''):
    """
    Joins the elements together until they reach the length limit.
    Returns all of the segments that could be generated.

    Note that if one element is longer than the limit, it will have its own segment.

    :param iterable: The iterable to join .
    :param length_limit: The length limit for a section.
    :param joiner: The string to put between the elements.
    """

    segments = []

    working_message = str(iterable[0])
    for entry in (str(entry) for entry in iterable[1:]):
        if len(working_message) + len(joiner) + len(entry) <= length_limit:
            working_message += joiner + entry
        else:
            segments.append(working_message)
            working_message = entry
    segments.append(working_message)

    return segments
