from django.urls import path
from .views import article_list, article_detail,article_list_api,api_details,ArticleApiView,ArticleDetails

urlpatterns = [
    path('article/', article_list),
    path('api/',article_list_api),
    path('detail/<int:pk>/', article_detail),
    path('api/<int:pk>/',api_details),
    path('article_api/',ArticleApiView.as_view()),
    path('article_api/<int:id>/',ArticleDetails.as_view())
]
