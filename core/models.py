from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phone_field import PhoneField
from PIL import Image


# Create your models here.

class Section(models.Model):
    topic = models.CharField(max_length=255)

    def __str__(self):
        return self.topic


class Authors(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    mail_address = models.EmailField(max_length=255, unique=True, blank=True)
    tel_num = PhoneField(null=False, blank=True, unique=True)
    birth_day = models.DateField(blank=True)
    portrait = models.ImageField(upload_to="authors_images/", null=True, blank=True)
    inf_about = models.TextField(max_length=2550, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class News(models.Model):
    title = models.CharField(max_length=255, blank=True)
    topic = models.ManyToManyField(Section)
    summary = models.TextField(max_length=25500, blank=True)
    picture = models.ImageField(upload_to="news_images/", null=True, blank=True)
    auth_opinion = models.TextField(max_length=2550, null=True)
    authors = models.ForeignKey('Authors', on_delete=models.SET_NULL, null=True)
    source = models.URLField(null=True)
    d_created = models.DateTimeField(blank=True, auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.title, self.authors)


class Post(models.Model):
    title = models.CharField(max_length=255)
    topic = models.ManyToManyField(Section)
    caption = models.TextField(max_length=25500, blank=True)
    image = models.ImageField(upload_to="post_images/")
    likes = models.ManyToManyField(User, blank=True)
    date_posted = models.DateTimeField(blank=True, auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username}\'s Post- {self.title}'

    def like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            # output_size = (300, 300)
            # img.thumbnail(output_size)
            im = img.resize((400, 400))
            im.save(self.image.path)
        elif img.height < 400 or img.width < 400:
            im = img.resize((400, 400))
            im.save(self.image.path)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default="de_fault.png", upload_to="profiles")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Комментарий к посту {} от пользователя {}'.format(self.post.title, self.user.username)


#
#        # resize the image
#        img = Image.open(self.avatar.path)
#        if img.height > 300 or img.width > 300:
#            output_size = (300, 300)
#            # create a thumbnail
#            img.thumbnail(output_size)
#            # overwrite the larger image
#            img.save(self.avatar.path)
