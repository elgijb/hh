import os
import requests

def get_superjob_statistics(professions, town_id, catalogues):
    statistics = {}
    SECRET_KEY = os.getenv('SECRET_KEY')

    for profession in professions:
        salary_from = []
        salary_to = []
        vacancies_found = 0
        vacancies_processed = 0
        
        url = 'https://api.superjob.ru/2.0/vacancies/'
        params = {
            'town': town_id,
            'catalogues': catalogues,
            'keyword': profession,
            'count': 100
        }
        headers = {
            'X-Api-App-Id': SECRET_KEY
        }
        
        response = requests.get(url, params=params, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка при запросе Sj: {e}")
            return None
        
        all_items = response.json().get('objects', [])
        
        vacancies_found = len(all_items)
        vacancies_processed = len(all_items)
        
        for item in all_items:
            salary_from = item.get('payment_from')
            salary_to = item.get('payment_to')
            if salary_from is not None:
                salary_from.append(salary_from)
            if salary_to is not None:
                salary_to.append(salary_to)
        
        average_salary = None
        if salary_from or salary_to:
            combined_salaries = salary_from + salary_to
            average_salary = sum(combined_salaries) / len(combined_salaries)
        
        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }
    
    return statistics
