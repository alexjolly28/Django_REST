from django.urls import path
from .views import GenericApiView

urlpatterns = [
    # path('article/', article_list),
    # path('api/', article_list_api),
    # path('detail/<int:pk>/', article_detail),
    # path('api/<int:pk>/', api_details),
    # path('article_api/', ArticleApiView.as_view()),
    # path('article_api/<int:id>/', ArticleDetails.as_view()),
    path('generic/', GenericApiView.as_view())
]
