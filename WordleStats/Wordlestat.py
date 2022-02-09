import tweepy as tw
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# https://docs.tweepy.org/en/v4.0.0/api.html#tweepy.API.search_tweets

consumer_key = 'xxx'
consumer_secret='yyy'
access_token= 'vvv-ccc'
access_token_secret= 'rrr'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

wordle_num = pd.read_csv('wordle_num.csv')
search_words = '"Wordle %d"' %(wordle_num['wordle_num'][wordle_num.shape[0]-1])
print(search_words)

#new_search = search_words + " -filter:retweets" to remove retweets
count=0
scores = []
max_scores = []
ids = []
locations = []
for tweet in api.search_tweets(q=search_words, lang="en",
                               #until=date_until,
                               count=100, result_type='recent'):
    count = count+1
    max_id = tweet.id
    text = tweet.text
    try:
        score = text.split(r'/')[0][-1]
        max_score = text.split(r'/')[1][0]
        scores.append(score)
        max_scores.append(max_score)
        ids.append(tweet.id)
        locations.append(tweet.user.location)
    except:
        continue

keeprunning = True
while keeprunning:
    tweets = api.search_tweets(q=search_words,
                               lang="en",
                               #until=date_until,
                                count=100, result_type='recent', max_id=max_id)
    for tweet in tweets:
        count = count + 1
        max_id = tweet.id
        text = tweet.text
        try:
            score = text.split(r'/')[0][-1]
            max_score = text.split(r'/')[1][0]
            scores.append(score)
            max_scores.append(max_score)
            ids.append(tweet.id)
            locations.append(tweet.user.location)
        except:
            continue

    print(count)
    df = pd.DataFrame([scores, max_scores, ids,locations]).T
    df.to_csv('Wordle %d' %(wordle_num['wordle_num'][wordle_num.shape[0]-1])+'.csv', index=False)
    # if count==300:
    #     keeprunning = False
    #     break
    if len(tweets) < 100:
        keeprunning = False
        break

## STATS
df = pd.read_csv('Wordle %d' %(wordle_num['wordle_num'][wordle_num.shape[0]-1])+'.csv')
df.columns=['score','max_score','ids','locations']
df = df.drop_duplicates(subset='ids')
df = df[df.max_score==6]
df = df[df['score'].isin(['1','2','3','4','5','6','X'])]
tweeter_wordlers = df.shape[0]
median = df[df['score'].isin(['1','2','3','4','5','6'])]['score'].median(axis=0)
mean = df[df['score'].isin(['1','2','3','4','5','6'])]['score'].astype('int').mean(axis=0)

df_g = df.groupby('score')['ids'].count().reset_index()
df_g.columns =  ['# Guesses','# Wordlers']
df_g['Percentage'] = 100*df_g['# Wordlers']/tweeter_wordlers

df_g2 = df.groupby('locations')['ids'].count().reset_index()
pal = sns.color_palette("RdYlGn_r", len(df_g))
rank = df_g.Percentage.argsort().argsort()
g = sns.barplot(x='# Guesses',y='# Wordlers',data=df_g,palette=np.array(pal[::-1])[rank])
csfont = {'fontname':'monospace'}
plt.title('Wordle %d' %(wordle_num['wordle_num'][wordle_num.shape[0]-1])+' Stats', fontsize=40, fontweight=20,
          #backgroundcolor='green',
          color='green', **csfont)
patches = g.patches
for i in range(len(patches)):
   x = patches[i].get_x() + patches[i].get_width()/2
   y = patches[i].get_height()+.05
   g.annotate('{:.1f}%'.format(df_g.Percentage[i]), (x, y), ha='center', fontsize=10)

mean_string='Average # Guesses needed: \n'+str(round(mean,2))
g.annotate(mean_string, xy=(0.80, 0.90), ha='center', fontsize=10, xycoords='axes fraction')
plt.tight_layout()
plt.xlabel('# Guesses', fontsize=16, fontweight=10)
plt.ylabel('# Wordlers', fontsize=16,fontweight=10)
plt.savefig('Wordle %d' %(wordle_num['wordle_num'][wordle_num.shape[0]-1])+'.png')

filenames = ['Wordle %d' %(wordle_num['wordle_num'][wordle_num.shape[0]-1])+'.png']
media_ids = []
for filename in filenames:
     res = api.media_upload(filename)
     media_ids.append(res.media_id)

# Tweet with multiple images
#api.update_status(status='''#Wordle%d Stats - [Based on %d Twitter Shares] @powerlanguish''' %(wordle_num['wordle_num'][wordle_num.shape[0]-1],tweeter_wordlers),
 #                 media_ids=media_ids)

wordle_num_list = wordle_num['wordle_num'].to_list()
wordle_num_list.append(wordle_num['wordle_num'][wordle_num.shape[0] - 1] + 1)
Wordlers_list = wordle_num['Wordlers'].to_list()
Wordlers_list.append(tweeter_wordlers)
Wordlers_list = [x for x in Wordlers_list if str(x) != 'nan']
wordle_num=pd.DataFrame([wordle_num_list, Wordlers_list]).T
wordle_num.columns=['wordle_num', 'Wordlers']
wordle_num.to_csv('wordle_num.csv', index=False)

