import django_filters
from .models import Announcement, PropertyCategory, RATING_CHOISES,DAY_CHOICES ,ChildrenAge
from django.utils.translation import gettext_lazy as _


class AnnouncementFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city__title',label='City', lookup_expr='icontains')
    property_categories = django_filters.ModelMultipleChoiceFilter(
        field_name = 'property_category__id',
        to_field_name = 'id',
        queryset=PropertyCategory.objects.all(),
    )
    ratings = django_filters.MultipleChoiceFilter(
        field_name = 'rating',
        choices = RATING_CHOISES
    )
    children_ages = django_filters.ModelMultipleChoiceFilter(
        field_name = 'children_ages__id',
        to_field_name = 'id',
        queryset=ChildrenAge.objects.all(),
    )
    preferred_nights = django_filters.MultipleChoiceFilter(
        field_name = 'preferred_nights',
        choices = DAY_CHOICES
    )
    
    ordering = django_filters.OrderingFilter(
        choices=(
            ('distance_from_center', _('Distance from city center')),
            ('-rating', _('Rating')),
            ('rating', _('Rating descending')),
            ('-whole_house_or_apartment', _('First houses or apartments')),
        ),
        empty_label='Default',
    )

    class Meta:
        model = Announcement
        fields = ['ratings','whole_house_or_apartment','for_travel','room_count','preferred_nights', 'property_categories', 'city',]
