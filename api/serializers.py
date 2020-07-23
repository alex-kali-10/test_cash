from api.models import *
from rest_framework import serializers


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'view_text']

class ArticleSerializerFull(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'text', 'href']


