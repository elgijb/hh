# Job Statistics Aggregator

Этот проект позволяет собирать и отображать статистику по вакансиям с сайтов HeadHunter и SuperJob для различных языков программирования. Результаты отображаются в виде таблиц в терминале.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/job-statistics-aggregator.git
   cd job-statistics-aggregator

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # для Windows используйте venv\Scripts\activate

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt

4. Создайте файл .env в корневой папке проекта и добавьте ваш SuperJob API ключ:
    ```bash
    SECRET_KEY=ваш_ключ_от_API_SuperJob

5. Использование
Запустите основной скрипт для получения статистики:
    ```bash
    python main.py
    В консоли отобразятся таблицы с количеством найденных и обработанных вакансий, а также средней зарплатой для каждого языка программирования.

## Структура проекта

main.py - основной файл для запуска приложения.
hh_statistics.py - модуль для работы с API HeadHunter и получения статистики.
sj_statistics.py - модуль для работы с API SuperJob и получения статистики.
statistics_table.py - модуль для отображения собранной статистики в виде таблицы.

## Зависимости
requests - библиотека для выполнения HTTP-запросов.
terminaltables - библиотека для отображения данных в виде таблиц в терминале.
python-dotenv - библиотека для загрузки переменных окружения из .env файла.