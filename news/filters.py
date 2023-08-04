from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'author': ['exact'],
           'rate_of_post': ['gte'],
           'header': ['contains'],
           'date_and_time': ['date__gt']
       }