import openai

openai.api_key = "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"

def get_sentiment_score_gpt(company, headline, term):
    prompt = f"Forget all your previous instructions. \
        Pretend you are a financial expert. You are a financial expert with stock recommendation experience. \
        Answer “YES” if good news, “NO” if bad news, or “UNKNOWN” if uncertain in the first line. \
        Then elaborate with one short and concise sentence on the next line. \
        Is this headline good or bad for the stock price of {company} in the {term} term?\n Headline: {headline}\n\n"
    
    # Generate response using the ChatGPT API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=5,
        temperature=0.7,
        n=1,
        stop=None,
    )
    
    # Extract the generated response
    generated_text = response.choices[0].text.strip().lower()
    
    # Assign sentiment score based on the generated response
    if generated_text.startswith("yes"):
        sentiment_score = 100
    elif generated_text.startswith("no"):
        sentiment_score = 0
    else:
        sentiment_score = 50
    
    return sentiment_score

if __name__ == "__main__":
    # Example usage
    company_name = "Tesla"
    news_headline = "Tesla reports better-than-expected earnings"
    term = "short"
    score = get_sentiment_score_gpt(company_name, news_headline, term)
    print(f"Sentiment score: {score}")
