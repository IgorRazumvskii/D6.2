from rest_framework import serializers
from .models import Post, Category

#  Serializer, ModelSerializer, ListSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        #  fields = "__all__"
        fields = ['header']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #  fields = "__all__"
        fields = ['header']

