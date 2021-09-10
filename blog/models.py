from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html

from account.models import User
from extensions.utils import jalali_converter


class PublishedManager(models.Manager):
	"""A manager that return all active objects."""		
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset() \
											.filter(published_status='p')


class Category(models.Model):
	title = models.CharField(max_length = 150, verbose_name = "عنوان دسته‌بندی")

	class Meta:
		verbose_name = "دسته‌بندی"
		verbose_name_plural = "دسته‌بندی‌ها"

	def __str__(self):
		return self.title


class Article(models.Model):
	PUBLISH_STATUS_CHOICES = (
		('p', 'منتشر شده'),
		('d', 'پیش‌نویس'),
		('c', 'در حال بررسی'),
		('b', 'برگشت داده شده'),
	)
	author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, 
							   related_name="articles", verbose_name="نویسنده")
	title = models.CharField(max_length=150, verbose_name="عنوان مقاله")
	description = models.TextField(verbose_name="محتوا")
	image = models.ImageField(upload_to = "articles/images/%Y/%m/%d/", 
							  verbose_name="تصویر")
	categories = models.ManyToManyField(Category, verbose_name = "دسته‌بندی", 
										related_name = "articles")
	published_status = models.CharField(max_length=1, 
										choices=PUBLISH_STATUS_CHOICES, 
										verbose_name="وضعیت انتشار")
	publish = models.DateTimeField(default=timezone.now, 
								   verbose_name="زمان انتشار")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	update_guide = models.TextField(verbose_name='راهنمای به‌روزرسانی', 
									null=True, blank=True)

	objects = models.Manager()
	published = PublishedManager()

	class Meta:
		verbose_name = "مقاله"
		verbose_name_plural = "مقالات"
		ordering = ['-publish']

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		"""
		Set update_guide field to None if published status is not back.
		And resize article image.
		"""			
		if self.published_status != 'b':
			self.update_guide = None
		super(Article, self).save(*args, **kwargs)
		
		# Resize article image
		from PIL import Image
		image = Image.open(self.image.path)
		image = image.resize((730, 396))
		image.save(self.image.path)

	def jpublish(self):
		"""return the publish in jalali date."""
		return jalali_converter(self.publish)
	jpublish.short_description = "زمان انتشار"

	img_tag = "<img width=120 height=75 style='border-radius: 5px;' src='{}'>"
	def image_tag(self):
		"""
		return an HTML tag to show article image in django admin panel.
		"""
		return format_html(self.img_tag.format(self.image.url))
	image_tag.short_description = "تصویر"

	def link_tag(self):
		"""
		return an HTML tag to show the link of articles in django admin panel.
		"""
		if self.published_status == 'p':
			href_tag = '<a href="{}">نمایش</a>'
			return format_html(
				href_tag.format(reverse('blog:article_detail', 
								   kwargs={'article_id':self.id}))
			)
		else:
			href_tag = '<a href="{}">پیش‌نمایش</a>'
			return format_html(
				href_tag.format(reverse('account:article_preview', 
								   kwargs={'article_id':self.id}))
			)
	link_tag.short_description = "مشاهده مقاله"
