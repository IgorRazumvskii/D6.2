from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from django.core.validators import MinValueValidator
from django.urls import reverse

CHOICES = [
    ("AR", 'article'),
    ("NE", 'news'),
]


class Author(models.Model):
    rate = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

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

    def __str__(self):
        return self.name_of_category


class Post(models.Model):
    article_or_news = models.CharField(max_length=2, choices=CHOICES)
    date_and_time = models.DateTimeField(auto_now=True)
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

