import os

from . import local_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'account.apps.AccountConfig',
	'real_estate.apps.RealEstateConfig',
	'site_setting.apps.SiteSettingConfig',
	'blog.apps.BlogConfig',
	'contact_us.apps.ContactUsConfig',
	'subscription.apps.SubscriptionConfig',

	# third party
	'crispy_forms',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'homeo.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'homeo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': local_settings.db_name,
		'USER': local_settings.db_user,
		'PASSWORD': local_settings.db_password,
		'HOST': local_settings.db_host,
		'OPTIONS': {
			'sql_mode': 'traditional',
		}
	}
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'account.User'

LANGUAGE_CODE = 'fa'

CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = "site_setting:home"
LOGOUT_REDIRECT_URL = "account:login"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = local_settings.EMAIL_HOST
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = local_settings.EMAIL_PORT
EMAIL_USE_TLS = True
