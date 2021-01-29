import django_filters
from django_filters import DateFilter

from .models import *

class orderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name = "date_created" , lookup_expr= 'gte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']