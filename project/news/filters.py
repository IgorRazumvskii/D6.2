from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):

   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'author': ['icontains'],
           'rate_of_post': ['gt'],
       }