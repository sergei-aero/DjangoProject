from .models import Product

def get_products_by_category(category_id):
    """Возвращает QuerySet продуктов для указанной категории"""
    return Product.objects.filter(category_id=category_id, is_published=True)