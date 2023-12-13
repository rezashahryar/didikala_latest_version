from django.shortcuts import render

# Create your views here.


def home_page_view(request):
    return render(request, 'pages/home.html')


def test_page(request):
    return render(request, 'pages/test-page.html')