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




class NewMedicationViewset(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super(NewMovieViewset, self).get_serializer_context()
    

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
        print('this is pre-save serializery', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





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
                    'message': 'upload a valid image. The file you uploaded was '
                                'neither not an image or a corrupted image.'
                }, code=406
            )
        print('this is new request data', request.data)
        serializer = self.get_serializer(data=request.data)
        
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




    

    




