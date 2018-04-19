from project import newsapi, indicoio
from newspaper import Article
import copy
'''
1. Call NewsAPI get_top_headlines() to get top k articles
2. Pass these articles and their links into the NewsPaperAPI to get all the text
   for each article
3. Pass this text into the indicoio API to get political sentiment for each article
4. Make list of articles that are of certain political sentiment and return to frontend
'''
def get_top_headlines(current_user):
    articles = {}
    sources = ['abc-news', 'associated-press', 'breitbart-news', 'fox-news', 'reuters', 'the-economist', 'the-new-york-times', \
        'bbc-news', 'bloomberg', 'cnn', 'hacker-news', 'the-wall-street-journal']
    top_headlines = newsapi.get_top_headlines(sources=','.join(sources), language='en')
    article_data = {}
    for headline in top_headlines['articles']:
        article_data["article_name"] = headline['title']
        article_data["source"] = headline['source']['name']
        article_data["description"] = headline['description']
        article_data["url"] = headline['url']
        article = Article(article_data["url"],"en")
        article.download()
        article_data['html'] = article.html
        article.parse()
        article_data["text"] = article.text
        try:
            political_leaning = indicoio.political(article_data["text"])
            score = calculate_political_score(political_leaning["Liberal"], political_leaning["Conservative"])
            if score not in current_user.target_scores:
                continue
            else:
                article_data["political_leaning"] = score
        except:
            continue
        articles[copy.deepcopy(article_data["article_name"])] = copy.deepcopy(article_data)
    return articles

def calculate_political_score(liberal,conservative):
    score = 0
    if liberal < conservative:
        score = 9-round(liberal/(liberal+conservative) * 9)
    else:
        score = round(conservative/(liberal+conservative) * 9)
    return score