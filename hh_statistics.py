import requests
from itertools import count

def get_headhunter_statistics(professions, town_id, catalogs):
    statistics = {}
    for profession in professions:
        salaries = []
        vacancies_found = 0
        vacancies_processed = 0

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
                response.raise_for_status()

                received_vacancies = response.json()
                if page >= received_vacancies['pages'] - 1:
                    break

                vacancies_found = received_vacancies.get('found', 0)

                for vacancy in received_vacancies['items']:
                    salary = vacancy.get('salary')
                    if salary and salary['currency'] == 'RUR':
                        salary_from = salary.get('from')
                        salary_to = salary.get('to')

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
