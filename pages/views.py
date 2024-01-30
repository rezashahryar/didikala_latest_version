from django.shortcuts import render, redirect
from .forms import NewsLetterForm
from products.models import ProductCategory, Product, Brand
from django.core.paginator import Paginator


# Create your views here.


def home_page_view(request):
    categories = ProductCategory.objects.prefetch_related('children').all()
    product_discounts = Product.objects.select_related('category').filter(discount__isnull=False, discount__gt=0)
    products_most_sales = Product.objects.select_related('category').filter(available=True).order_by('-sales_number')[
                          :8]
    products_most_visited = Product.objects.select_related('category').filter(available=True).order_by(
        '-counted_views')[:8]
    cheapest_product = Product.objects.select_related('category').filter(available=True).order_by('price')[:8]
    context = {
        'categories': categories,
        'product_discount': product_discounts,
        'products_most_sales': products_most_sales,
        'products_most_visited': products_most_visited,
        'cheapest_product': cheapest_product,
    }
    return render(request, 'pages/home.html', context)


def get_products_discount(request):
    products_discount = Product.list.filter(discount__isnull=False).select_related('category')
    paginator = Paginator(products_discount, 12)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    context = {
        'products': products
    }
    return render(request, 'pages/products_discount.html', context)


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


def welcome_page(request):
    return render(request, 'pages/welcome.html')


def search(request):
    query = request.GET.get('query')
    if product := Product.objects.filter(title__icontains=query):
        context = {
            'products': product,
            'query': query,
        }
        return render(request, 'pages/search_product.html', context)
    return redirect('pages:404_page')