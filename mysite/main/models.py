from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from django.db.models import Sum

# Create your models here.
class Product(models.Model):
	product_name = models.CharField(max_length=150)
	product_type = models.CharField(max_length=25)
	product_description = models.TextField()
	affiliate_url = models.SlugField(blank=True, null=True)
	product_image = models.ImageField(upload_to='images/')
	comfort_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	performance_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	durability_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)

	def __str__(self):
		return self.product_name


class Tag(models.Model):
	tag_name = models.CharField(max_length=15)
	tag_slug = models.SlugField()
    
	def __str__(self):
		return self.tag_name


class Article(models.Model):
	article_title = models.CharField (max_length=200)
	article_published = models.DateTimeField('date published')
	article_image = models.ImageField(upload_to='images/')
	article_tags = models.ManyToManyField(Tag)   #add this
	article_content = HTMLField()
	article_slug = models.SlugField()

	def __str__(self):
		return self.article_title


class Profile(models.Model):   
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product)

	@receiver(post_save, sender=User) #add this
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User) #add this
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
        

	def __str__(self):
		return self.user.username

class Vote(models.Model):   #add this class and the following fields
	profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	comfort = models.IntegerField(default=0)
	performance = models.IntegerField(default=0)
	durability = models.IntegerField(default=0)

	def calculate_averages(self):
			product = self.product
			vote_qs = Vote.objects.filter(product=product)
			vote_count = vote_qs.count()
			comfort_total = vote_qs.aggregate(Sum('comfort'))
			performance_total = vote_qs.aggregate(Sum('performance'))
			durability_total = vote_qs.aggregate(Sum('durability'))
			product.comfort_average = comfort_total['comfort__sum']/vote_count
			product.performance_average = performance_total['performance__sum']/vote_count
			product.durability_average = durability_total['durability__sum']/vote_count
			product.save()