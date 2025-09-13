import glob
import time
import random
import requests
import xlsxwriter
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_item_links():
    page_num = 1
    max_page = 2
    item_link_list = []
    # base_url = 'https://sellviacatalog.com/products?page=1'

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
                    full_link = 'https://sellviacatalog.com' + item
                    item_link_list.append(full_link)
                    print(f'link found {full_link}')

            print(f'Page {page_num} is handled. Found items {len(item_link_list)}')
            print('Waiting for 8 seconds to load next page')
            time.sleep(8)

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
    return f'Found {len(item_link_list)}'


# get_item_links()


def download_pages():
    df = pd.read_excel('item_links.xlsx')
    links = df.iloc[:, 0].dropna().tolist()

    for i, link in enumerate(links, 1):
        print(f'Downloading {i}/{len(links)}: {link}')
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()

            with open(f'page_{i}.html', 'w', encoding='utf-8') as file:
                file.write(BeautifulSoup(response.content, 'lxml').prettify())

            time.sleep(7)
        except Exception as e:
            print(f'Download error: {e}')


# download_pages()


def get_item_info():
    html_files = glob.glob('page_*.html')
    links_num = 1

    titles = []
    sale_prices = []
    retail_prices = []
    save_amounts = []
    descriptions = []
    img_urls = []

    for i in html_files:
        try:
            with open(i, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'lxml')

                title_element = soup.find('form', id='form_singleProduct')
                if title_element:
                    title = title_element.find('h1', class_='h4').text.strip()
                else:
                    title = 'Not found'

                sale_price = soup.find('input', {'name': '_salePrice'}).get('value')
                if sale_price:
                    sale_price = '$' + sale_price
                else:
                    'Not found'

                retail_price = soup.find('input', {'name': '_price'}).get('value')
                if retail_price:
                    retail_price = '$' + retail_price
                else:
                    'Not found'

                save_amount = soup.find('input', {'name': '_save'}).get('value')
                if save_amount:
                    save_amount = '$' + save_amount
                else:
                    'Not found'

                description_div = soup.find('div', itemprop='description')
                if description_div:
                    description = description_div.get_text(separator='\n', strip=True)
                else:
                    description = 'Not found'

                img_url = soup.find('div', class_='itembgr')
                if img_url:
                    img_url = img_url.get('data-img', '')
                else:
                    img_url = 'Not found'

                titles.append(title)
                sale_prices.append(sale_price)
                retail_prices.append(retail_price)
                save_amounts.append(save_amount)
                descriptions.append(description)
                img_urls.append(img_url)

                sleep_time = random.uniform(1, 4)
                print(f'handled link {i}/{links_num}')
                print(f'Pause {sleep_time:.1f} seconds...')
                time.sleep(sleep_time)
                links_num += 1

        except Exception as e:
            print(f'Error while handling {i}: {e}')
            titles.append('Error')
            sale_prices.append('Error')
            retail_prices.append('Error')
            save_amounts.append('Error')
            descriptions.append('Error')
            img_urls.append('Error')

            time.sleep(3)

    result_df = pd.DataFrame({
        'Title': titles,
        'Sale price': sale_prices,
        'Retail price': retail_prices,
        'Save amount': save_amounts,
        'Description': descriptions,
        'IMG URL': img_urls,
    })
    print(result_df)

    book = xlsxwriter.Workbook(r'D:\web_scraping\projects\sellviacatalog\items.xlsx')
    page = book.add_worksheet('Items')

    page.set_column('A:A', 150)
    page.set_column('B:B', 30)
    page.set_column('C:C', 30)
    page.set_column('D:D', 30)
    page.set_column('E:E', 200)
    page.set_column('F:F', 100)

    page.write(0, 0, 'Title')
    page.write(0, 1, 'Sale Price')
    page.write(0, 2, 'Retail Price')
    page.write(0, 3, 'Save Amount')
    page.write(0, 4, 'Description')
    page.write(0, 5, 'IMG URL')

    for row, (title,
              sale_price,
              retail_price,
              save_amount,
              description, img_url) in enumerate(zip(titles,
                                                     sale_prices,
                                                     retail_prices,
                                                     save_amounts,
                                                     descriptions,
                                                     img_urls), 1):
        page.write(row, 0, title)
        page.write(row, 1, sale_price)
        page.write(row, 2, retail_price)
        page.write(row, 3, save_amount)
        page.write(row, 4, description)
        page.write(row, 5, img_url)

    book.close()
    print('File saved successfully!')


get_item_info()
