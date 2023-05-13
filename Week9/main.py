from crawler import extract_news_titles
from word2vec import plot_word2vec
from sentiment_score import get_sentiment_score
from sentiment_score_chatgpt import get_sentiment_score_gpt

import argparse

parser = argparse.ArgumentParser(description='Get sentiment score of news titles')
parser.add_argument('--query', type=str, default='TESLA', help='Query to search for')
parser.add_argument('--num_pages', type=int, default=3, help='Number of pages to fetch')
parser.add_argument('--plot', action='store_true', help='Plot the word vectors in 2D space')
parser.add_argument('--gpt', action='store_true', help='Use GPT to get sentiment score')
args = parser.parse_args()

titles = extract_news_titles(args.query, args.num_pages)

if args.plot:
    plot_word2vec(titles)

nltk_scores = [get_sentiment_score(title) for title in titles]
gpt_socres = [get_sentiment_score_gpt(args.query, title, "short") if args.gpt else None for title in titles]
for title, nltk_score, gpt_score in zip(titles, nltk_scores, gpt_socres):
    print(f"Sentiment score for '{title}': NLTK {nltk_score}, GPT {gpt_score}")