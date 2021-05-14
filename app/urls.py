from django.urls import path,include
from . import views
from rest_framework import routers
from .views import RegisterView ,LoginView

router = routers.DefaultRouter()
router.register('advisor/admin',views.AdvisorView)

urlpatterns = [
    path('',include(router.urls)),    
    path('user/register', RegisterView.as_view() ,name='user_register'),
    path('user/login',LoginView.as_view(), name='user_login'),
    path('user/<int:user_id>/advisor',views.seeadvisor,name='seeadvisor'),
    path('user/<int:user_id>/advisor/<int:advisor_id>',views.bookcall,name='bookcall'),
    path('user/<int:user_id>/advisor/booking',views.getbooking,name='getbooking'),
]
