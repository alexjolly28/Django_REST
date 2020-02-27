from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
import json
from api_basic.models import Article


class GenericApiView(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        title = request.data['title']
        print(title)
        queryset = Article.objects.get(id=37)
        serializer = ArticleSerializer(queryset)
        print(serializer.data['author'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ArticleApiView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #
    #     # received_json_data = json.loads(request.data)
    #
    #     return Response({'received data': received_json_data})

    def post(self, request):
        print(request.data)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.save()
            # serializer.save()

            # print(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def article_list_api(request):
    if request.method == 'GET':
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        print(request.data)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)


@api_view(['GEt', 'PUT', 'DELETE'])
def api_details(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
