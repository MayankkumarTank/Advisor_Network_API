from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AdvisorSerializer,RegisterSerializer,LoginSerializer,AllAdvisorSerializer,BookCallSerializer,BookViewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Advisor, User, Booking
from rest_framework.permissions import AllowAny

# Create your views here.
class AdvisorView(viewsets.ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer

class RegisterView(APIView):
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, **kwargs):
        data = {'email': request.data.get('email', ''), 'name': request.data.get('name', ''),
                'password': request.data.get('password', '')}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):
    #i add it because of readonly permission
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        data = {'email': request.data.get('email', ""), 'password': request.data.get('password', "")}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def seeadvisor(request,user_id):
    permission_classes = (AllowAny,)
    #check the user is registered or not
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response('User is not Registered...', status=status.HTTP_404_NOT_FOUND)

    records = Advisor.objects.all()
    serializer = AllAdvisorSerializer(records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def bookcall(request,user_id,advisor_id):
    permission_classes = (AllowAny,)
    #check the user is registered or not
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response('User is not Registered...', status=status.HTTP_404_NOT_FOUND)
    #check the advisor is registered or not
    try:
        advisor = Advisor.objects.get(pk=advisor_id)
    except Advisor.DoesNotExist:
        return Response('Advisor is not Registered...', status=status.HTTP_404_NOT_FOUND)
    book_date = request.data.get('date')
    data['date'] = book_date
    record = Booking(user_id=user,advisor_id=advisor,booking_date=book_date)
    #saving the record
    record.save()
    serializer = BookCallSerializer(data=record)
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getbooking(request,user_id):
    try:
        user = User.objects.get(pk=user_id)
    except NewUser.DoesNotExist:
        return Response('User is not Registered...', status=status.HTTP_404_NOT_FOUND)
    record = Booking.objects.filter(user_id=user)

    serializer = BookViewSerializer(record, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)