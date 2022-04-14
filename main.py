import csv
from pathlib import Path
from vacancy import Vacancy
from common import get_dict_from_request, get_city_id


def collect_request_parameters():
    params = {}
    params["text"] = input("Enter vacancy search request (e.g. Role, Company name): ")
    experience = int(input("Specify your experience in years: "))
    match experience:
        case num if num == 0:
            params["experience"] = "noExperience"
        case num if num in range(1, 3):
            params["experience"] = "between1And3"
        case num if num in range(3, 6):
            params["experience"] = "between3And6"
        case num if num in range(6, 70):
            params["experience"] = "moreThan6"
        case _:
            print("Incorrect experience")
    employment_type = int(input("Select employment type:\n"
                                "1. Full-time\n"
                                "2. Part-time\n"
                                "3. For single project\n"
                                "4. Volunteer\n"
                                "5. Probation\n"))
    match employment_type:
        case 1:
            params["employment"] = "full"
        case 2:
            params["employment"] = "part"
        case 3:
            params["employment"] = "project"
        case 4:
            params["employment"] = "volunteer"
        case 5:
            params["employment"] = "probation"
    params["only_with_salary"] = input("Show vacancies only with salary? True/False: ").lower()
    city = input("Define city of search in cyrillic: ")
    if city != "":
        params["area"] = get_city_id(city)
        if params["area"] is None:
            print("Specified city not found")
    params["per_page"] = "100"
    return params


if __name__ == '__main__':

    params = collect_request_parameters()
    output_file_name = input("Set output file name: ") + '.csv'
    print("Writing to file, please, wait.")
    vacancies = []

    vacancies_raw = get_dict_from_request("https://api.hh.ru/vacancies", params=params)
    available_pages = vacancies_raw["pages"]

    for item in vacancies_raw["items"]:
        vacancy = Vacancy(item["id"])
        vacancies.append(vacancy)

    for page in range(1, min(5, available_pages)):  # goes through next pages, with limit of max 5 pages
        params["page"] = page
        vacancies_raw = get_dict_from_request("https://api.hh.ru/vacancies", params=params)

        for item in vacancies_raw["items"]:
            vacancy = Vacancy(item["id"])
            vacancies.append(vacancy)

    with open(output_file_name, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ["id", "name", "description", "link", "salary", "required_skills", "city", "required_experience"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(vacancies)

    parent = Path(__file__).resolve().parent
    print(f'saved to file {parent}\{output_file_name}')
