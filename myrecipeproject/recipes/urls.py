from django.urls import path 
# from .views import RecipeList, RecipeDetail
from .views import RecipeViewSet 
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    # path('recipe_list/', RecipeList.as_view(), name='recipe_list'),
    # path('recipe_detail/<int:pk>', RecipeDetail.as_view(), name='recipe_detail'),
]

urlpatterns += router.urls