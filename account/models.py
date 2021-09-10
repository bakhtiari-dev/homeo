from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.html import format_html

from extensions.utils import jalali_converter


class CustomUserManager(BaseUserManager):
	"""
	A custom user manager to authenticate users by email instead of username.
	"""
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The Email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self.create_user(email, password, **extra_fields)


class ActiveManager(models.Manager):
	"""A manager that return all active objects."""	
	def get_queryset(self):
		return super(ActiveManager, self).get_queryset() \
											.filter(is_active=True)


class User(AbstractUser):
	first_name = models.CharField(max_length=150, verbose_name='نام')
	image = models.ImageField(upload_to="users/images/%Y/%m/%d/", verbose_name="تصویر")
	phone = models.CharField(max_length=11, verbose_name='تلفن')
	email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
	description = models.TextField(
		blank=True, null=True, verbose_name="توضیحات"
	)
	website = models.URLField(
		blank=True, null=True, verbose_name="آدرس وب سایت"
	)
	facebook = models.URLField(
		blank=True, null=True, verbose_name="آدرس فیسبوک"
	)
	twitter = models.URLField(
		blank=True, null=True, verbose_name="آدرس توییتر"
	)
	linkedin = models.URLField(
		blank=True, null=True, verbose_name="آدرس لینکداین"
	)
	instagram = models.URLField(
		blank=True, null=True, verbose_name="آدرس اینستاگرام"
	)
	telegram = models.URLField(
		blank=True, null=True, verbose_name="آدرس تلگرام"
	)
	youtube = models.URLField(blank=True, null=True, verbose_name="آدرس یوتوب")

	is_email_verified = models.BooleanField(
		default=False, verbose_name='ایمیل تأیید شده'
	)
	email_verify_code = models.CharField(
		blank=True, null=True, max_length=4, verbose_name='کد تأیید ایمیل'
	)
	
	__original_email = None

	objects = CustomUserManager()
	active = ActiveManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'phone', 'image']
	
	username = None
	last_name = None
	
	AbstractUser.first_name.short_description = "نام"

	class Meta:
		ordering = ('-date_joined',)
		verbose_name = "نماینده"
		verbose_name_plural = "نمایندگان"		

	def __init__(self, *args, **kwargs):
		"""
		Set a __original_email variable to store the email of user and track 
		changes.
		"""
		super(User, self).__init__(*args, **kwargs)
		self.__original_email = self.email

	def __str__(self):
		return self.first_name

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		"""
		Change email verification status to False if email has been changed
		and resize the user iamge.
		"""
		if self.email != self.__original_email:
			self.is_email_verified = False
		super(User, self).save(force_insert, force_update, *args, **kwargs)
		self.__original_email = self.email

		# Resize user image
		from PIL import Image
		image = Image.open(self.image.path)
		image = image.resize((420, 420))
		image.save(self.image.path)

	def image_tag(self):
		"""
		return an HTML tag to show user image in django admin panel.
		"""
		return format_html(
			"<img width=100 height=100 style='border-radius: 5px;' src='{}'>" \
			.format(self.image.url)
		)
	image_tag.short_description = "تصویر"

	def jdate_joined(self):
		"""
		return the date_joined in jalali date.
		"""		
		return jalali_converter(self.date_joined)
	jdate_joined.short_description = "تاریخ عضویت"
