from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views=models.IntegerField(default=0)
    likes=models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
class ProfilUser(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='profil_img' , blank=True)
	website = models.URLField(blank=True)
	
	def __unicode__(self):
		return self.user.username

