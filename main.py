#!/usr/bin/env python3
import requests
from datetime import date
import json
import time
import tweepy
import config


def tweet(msg):
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    try:
        api.update_status(msg)
    except:
        msg += ' '
        api.update_status(msg)


def fetch_data():
    with open('districts.json', 'r') as f:
        fetch = json.load(f)

    current_date = date.today()
    day = current_date.strftime('%d-%m-%Y')
    districts = fetch['districts']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
    for element in districts:
        district_id = str(element['district_id']).zfill(3)
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
        params = {
            'district_id': district_id,
            'date': day,
        }
        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()
        time.sleep(3)
        for centre in data['centers']:
            block_name = centre['block_name']
            district_name = centre['district_name']
            name = centre['name']
            pincode = centre['pincode']
            fee = centre['fee_type']
            state = centre['state_name']

            for session in centre['sessions']:
                cur_date = session['date']
                min_age_limit = session['min_age_limit']
                if session['available_capacity'] > 0:
                    # print('Available')
                    msg = f'Vaccine appointment available for: \n\n' \
                          f' - Age: {min_age_limit}+ \n' \
                          f' - On: {cur_date}\n' \
                          f' - Fee: {fee} \n\n' \
                          f'In {name}, {block_name}, {district_name}, {state}, {pincode}'
                    print(msg)
                    tweet(msg)
                    time.sleep(30)


if __name__ == '__main__':
    # time.sleep(120)
    print('Started bot...')
    while True:
        fetch_data()
        time.sleep(14400)
