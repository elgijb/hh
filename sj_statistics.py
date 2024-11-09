import requests
from itertools import count
from salary_utils import calculate_expected_salary

def get_superjob_statistics(professions, secret_key):
    statistics = {}
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key
    }

    for profession in professions:
        salaries = []
        vacancies_found = 0

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
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return None
            except requests.exceptions.ConnectionError as conn_err:
                print(f"Connection error occurred: {conn_err}")
                return None

            if not received_vacancies.get('objects'):
                break

            vacancies_found = received_vacancies.get('total', 0)

            for vacancy in received_vacancies['objects']:
                salary_from = vacancy.get('payment_from')
                salary_to = vacancy.get('payment_to')

                expected_salary = calculate_expected_salary(salary_from, salary_to)
                if expected_salary:
                    salaries.append(expected_salary)

            if not received_vacancies.get('more', False):
                break

        average_salary = sum(salaries) / len(salaries) if salaries else None

        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(salaries),
            'average_salary': average_salary
        }

    return statistics
