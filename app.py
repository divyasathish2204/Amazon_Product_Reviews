import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging
logging.basicConfig(filename='scraper.log',level=logging.INFO)
# Header to set the requests as a browser requests
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
# URL of the amazon URL page
amazon_url = "https://www.amazon.in/dp/B09N3ZNHTY/ref=s9_acsd_al_bw_c2_x_1_t?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-6&pf_rd_r=M3W7DY4S8Y9VJ606WDWJ&pf_rd_t=101&pf_rd_p=1db6ae40-7e81-4c32-859a-83cd4aa3d3ed&pf_rd_i=976419031#customerReviews"

# Define Page No
len_page = 4
### <font color="red">Functions</font>
# Extra Data as Html object from amazon Review page
def reviewshtml(url,len_page):
     # Empty List define to store all pages html data
    soups = []
    #loop to gather all reviews
    for page_no in range(1,len_page+1):
        # parameter set as page no to the requests body
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }
        # Request make for each page
        response = requests.get(url,headers=headers)
         # Save Html object by using BeautifulSoup4 and html parser
        soup = BeautifulSoup(response.text, 'html parser')
        soups.append(soup)
    return soups
# Grab Reviews name, description, date, stars, title from HTML
def getreviews(html_data):
    # Create Empty list to Hold all data
    data_dicts = []
    # Select all Reviews BOX html using css selector
    boxes = html_data.select('div[data-hook="review"]')
    #Iterate all reviews box
    for box in boxes:

     # Select Name using css selector and cleaning text using strip()
    # If Value is empty define value with 'N/A' for all.
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except Exception as e:
            name = 'N/A'

        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except Exception as e:
            logging.info(e)
            stars = 'N/A'   

        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except Exception as e:
            logging.info(e)
            title = 'N/A'

        try:
            # Convert date str to dd/mm/yyy format
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except Exception as e:
            logging.info(e)
            date = 'N/A'

        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            logging.info(e)
            description = 'N/A'
            #create dictionary with all review data
            data_dict = {
                'Name' : 'name',
                'Stars' : 'stars',
                'Title' : 'title',
                'Date' : 'date',
                'Description' : 'description'
            }
            # Add Dictionary in master empty List
            data_dicts.append(data_dict)
        return data_dicts
    #grab all html
    html_datas = reviewshtml(amazon_url,len_page)
    reviews = []
    #iterate all html_datas
    for html_data in html_datas:
        #grab review data
        review = getreviews(html_data)
        # add review data to the reviews empty list
        reviews += review
    # create a dataframe with reviews data
    df_reviews = pd.DataFrame(reviews)
    print(df_reviews)
    #save data
    df_reviews.to_csv('reviews.csv',index = False)























