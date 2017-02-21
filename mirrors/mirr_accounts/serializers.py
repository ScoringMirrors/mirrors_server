from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import UserProfile


class CreateUserSerializer(ModelSerializer):

    nikename = SerializerMethodField()
    mobile_no = SerializerMethodField()
    gender = SerializerMethodField()

    class Meta:
        models = User
        fields = ('email', 'password', 'password2', 'nikename', 'mobile_no', 'gender')
        extra_kwargs = {'password': {'write_only': True},
                        'password2': {'write_only': True}, }

    def create(self, validated_data):
        pass
