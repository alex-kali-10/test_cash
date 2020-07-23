from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import auth
from datetime import datetime
from django.core import serializers
from django.contrib.auth.models import User


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *
from .models import *
from test_cash import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(['GET'])

@permission_classes([permissions.AllowAny,])

def article_list(request):
    '''
    Отображает набор элементов сортированных по id.
    Реализованна пагинация.
    По 3 элемента на странице.
    data = {
        "count": ...,
        "next": ...,
        "previous": ...,
        "results":[
            {
                name: ...,
                view_text: ...,
                href: ...,
            }
        ]...
    '''
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 3

        list_article = Article.objects.all().order_by('id')
        result_page = paginator.paginate_queryset(list_article, request)
        serializer = ArticleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET','PUT','DELETE'])
def article(request,pk):
    '''
    pk = id

    GET = Просмотр элемента
    PUT = Изменяет элемент
    DELETE = Удаляет элемент

    data={
        name: ...,
        text: ...,
        href: ...,
    }
    '''
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializerFull(article, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ArticleSerializerFull(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)