import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_item_links():
    page_num = 1
    max_page = 2
    item_link_list = []
    base_url = 'https://sellviacatalog.com/products?page=1'

    while page_num <= max_page:
        url = f'https://sellviacatalog.com/products?page={page_num}'
        print(f'Handling page {page_num}')

        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                print(f'Error {requests.status_codes} on page {page_num}')
                break
            soup = BeautifulSoup(response.text, 'lxml')

            items = soup.find_all('div', class_='product-item item-sp')

            if not items:
                print(f'Items not found on page {page_num}')
                break

            for item in items:
                item = item.find('a')['href']
                if item:
                    full_link = base_url + item
                    item_link_list.append(full_link)
                    print(f'link found {full_link}')

            print(f'Page {page_num} is handled. Found items {len(item_link_list)}')
            print('Waiting for 3 seconds to load next page')
            time.sleep(3)

        except requests.exceptions.RequestException as e:
            print(f'Error {e} on page {page_num}')
            break
        except Exception as e:
            print(f'Unexpected error {e} on page {page_num}')

        page_num += 1

    if item_link_list:
        df = pd.DataFrame(item_link_list, columns=['Item Links'])
        df.to_excel('item_links.xlsx', index=False)
        print(f'Saved {len(item_link_list)} to item_links.xlsx')
    else:
        print('Items not found')


get_item_links()
