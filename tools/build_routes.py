from base64 import encode
from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
import json


def get_transporters_from_mp():
    """
    Extracts all transporters.
    """
    url = "https://moovitapp.com/index/uk/%D0%93%D1%80%D0%BE%D0%BC%D0%B0%D0%B4%D1%81%D1%8C%D0%BA%D0%B8%D0%B9_%D1%82%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82-Lviv-4429"
    transporter_lst = list()
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    all_lines = soup.find('div', {'class': 'content-wrapper clearfix'})

    for link in all_lines.find_all('a',
                                   attrs={'class': 'agency-group'}):
        linkk = link.get('href')
        if not linkk.startswith("https://moovitapp.com/index/uk/"):
            linkk = "https://moovitapp.com/index/uk/" + linkk
        transporter_lst.append(linkk)

    return transporter_lst


def get_routes(url):
    """
    Gets url to the page with route's all stations.
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    all_lines = soup.find('div', {'class': 'lines-container agency-lines'})
    routes_links = []

    for link in soup.find_all('a',
                              attrs={'href': re.compile("^https://moovitapp.com/index/uk")}):
        routes_links.append((link.get('href')))

    return routes_links


def get_route_station(url):
    """
    Extracts stations from the given route.
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    all_stations = soup.find('ul', {'class': 'stops-list bordered'})

    stations = []
    for li in soup.find_all('h3'):
        li = str(li)
        if '<h3>' in li:
            stations.append(li.replace('<h3>', '').replace('</h3>', ''))

    return stations


def get_tran_type(id):
    """
    Check transport's type.
    """
    trams = ["947583", "2079764"]
    trolleybuses = ["947584", "2079765"]

    if id in trams:
        return 'tram'
    elif id in trolleybuses:
        return 'trolleybus'
    else:
        return 'bus'


def get_route_name(url):
    """
    Extracts routes name together with transport's type.
    """
    prompt = r'line-.+'
    name = re.findall(prompt, url)[0]
    name_arr = name.split('-')
    transport_class = get_tran_type(name_arr[-3])
    name = f"{name_arr[0]} {name_arr[1]} ({transport_class})"
    return name


def get_data():
    """
    Extracts all routes together with their stations.
    """
    transporters = get_transporters_from_mp()

    even_routes = {}
    odd_routes = {}

    for t_link in transporters:
        t_routes = get_routes(t_link)

        for route in t_routes:

            if route[-1] == "0":
                stations = get_route_station(route)
                r_title = get_route_name(route)
                even_routes[r_title] = stations

                route = route[:-1] + "1"

                stations = get_route_station(route)
                r_title = get_route_name(route)
                odd_routes[r_title] = stations

    return even_routes, odd_routes


if __name__ == '__main__':
    route1, route2 = get_data()
    with open("route1.json", "w", encoding='utf-8') as outfile:
        json.dump(route1, outfile, ensure_ascii=False, indent=4)

    with open("route2.json", "w", encoding='utf-8') as outfile:
        json.dump(route2, outfile, ensure_ascii=False, indent=4)
