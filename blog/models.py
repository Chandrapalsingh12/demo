from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.IntegerField(primary_key = True)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000)    
    author = models.CharField(max_length=50)  
    slug = models.CharField(max_length=130)  
    views = models.IntegerField(default=0)
    timestamp = models.DateField(blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author

class BlogComment(models.Model):
    sno = models.IntegerField(primary_key = True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timestamp = models.DateField(default=now)

    def __str__(self):
        return self.comment[0:13] + "---" + "by " + self.user.username
    