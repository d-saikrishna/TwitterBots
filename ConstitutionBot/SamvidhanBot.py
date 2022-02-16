import tweepy as tw
import pygsheets
import random
from decouple import config
import os
import time

cwd = os.getcwd()
def tweet_constititution_wisdom():
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    access_token = config('access_token')
    access_token_secret = config('access_token_secret')
    #print('Hi')
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    gc = pygsheets.authorize(service_file=cwd+r'/ConstitutionBot/constitutionbot-3e833b17dba1.json')
    sh = gc.open('ConstitutionBot')
    wks = sh.worksheet('title', 'Sheet1')
    df = wks.get_as_df()
    df = df[(df['Length'] <= 275) & (df['Length'] > 0)].reset_index(drop=True)
    n = random.randint(0, df.shape[0] - 1)

    files = os.listdir(cwd+r'/ConstitutionBot')
    if (df['Author'][n] == 'NA'):
        tweet = str(df['Tweet'][n])
        author_images = [k for k in files if 'fact' in k]
    elif (df['Author'][n] == 'Shri Prem Behari Narain Raizada') or (df['Author'][n] == 'Raghu Vira') \
            or (df['Author'][n] == 'women') or (df['Author'][n] == 'words') \
            or ('Article' in df['Author'][n]) or (df['Author'][n] == 'Gandhi') or (
            df['Author'][n] == 'Narayan Agarwal'):
        tweet = str(df['Tweet'][n])
        author_images = [k for k in files if df['Author'][n] in k]
    else:
        tweet = '"' + str(df['Tweet'][n]) + '" - ' + str(df['Author'][n])
        try:
            author_images = [k for k in files if df['Author'][n] in k]
        except:
            pass

    tweet = tweet
    #print(type(df['Author'][n]))
    #print(author_images)
    #print(tweet)
    media_ids = []

    try:
        filename = author_images[random.randint(0, len(author_images) - 1)]
        res = api.media_upload(cwd+r'/ConstitutionBot/'+filename)
        media_ids.append(res.media_id)
        api.update_status(status=tweet, media_ids=media_ids)
    except:
        api.update_status(status=tweet)

def run():
    while True:
        tweet_constititution_wisdom()
        time.sleep(7200+7200)

if __name__ == "__main__":
    run()