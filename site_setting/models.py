from django.db import models
from django.db.models.fields import BooleanField
from django.utils.html import format_html

from extensions.utils import jalali_converter


class SiteSetting(models.Model):
	name = models.CharField(max_length=30, verbose_name='نام سایت')
	main_logo = models.ImageField(upload_to='site_setting/images/%Y/%m/%d/', 
									   verbose_name='لوگو اصلی')
	second_logo = models.ImageField(upload_to='site_setting/images/%Y/%m/%d/', 
							 verbose_name='لوگو دوم')
	background_image = models.ImageField(
		upload_to='images/site_setting', verbose_name='تصویر بکگراند صفحه اصلی'
	)
	home_page_text = models.CharField(max_length=200, 
									  verbose_name='متن صفحه اصلی سایت')
	home_page_second_text = models.CharField(
		max_length=200, verbose_name='متن دوم صفحه اصلی سایت'
	)
	not_found_image = models.ImageField(
		upload_to='site_setting/images/%Y/%m/%d/', 
		verbose_name='تصویر صفحه 404'
	)
	about_us_image = models.ImageField(
		upload_to='site_setting/images/%Y/%m/%d/', 
		verbose_name='تصویر صفحه درباره ما'
	)
	about_us = models.TextField(verbose_name='درباره ما')
	short_about_us = models.CharField(max_length=300, 
									  verbose_name='خلاصه درباره ما')
	address = models.CharField(max_length=300, verbose_name='آدرس')
	email = models.EmailField(verbose_name='ایمیل')
	phone = models.CharField(max_length=11, verbose_name='تلفن تماس')
	facebook = models.URLField(blank=True, null=True, verbose_name="فیسبوک")
	twitter = models.URLField(blank=True, null=True, verbose_name="توییتر")
	linkedin = models.URLField(blank=True, null=True, verbose_name="لینکداین")
	instagram = models.URLField(blank=True, null=True, 
								verbose_name="اینستاگرام")
	telegram = models.URLField(blank=True, null=True, verbose_name="تلگرام")
	youtube = models.URLField(blank=True, null=True, verbose_name="یوتوب")

	is_active = BooleanField(verbose_name='فعال')
	created = models.DateTimeField(auto_now_add=True, 
								   verbose_name='تاریخ ایجاد')
	updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش') 	

	class Meta:
		ordering = ('-created',)
		verbose_name = "تنظیمات سایت"
		verbose_name_plural = "تنظیمات سایت"

	def save(self, *args, **kwargs):
		active_objects = SiteSetting.objects.filter(is_active=True)

		# Active this object if others are not active.
		# (Site needs at least one active setting)
		if not active_objects:
			self.is_active = True
		
		# deactivate other objects if the current object is active.
		if active_objects and self.is_active == True:
			for object in active_objects:
				if object == self:
					continue
				object.is_active = False
				object.save()
		if active_objects and active_objects[0] == self:
			self.is_active = True
		super(SiteSetting, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	img_tag = "<img width=200 height=100 style='border-radius: 5px;' src='{}'>"
	def second_logo_tag(self):
		"""
		return an HTML tag to show the second_logo in django admin panel.
		"""	
		return format_html(self.img_tag.format(self.second_logo.url))
	second_logo_tag.short_description = "لوگو سایت"

	def background_image_tag(self):
		"""
		return an HTML tag to show the background_image in django admin panel.
		"""			
		return format_html(self.img_tag.format(self.background_image.url))
	background_image_tag.short_description = "تصویر بکگراند صفحه اصلی سایت"

	def about_us_image_tag(self):
		"""
		return an HTML tag to show the about_us_image in django admin panel.
		"""			
		return format_html(self.img_tag.format(self.about_us_image.url))
	about_us_image_tag.short_description = "تصویر درباره ما"

	def not_found_image_tag(self):
		"""
		return an HTML tag to show the not_found_image in django admin panel.
		"""				
		return format_html(self.img_tag.format(self.not_found_image.url))
	not_found_image_tag.short_description = "تصویر صفحه 404"


class Faq(models.Model):
	title = models.CharField(max_length=250, verbose_name='عنوان')
	description = models.TextField(verbose_name='توضیحات')
	created = models.DateTimeField(auto_now_add=True, 
								   verbose_name='تاریخ ایجاد')
	updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')    

	class Meta:
		ordering = ('-created',)
		verbose_name = "سوال"
		verbose_name_plural = "سوالات متداول"

	def __str__(self):
		return self.title

	def jcreated(self):
		"""return the created in jalali date."""
		return jalali_converter(self.created)
	jcreated.short_description = "تاریخ ایجاد"

	def jupdated(self):
		"""return the updated in jalali date."""		
		return jalali_converter(self.updated)
	jupdated.short_description = "تاریخ ویرایش"
