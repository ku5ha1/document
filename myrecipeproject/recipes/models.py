from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    ingredients = models.CharField()
    created = models.DateTimeField(auto_now_add=True)
    time_required = models.CharField(max_length=30)

    def __str__(self):
        return self.title