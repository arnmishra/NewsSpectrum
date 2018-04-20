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
    threads = []
    for headline in top_headlines['articles']:
        thread = Thread(target=get_article_data, args=(headline, ))
        threads.append(thread)
        thread.daemon = True
        thread.start()
    for thread in threads:
        thread.join()

def get_article_data(headline):
    title = headline['title']
    source = headline['source']['name']
    if Articles.query.filter(Articles.article_name==title).filter(Articles.source==source).first() != None:
        return
    description = headline['description']
    url = headline['url']
    article = Article(url,"en")
    article.download()
    article.parse()
    text = article.text
    new_article = []
    try:
        political_leaning = indicoio.political(text)
        score = calculate_political_score(political_leaning["Liberal"], political_leaning["Conservative"])
        new_article = Articles(title, source, description, url, text, score)
    except Exception as e:
        print("Exception", e)
        return
    db.session.add(new_article)
    db.session.commit()

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
