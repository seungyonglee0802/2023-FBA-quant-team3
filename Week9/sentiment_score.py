import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# nltk.download('vader_lexicon')

def get_sentiment_score(title):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(title)
    
    # Convert sentiment score to a range of 0 to 100
    sentiment_score = (sentiment_scores["compound"] + 1) * 50
    
    return sentiment_score

if __name__ == "__main__":
    # Example usage
    title = "I love you"
    score = get_sentiment_score(title)
    print(f"Sentiment score for '{title}': {score}")
