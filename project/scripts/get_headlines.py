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
    sources = ['breitbart-news', 'fox-news', 'reuters', 'the-economist', 'the-new-york-times', 'buzzfeed']
    top_headlines = newsapi.get_top_headlines(sources=','.join(sources), language='en')
    article_data = {}
    for headline in top_headlines['articles']:
        article_data["article_name"] = headline['title']
        article_data["source"] = headline['source']['name']
        article_data["description"] = headline['description']
        article_data["url"] = headline['url']
        article = Article(article_data["url"],"en")
        article.download()
        article.parse()
        article_data["text"] = article.text
        try:
            article_data["political_leaning"] = indicoio.political(article_data["text"])
        except:
            continue
        articles[article_data["article_name"]] = copy.deepcopy(article_data)
    return articles
