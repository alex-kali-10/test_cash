from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from .models import Article
from .views import article,article_list

class ArticleTest(APITestCase):
    '''
    Мой первый тест(
    setUp - Забивает данные в тестовую бд для теста
    test_list - тестирует article_list
    test_single_get - тестирует get article
    test_single_put - тестирует put article
    test_single_delete - тестирует delete article
    '''
    def setUp(self):
        self.item_article = Article.objects.create(id=1, name='Casper1', text='123', href='my_href')
        Article.objects.create(id=2, name='Casper2', text='123', href='my_href')
        Article.objects.create(id=3, name='Casper3', text='123', href='my_href')
        Article.objects.create(id=4, name='Casper4', text='123', href='my_href')

    def test_list(self):
        factory = APIRequestFactory()
        request = factory.get('article_list/?1=', content_type='application/json')
        data = dict(article_list(request).data)
        self.assertEqual(data['count'], 4)
        self.assertEqual(dict(data['results'][0])['name'], self.item_article.name)

    def test_single_get(self):
        factory = APIRequestFactory()
        request = factory.get('/article/1', content_type='application/json')
        self.assertEqual(article(request,1).data['name'],self.item_article.name)

    def test_single_put(self):
        factory = APIRequestFactory()
        request = factory.put('/article/1',{"name": "new_name"})
        article(request, 1)
        self.assertEqual(Article.objects.get(id = 1).name,"new_name")

    def test_single_delete(self):
        factory = APIRequestFactory()
        request = factory.delete('/article/1',content_type='application/json')
        article(request, 1)
        self.assertEqual(Article.objects.filter(id=1).exists(),False)