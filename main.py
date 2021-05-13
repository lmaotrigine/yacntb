#!/usr/bin/env python3
import sys
import requests
from datetime import date, datetime
import json
import time
import logging
from logging.handlers import RotatingFileHandler
import tweepy
import config
import traceback
import sqlite3

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
max_bytes = 32 * 1024 * 1024  # 32 MiB
handler = RotatingFileHandler(filename='yacntb.log', encoding='utf-8', mode='w', maxBytes=max_bytes, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)

db = sqlite3.connect('update_logs.db')
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS update_logs (
                 district_id TEXT PRIMARY KEY,
                 last_updated TEXT
              );
          ''')
db.commit()
c.close()

SLEEP_TIME = 28_800  # 8 hours
DATE_FMT = '%d/%m/%Y %H:%M:%S'

def generate_hashtags(state):
    # TODO: Maybe there's some more relevant ones to add here?
    state = state.replace(' ', '')
    return f'#COVID19 #COVID19Vaccine #COVIDIndia #Vaccination #{state}'


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
    cur_time = datetime.utcnow()
    districts = fetch['districts']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
    for element in districts:
        district_id = str(element['district_id']).zfill(3)
        cur = db.cursor()
        cur.execute('SELECT last_updated FROM update_logs WHERE district_id = ?', (district_id,))
        dt = cur.fetchone()
        if dt is not None:
            dt = datetime.strptime(dt[0], DATE_FMT)
            if (cur_time - dt).total_seconds() < SLEEP_TIME:
                print(f'District ID {district_id} updated at {dt} which is less than 4 hours ago. Skipping...')
                continue
        cur.close()

        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
        params = {
            'district_id': district_id,
            'date': day,
        }
        resp = requests.get(url, params=params, headers=headers)
        log.debug('Fetching %s returned status %s', district_id, resp.status_code)
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
                available = session ['available_capacity']
                if available > 0 and min_age_limit == 18:
                    # we stopped caring about older people because of new rate limits
                    msg = f'Vaccine appointment available for: \n\n' \
                          f' - Age: {min_age_limit}+ \n' \
                          f' - Slots Available: {available}\n' \
                          f' - On: {cur_date}\n' \
                          f' - Fee: {fee} \n\n' \
                          f'In {name}, {block_name}, {district_name}, {state}, {pincode}\n\n' \
                          f'{generate_hashtags(state)}'
                    log.info(f'Found slot:\n\n{msg}')
                    msg.replace('Dadra and Nagar Haveli', 'DNH')  # shorten to fit limits
                    tweet(msg)
                    time.sleep(30)
        cur = db.cursor()
        cur.execute('REPLACE INTO update_logs (district_id, last_updated) VALUES (?, ?);', (district_id, cur_time.strftime(DATE_FMT)))
        db.commit()
        cur.close()


if __name__ == '__main__':
    # time.sleep(120)
    print('Started bot...')
    try:
        while True:
            try:
                fetch_data()
                print('=====================================================')
                print('All districts fetched. Sleeping for 4 hours...')
                print('=====================================================')
            except Exception as exc:
                log.exception(traceback.format_exc())
                traceback.print_exc()
            else:    
                time.sleep(SLEEP_TIME)
    finally:
        db.close()

