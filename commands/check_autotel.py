from telegram import ChatAction
from typing import List
from urllib.parse import urlencode

from plates_game import get_autotel_license_plate_mapping
import messaging


def get_autotel_cars_with_number_html_lines(num: int) -> List[str]:
    """
    Returns nice HTML lines showing how many AutoTel cars with the given number exist, including a hyperlink to where
    they are parking.

    :param num: The number to look for.
    """

    MESSAGE_FORMAT = ("With license plate {license_plate} (Car #{id}) at:\n"
                      "<a href='{navigate_link}'>{address}</a>")

    if num < 0 or num > 999:
        raise IndexError(f"License plate number {num} is out of range")

    cars = get_autotel_license_plate_mapping()[num]
    car_count = len(cars)
    if car_count == 0:
        return ["No cars were found."]

    lines = ["One car was found:" if car_count == 1 else f"{car_count} cars were found:"]
    for car in cars:
        lines.append(MESSAGE_FORMAT.format(
            license_plate=car.license_plate,
            id=car.id,
            navigate_link=f"https://www.google.com/maps/dir/?api=1&{urlencode({'destination': car.address})}",
            address=car.address
        ))
    return lines


def handle_check_autotel_command(update, context):
    args = context.args
    if len(args) < 1 or not args[0].isdigit():
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid argument. please specify a number "
                                                                        "between 0 and 999.")
        return

    try:
        number = int(args[0])
        context.bot.send_chat_action(update.message.chat_id, ChatAction.TYPING)
        messaging.send_long_message(update, context, get_autotel_cars_with_number_html_lines(number), parse_mode="HTML")
    except IndexError as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(ex))
    except Exception as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"An exception occurred! error: {ex}")
