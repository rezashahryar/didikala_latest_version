from django.shortcuts import render, redirect
from .forms import NewsLetterForm
from products.models import ProductCategory


# Create your views here.


def home_page_view(request):
    categories = ProductCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'pages/home.html', context)


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages:home_page_view')


def test_page(request):
    return render(request, 'pages/test-page.html')


# custom 404 view
def custom_404(request, exception):
    return render(request, 'pages/404_page.html', status=404)


def page_faq_view(request):
    return render(request, 'pages/page_faq.html')


def page_faq_category(request):
    return render(request, 'pages/page_faq_category.html')


def page_faq_question(request):
    return render(request, 'pages/page_faq_question.html')


def page_privacy(request):
    return render(request, 'pages/page_privacy.html')
