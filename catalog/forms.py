from django import forms
from .models import Product


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control-file'})

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

