# artworks/filters.py
import django_filters
from django import forms
from django.db.models import Q
from .models import Artwork, Category, Theme, Collection


class ArtworkFilter(django_filters.FilterSet):
    # Статус (чекбоксы)
    status = django_filters.MultipleChoiceFilter(
        choices=Artwork.STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Статус",
        field_name='status'
    )
    
    # Категория (чекбоксы)
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Категория",
        field_name='category'
    )
    
    # Тематика (чекбоксы)
    theme = django_filters.ModelMultipleChoiceFilter(
        queryset=Theme.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Тематика",
        field_name='theme'
    )
        
    # Размер (чекбоксы)
    size = django_filters.MultipleChoiceFilter(
        choices=Artwork.SIZE_CHOICES,
        method='filter_by_size',
        widget=forms.CheckboxSelectMultiple,
        label="Размер"
    )
    
    # Цена (диапазон)
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label="Цена от",
        widget=forms.NumberInput(attrs={'placeholder': 'От'})
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label="Цена до",
        widget=forms.NumberInput(attrs={'placeholder': 'До'})
    )
    
    class Meta:
        model = Artwork
        fields = ['status', 'category', 'theme', 'collection', 'size']
    
    def filter_by_size(self, queryset, name, value):
        if not value:
            return queryset

        small_q = Q(width_cm__lte=25, height_cm__lte=25)
        medium_q = (
            (Q(width_cm__lte=40, height_cm__lte=60) | Q(width_cm__lte=60, height_cm__lte=40)) &
            ~small_q
        )
        large_q = ~(small_q | medium_q)

        final_q = Q()

        if 'small' in value:
            final_q |= small_q
        if 'medium' in value:
            final_q |= medium_q
        if 'large' in value:
            final_q |= large_q

        return queryset.filter(final_q)