from django.db import models
from django.contrib.auth.models import User

class APICallCount(models.Model):
    count = models.IntegerField(default=0)
    last_reset = models.DateTimeField(auto_now=True)

    @classmethod
    def increment(cls):
        obj, created = cls.objects.get_or_create(id=1)
        obj.count += 1
        obj.save()
        return obj.count

    @classmethod
    def get_count(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj.count

    @classmethod
    def reset(cls):
        obj, created = cls.objects.get_or_create(id=1)
        obj.count = 0
        obj.save()

    

    