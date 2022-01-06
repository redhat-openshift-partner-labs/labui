from django.db import models


class Faqs(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.TextField()
    status = models.BooleanField()
