from __future__ import absolute_import, unicode_literals


from celery import Celery

from django.utils import timezone
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_cash.settings')
import django
django.setup()


app = Celery('test_cash')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()



from api.models import *

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, example_task.s(), name='add every 10')

    sender.add_periodic_task(30.0, parser.s(), name='add every 30')

    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=7),
        parser.s(),
    )


@app.task
def example_task():
    print('задача для доказательства что оно работает')


@app.task
def parser():
    '''
    Парсер состоит из 2 блоков.
    Первый забивает все ссылки масив.
    Второй Проходит по этим ссылкам и сохраняет необходимые данные.
    '''
    #Article.objects.filter().delete()
    mass_href = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = 'https://habr.com/ru/top'
    req = Request(url=reg_url, headers=headers)
    page = urlopen(req).read()
    soup = BeautifulSoup(page,features="html.parser")
    list = soup.find_all('a', {'class': 'post__title_link'})
    for i in list:
        href = i.get('href')
        mass_href.append(href)
    for href_page in mass_href:
        if(Article.objects.filter(href=href_page).exists()):
            pass
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url = href_page
            req = Request(url=reg_url, headers=headers)
            page = urlopen(req).read()
            soup = BeautifulSoup(page,features="html.parser")
            name = soup.find('span', {'class': 'post__title-text'}).text
            text = str(soup.find('div', {'class': 'post__body_full'}))
            article = Article(name = name, text = text,href = href_page)
            article.save()