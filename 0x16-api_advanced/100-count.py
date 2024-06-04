#!/usr/bin/python3
import requests
from collections import Counter
import sys

def count_words(subreddit, word_list):
    word_list = [word.lower() for word in word_list]
    word_counter = Counter()
    base_url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    
    def recurse(url, after=None):
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {'limit': 100}
        if after:
            params['after'] = after
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return

        data = response.json()
        if 'data' not in data:
            return

        titles = [child['data']['title'] for child in data['data']['children']]
        count_keywords(titles)

        after = data['data'].get('after')
        if after:
            recurse(url, after)
    
    def count_keywords(titles):
        for title in titles:
            words = title.lower().split()
            for word in word_list:
                word_counter[word] += words.count(word)
    
    recurse(base_url)
    
    if not word_counter:
        return

    sorted_counts = sorted(word_counter.items(), key=lambda item: (-item[1], item[0]))

    for word, count in sorted_counts:
        if count > 0:
            print(f'{word}: {count}')
