from django.db import models
from django.contrib.auth.models import User
from param import *


class Author(models.Model):
    content_creator = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_content = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_sum_rating = Post.objects.filter(creator=self.content_creator).values("rating")
        comment_sum_rating = Comment.objects.filter(user=self.content_creator).values("rating_content")
        self.content_creator = post_sum_rating * 3 + comment_sum_rating
        self.save()

    def __str__(self):
        return f'{self.content_creator}'


class Category(models.Model):
    paper_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.paper_name}'


class Post(models.Model):
    comment = 'comment'
    content = 'content'
    CATEGORY = [(comment, 'комментарий'), (content, 'статья')]
    creator = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_choice = models.CharField(max_length=7, choices=CATEGORY, default=content)
    creation_time = models.DateTimeField(auto_now=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[0:124] + '...'

    def __str__(self):
        return f'{self.header}, {self.preview()}, {self.creation_time}'


class PostCategory(models.Model):
    post_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_to_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_to_post}, из категории: {self.post_to_category}'


class Comment(models.Model):
    comment_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_time}, {self.comment_text}'
