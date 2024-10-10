import os
import requests
from dotenv import load_dotenv
from itertools import count

def get_superjob_statistics(professions):
    statistics = {}
    load_dotenv()
    SJ_SECRET_KEY = os.getenv('SECRET_KEY')

    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': SJ_SECRET_KEY
    }

    for profession in professions:
        salaries = []
        vacancies_found = 0
        vacancies_processed = 0

        params = {
            'town': "Moscow",
            'keyword': profession
        }

        for page in count(0):
            params['page'] = page

            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()

                received_vacancies = response.json()

                if not received_vacancies.get('objects'):
                    break

                vacancies_found = received_vacancies.get('total', 0)

                for vacancy in received_vacancies['objects']:
                    salary_from = vacancy.get('payment_from')
                    salary_to = vacancy.get('payment_to')

                    if salary_from is not None and salary_to is not None:
                        expected_salary = (salary_from + salary_to) / 2
                    elif salary_from is not None:
                        expected_salary = salary_from * 1.2
                    elif salary_to is not None:
                        expected_salary = salary_to * 0.8
                    else:
                        expected_salary = None

                    if expected_salary:
                        salaries.append(expected_salary)

                    vacancies_processed += 1

                if not received_vacancies.get('more', False):
                    break

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return None
            except Exception as err:
                print(f"An error occurred: {err}")
                return None

        average_salary = sum(salaries) / len(salaries) if salaries else None

        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }

    return statistics
