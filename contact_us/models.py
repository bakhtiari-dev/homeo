from django.db import models

from extensions.utils import jalali_converter


class ContactUs(models.Model):
	name = models.CharField(verbose_name='نام پیام دهنده', max_length=100)
	email = models.EmailField(verbose_name='ایمیل')
	phone = models.CharField(verbose_name='تلفن', max_length=15)
	subject = models.CharField(verbose_name='موضوع پیام', max_length=250)
	message = models.TextField(verbose_name='متن پیام')
	reviewed = models.BooleanField(verbose_name='بررسی شده', default=False)
	created = models.DateTimeField(auto_now_add=True, 
								   verbose_name='تاریخ ایجاد')

	class Meta:
		verbose_name = 'پیام‌ دریافت شده'
		verbose_name_plural = 'پیام‌‌های دریافت شده'
		ordering = ['-created']

	def __str__(self):
		return self.name

	def jcreated(self):
		"""return the created in jalali date."""			
		return jalali_converter(self.created)
	jcreated.short_description = "تاریخ ایجاد"
