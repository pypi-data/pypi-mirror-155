import json
import requests
import sys


def stats():
    try:
        org_api = sys.argv[1]
        netlocs = sys.argv[2]
        start_date = sys.argv[3]
        end_date = sys.argv[4]

        url = f"https://crawlera-stats.scrapinghub.com/stats/?netlocs={netlocs}&start_date={start_date}&end_date={end_date}&groupby=day&domain-wise=true"

        payload = {}

        response = requests.request("GET", url, auth=(org_api, 'x'), data=payload)

        response = json.loads(response.text)

        return print(json.dumps(response, indent=3))

    except IndexError:
        return print(
            "Please enter all the Arguments as given below: \npython -m zyte.spmstats <ORG-API> amazon.com "
            "2022-06-15T18:50:00 2022-06-17T23:00")


if __name__ == '__main__':
    stats()
