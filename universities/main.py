import logging
import requests

from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()


class HackerrankClient(object):

    def __init__(self):
        self.base_url = 'https://jsonmock.hackerrank.com/api/universities'

    def _get(self, page=1):
        """
        Fetches one page from Hackerrank's API and returns the JSON response or None
        if a ConnectionError or HTTPError occurs
        """
        try: 
            response = requests.get(self.base_url, params={'page': page})
            return response.json()

        except (requests.ConnectionError, requests.HTTPError) as e:
            logger.error('Could not fetch all universities data %s', e, exc_info=True)
            return None

    def get_all_pages(self):
        """
        Fetches all pages from Hackerrank's API and returns a list where each element is a 
        3-tuple with city, university name and international_students
        """
        page = 1
        all_universities = []
        while True:
            logger.info('Getting page %s from Hackerrank API', page)
            response = self._get(page=page)
            if not response:
                break

            page_data = response['data']
            all_universities.extend([
                (
                    uni_data.get('location', {}).get('city').lower(), 
                    uni_data.get('university'),
                    int(uni_data.get('international_students', '0').replace(',', ''))
                ) for uni_data in page_data
            ])

            if response['page'] >= response['total_pages']:
                break

            page += 1

        return all_universities
    

def process_university_data():
    """
    Processes data retrieved from Hackerrank's API and forms a dictionary that has the university with the
    most international students per city.
    """
    hr_client = HackerrankClient()
    uni_data = hr_client.get_all_pages()

    logger.info("Processing fetched data and getting university with max international students per city")
    universities_dict = defaultdict(dict)
    for city, university, int_students in uni_data:
        if int_students >= universities_dict[city].get('international_students', 0):
            universities_dict[city] = {
                'university': university,
                'international_students': int_students
            }

    return universities_dict


def highestInternationalStudents(city1, city2):
    universities_info = process_university_data()
    return (
        universities_info.get(city1.lower(), {}).get('university') 
        or 
        universities_info.get(city2.lower(), {}).get('university')
    )


logger.info(highestInternationalStudents('Pune', 'New Delhi'))
