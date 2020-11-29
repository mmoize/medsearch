from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import NewMedicationViewset,  MedicationDetail, MedicationViewSet, SearchMedication, getAllOwnersMedication, RecentMedication

router = routers.DefaultRouter()
router.register('medications', MedicationViewSet)


newmedication = NewMedicationViewset.as_view({'post': 'create'})
searchmedication = SearchMedication.as_view({'get': 'list'})
getallOwnerMedication =  getAllOwnersMedication.as_view({'get': 'list'})

app_name = 'medication'

urlpatterns = [
    path('', include(router.urls)),
    path('create_medication/', newmedication, name='create_medication'),
    path('searchmed/', searchmedication , name='search_medication'),
    path('medidetail/<int:id>', MedicationDetail , name='medication_detail'),
    path('recentmedication/', RecentMedication , name='recent_medication'),
    path('ownersmedication/', getallOwnerMedication , name='allowners_medication')
    
]
