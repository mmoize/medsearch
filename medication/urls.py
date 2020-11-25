from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import NewMedicationViewset, MedicationViewSet

router = routers.DefaultRouter()
router.register('medications', MedicationViewSet)


newmedication = NewMedicationViewset.as_view({'post': 'create'})

app_name = 'medication'

urlpatterns = [
    path('movie/', include(router.urls)),
    path('newmovie', newmedication, name='medication_create'),
          
]
