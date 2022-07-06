# Homework Checker Telegram Bot
Телеграм-бот который проверяет статус домашки в Яндекс.Практикум

# Setup

## 1. Prerequisites
Убедитесь, что на машине установлены:

 - `python >= 3.6` (проверить можно командой `python3 --version`)
 - `pip` (установка: `sudo apt install python3-pip`)

Склонируйте репозиторий:

```
git clone https://github.com/tuda-suda/tg_hw_checker.git
```

Установите зависимости:

```
cd tg_hw_checker
sudo -H pip install -r requirements.txt
```

## 2. `.env` & systemd
### Настройка `.env`:
Откройте `.env.template`, и установите переменные:

 - `PRACTICUM_TOKEN` - токен для API Практикума можно взять [здесь](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a) (понадобится войти с пользователем, который учится в Практикуме)
 - `TELEGRAM_TOKEN` - токен для бота в телеграм можно спросить у [BotFather](https://t.me/botfather) (команда /newbot)
 - `TELEGRAM_CHAT_ID` - ID вашего юзера в телеграм можно взять у [userinfobot](https://t.me/userinfobot) (команда /start)
 - (optional)`POLL_PERIOD` - Частота в секундах с которой бот обращается к API, по-умолчанию - 900

Скопируйте файл в `.env`:
```
cp .env.template .env
```

### Настройка unit-файла:
Откройте `tg-hw-checker.service.template`, и настройте в нем:

 - `User` - юзер, под которым будет работать daemon
 - `ExecStart` - путь до `main.py` в репозитории
 - `StandardOutput` - путь до файла, в который будут складываться логи

Скопируйте unit-файл:
```
sudo cp tg-hw-checker.service.template /etc/systemd/system/tg-hw-checker.service
```
Перезагрузите `systemctl`:
```
sudo systemctl daemon-reload
```

## 3. Start
Запустить бота можно командой:
```
sudo systemctl start tg-hw-checker
```
А для остановки выполните:
```
sudo systemctl stop tg-hw-checker
```