import requests

def get_headhunter_statistics(professions, town_id, catalogues):
    statistics = {}
    for profession in professions:
        salary_from = []
        salary_to = []
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
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"Ошибка при запросе к HH на странице {page + 1}: {e}")
                continue
            
            page_data = response.json()
            all_items.extend(page_data.get('items', []))
        
        vacancies_processed = len(all_items)
        
        for item in all_items:
            salary = item.get('salary', {})
            if isinstance(salary, dict):
                salary_from = salary.get('from')
                salary_to = salary.get('to')
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
