import praw
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask
from flask import request
import openai
openai.api_key = "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"
app = Flask(__name__)


def predict(query):
    
        labels=['depression','ptsd','schizophrenia','adhd','bipolar','autism','bpd','anxiety']
        result = openai.Classification.create(
        file="file-ipYxEBf8HDrgCPl2eLkxX7Al",
        query=query,
        search_model="ada",
        model="curie",
        max_examples=8,
        labels=labels,
        logprobs=9,  # Here we set it to be len(labels) + 1, but it can be larger.
        expand=["completion"])
        return result.label
   



def getData(subreddit):
    reddit_read_only = praw.Reddit(client_id="nu-mJ-a_GkxRU6gL4De8KQ",		 # your client id
                                   client_secret="wwIbMQ0baO3dUxnI6nmDn5CteqQnjg",	 # your client secret
                                   user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36")	 # your user agent

    subreddit = reddit_read_only.subreddit(subreddit)
    posts = subreddit.top("month", limit=50)
    # Scraping the top posts of the current month
    posts_dict = {"Title": [], "Post Text": [],
                  "ID": [], "Score": [],
                  "Total Comments": [], "Post URL": []
                  }

    for post in posts:
        # Title of each post
        posts_dict["Title"].append(post.title)

        # Text inside a post
        posts_dict["Post Text"].append(post.selftext)

        # Unique ID of each post
        posts_dict["ID"].append(post.id)

        # The score of a post
        posts_dict["Score"].append(post.score)

        # Total number of comments inside the post
        posts_dict["Total Comments"].append(post.num_comments)

        # URL of each post
        posts_dict["Post URL"].append(post.url)
    # Saving the data in a pandas dataframe
    top_posts = pd.DataFrame(posts_dict)
    df = pd.DataFrame(top_posts["Post Text"])
    return df


def clean_data(data):
    df = data
    # rename column post text to selftext
    df.rename(columns={'Post Text': 'selftext'}, inplace=True)
    # remove nan values
    df.dropna(inplace=True)
    # remove all extra spaces from selftext
    df['selftext'] = df['selftext'].str.replace('\s+', ' ')
    # remove all special characters from selftext
    df['selftext'] = df['selftext'].str.replace('[^\w\s]', '')
    # convert all selftext to lowercase
    df['selftext'] = df['selftext'].str.lower()
    return df


@app.route('/query', methods=['GET', 'POST'])
def index():
    # read paramerters from the url
    query = request.args.get('query')
    # call the function to get the response
    response = predict(query)
    return response


@app.route('/search', methods=['GET', 'POST'])
def search():
    # read paramerters from the url
    query = request.args.get('search')
    # call the function to get the response
    #response = query  # predict(query)
    df=getData(query)
    df=clean_data(df)
    df.to_csv("final_data.csv")
    df=pd.read_csv("final_data.csv",index_col=0)
    df.dropna(inplace=True)
    responce=df.to_json(orient='records')
    return responce


if __name__ == '__main__':
    app.run(debug=True)
