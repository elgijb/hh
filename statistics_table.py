from terminaltables import AsciiTable

def print_statistics_table(title, statistics):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    
    for profession, stats in statistics.items():
        table_data.append([
            profession,
            stats.get('vacancies_found', 0),
            stats.get('vacancies_processed', 0),
            int(stats.get('average_salary', 0)) if stats.get('average_salary') is not None else 'Нет данных'
        ])
    
    table = AsciiTable(table_data)
    table.title = title
    print(table.table)
