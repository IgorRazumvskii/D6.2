from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = '-date_and_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2


class PostDetail(DetailView):  # HELP!
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostOrAricleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    article_or_news_at = None

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = self.article_or_news_at
        return super().form_valid(form)


class PostCreate(PostOrAricleCreate, CreateView):
    article_or_news_at = 'NE'


class ArticleCreate(PostOrAricleCreate, CreateView):
    article_or_news_at = 'AR'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


'''class PostDelete(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_queryset(self):
        print(self.kwargs['pk'])
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.delete()
        return Post.objects.all()
'''


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(article_or_news='NE')


class PostUpdate(UpdateView):
    model = Post
    template_name = 'news_update.html'
    success_url = reverse_lazy('post_list')
    fields = ['header', 'text']

    def get_queryset(self):
        return Post.objects.filter(article_or_news='NE')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(article_or_news='AR')


class ArticleUpdate(UpdateView):
    model = Post
    template_name = 'news_update.html'
    success_url = reverse_lazy('post_list')
    fields = ['header', 'text']

    def get_queryset(self):
        return Post.objects.filter(article_or_news='AR')