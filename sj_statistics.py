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
        salaries_from = []
        salaries_to = []
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
                
                if 'error' in response.json():
                    raise requests.exceptions.HTTPError(response.json()['error'])

                received_vacancies = response.json()

                if not received_vacancies.get('objects'):
                    break

                vacancies_found = received_vacancies.get('total', 0)

                for vacancy in received_vacancies['objects']:
                    salary_from = vacancy.get('payment_from')
                    salary_to = vacancy.get('payment_to')

                    if salary_from:
                        salaries_from.append(salary_from)
                    if salary_to:
                        salaries_to.append(salary_to)
                    vacancies_processed += 1

                if not received_vacancies.get('more', False):
                    break
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return None
            except Exception as err:
                print(f"An error occurred: {err}")
                return None

        if salaries_from or salaries_to:
            combined_salaries = salaries_from + salaries_to
            average_salary = sum(combined_salaries) / len(combined_salaries) if combined_salaries else None
        else:
            average_salary = None

        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }

    return statistics
