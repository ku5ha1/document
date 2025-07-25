from django.urls import path 
from .views import RecipeList


urlpatterns = [
    path('recipe_list/', RecipeList.as_view(), name='recipe_list')
]