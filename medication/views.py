from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Medication, MedicationImage
from .serializers import MedicationSerializer, MedicationImageSerializer, Medication_ImageSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAcceptable
from .utils import MultipartJsonParser
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



# Modelviewset for creating a new medication..
class NewMedicationViewset(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super(NewMedicationViewset, self).get_serializer_context()
    

        if len(self.request.data) > 0:
            context.update({
                'included_images': self.request.FILES
            })
            context.update({
                'medication_info': self.request.data
            })

        return context

        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




# Retreiving  medication..
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    parser_classes = [MultipartJsonParser, JSONParser]
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )


    def get_serializer_context(self):
        context = super(MedicationViewSet, self).get_serializer_context()
 
        if len(self.request.data) > 0:
            context.update({
               'included_images': self.request.FILES
            })
            context.update({
                'medication_info': self.request.data
            })

        return context

    def create(self, request, *args, **kwargs):
    
        try:
            MedicationImage_serializer = MedicationImageSerializer(data=request.FILES)
            
            MedicationImage_serializer.is_valid(raise_exception=True)
        except Exception:
            raise NotAcceptable(

                detail={
                    'message': 'Please upload a valid image. The file you uploaded was '
                                'either not an image or a corrupted image.'
                }, code=406
            )

        serializer = self.get_serializer(data=request.data)
        
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SearchMedication(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()


    def get_queryset(self, *args, **kwargs):

        queryset = Medication.objects.all()

        name__startswith = self.request.query_params.get('name__startswith', None)
        print("name startwith", name__startswith)

        name__in = self.request.query_params.get('name__in', None)
        name__exact = self.request.query_params.get('name__exact', None)

        dose__lt = self.request.query_params.get('dose__lt', None)
        dose__gt = self.request.query_params.get('dose__gt', None)
        dose__exact = self.request.query_params.get('dose__exact', None)

        number_of_items__lt = self.request.query_params.get('number_of_items__lt', None)
        number_of_items__gt = self.request.query_params.get('number_of_items__gt', None)
        number_of_items__exact = self.request.query_params.get('number_of_items__exact', None)


        if name__startswith is not None:
            
            if name__startswith == 'None':
                # The request doesn't a have a search term "name".
                pass
            else:
                # Request contains a search term "name", 
                newqueryset = queryset.filter(name__startswith=name__startswith.lower())
                print("new queryset", newqueryset)
                if not newqueryset.exists():
                    pass
                else:
                    
                    queryset = newqueryset



        if name__in is not None:

            if name__startswith == 'None':
                # The request doesn't a have a search term "name".
                pass
            else:
                # Request contains a search term "name", 
                queryset = queryset.filter(name__in=name__startswith.lower())

        if name__exact is not None:

            if name__startswith == 'None':
                # The request doesn't a have a search term "name".
                pass
            else:
                # Request contains a search term "name", 
                queryset = queryset.filter(name__exact=title__startswith.lower())


        if dose__gt is not None:
            if dose__gt == 'None':
                # Request does not contain a Minimum value for doses.
                pass
            else:
                # Request contains a Minimum value for doses.
                queryset = queryset.filter(dose__gt=dose__gt)

            
        if dose__lt is not None:
            if dose__lt == 'None':
                # Request does not contain a Maximum value for doses.
                pass
            else:
                # Request does contain a Maximum value for doses.
                queryset = queryset.filter(dose__lt=dose__lt) 
             
        # if dose__exact is not None:
        #     queryset = queryset.filter(dose__exact=dose__exact)  

        
        if number_of_items__gt is not None:
            if dose__gt == 'None':
                # Request does not contain a Minimum value for number_of_items.
                pass
            else:
                # Request does  contain a Minimum value for number_of_items.
                queryset = queryset.filter(number_of_items__gt=number_of_items__gt)

            
        if number_of_items__lt is not None:
            if dose__lt == 'None':
                # Request does not  contain a Maximum value for number_of_items.
                pass
            else:
                # Request does  contain a Maximum value for number_of_items.
                queryset = queryset.filter(number_of_items__lt=number_of_items__lt) 
             
        if number_of_items__exact is not None:
            queryset = queryset.filter(number_of_items__exact=number_of_items__exact)  



        return queryset







    
@csrf_exempt
def MedicationDetail(request, id):

    if request.method == 'GET':

        medication = Medication.objects.filter(id=id)
        serializer = MedicationSerializer(medication, many=True)
        return JsonResponse(serializer.data, safe=False)
    


@csrf_exempt
def RecentMedication(request):

    if request.method == 'GET':

        medication = Medication.objects.all()[:5]
        serializer = MedicationSerializer(medication, many=True)
        return JsonResponse(serializer.data, safe=False)

