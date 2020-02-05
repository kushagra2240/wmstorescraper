import csv
import requests
import json
import pandas as pd
import time 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def locate_stores(zip_code):

    url = f"https://www.walmart.com/store/finder/electrode/api/stores?singleLineAddr={zip_code}&serviceTypes=pharmacy&distance=50"
    headers = { 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
                'cache-control':'max-age=0',
                'upgrade-insecure-requests':'1',
                'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    stores = []
    print("retrieving stores")
    for retry in range(10):
        try:
            get_store = requests.get(url, headers=headers, verify=False)
            store_response = get_store.json()
            stores_data = store_response.get('payload',{}).get("storesData",{}).get("stores",[])
            
            if not stores_data:
                print(f"no stores found near {zipcode}")
                return []
            print("processing store details")
            #iterating through all stores
            for store in stores_data:
                store_id = store.get('id')
                display_name = store.get("displayName")
                address = store.get("address").get("address")
                postal_code = store.get("address").get("postalCode")
                city = store.get("address").get("city")
                phone = store.get("phone")
                distance = store.get("distance")

                data = {
                        "name":display_name,
                        "distance":distance,
                        "address":address,
                        "zip_code":postal_code,
                        "city":city,
                        "store_id":store_id,
                        "phone":phone,
                }
                stores.append(data)
            return stores
        except Exception as e:
        	print (e)
    
    return []   

def get_stores():
    df_zipcodes = pd.read_csv('zipcode_list.csv')
    list_zipcodes = df_zipcodes['Zipcode'].to_list()
    print (f'number of unique zipcodes :: {len(list_zipcodes)}')
    return (list_zipcodes)


if __name__=="__main__":
    zipcodes = get_stores()
    storecount = 0
    rows_list = []
    try :
        for zipcode in zipcodes:
            scraped_data = locate_stores(zipcode)
            if scraped_data:
                print (f"Scraped data for zipcode {zipcode}")
                rows_list.extend(scraped_data)
                time.sleep(1)

    except Exception as e:
        print (e)
    df = pd.DataFrame(rows_list)
    print (df.shape)
    df.to_csv('all_zipcode_stores.csv',index=False)

    #drop duplicate store ids 
    df = df.drop_duplicates('store_id', keep='last')
    df.to_csv('unique_storeid_stores.csv',index=False)