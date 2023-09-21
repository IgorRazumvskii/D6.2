from .models import Post, User, BaseRegisterForm, Category
from .filters import PostFilter
from .forms import PostForm, LetterForm
from news.tasks import *

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMessage, mail_managers
from django.http import HttpResponse

from rest_framework.generics import ListAPIView
from .serializers import PostSerializer, CategorySerializer

from django.utils.translation import gettext as _
from django.utils import timezone

import pytz


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Index(View):

    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


# Вывод новостей
class PostList(ListView):
    model = Post
    ordering = '-date_and_time'
    template_name = 'news.html'
    context_object_name = 'news'
    # paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Post.objects.all().select_related('author')


# Вывод по категориям
class CategoryList(ListView):
    model = Post
    ordering = '-date_and_time'
    template_name = 'category.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['pk' ])


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'index.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostOrAricleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    article_or_news_at = None
    login_url = reverse_lazy('login')

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


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(article_or_news='NE')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    template_name = 'news_update.html'
    success_url = reverse_lazy('post_list')
    fields = ['header', 'text']

    def get_queryset(self):
        return Post.objects.filter(article_or_news='NE')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(article_or_news='AR')


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    template_name = 'news_update.html'
    success_url = reverse_lazy('post_list')
    fields = ['header', 'text']

    def get_queryset(self):
        return Post.objects.filter(article_or_news='AR')


def sign_in(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')

    else:
        form = UserCreationForm()
    return render(request, 'registration.html', context={'form': form})


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')

    else:
        form = AuthenticationForm()
    return render(request, 'auth.html', context={'form': form})


def log_out(request):
    logout(request)
    return redirect('login')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('post_list')


def submit(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    category.subscribers.add(user)
    category.save()
    return render(request, 'submit.html')


