from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Sum

from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django import forms

from allauth.account.forms import SignupForm

from django.utils import timezone

from django.dispatch import receiver

CHOICES = [
    ("AR", 'article'),
    ("NE", 'news'),
]


class Author(models.Model):
    rate = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    #  ToDo: fix
    def update_rating(self):
        rating_of_post_by_author = Post.objects.filter(author=self).aggregate(Sum('rate_of_post')).get('rate_of_post__sum')*3
        print(rating_of_post_by_author)
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rate_of_comment')).get('rate_of_comment__sum', 0)
        print(rating_of_comments_by_author)
        rating_of_comment_by_post = Comment.objects.filter(post__in=Post.objects.filter(author=self)).aggregate(Sum('rate_of_comment')).get('rate_of_comment__sum', 0)
        print(rating_of_comment_by_post)
        #rating_of_comment_by_post = Comment.objects.filter(post=Post.objects.filter(author=self)).aggregate(Sum('rate_of_comment')).get('rate_of_comment__sum')
        self.rate = rating_of_post_by_author + rating_of_comments_by_author + rating_of_comment_by_post
        self.save()


class Category(models.Model):
    name_of_category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='get_subscribers', blank=True)

    def __str__(self):
        return self.name_of_category


class Post(models.Model):
    article_or_news = models.CharField(max_length=2, choices=CHOICES)
    date_and_time = models.DateTimeField(default=timezone.now)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rate_of_post = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory', related_name='get_posts')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        self.rate_of_post += 1
        self.save()

    def dislike(self):
        self.rate_of_post -= 1
        self.save()

    def preview(self):
        return self.text[:124:]+"..."

    def __str__(self):
        return f'{self.header.title()}:{self.text.title()}:{self.date_and_time}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} : {self.post.header}'


class Comment(models.Model):
    text = models.TextField()
    date_and_time = models.DateTimeField(auto_now_add=True)
    rate_of_comment = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate_of_comment += 1
        self.save()

    def dislike(self):
        self.rate_of_comment -= 1
        self.save()


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


#  Help
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


def send_m(sender, instance, created, **kwargs):
    send_mail(
        f'{instance.header} was created',
        f'{instance.author} is an author',
        'razumovskijigor6@gmail.com',
        ['bogomolovog@email.ru', ]
        )


post_save.connect(receiver=send_m, sender=Post)
