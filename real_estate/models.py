from django.db import models
from django.urls import reverse

from account.models import User
from extensions.utils import jalali_converter
from django.utils.html import format_html


class PublishedManager(models.Manager):
	"""A manager that return all active objects."""
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset() \
											.filter(published_status='p')								


class City(models.Model):
	name = models.CharField(verbose_name='نام شهر', max_length=50, unique=True)

	class Meta:
		verbose_name = "شهر"
		verbose_name_plural = "شهرها"

	def __str__(self):
		return self.name


class Estate(models.Model):
	STATUS_CHOICES = (
		('s', 'فروش'),
		('r', 'اجاره'),
	)
	PUBLISH_STATUS_CHOICES = (
		('p', 'منتشر شده'),
		('d', 'پیش‌نویس'),
		('c', 'در حال بررسی'),
		('b', 'برگشت داده شده'),
	)
	main_image = models.ImageField(upload_to="estates/images/%Y/%m/%d/", 
								   verbose_name="تصویر اصلی")
	agent = models.ForeignKey(to=User, on_delete=models.CASCADE, 
							  related_name='estates', verbose_name='نماینده')
	city = models.ForeignKey(to=City, on_delete=models.CASCADE, 
							 related_name='estates', verbose_name='شهر')
	title = models.CharField(max_length=120, verbose_name='عنوان')
	description = models.TextField(verbose_name = "توضیحات")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, 
							  verbose_name='نوع ملک')
	size = models.PositiveIntegerField(verbose_name='متراژ')
	price = models.PositiveIntegerField(verbose_name='قیمت')
	monthly_rent = models.PositiveIntegerField(null=True, blank=True, 
											   verbose_name='اجاره ماهانه')
	room = models.PositiveIntegerField(verbose_name='تعداد اتاق‌ها')
	year = models.PositiveIntegerField(verbose_name='سال ساخت')
	floor = models.PositiveIntegerField(verbose_name='طبقه')
	elevator = models.BooleanField(verbose_name='آسانسور')
	parking = models.BooleanField(verbose_name='پارکینگ')
	warehouse = models.BooleanField(verbose_name='انباری')

	published_status = models.CharField(max_length=1, 
										choices=PUBLISH_STATUS_CHOICES, 
										default='p', 
										verbose_name='وضعیت انتشار')
	created = models.DateTimeField(auto_now_add=True, 
								   verbose_name='تاریخ ایجاد')
	updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
	update_guide = models.TextField(verbose_name='راهنمای به‌روزرسانی', 
									null=True, blank=True)

	objects = models.Manager()
	published = PublishedManager()

	class Meta:
		ordering = ('-created',)
		verbose_name = "ملک"
		verbose_name_plural = "املاک"

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		# Set the monthly_rent to None if estate is for sale.
		if self.status == 's' and self.monthly_rent:
			self.monthly_rent = None
		# Set the monthly_rent to 0 if estate is for rent but no value provided
		# for monthly_rent.
		if self.status == 'r' and not self.monthly_rent:
			self.monthly_rent = 0

		# Set update_guide field to None if published status is not back.
		if self.published_status != 'b':
			self.update_guide = None

		super(Estate, self).save(*args, **kwargs)

		# Resize article image
		from PIL import Image
		main_image = Image.open(self.main_image.path)
		main_image = main_image.resize((850, 550))
		main_image.save(self.main_image.path)

	def jcreated(self):
		"""return the created in jalali date."""	
		return jalali_converter(self.created)
	jcreated.short_description = "تاریخ ایجاد"	    

	def jupdated(self):
		"""return the updated in jalali date."""	
		return jalali_converter(self.updated)
	jupdated.short_description = "تاریخ ویرایش"

	def link_tag(self):
		"""
		return an HTML tag to show the link of estates in django admin panel.
		"""			
		if self.published_status == 'p':
			return format_html(
				'<a href="{}">نمایش</a>'.format(
					reverse('real_estate:estate_detail', 
							kwargs={'estate_id':self.id})
				)
			)
		else:
			return format_html(
				'<a href="{}">پیش‌نمایش</a>'.format(
					reverse('account:estate_preview', 
							kwargs={'estate_id':self.id})
				)
			)
	link_tag.short_description = "مشاهده ملک"


class EstateImage(models.Model):
	estate = models.ForeignKey(to=Estate, on_delete=models.CASCADE, 
							   related_name='images', verbose_name='ملک')
	image = models.ImageField(upload_to="estates/images/%Y/%m/%d/", 
							  verbose_name="تصویر")
	created = models.DateTimeField(auto_now_add=True, 
								   verbose_name='تاریخ ایجاد')
	updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

	def __str__(self):
		return self.estate.title
