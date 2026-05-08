from PIL import Image
from django import forms
from .models import Product
from .forms_mixin import StyleFormMixin


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def clean_name(self):
        """Валидация названия продукта на наличие запрещённых слов"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(f'Название не может содержать слово "{word}".')
        return name

    def clean_description(self):
        """Валидация описания на наличие запрещённых слов"""
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise forms.ValidationError(f'Описание не может содержать слово "{word}".')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверка размера (не более 5 МБ = 5 * 1024 * 1024 байт)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Размер изображения не должен превышать 5 МБ.')

            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('Допустимые форматы: JPEG, PNG.')

            # Дополнительная проверка через Pillow (надёжнее)
            try:
                with Image.open(image) as img:
                    if img.format not in ['JPEG', 'PNG']:
                        raise forms.ValidationError('Файл должен быть изображением в формате JPEG или PNG.')
            except Exception:
                raise forms.ValidationError('Некорректный файл изображения.')

        return image

