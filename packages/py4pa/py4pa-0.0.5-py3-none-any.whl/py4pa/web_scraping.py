import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base64
import os
import urllib3
urllib3.disable_warnings()
from fake_useragent import UserAgent

def get_random_useragent(browser=None):
    '''Function to generate a random user agent for web scraping

    Parameters
    ----------
    browser: String
        Valid values are: 'ie', 'opera', 'chrome', 'firefox', 'safari'

    Returns
    ----------
    String of valid User Agent

    '''

    ua = UserAgent()

    useragent = ua.random

    if browser is not None:
        useragent = ua[browser]

    return useragent

def get_glassdoor_ratings(glassdoor_id):
    base_url = f'https://www.glassdoor.co.uk/Reviews/{glassdoor_id}'
    reviews = []
    today = datetime.today().strftime('%Y-%m-%d')
    headers = {
        'user-agent': get_random_useragent()
    }
    urllib3.disable_warnings()

    #Overall Rating
    temp_url = base_url + '.htm'
    response = requests.get(temp_url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Global Values
    country = 'Experian Global'
    rating = soup.find(
        'div',
        attrs={'class': 'common__EIReviewsRatingsStyles__ratingNum'}
    )
    num_reviews = soup.find(
        'div',
        attrs={'class': 'common__EIReviewSortBarStyles__sortsHeader'}
    )
    #Temporary Dictionary of values
    temp_dict = {
        'date': today,
        'country': country,
        'num_reviews': int(num_reviews.h2.span.strong.text),
        'rating': float(rating.text)
    }
    reviews.append(temp_dict)

    #Loop over all countries until no more found
    i=1
    keep_looping = True
    while keep_looping:
        try:
            temp_url = base_url + '-EI_IE42406.0,8_IL.9,23_IN' + str(i) + '.htm'
            response = requests.get(temp_url, headers=headers, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')

            country = soup.find(
                'div',
                attrs={'class': 'eiReviews__EIReviewsPageContainerStyles__EIReviewsPageContainer'}
            ).h1.text[9:-8]
            rating = soup.find(
                'div',
                attrs={'class': 'common__EIReviewsRatingsStyles__ratingNum'}
            )
            num_reviews = soup.find(
                'div',
                attrs={'class': 'common__EIReviewSortBarStyles__sortsHeader'}
            )

            if len(country) > 0:
                if num_reviews is not None:
                    temp_dict = {
                        'date': today,
                        'country': country,
                        'num_reviews': int(num_reviews.h2.span.strong.text),
                        'rating': float(rating.text)
                    }

                    reviews.append(temp_dict)
            else:
                keep_looping = False

            i+=1
            continue
        except Exception as e:
            keep_looping = False
            i+=1
            continue

    return pd.DataFrame(reviews)



def get_visier_data_connection(data_connector_id, user, pword, api_key, company,fName=None):
    """Function to make API call to Visier Data Connectors

    Parameters
    ----------
    data_connector_id: String
        String of id of data connector, available from Visier

    user: String
        Your Visier username

    pword: String
        Your Data Connector Password

    api_key: String
        Your company's API key, availabel from Visier onboarding

    company:String
        Your company name that you use to access visier (https://<<company>>.visier.com)

    fName: String, optional
        File name, excluding .csv extension that you want to give your file if you want to save it.

    Returns
    ----------
    Pandas df of returned data

    """
    dataConnectorUrl = f"https://{company}.api.visier.io/api/dataconnector/getData"
    save = True
    if fName is None:
        fName = 'temp'
        save = False

    params = {
        'id': data_connector_id,
        'apikey': api_key,
        'a':'b'
    }
    urllib3.disable_warnings()

    authorization = "Basic {}==".format(base64.b64encode(bytes("{}:{}".format(user,pword),"utf-8")).decode("utf-8"))
    header = {"Authorization":authorization}
    r = requests.get(dataConnectorUrl, params=params, headers=header, verify=False)

    if r.status_code == 200:
        f=open(f'{fName}.csv','wb')
        f.write(r.content)
        f.close()

        df = pd.read_csv(f'{fName}.csv')

        return df
    else:
        raise ValueError(f'API call failed with status code: {r.status_code}')
