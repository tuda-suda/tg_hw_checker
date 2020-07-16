import logging
import os
import time
from http.client import responses as status_codes_desc

import requests
import telegram
from dotenv import load_dotenv


logging.basicConfig(
    format='[{levelname}]: {message}', 
    level=logging.INFO,
    style='{'
)

load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PRACTICUM_API_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'


TG_BOT = telegram.Bot(token=TELEGRAM_TOKEN)


def _log_and_raise_error(error_msg, exception=Exception, status_code=None):
    """
    Log an error and raise exception. If HTTP status_code is provided, 
    also log a status code with a description.
    """
    if status_code:
        logging.error(f'{error_msg} Status code: {status_code} {status_codes_desc[status_code]}')
    else:
        logging.error(error_msg)

    raise exception(error_msg)
    

def parse_homework_status(homework):
    try:
        homework_name = homework['homework_name']
        if homework['status'] == 'rejected':
            verdict = 'К сожалению в работе нашлись ошибки.'
        elif homework['status'] == 'approved':
            verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
        else:
            raise ValueError
    except (KeyError, ValueError) as e:
        _log_and_raise_error(
            'Invalid server response.',
            exception=e
        )

    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        _log_and_raise_error(
            'current_timestamp is None.',
            exception=ValueError
        )

    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}

    logging.info('Making a request to API...')

    homework_statuses = requests.get(
        url=PRACTICUM_API_URL,
        params=params, 
        headers=headers
    )

    resp_status_code = homework_statuses.status_code

    if resp_status_code >= 500:
        _log_and_raise_error(
            'API server error.', 
            exception=requests.exceptions.RequestException, 
            status_code=resp_status_code
        )
    elif resp_status_code >= 400:
        _log_and_raise_error(
            'Client error.', 
            exception=requests.exceptions.RequestException, 
            status_code=resp_status_code
        )

    logging.info('Request success.')

    return homework_statuses.json()


def send_message(message):
    logging.info('Sending message to user...')

    bot = TG_BOT

    try:
        sent_message = bot.send_message(text=message, chat_id=CHAT_ID)
    except telegram.TelegramError as e:
        _log_and_raise_error(
            f'Failed to send a message. Error message: "{e}"',
            exception=e
        )

    logging.info(f'Success! Message text: {message}')

    return sent_message


def main():
    logging.info('Starting...')

    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            else: 
                logging.info('No homeworks found. Trying again in 5 mins...')
            current_timestamp = new_homework.get('current_date')
            time.sleep(300)

        except Exception as e:
            logging.warn('Bot failure. Trying again in 5 seconds...')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
