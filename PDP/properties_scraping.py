#!/usr/bin/env python
#
# Very basic script to scrap properties information
#
# $ python properties_scraping.py >> logs/logs.txt
#
# Disclaimer:
# - This script is only for personal use.
#

"""
Script to search for properties

$ python properties_scraping.py >> logs/logs.txt

Disclaimer:
- This script is only for personal use.
"""

# Standard packages
import requests
import os
import csv
import pandas as pd
import numpy as np
import re
import time

# Installed packages
## NOTE: Nothing for now

# Local packages
## NOTE: Nothing for now

# Constants
MAP_ZOOM = 9
MAP_WEST = -126.29809186925162 # USA most west point
MAP_SOUTH = 22.87133004254051 # USA most south point
MAP_EAST = -66.65550054564635 # USA most east point
MAP_NORTH = 49.592171261874455 # USA most north point
MAP_SEGMENT_SIZE = -99.65638785475313 + 102.08985953444063
CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))
LOGS_FOLDER = os.path.join(CURRENT_FOLDER, 'logs')
JSON_FOLDER = os.path.join(CURRENT_FOLDER, 'jsons')
CSV_FOLDER = os.path.join(CURRENT_FOLDER, 'csvs')
CSV_FILE = os.path.join(CSV_FOLDER, 'properties.csv')
CURL_FILE = os.path.join(CURRENT_FOLDER, 'renew_curl_here.txt')

class Map:
    """Map coordinates class, this provide functionality
       to split the map on smaller segments"""

    def __init__(
            self,
            west,
            south,
            east,
            north,
            ):
        """Initialize coordinates"""
        self.west = west
        self.east = east
        assert self.east > self.west, 'East must be greater than west'
        self.south = south
        self.north = north
        assert self.north > self.south, 'North must be greater than south'
        self.segment_size = None
        self.x_index = None
        self.y_index = None

    def _get_map_height(self):
        """Return height"""
        return self.north - self.south

    def _get_map_width(self):
        """Return width"""
        return self.east - self.west

    def _get_west_segment(self):
        """Return west segment"""
        if self.x_index is None:
            return None
        return self.west + (self.x_index * self.segment_size)

    def _get_south_segment(self):
        """Return south segment"""
        if self.y_index is None:
            return None
        return self.south + (self.y_index * self.segment_size)

    def _get_east_segment(self):
        """Return east segment"""
        west = self._get_west_segment()
        if west is None:
            return None
        return west + self.segment_size

    def _get_north_segment(self):
        """Return north segment"""
        south = self._get_south_segment()
        if south is None:
            return None
        return south + self.segment_size

    def _advance_segment(self):
        """Advance segment"""
        max_x_index = int(self._get_map_width() / self.segment_size) - 1
        max_y_index = int(self._get_map_height() / self.segment_size) - 1
        if (self.x_index < max_x_index):
            self.x_index += 1
        elif (self.y_index < max_y_index):
            self.x_index = 0
            self.y_index += 1
        else:
            self.x_index = None
            self.y_index = None

    def set_segment_size(self, segment_size):
        """Set segment size"""
        assert segment_size > 0, 'Segment size must be greater than 0'
        self.segment_size = segment_size
        # Reset segment index
        self.x_index = 0
        self.y_index = 0

    def get_next_segment(self):
        """Return next fraction"""
        west = self._get_west_segment()
        south = self._get_south_segment()
        east = self._get_east_segment()
        north = self._get_north_segment()
        if (None in [west, south, east, north]):
            return None
        self._advance_segment()
        return Map(west, south, east, north)

def run_map_search_request(map: Map, page_number: int) -> str:
    """Send single requests for MAP and PAGE_NUMBER"""
    cookies = extract_cookies()
    if not cookies:
        wait_until_curl_are_updated(cookies)
    headers = {
        'authority': 'www.zillow.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
    }
    response = requests.get(
        f'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A{map.north}%2C%22east%22%3A{map.east}%2C%22south%22%3A{map.south}%2C%22west%22%3A{map.west}%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sortSelection%22%3A%7B%22value%22%3A%22days%22%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22isElementarySchool%22%3A%7B%22value%22%3Afalse%7D%2C%22isMiddleSchool%22%3A%7B%22value%22%3Afalse%7D%2C%22isHighSchool%22%3A%7B%22value%22%3Afalse%7D%2C%22isPublicSchool%22%3A%7B%22value%22%3Afalse%7D%2C%22isPrivateSchool%22%3A%7B%22value%22%3Afalse%7D%2C%22isCharterSchool%22%3A%7B%22value%22%3Afalse%7D%2C%22includeUnratedSchools%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A{MAP_ZOOM}%2C%22pagination%22%3A%7B%22currentPage%22%3A{page_number}%7D%7D&wants={{%22cat1%22:[%22listResults%22,%22mapResults%22],%22cat2%22:[%22total%22],%22regionResults%22:[%22regionResults%22]}}&requestId=70',
        headers=headers,
        cookies=cookies,
    )
    if is_captcha_required(response):
        print('Captcha required, waiting for cookies to be updated...')
        wait_until_curl_are_updated(cookies)
        # Rerun the request
        return run_map_search_request(map, page_number)
    if response.status_code != 200 or response.text == 'null':
        error_filename = (
            f'{JSON_FOLDER}/error_map_search_'
            f'w{map.west}_'
            f's{map.south}_'
            f'e{map.east}_'
            f'n{map.north}_'
            f'z{MAP_ZOOM}_'
            f'p{page_number}'
            f'.json'
            )
        # The response is saved for debug purposes
        save(error_filename, response.text)
        raise Exception(f'Requests has failed, check {error_filename}')
    return response

def wait_until_curl_are_updated(old_cookies: str) -> None:
    """Wait until the cookies are updated."""
    set_renew_file_to_default()
    print('Waiting for cUrl file to be updated...')
    while True:
        time.sleep(2)
        new_cookies = extract_cookies()
        if not new_cookies:
            continue
        if new_cookies != old_cookies:
            break
    print('\t- updated!')

def is_captcha_required(response: requests.Response) -> bool:
    """Check if the response is a captcha."""
    is_captcha_present = 'captcha' in response.text.lower()
    is_html_tag_present = '<' in response.text
    return is_captcha_present and is_html_tag_present

def extract_cookies() -> dict:
    """Extract cookies from the renew cUrl file"""
    with open(CURL_FILE, 'r') as f:
        curl_content = f.read()
    match = re.search(r"-H 'cookie: (.+)\\", curl_content)
    cookies_as_string = match.group(1) if match else ''
    cookies_as_dict = {}
    if not cookies_as_string:
        return cookies_as_dict
    for cookie in cookies_as_string.split(';'):
        key, value = cookie.split('=', 1)
        cookies_as_dict[key] = value
    return cookies_as_dict

def set_renew_file_to_default() -> None:
    """Set the steps to renew the curl requests."""
    content = (
        'This file must be constantly updated to keep the script working.\n'
        '\n'
        'To update this file follow the next steps:\n'
        '1.\tVisit Zillow and search in the map for properties.\n'
        '2.\tOpen "Developer Tools" or press F12.\n'
        '3.\tGo to "Network" tab.\n'
        '4.\tFilter by "/GetSearchPageState.htm" and "Copy as cURL" the latest one.\n'
        '4.1\tif this requests has a 307 status code, click on url, solve Captcha and back to [1]\n'
        '5.\tReplace this text with the copied text and save.\n'
        '\n'
        'This could be automated but I don\'t have time to do it right now.'
    )
    with open(CURL_FILE, 'w') as f:
        f.write(content)

def run_map_search_scan(map: Map) -> None:
    """Run a scan of the map and save the JSON responses to files."""
    # Loop over map segments
    while True:
        current_segment = map.get_next_segment()
        if current_segment is None:
            break
        print('scanning:')
        print(f'\tW {current_segment.west} <---> E {current_segment.east}')
        print(f'\tS {current_segment.south} <---> N {current_segment.north}')
        # Loop over pages
        amount_of_pages = 0
        current_page = 1
        while True:
            print(f'\tpage {current_page}.')
            response = run_map_search_request(current_segment, current_page)
            save_properties_json_into_csv(response.json())
            if amount_of_pages == 0:
                amount_of_pages = get_json_path('cat1.searchList.totalPages', response.json(), 0)
            if current_page >= amount_of_pages:
                break
            current_page += 1

def save_properties_json_into_csv(json_content: dict) -> None:
    """Extract data from the JSON response."""
    number_of_results = get_json_path('categoryTotals.cat1.totalResultCount', json_content, 0)
    if number_of_results == 0:
        return
    properties = get_json_path('cat1.searchResults.listResults', json_content, [])
    for property in properties:
        data = {
            'statusType': get_json_path('statusType', property,  np.NaN),
            'statusText': get_json_path('statusText', property, np.NaN),
            'imgSrc': get_json_path('imgSrc', property, np.NaN),
            'detailUrl': get_json_path('detailUrl', property, np.NaN),
            'currency': get_json_path('hdpData.homeInfo.currency', property, np.NaN),
            'country': get_json_path('hdpData.homeInfo.country', property, np.NaN),
            'city': get_json_path('hdpData.homeInfo.city', property, np.NaN),
            'state': get_json_path('hdpData.homeInfo.state', property, np.NaN),
            'unformattedPrice': get_json_path('unformattedPrice', property, np.NaN),
            'addressStreet': get_json_path('addressStreet', property, np.NaN),
            'addressCity': get_json_path('addressCity', property, np.NaN),
            'addressState': get_json_path('addressState', property, np.NaN),
            'addressZipcode': get_json_path('addressZipcode', property, np.NaN),
            'bedrooms': get_json_path('beds', property, np.NaN),
            'bathrooms': get_json_path('baths', property, np.NaN),
            'area': get_json_path('area', property, np.NaN),
            'livingArea': get_json_path('hdpData.homeInfo.livingArea', property, np.NaN),
            'latitude': get_json_path('latLong.latitude', property, np.NaN),
            'longitude': get_json_path('latLong.longitude', property, np.NaN),
            'homeType': get_json_path('hdpData.homeInfo.homeType', property, np.NaN),
            'lotAreaValue': get_json_path('hdpData.homeInfo.lotAreaValue', property, np.NaN),
            'lotAreaUnit': get_json_path('hdpData.homeInfo.lotAreaUnit', property, np.NaN),
            'zestimate': get_json_path('hdpData.homeInfo.zestimate', property, np.NaN),
            'rentZestimate': get_json_path('hdpData.homeInfo.rentZestimate', property, np.NaN),
            'isNonOwnerOccupied': get_json_path('hdpData.homeInfo.isNonOwnerOccupied', property, np.NaN),
            'isPremierBuilder': get_json_path('hdpData.homeInfo.isPremierBuilder', property, np.NaN),
            'taxAssessedValue': get_json_path('hdpData.homeInfo.taxAssessedValue', property, np.NaN),
            'brokerName': get_json_path('hdpData.homeInfo.brokerName', property, np.NaN),
            'isZillowOwned': get_json_path('hdpData.homeInfo.isZillowOwned', property, np.NaN),
        }
        df = pd.DataFrame.from_dict([data])
        csv_exists = os.path.isfile(CSV_FILE)
        df.to_csv(CSV_FILE, mode='a', index=False, header=not csv_exists)
    print('\t- ...appending extracted data to csv file.')

def get_json_path(path: str, json_content: dict, default: any='') -> dict:
    """Get a path from a JSON object, with DEFAULT if it does not exist."""
    # Solution from https://stackoverflow.com/a/52478111
    for i in path.split("."):
        if i in json_content:
            json_content = json_content[i]
        else:
            return None
    return json_content if json_content else default

def save(filename:str, content:str) -> None:
    """Save the content to a file and print a message."""
    with open(filename, 'w') as f:
        f.write(content)
    print(f'\t- saved json file {filename}.')

def append_row_to_csv(filename: str, row: dict) -> None:
    """Append a row to a csv file."""
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row.values())

if __name__ == '__main__':
    set_renew_file_to_default()
    full_map = Map(
        west=MAP_WEST,
        south=MAP_SOUTH,
        east=MAP_EAST,
        north=MAP_NORTH,
    )
    full_map.set_segment_size(MAP_SEGMENT_SIZE)
    run_map_search_scan(full_map)
    ## TODO: deep_into_property()
    print('Done.')
    set_renew_file_to_default()
