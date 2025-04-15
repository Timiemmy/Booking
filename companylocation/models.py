from django.db import models

class ComapanyLocation(models.Model):
    stree_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    park = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.park} - {self.city} - {self.state} - {self.country}'