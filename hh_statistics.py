import requests

def get_headhunter_statistics(professions, town_id, catalogues):
    statistics = {}
    for profession in professions:
        salary_from_list = []
        salary_to_list = []
        vacancies_found = 0
        vacancies_processed = 0
        
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': profession,
            'area': town_id,
            'catalogues': catalogues,
            'per_page': 100
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        vacancies_found = data.get('found', 0)
        total_pages = (vacancies_found // 100) + 1
        
        all_items = []
        for page in range(total_pages):
            params['page'] = page
            response = requests.get(url, params=params)
            page_data = response.json()
            all_items.extend(page_data.get('items', []))
        
        vacancies_processed = len(all_items)
        
        for item in all_items:
            salary = item.get('salary', {})
            if isinstance(salary, dict):
                salary_from = salary.get('from')
                salary_to = salary.get('to')
                if salary_from is not None:
                    salary_from_list.append(salary_from)
                if salary_to is not None:
                    salary_to_list.append(salary_to)
        
        average_salary = None
        if salary_from_list or salary_to_list:
            combined_salaries = salary_from_list + salary_to_list
            average_salary = sum(combined_salaries) / len(combined_salaries)
        
        statistics[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }
    
    return statistics
