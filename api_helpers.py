import requests
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

def fetch_vacancies(url, params, headers):
    all_items = []
    page = 0
    while True:
        params['page'] = page
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if isinstance(data, dict):
            all_items.extend(data.get('objects', data.get('items', [])))
            if 'more' in data and not data.get('more', False):
                break
        elif isinstance(data, list):
            all_items.extend(data)
            break
        
        page += 1
    
    return all_items