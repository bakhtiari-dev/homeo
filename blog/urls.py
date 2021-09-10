from django.urls import path

from .views import ArticleList, ArticleDetail


app_name = 'blog'
urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('article/<int:article_id>/', ArticleDetail.as_view(), 
         name='article_detail'),
    path('category/<int:category_id>/', ArticleList.as_view(), 
         name='category'),
    path('author/<int:author_id>/', ArticleList.as_view(), name = "author"),
]
