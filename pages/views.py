from django.shortcuts import render, redirect
from .forms import NewsLetterForm
from .models import NewsLetter
# Create your views here.


def home_page_view(request):
    return render(request, 'pages/home.html')


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages:home_page_view')


def test_page(request):
    return render(request, 'pages/test-page.html')