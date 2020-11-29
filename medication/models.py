import os
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django_resized import ResizedImageField

# Medication image path 
def Medication_image_path(instance, filename):
    return os.path.join('Medication', str(instance.medication), filename)

# The medication class..
class Medication(TimeStampedModel):

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=360)
    dose = models.IntegerField()
    number_of_items = models.IntegerField()
    user = models.ForeignKey(User, default=1,  on_delete=models.CASCADE)

    # medication item object string represation
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created',]

# Medication image class 
class MedicationImage(TimeStampedModel):
    medication= models.ForeignKey(Medication, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= Medication_image_path)
    user = models.ForeignKey(User, default="1", on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.medication}'
        return template.format(self)

    class Meta:
        ordering = ['-created',]



class ViewsNumber(models.Model):
    Medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    numberview = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)