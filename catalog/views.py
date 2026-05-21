from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        if user == product.owner:
            return True
        if user.has_perm('catalog.can_unpublish_product'):  # или проверка группы
            return True
        return False

class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 9  # опционально

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        cache_key = f'products_category_{self.category.pk}_published'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = list(get_products_by_category(self.category.pk))  # материализуем
            cache.set(cache_key, queryset, 60 * 10)  # 10 минут
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

@require_POST
@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:product_list')