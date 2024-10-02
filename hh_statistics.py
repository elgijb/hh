import requests
from itertools import count


def get_headhunter_statistics(professions, town_id, catalogs, page=0):
    statistics = {}
    for profession in professions:
        salarys_from = []
        salarys_to = []
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
            
            response = requests.get(url, params=params)

            received_vacancies = response.json()
            if page >= received_vacancies['pages'] - 1:
                break
            vacancies_found = received_vacancies.get('found', 0)

            for vacancyes in received_vacancies['items']:
                salary = vacancyes.get('salary')
                if salary and salary['currency'] == 'RUR':
                    salary_from = salary.get('from')
                    salary_to = salary.get('to')
                    if salary_from is not None:
                        salarys_from.append(salary_from)
                    if salary_to is not None:
                        salarys_to.append(salary_to)
                    vacancies_processed += 1
        
        average_salary = None
        if salarys_from or salarys_to:
            combined_salaries = salarys_from + salarys_to
            if len(combined_salaries) > 0:
                average_salary = sum(combined_salaries) / len(combined_salaries)
        
        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }
    
    return statistics