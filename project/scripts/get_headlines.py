from project import newsapi, indicoio, db
from ..models import Articles
from newspaper import Article
import datetime
from threading import Thread

'''
1. Call NewsAPI get_top_headlines() to get top k articles
2. Pass these articles and their links into the NewsPaperAPI to get all the text
   for each article
3. Pass this text into the indicoio API to get political sentiment for each article
4. Make list of articles that are of certain political sentiment and return to frontend
'''
def get_top_headlines():
    clear_old_data()
    sources = ['abc-news', 'associated-press', 'breitbart-news', 'fox-news', 'reuters', 'the-economist', 'the-new-york-times', \
        'bbc-news', 'bloomberg', 'cnn', 'hacker-news', 'the-wall-street-journal', 'daily-mail']
    top_headlines = newsapi.get_top_headlines(sources=','.join(sources), language='en', page_size=100)
    url_text = {}
    url_score = {}
    new_articles = []
    for headline in top_headlines['articles']:
        title = headline['title']
        source = headline['source']['name']
        if Articles.query.filter(Articles.article_name==title).filter(Articles.source==source).first() != None:
            return
        description = headline['description']
        url = headline['url']
        url_text[url] = ""
        url_score[url] = 0
        new_articles.append(Articles(title, source, description, url))
    threads = []
    for url in url_text:
        threads.append(create_url_data_thread(url, url_text))
    for thread in threads:
        thread.join()

    political_leanings = indicoio.political(list(url_text.values()))
    urls = url_text.keys()
    for political_leaning,url in zip(political_leanings,urls):
        url_score[url] = calculate_political_score(political_leaning["Liberal"], political_leaning["Conservative"])

    for new_article in new_articles:
        try:
            new_article.set_score(url_score[new_article.url])
            new_article.set_text(url_text[new_article.url])
            db.session.add(new_article)
        except:
            continue
    db.session.commit()

def create_url_data_thread(url, url_text):
    thread = Thread(target=get_article_data, args=(url, url_text, ))
    thread.daemon = True
    thread.start()
    return thread

def get_article_data(url, url_text):
    article = Article(url,"en")
    article.download()
    article.parse()
    text = article.text
    if len(text) == 0:
        del url_text[url]
    else:
        url_text[url] = text
    

def calculate_political_score(liberal,conservative):
    score = 0
    if liberal < conservative:
        score = 9-round(liberal/(liberal+conservative) * 9)
    else:
        score = round(conservative/(liberal+conservative) * 9)
    return score

def clear_old_data():
    Articles.query.filter(Articles.creation_date < datetime.datetime.now()-datetime.timedelta(days=1)).delete()
    db.session.commit()
