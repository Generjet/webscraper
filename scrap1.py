import requests
from bs4 import BeautifulSoup
import json
import sys

# URL
url = 'https://www.amazon.com/product-review/B07S9PTLNZ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&sortBy=recent&formatType=current_format&pageNumber=1'

def scrape_products():
  try:
    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'html.parser')

    review_list = soup.find('div', {'id': 'cm_cr-review_list'} )
    # print(review_list)
    

    user_comments = []

    # heregtei attributuudaa avah heseg
    for row in review_list.find_all('div', {'class':"a-section review aok-relative"}):
      product = {}

      product['userName'] = row.find('div', {'class': 'a-row a-spacing-none'}).find('div', {'class':'a-section celwidget'}).find('div',{'class':'a-row a-spacing-mini'}).text
      product['star'] = row.find('div',{'class':'a-row'}).find('a', {'class':'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}).find('i').text
      product['title'] = row.find('div',{'class':'a-row'}).find('a', {'class':'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}).find_all('span')[2].text
      product['date'] = row.find('span',{'class':'a-size-base a-color-secondary review-date'}).text
      product['product_cat'] = row.find('div', {'class':'a-row a-spacing-mini review-data review-format-strip'}).find('a').text
      product['comment'] = row.find('div', {'class':'a-row a-spacing-small review-data'}).text
      print(product['comment'])
      print("****************")

      user_comments.append(product)

    # Save data to JSON file
    with open('products.json', 'w') as json_file:
      json.dump(user_comments, json_file, indent=2)
    print('Product data scraped and saved to products.json')
    print(user_comments)

  except requests.exceptions.RequestException as error:
    print('Error scraping products:', error)

scrape_products()
