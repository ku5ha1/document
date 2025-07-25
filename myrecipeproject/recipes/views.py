from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import RecipeSerializer
from .models import Recipe
from django.http import Http404

class RecipeList(APIView):
    
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RecipeDetail(APIView):

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        pass