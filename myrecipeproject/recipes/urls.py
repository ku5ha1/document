from django.urls import path 
from .views import RecipeList, RecipeDetail


urlpatterns = [
    path('recipe_list/', RecipeList.as_view(), name='recipe_list'),
    path('recipe_detail/<int:pk>', RecipeDetail.as_view(), name='recipe_detail'),
]