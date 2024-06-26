# SchoolTelegramBot

## Быстрый старт
1. Клонируйте проект `git clone https://github.com/klimvill/school-telegram-bot.git`
2. Создайте виртуальное окружение `python -m venv .venv` и активируйте его `venv\Scripts\activate.bat`
3. Установите библиотеки `pip install -r requirements.txt`
4. [Добавьте в переменное окружение BOT_TOKEN](https://stackoverflow.com/questions/42708389/how-to-set-environment-variables-in-pycharm)
5. Есть два способа настроить получение расписания:
   - Скопируйте на гугл диск [таблицу](https://docs.google.com/spreadsheets/d/10tHlL4Z_HsXdtDCiLJn2lElQew0aoh-W1J1dOpEKAwA/edit?usp=sharing). [Создайте ключ от google api](https://azzrael.ru/google-cloud-platform-create-app). Поместите его в папку `bot/config`, назвав `private_key_google.json`
   - Или замените функцию `reading_schedule` в `bot/database/main.py` на следующую:
    ```python
   from os import path, getcwd
   import json

   working_directory = getcwd()

   def reading_schedule() -> dict[str: dict[str: list[str]]]:
        with open(path.join(working_directory, "bot/database/schedules.json"), encoding="utf-8") as file:
             return json.load(file)
   ```
6. Запустите `run.py`
