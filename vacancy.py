from common import get_dict_from_request, remove_html_tags


class Vacancy:
    """ Class that stores information about vacancy """
    def __init__(self, vacancy_id):
        self.id = vacancy_id
        self.name = None
        self.description = None
        self.link = None
        self.salary = ""
        self.required_skills = None
        self.city = None
        self.required_experience = None
        self.update_info()

    def update_info(self):
        """ Gets detailed information about vacancy """
        details = get_dict_from_request("https://api.hh.ru/vacancies/" + str(self.id))
        self.name = details['name']
        self.description = remove_html_tags(details['description'])
        self.link = details['alternate_url']
        if details['salary'] is not None:
            if details['salary']['from']:
                self.salary = f"От {details['salary']['from']}"
            if details['salary']['to']:
                self.salary += f"до {details['salary']['to']}"
        self.required_skills = [skill['name'] for skill in details['key_skills']]
        self.city = details['area']['name']
        self.required_experience = details['experience']['name']

    def __iter__(self):
        return iter([self.id, self.name, self.description, self.link, self.salary, self.required_skills, self.city,
                     self.required_experience])
