from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Advisor, User, Booking
from rest_framework.validators import UniqueValidator

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('name', 'profile_url')
    
    name = serializers.CharField(max_length=100, required=True, write_only=True)
    profile_url = serializers.CharField(max_length=2000, required=True, write_only=True)

class AllAdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('name','profile_url','id')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('name','email','password')

    def create(self, validated_data):
        record = User(name=validated_data["name"],email=validated_data["email"],password=validated_data["password"])
        record.save()
        return record

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email','password')

    def auth(self,received_data):
        email = received_data.get('email',None)
        password = received_data.get('password',None)
        print(email)
        print(password)
        record = authenticate(email=email,password=password)
        if record is None:
            raise serializers.ValidationError(
                'User not found'
            )
        else:
            return{
                'id':record.pk,
                'gen_token':record.token
            }
            

class BookCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('user_id','advisor_id','booking_date')
    
    user_id = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    advisor_id = serializers.PrimaryKeyRelatedField(many=False,queryset=Advisor.objects.all())
    booking_date = serializers.DateTimeField()

class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('user_id','advisor_id','booking_date')