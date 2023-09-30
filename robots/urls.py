from django.urls import path
from .views import CreateRobotView

urlpatterns = [
    path('create/', CreateRobotView.as_view(), name='create-robot'),
]