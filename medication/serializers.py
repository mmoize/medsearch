from rest_framework import serializers
from .models import Medication, MedicationImage
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from account.serializers import UserSerializer
from django.forms import ImageField as DjangoImageField




class Medication_ImageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="medication:medicationimage-detail", read_only=True, lookup_field="medicationimage")
    medication = serializers.HyperlinkedRelatedField(view_name="medication:medication-detail", read_only=True, source="medication_user")
    user = UserSerializer(read_only=True)

    class Meta:
        model = MedicationImage
        fields =['id', 'medication','url', 'image', 'created', 'user']
        extra_kwargs = { 
            'medication': {'required': False},
        }



class MedicationImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="medication:medicationimage-detail", read_only=True, lookup_field="medicationimage")
    medication = serializers.HyperlinkedRelatedField(view_name="medication:medication-detail", read_only=True, source="user_medication")
    user = UserSerializer(read_only=True)

    class Meta:
        model = MedicationImage
        fields =['id', 'medication','url', 'image', 'created', 'user']
        extra_kwargs = { 
            'medication': {'required': False},
            'medication_id': {'required': False},
            'url': {'view_name': 'medication:medicationimage-detail'}, 
        }
 
    
    def validate(self, attrs):
    
        default_error_messages = {
            'Image Provided is Invalid':
            'Please Upload a valid image. The file you uploaded was either not an image'
        }

        for i in self.initial_data.getlist('image'):

            django_field = DjangoImageField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)
        return attrs




class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    medicationimage_set = Medication_ImageSerializer(allow_null=True, many=True, read_only=True)
    user = UserSerializer(read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name="medication:medication-detail", read_only=True, lookup_field="user")
    class Meta:
        model = Medication
        fields = ['id','url', 'user', 'name', 'description', 'number_of_items', 'dose']

    def create(self, validated_data):

        data = self.context['medication_info']
        medication_name = data['name']
        medication_description = data['description']
        medication_dose = data['dose']
        medication_number_of_items = data['number_of_items']

        
        
        currentUser = User.objects.get(id=self.context['request'].user.id)
        
        medication_obj = Medication.objects.get_or_create(
            name = medication_name,
            description = medication_description,
            dose = medication_dose,
            number_of_items = medication_number_of_items
        )

        images_data = self.context['included_images']
        medication_instance = medication_obj[0]

        for i in images_data.getlist('image'):
            MedicationImage.objects.create(medication=medication_instance, image=i,  user=self.context['request'].user)
        return medication_instance


