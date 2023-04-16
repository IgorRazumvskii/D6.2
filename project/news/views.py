from django.views.generic import ListView, DetailView
from .models import Post
#  from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-date_and_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1

'''    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
'''


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
