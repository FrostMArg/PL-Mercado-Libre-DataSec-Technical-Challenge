import logging
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class HackerrankClient:
    def __init__(self):
        self.base_url = 'https://jsonmock.hackerrank.com/api/universities'

    def _get(self, page=1):
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            response = session.get(self.base_url, params={'page': page})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error('Could not fetch all universities data %s', e, exc_info=True)
            return None

    def get_all_pages(self):
        page = 1
        response = self._get(page=page)
        if not response:
            return []

        total_pages = response['total_pages']

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_page = {executor.submit(self._get, page): page for page in range(1, total_pages + 1)}
            all_universities = []
            for future in future_to_page:
                page_response = future.result()
                if page_response:
                    page_data = page_response['data']
                    all_universities.extend([
                        (
                            uni_data.get('location', {}).get('city').lower(),
                            uni_data.get('university'),
                            int(uni_data.get('international_students', '0').replace(',', ''))
                        ) for uni_data in page_data
                    ])
        return all_universities

def process_university_data():
    hr_client = HackerrankClient()
    uni_data = hr_client.get_all_pages()

    logger.info("Processing fetched data and getting university with max international students per city")
    universities_dict = defaultdict(dict)
    for city, university, int_students in uni_data:
        if not city or not university or int_students < 0:
            logger.warning("Invalid data detected: city=%s, university=%s, int_students=%d", city, university, int_students)
            continue

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

if __name__ == "__main__":
    logger.info(highestInternationalStudents('Pune', 'New Delhi'))
