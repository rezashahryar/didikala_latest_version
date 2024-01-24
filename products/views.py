from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .models import ProductCategory, SubProductCategory, Product, Brand, Color, Question, SetProductProperty
from .forms import QuestionForm
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
# Create your views here.


@require_POST
def question(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.product = product
            new_form.save()
            return redirect('products:product_detail', product.slug)


@require_POST
def answer(request, pk, qpk):
    product = get_object_or_404(Product, pk=pk)
    question_id = get_object_or_404(Question, pk=qpk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.product = product
            new_form.parent = question_id
            new_form.save()
            return redirect('products:product_detail', product.slug)


class CategoryObjectsView(generic.ListView):
    context_object_name = 'products'
    template_name = 'products/product_list.html'
    paginate_by = 12

    def get_queryset(self):
        global cat
        slug = self.kwargs.get('slug')
        cat = get_object_or_404(ProductCategory, slug=slug)
        return cat.products.filter(available=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['most_visited_products'] = Product.objects.select_related('category').filter(available=True, category=cat).order_by('-counted_views')
        context['latest_products'] = Product.objects.select_related('category').filter(available=True, category=cat).order_by('-created_date')
        context['cheapest_products'] = Product.objects.select_related('category').filter(available=True, category=cat).order_by('price')
        context['most_expensive_products'] = Product.objects.select_related('category').filter(available=True, category=cat).order_by('-price')
        context['categories'] = ProductCategory.objects.all()
        context['brands'] = Brand.objects.all()
        context['colors'] = Color.objects.all()
        return context


class SubCategoryObjectsView(generic.ListView):
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        sub_cat = get_object_or_404(SubProductCategory, slug=slug)
        return sub_cat.products.filter(available=True)


class ProductDetail(generic.DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        slug = self.kwargs.get('slug')
        queryset = Product.objects.prefetch_related('questions__user').prefetch_related('property').select_related('category')
        product = get_object_or_404(queryset, slug=slug)
        product.counted_views += 1
        product.save()
        return product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['questions'] = Product.objects.prefetch_related('questions__parent')
        return context


def product_filter(request):
    products = None
    product_name = request.GET.get('product_name')
    if product_name:
        products = Product.objects.filter(title__icontains=product_name)
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category__title=category)
    brand = request.GET.get('brand')
    if brand:
        products = Product.objects.filter(brand__title=brand)
    color = request.GET.get('color')
    if color:
        products = Product.objects.filter(color__title=color)
    available = request.GET.get('available')
    if available == 'true':
        products = Product.objects.filter(available=True)
    min_price = request.GET.get('min_price')
    if min_price:
        products = Product.objects.filter(price__gte=min_price)
    max_price = request.GET.get('max_price')
    if max_price:
        products = Product.objects.filter(price__lte=max_price)
    if min_price and max_price:
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    if min_price and max_price and available:
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price, available=True)
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)