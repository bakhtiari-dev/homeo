from django.db import models

from account.models import User
from extensions.utils import jalali_converter


class Plan(models.Model):
	name = models.CharField(max_length=50, verbose_name='نام طرح')
	estate_count = models.PositiveIntegerField(verbose_name='تعداد ملک')
	day_count = models.PositiveIntegerField(verbose_name='تعداد روز')
	price = models.PositiveIntegerField(verbose_name='قیمت')

	class Meta:
		verbose_name = "طرح"
		verbose_name_plural = "طرح‌ها"

	def __str__(self):
		return self.name


class Subscription(models.Model):
	active = models.BooleanField(default=True, verbose_name='وضعیت')
	agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
							  blank=True, related_name='subscriptions', 
							  verbose_name='نماینده')
	name = models.CharField(max_length=50, verbose_name='نام طرح خریداری شده')
	price = models.PositiveIntegerField(verbose_name='قیمت')
	created = models.DateTimeField(auto_now_add=True, 
								   verbose_name='تاریخ خرید')
	day_count = models.PositiveIntegerField(verbose_name='تعداد روز')
	estate_count = models.PositiveIntegerField(verbose_name='تعداد ملک')
	created_estates = models.PositiveIntegerField(
		default=0, verbose_name='تعداد ملک ثبت شده'
	)
	expiration_date = models.DateTimeField(verbose_name='تاریخ انقضا')
	

	class Meta:
		ordering = ('-created',)
		verbose_name = "اشتراک"
		verbose_name_plural = "اشتراک‌ها"
		
	def __str__(self):
		return f"{self.agent} - {self.name}"

	def jcreated(self):
		"""return the created in jalali date."""
		return jalali_converter(self.created, detail=True)
	jcreated.short_description = "تاریخ خرید"	        

	def jexpiration_date(self):
		"""return the expiration_date in jalali date."""
		return jalali_converter(self.expiration_date, detail=True)
	jexpiration_date.short_description = "تاریخ انقضا"	

	def is_active(self):
		"""
		Check the subscription and return True if it is active else return 
		False and deactivate the subscription.
		"""
		from datetime import datetime
		if not self.active or self.created_estates == self.estate_count \
			or datetime.now() > self.expiration_date.replace(tzinfo=None):
			self.active = False
			self.save()
			return False
		return True
		