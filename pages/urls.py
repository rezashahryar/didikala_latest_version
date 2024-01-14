from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home_page_view, name='home_page_view'),
    path('newsletter/', views.newsletter_view, name='newsletter'),
    path('test-page/', views.test_page, name='test-page'),
    path('404/', views.custom_404, name='404_page'),
    path('privacy/', views.page_privacy, name='page_privacy'),
    path('page-faq/', views.page_faq_view, name='page_faq'),
    path('page-faq-category/', views.page_faq_category, name='page_faq_category'),
    path('page-faq-question/', views.page_faq_question, name='page_question'),
]
