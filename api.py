import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import requests
import time
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not XAI_API_KEY:
    raise ValueError("XAI_API_KEY not found in environment variables")
if not TWITTER_BEARER_TOKEN:
    raise ValueError("TWITTER_BEARER_TOKEN not found in environment variables")

def get_twitter_username(url):
    # Extract username from Twitter URL
    match = re.search(r'twitter\.com/|x\.com/(?!home)(@?\w+)', url)
    if match:
        username = match.group(1)
        print(f"Extracted username: {username}")  # Debug print
        return username
    print("Failed to extract username from URL")  # Debug print
    return None

def get_twitter_profile(username, tweet_count=20, max_retries=5):
    print(f"Fetching profile for username: {username}")  # Debug print
    
    headers = {
        'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'
    }
    
    # Get user profile data including pinned tweet ID
    user_url = f'https://api.twitter.com/2/users/by/username/{username}?user.fields=description,pinned_tweet_id'
    
    for retry in range(max_retries):
        user_response = requests.get(user_url, headers=headers)
        
        if user_response.status_code == 200:
            break
        elif user_response.status_code == 429:
            # Use the rate limit reset time if available
            reset_time = int(user_response.headers.get('x-rate-limit-reset', 2 ** retry))
            wait_time = max(reset_time - int(time.time()), 2 ** retry)
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            continue
        else:
            print(f"Error response: {user_response.text}")
            return None
    
    try:
        user_data = user_response.json()['data']
        
        # Use Twitter API v2 to get tweets
        tweets_url = f'https://api.twitter.com/2/users/{user_data["id"]}/tweets'
        params = {
            'max_results': tweet_count,
            'tweet.fields': 'created_at,public_metrics',
            'exclude': 'retweets,replies'
        }
        
        tweets = []
        for retry in range(max_retries):
            # Add delay between requests to avoid rate limits
            time.sleep(1)
            
            tweets_response = requests.get(tweets_url, headers=headers, params=params)
            print(f"Tweets API Response Status: {tweets_response.status_code}")  # Debug print
            
            if tweets_response.status_code == 200:
                tweets_data = tweets_response.json()
                tweets = [tweet['text'] for tweet in tweets_data.get('data', [])]
                break
            elif tweets_response.status_code == 429:
                reset_time = int(tweets_response.headers.get('x-rate-limit-reset', 2 ** retry))
                wait_time = max(reset_time - int(time.time()), 2 ** retry)
                print(f"Rate limited on tweets. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Failed to get tweets: {tweets_response.text}")
                break
        
        # Get pinned tweet if it exists
        pinned_tweet = None
        if 'pinned_tweet_id' in user_data:
            for retry in range(max_retries):
                time.sleep(1)  # Add delay to avoid rate limits
                pinned_url = f'https://api.twitter.com/2/tweets/{user_data["pinned_tweet_id"]}'
                pinned_response = requests.get(pinned_url, headers=headers)
                
                if pinned_response.status_code == 200:
                    pinned_tweet = pinned_response.json()['data']
                    break
                elif pinned_response.status_code == 429:
                    reset_time = int(pinned_response.headers.get('x-rate-limit-reset', 2 ** retry))
                    wait_time = max(reset_time - int(time.time()), 2 ** retry)
                    print(f"Rate limited on pinned tweet. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
        
        return {
            'username': user_data['username'],
            'name': user_data.get('name', ''),
            'description': user_data.get('description', ''),
            'pinned_tweet': pinned_tweet['text'] if pinned_tweet else None,
            'recent_tweets': tweets
        }
    except Exception as e:
        print(f"Error processing user data: {str(e)}")  # Debug print
        return None

# Get the Twitter profile data
url = "https://x.com/ylecun"
username = get_twitter_username(url)
profile_data = get_twitter_profile(username) if username else None

# Update and print the profile context
profile_context = (
    f"Username: {profile_data['username']}\n"
    f"Name: {profile_data['name']}\n"
    f"Description: {profile_data['description']}\n"
    f"Pinned Tweet: {profile_data['pinned_tweet']}\n"
    f"Recent Tweets:\n" + "\n".join(f"- {tweet}" for tweet in profile_data['recent_tweets'])
) if profile_data else "No profile data available"

print("=== Profile Context ===")
print(profile_context)
print("====================\n")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
    model="grok-beta",
    messages=[
        {"role": "system", "content": '''you are a roasting master in socials who can use the most hilarious word 
                                        to roast people based on their x profile. Now I'll give you the link to a x profile 
                                        and I want you to roast this guy, using a tone that is sarcastic and funny.
                                        Pretend you are this guy itself who is acting as Santa Claus. Say the words that
                                        this guy would say if it's Santa. Make the content related to Christmas as much as you can. 
                                        Keep your answer short and concise within 100 words.
                                        Only use real information and don't make up any facts. 
                                        The output you give will be used as a script for a speaker, so no emojis or hashtags.'''},
        {"role": "user", "content": f"Here's the profile information: {profile_context}"},
    ],
)

print(completion.choices[0].message.content)
