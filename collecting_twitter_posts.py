import tweepy
import pandas as pd
import numpy as np
import time
import glob
import json                          
import plotly.graph_objects as go    
import tqdm
from tqdm import trange
from tqdm import tqdm
from psaw import PushshiftAPI
import datetime as dt
start_epoch=int(dt.datetime(2022, 1, 1).timestamp())

api_key = '<api_key>'  # add in your api key from your Twitter Developer Account here
api_key_secret = '<api_key_secret>' # add in your api secret from Twitter Developer Account here
bearer_token = '<bearer_token>'
access_token = '<access_token>'
access_token_secret = '<access_token_secret>'
client = tweepy.Client(bearer_token=bearer_token)




# News Categories:
mainstream = '((url:"www.bloomberg.com") OR (url:"www.fortune.com") OR (url:"www.theguardian.com") OR (url:"www.npr.org") OR (url:"www.salon.com") OR  (url:"www.newsweek.com") OR (url:"www.politico.com") OR (url:"www.pbs.org") OR (url:"www.economist.com") OR (url:"www.nbc.com") OR (url:"www.abcnews.com") OR (url:"www.cbsnews.com") OR (url:"www.cnn.com") OR (url:"www.foxnews.com") OR (url:"www.sfchronicle.com"))'
leaning_democrat = '((url:"www.Buzzfeed.com") OR (url:"www.cbsnews.com") OR (url:"www.abcnews.go.com") OR (url:"www.cnn.com") OR (url:"www.latimes.com") OR (url:"www.nytimes.com") OR (url:"www.nbcnews.com") OR (url:"www.newsweek.com") OR (url:"www.politico.com") OR (url:"www.theguardian.com") OR (url:"www.time.com") OR (url:"www.usnews.com") OR (url:"www.vanityfair.com") OR (url:"www.theatlantic.com") OR (url:"www.economist.com") OR (url:"www.theverge.com") OR (url:"www.washingtonpost.com"))'
leaning_republican = '((url:"www.bostonherald.com") OR (url:"www.thefiscaltimes.com") OR (url:"www.foxnews.com") OR (url:"www.dailypress.com") OR (url:"www.intellectualconservative.com") OR (url:"www.investors.com") OR (url:"www.post-gazette.com") OR (url:"www.reason.org") OR (url:"www.theamericanconservative.com") OR (url:"www.theepochtimes.com") OR (url:"www.thelibertarianrepublic.com") OR (url:"www.telegraph.co.uk") OR (url:"www.washingtonexaminer.com") OR (url:"www.washingtontimes.com"))'
democrat = '((url:"www.currentaffairs.org") OR (url:"www.democracynow.org") OR (url:"www.huffingtonpost.com") OR (url:"www.msnbc.com") OR (url:"www.nymag.com") OR (url:"www.rollingstone.com") OR (url:"www.sfchronicle.com") OR (url:"www.slate.com") OR (url:"www.mediamatters.org") OR (url:"www.nydailynews.com") OR (url:"www.salon.com") OR (url:"www.theintercept.com") OR (url:"www.newyorker.com") OR (url:"www.screen.yahoo.com") OR (url:"www.vice.com") OR (url:"www.vox.com"))'
republican = '((url:"www.conservativehq.com") OR (url:"www.americanthinker.com") OR (url:"www.cbn.com") OR (url:"www.dailymail.co.uk") OR (url:"www.infowars.com") OR (url:"www.rightwingnews.com") OR (url:"www.nationalreview.com") OR (url:"www.nypost.com") OR (url:"www.redstate.com") OR (url:"www.rightsidenews.com") OR (url:"www.dailycaller.com") OR (url:"www.theblaze.com") OR (url:"www.westernjournalism.com") OR (url:"www.dailywire.com") OR (url:"www.thefederalist.com") OR (url:"www.townhall.com"))'



query_params = {'query': <selection> + ' -is:retweet',                # <selection> is one of the categories from above.
           'tweet.fields': 'author_id,entities','max_results':100}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

response = connect_to_endpoint(search_url, query_params)


# Output an array given a search query:
def export (js):
  if 'urls' in ((js)['entities']):
    return ['www.twitter.com/anyuser/status/' + str((js)['id']), ((js)['text']), process((js)['text']), (((((js)['entities'])['urls'])[0])['expanded_url'])]
  else:
    return ['www.twitter.com/anyuser/status/' + str((js)['id']), ((js)['text']), process((js)['text']), '']


# This is necessary because the API generates results in pages.
def paginate(r):
  token = r['meta']['next_token']
  new_params = query_params
  new_params.update({'pagination_token':token})
  return connect_to_endpoint(search_url, new_params)



responses = []
responses.append(response)

# We arbitrarily chose to use 10 pages of max length 100.
for i in range(1,10):
  responses.append(paginate(responses[i-1]))




# Allocate all the responses in a .csv file:

table = []
def add_to_table(r):
  #response = connect_to_endpoint(search_url, query_params)
  for x in range(r['meta']['result_count']):
    row=[]
    row += (export(((r)['data'])[x]))
    table.append(row)

for r in responses:
  add_to_table(r)

df = pd.DataFrame({'Link': [i[0] for i in table], 
                   'Body': [i[1] for i in table],
                   'Processed Text': [i[2] for i in table],
                   'Article': [i[3] for i in table],
                   })
                   
df.to_csv('<selection>.csv')
