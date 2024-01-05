from django.db import models

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    data_join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name