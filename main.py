from hh_statistics import get_headhunter_statistics
from sj_statistics import get_superjob_statistics
from statistics_table import print_statistics_table

def main():
    professions = ["python", "c", "c#", "c++", "java", "js", "ruby", "go", "1с"]
    town_id = '1'
    catalogues = '48'
    
    hh_statistics = get_headhunter_statistics(professions, town_id, catalogues)
    
    sj_statistics = get_superjob_statistics(professions, catalogues)
    
    print_statistics_table('HeadHunter Moscow', hh_statistics)
    print_statistics_table('SuperJob Moscow', sj_statistics)

if __name__ == "__main__":
    main()