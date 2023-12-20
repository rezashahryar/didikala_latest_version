from django.urls import path
from . import views


app_name = 'pages'
urlpatterns = [
    path('', views.home_page_view, name='home_page_view'),
    path('newsletter/', views.newsletter_view, name='newsletter'),
    path('test-page/', views.test_page, name='test-page'),
]
