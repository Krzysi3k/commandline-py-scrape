from bs4 import BeautifulSoup
from requests_html import HTMLSession
from typing import List
import sys
import argparse

class OfferReader:
    def __init__(self, skill: str , min_salary_range: int, max_salary_range: int, filtered=True):
        self.subjects = ('go', 'data', 'security', 'blockchain', 'game', 'sap', 'pm', 'ux', 'devops',
        	'testing', 'mobile', 'c', 'scala', 'net', 'java', 'python','ruby', 'php', 'html', 'javascript')
        self.min_salary_range = min_salary_range
        self.max_salary_range = max_salary_range
        self.base_url = 'https://justjoin.it/warszawa'
        self.skill = skill
        self.filtered = filtered
        if self.skill not in self.subjects:
            print(f"you need to choose one of following skills for --skill parameter:\n{self.subjects}")
            sys.exit()


    def generate_offers(self) -> List[str]:
        url = self.base_url + f"/{self.skill}"
        session = HTMLSession()
        resp = session.get(url)
        resp.html.render()
        soup = BeautifulSoup(resp.html.html, 'html.parser')
        items = soup.find('ul', class_='offers-list')
        item_list = items.findAll(class_="item")
        output_list = []
        if len(item_list) > 0:
            for item in item_list:
                company = item.find(class_='company-name').text.replace('\n', '').replace('\ue0af', '').lstrip().rstrip()
                title = item.find(class_='title').text.replace('\n', '').lstrip().rstrip()
                salary = item.find(class_='salary').text
                offer_age = item.find(class_='age').text
                offer_url = 'https://justjoin.it' + item.attrs['href']
                output_list.append({
                    'skill':self.skill,
                    'company':company,
                    'title':title,
                    'salary':salary,
                    'url':offer_url,
                    'posted':offer_age
                })
        if self.filtered == False:
            return output_list
        return self.generate_filtered_offers(output_list)

    def generate_filtered_offers(self, all_offers: List[str]) -> List[str]:
        filtered_offers = []
        for offer in all_offers:
            ranges = offer['salary'].replace(' ','').replace('PLN','').replace('USD','').replace('EUR','')
            if 'Undisclosedsalary' in ranges:
                continue
            min_amount, max_amount = ranges.split('-')
            if (int(min_amount) >= self.min_salary_range) and (int(max_amount) <= self.max_salary_range):
                filtered_offers.append(offer)
        return filtered_offers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="webscrape ofert ze strony: 'https://justjoin.it/'",
                                    prog="your_python_script.py",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--skill', type=str, help="technologia np: Java, Devops, Python, etc...")
    parser.add_argument('--min', type=int, help="minimalna stawka wynagrodzenia [0 - 99999]")
    parser.add_argument('--max', type=int, help="maksymalna stawka wynagrodzenia [0 - 99999]")
    parser.add_argument('--filtered',  type=str, default="True", help="tylko filtrowane oferty od: min_value do: max_value")
    args = parser.parse_args()
    params = vars(args)
    print("provided parameters:")
    [print(f"{k} : {v}") for k,v in params.items()]
    if params['skill'] == None or params['min'] == None or params['max'] == None:
        parser.print_help()
        sys.exit()
    try:
        reader = OfferReader(params['skill'], params['min'], params['max'], eval(params['filtered']))
        offers = reader.generate_offers()
        [print(offer) for offer in offers]
    except Exception as e:
        print(str(e))
        parser.print_help()
        sys.exit()