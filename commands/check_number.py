from plates_game import get_total_record_count, check_number_rarity

_records_db_path = ""


def set_record_db_path(records_db_path):
    global _records_db_path
    _records_db_path = records_db_path


def handle_check_number_command(update, context):
    _MESSAGE_TEMPLATE = "The number {number_to_check} appears on {appearance_count:,} plates out of a total of " \
                        "{total_count:,}.\n" \
                        "The chance to find it is 1 in {chance}.\n" \
                        "The latest production year of a car with that number is {latest_production_year}."

    args = context.args
    if len(args) < 1 or not args[0].isdigit():
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid argument. please specify a number "
                                                                        "between 0 and 999.")
        return

    try:
        number_to_check = int(args[0])
        total_count = get_total_record_count(_records_db_path)
        appearance_count, latest_production_year = check_number_rarity(_records_db_path, number_to_check)
        message = _MESSAGE_TEMPLATE.format(number_to_check=number_to_check, appearance_count=appearance_count,
                                           total_count=total_count, chance=int(total_count/appearance_count),
                                           latest_production_year=latest_production_year)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except ValueError as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(ex))
    except Exception as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"An exception occurred! error: {ex}")
