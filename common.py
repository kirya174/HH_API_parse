""" Common functions are stored here """
import requests
import json
import re


html_tag_regex = re.compile('<.*?>')


def remove_html_tags(text):
    """ Function removes html tags from text (Tags are used in vacancy description) """
    updated_text = html_tag_regex.sub('', text)
    return updated_text


def get_city_id(name):
    """ Function search city id in dict from hh API based on city name """
    areas = get_dict_from_request("https://api.hh.ru/areas/")
    return search_in_cities_dict(areas, name)


def search_in_cities_dict(cities_dict, name):
    """ Recursive search in dictionary for city id"""
    for dict in cities_dict:
        if dict["name"].lower() == name.lower():
            return dict["id"]
        if dict["areas"]:
            id = search_in_cities_dict(dict["areas"], name)
            if id:
                return id


def get_dict_from_request(url, params=None):
    """ returns dictionary from request """
    response = requests.get(url, params)
    return json.loads(response.text)