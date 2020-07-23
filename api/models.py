from django.db import models

class Article(models.Model):
    class Meta():
        db_table = 'article'
    name = models.CharField(verbose_name='name',max_length=100,default='')
    text = models.CharField(verbose_name='text', max_length=100000, default='')
    href = models.CharField(verbose_name='href', max_length=100, default='')
    def view_text(self):
        return self.text[:700]
