import requests
from itertools import count
from salary_utils import calculate_expected_salary

def get_headhunter_statistics(professions, town_id, catalogs):
    statistics = {}
    for profession in professions:
        salaries = []
        vacancies_found = 0

        for page in count(0):
            url = 'https://api.hh.ru/vacancies'
            params = {
                'text': profession,
                'area': town_id,
                'catalogs': catalogs,
                'per_page': 100,
                'page': page
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raises HTTPError for bad responses
                received_vacancies = response.json()
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                return None
            except requests.exceptions.ConnectionError as conn_err:
                print(f"Connection error occurred: {conn_err}")
                return None

            if page >= received_vacancies['pages'] - 1:
                break

            vacancies_found = received_vacancies.get('found', 0)

            for vacancy in received_vacancies['items']:
                salary = vacancy.get('salary')
                if salary and salary['currency'] == 'RUR':
                    salary_from = salary.get('from')
                    salary_to = salary.get('to')

                    expected_salary = calculate_expected_salary(salary_from, salary_to)
                    if expected_salary:
                        salaries.append(expected_salary)

        average_salary = sum(salaries) / len(salaries) if salaries else None

        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(salaries),
            'average_salary': average_salary
        }

    return statistics
