#!/usr/bin/env python3
import requests
from datetime import datetime
import os

def refresh_sub_gap():
    pewds = int(requests.get('https://bastet.socialblade.com/youtube/lookup?query=UC-lHJZR3Gqxm24_Vd_AJ5Yw').text)
    tseries = int(requests.get('https://bastet.socialblade.com/youtube/lookup?query=UCq-Fj5jknLsUf-MWSy4_brA').text)
    sub_gap = pewds - tseries

    print("[%s] %d" % (datetime.today().isoformat(), sub_gap))

    limit = int(os.environ['SUB_GAP_ALERT_LIMIT'])
    if (sub_gap < limit):
        requests.post('https://maker.ifttt.com/trigger/sub_gap/with/key/{0}'.format(os.environ['IFTTT_WEBHOOK_KEY']), data = { 'value1': "{:.1f}k".format(limit / 1000.0), 'value2': sub_gap });
        print("[%s] %s" % (datetime.today().isoformat(), "Sent notification"))

def retry(func, max_attempts):
    attempt = 1
    while(attempt <= max_attempts):
        try:
            return func()
        except Exception as err:
            print("Attempt #{} / {} failed:\n{}".format(attempt, max_attempts, err))
            attempt += 1
    print ("Giving up")

retry(refresh_sub_gap, 3)
