from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import NewMedicationViewset, MedicationViewSet, SearchMedication

router = routers.DefaultRouter()
router.register('medications', MedicationViewSet)


newmedication = NewMedicationViewset.as_view({'post': 'create'})
searchmedication = SearchMedication.as_view({'get': 'list'})

app_name = 'medication'

urlpatterns = [
    path('', include(router.urls)),
    path('create_medication/', newmedication, name='create_medication'),
    path('searchmed/', searchmedication , name='search_medication'),
          
]
