from django.db import models


class Author(models.Model):
    full_name = models.CharField()
    age = models.IntegerField(blank=True)
    email = models.CharField(blank=True)


Author.objects.filter(age__lte=25).values('Author__full_name','email')
Author.objects.filter(age = 32).values("name")
