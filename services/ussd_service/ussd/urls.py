from django.urls import path
from .veiws import USSDGatewayView


urlpatterns = [
    path('ussd/', USSDGatewayView.as_view(), name='ussd-gatway'),
]
