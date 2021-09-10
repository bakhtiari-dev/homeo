from django.urls import reverse_lazy
from django.conf import settings
from django.http import Http404
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.views.generic import (
	CreateView, TemplateView, UpdateView, DeleteView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, PasswordChangeView, 
	PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
	PasswordResetCompleteView)
from django.shortcuts import redirect, render, get_object_or_404

from .models import User
from .mixins import (ArticleFieldsMixin, ArticleFormValidMixin, 
	ArticleUpdateMixin, ArticleDeleteMixin, CheckSubscriptionMixin, 
	AddCreatedEstatesMixin, EstateFieldsMixin, EstateFormValidMixin, 
	EstateUpdateMixin, EstateDeleteMixin, LogInMixin, UserFieldsMixin, 
	EmailVerifyRedirectMixin, CheckEmailActivationMixin)
from .forms import RegisterForm
from .generate_random_number import generate_random_number
from real_estate.models import Estate, EstateImage, City
from site_setting.models import SiteSetting
from blog.models import Article, Category
from site_setting.models import SiteSetting


class UserList(TemplateView):
	"""
	Retrieve list of active users, paginate them and send to the template.
	This view also handle the search and filters objects by given search key.
	"""
	def get(self, request, *args, **kwargs):
		users = User.active.annotate(estates_count=Count('estates'))

		search = request.GET.get('s', None)
		if search:
			users = users.filter(
				Q(first_name__contains=search) | 
				Q(description__contains=search)
			).distinct()

		# Paginate users
		paginator = Paginator(users, 6)
		page = request.GET.get('page', None)
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			# if page is not an integer deliver the first page
			users = paginator.page(1)
		except EmptyPage:
			# if page is out of range deliver last page of results
			users = paginator.page(paginator.num_pages)	

		# Last 3 published estates
		latest_estates = Estate.published.all()[:3]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
			
		return render(request, 'account/user_list.html',
					{'users': users, 
					'latest_estates': latest_estates, 
					'site_setting': site_setting})


class UserDetail(TemplateView):
	"""Retrieve a user by id and raise a 404 error if not found."""	
	def get(self, request, id, *args, **kwargs):
		user = get_object_or_404(
			User.active.annotate(estates_count=Count('estates')), id=id
		)

		# Last 3 published estates
		latest_estates = Estate.published.all()[:3]

		# Last 2 published estates of user
		user_estates = Estate.published.prefetch_related('city').filter(agent=user)[:2]

		# Last 2 published articles of user
		user_articles = Article.published.filter(author=user)[:2]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

		return render(request, 'account/user_detail.html',
					{'user': user, 
					'latest_estates': latest_estates, 
					'user_estates': user_estates,
					'user_articles': user_articles,
					'site_setting': site_setting})


class ArticleList(LoginRequiredMixin, TemplateView):
	"""
	Retrieve list of user articles and filter objects by given status.
	"""	
	def get(self, request, status=None, *args, **kwargs):
		user = request.user
		articles = user.articles.all()
		if status:
			if status == 'published':
				articles = articles.filter(published_status='p')
			elif status == 'draft':
				articles = articles.filter(published_status='d')
			elif status == 'check':
				articles = articles.filter(published_status='c')
			elif status == 'back':
				articles = articles.filter(published_status='b')

		return render(request, 'account/dashboard/article_list.html',
					{'articles': articles, 'status': status,})


class ArticleCreate(LoginRequiredMixin, CheckEmailActivationMixin, 
					ArticleFormValidMixin, ArticleFieldsMixin, CreateView):
	model = Article
	template_name = "account/dashboard/article_create_update.html"
	success_url = reverse_lazy('account:article_list')


class ArticleUpdate(LoginRequiredMixin, CheckEmailActivationMixin, 
					ArticleUpdateMixin, ArticleFormValidMixin, 
					ArticleFieldsMixin, UpdateView):
	model = Article
	template_name = "account/dashboard/article_create_update.html"
	success_url = reverse_lazy('account:article_list')	


class ArticleDelete(LoginRequiredMixin, CheckEmailActivationMixin, 
					ArticleDeleteMixin, DeleteView):
	model = Article
	template_name = "account/dashboard/confirm_delete.html"
	success_url = reverse_lazy('account:article_list')


class ArticlePreview(LoginRequiredMixin, CheckEmailActivationMixin, 
					 TemplateView):
	"""
	Retrieve an article by id and raise 404 error if not found. Also raise if
	the user is not the author of article or super user.
	"""			
	def get(self, request, article_id, *args, **kwargs):
		article = get_object_or_404(
			Article.objects.filter(published_status__in=['d', 'c', 'b']), 
								   id=article_id)
		if article.author != request.user and not request.user.is_superuser:
			raise Http404

		categories = Category.objects.all()

		latest_estates = Estate.published.all()[:3]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

		return render(request, 'blog/article_detail.html',
					{'article': article,
					'site_setting': site_setting,
					'latest_estates': latest_estates,
					'categories': categories})


class EstateList(LoginRequiredMixin, TemplateView):
	"""
	Retrieve list of user estates and filter objects by given status.
	"""		
	def get(self, request, status=None, *args, **kwargs):
		user = request.user
		estates = user.estates.all()
		if status:
			if status == 'published':
				estates = estates.filter(published_status='p')
			elif status == 'draft':
				estates = estates.filter(published_status='d')
			elif status == 'check':
				estates = estates.filter(published_status='c')
			elif status == 'back':
				estates = estates.filter(published_status='b')

		return render(request, 'account/dashboard/estate_list.html',
					{'estates': estates, 'status': status,})


class EstateCreate(LoginRequiredMixin, CheckEmailActivationMixin, 
				   CheckSubscriptionMixin, EstateFieldsMixin, 
				   EstateFormValidMixin, AddCreatedEstatesMixin, 
				   CreateView):
	model = Estate
	template_name = "account/dashboard/estate_create_update.html"
	success_url = reverse_lazy('account:estate_list')


class EstateUpdate(LoginRequiredMixin, CheckEmailActivationMixin, 
				   EstateUpdateMixin, EstateFormValidMixin, EstateFieldsMixin, 
				   UpdateView):
	model = Estate
	template_name = "account/dashboard/estate_create_update.html"
	success_url = reverse_lazy('account:estate_list')	


class EstateDelete(LoginRequiredMixin, CheckEmailActivationMixin, 
				   EstateDeleteMixin, DeleteView):
	model = Estate
	template_name = "account/dashboard/confirm_delete.html"
	success_url = reverse_lazy('account:estate_list')


class EstatePreview(LoginRequiredMixin, CheckEmailActivationMixin, 
					TemplateView):
	"""
	Retrieve an estate by id and raise 404 error if not found. Also raise if
	the user is not the agent of estate or super user.
	"""	
	def get(self, request, estate_id, *args, **kwargs):
		estate = get_object_or_404(
			Estate.objects.filter(published_status__in=['d', 'c', 'b']), 
								  id=estate_id
		)
		if estate.agent != request.user and not request.user.is_superuser:
			raise Http404

		latest_estates = Estate.published.all().exclude(id=estate.id)[:3]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

		# Get maximum amount of price, size and room to render search form in 
		# template.		
		obj = Estate.published.all()
		if obj:
			max_price = obj.order_by('-price')[0].price
			max_size = obj.order_by('-size')[0].size
			max_room = obj.order_by('-room')[0].room
		else:
			max_price = 1000000
			max_size = 1000
			max_room = 10

		cities = City.objects.all()

		return render(request, 'real_estate/estate_detail.html',
					{'estate': estate, 
					'latest_estates': latest_estates,
					'site_setting': site_setting,
					'max_price':max_price, 
				    'max_size': max_size, 
				    'max_room': max_room,
				    'cities': cities})


class EstateImageDelete(LoginRequiredMixin, CheckEmailActivationMixin, 
						TemplateView):
	"""Get the image of estate by id and delete it."""
	def get(self, request, image_id, *args, **kwargs):
		image = get_object_or_404(EstateImage, id = image_id)
		if image.estate.agent != request.user:
			raise Http404
		image.delete()
		return redirect('account:estate_update', image.estate.id)


class SubscriptionList(LoginRequiredMixin, TemplateView):
	"""Retrieve list of subscriptions of user."""
	def get(self, request, *args, **kwargs):
		user = request.user
		subscriptions = user.subscriptions.all()
		return render(request, 'account/dashboard/subscription_list.html',
					{'subscriptions': subscriptions})


class LogIn(LogInMixin, LoginView):
	template_name = 'account/auth/login.html'
	
	def get_context_data(self, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
		context = super().get_context_data(**kwargs)
		context["site_setting"] = site_setting
		return context


class Register(LogInMixin, CreateView):
	template_name = 'account/auth/register.html'
	form_class = RegisterForm
	success_url = reverse_lazy('account:user_update')

	def get_context_data(self, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
		context = super().get_context_data(**kwargs)
		context["site_setting"] = site_setting
		return context

	def form_valid(self, form):
		# Save the new user first
		form.save()
		# Get the email and password
		email = self.request.POST['email']
		password = self.request.POST['password1']
		# Authenticate user and login
		user = authenticate(email=email, password=password)
		login(self.request, user)
		return redirect('account:user_update')
		

class UserUpdate(LoginRequiredMixin, UserFieldsMixin, UpdateView):
	model = User
	template_name = "account/dashboard/user_update.html"
	success_url = reverse_lazy('account:user_update')	

	def get_object(self):
		obj = self.request.user
		return obj


class PasswordChange(PasswordChangeView):
	template_name = "account/auth/password_change.html"
	success_url = reverse_lazy('account:password_change_done')


class PasswordReset(PasswordResetView):
	template_name ='account/auth/password_reset.html'
	email_template_name ='account/auth/password_reset_email.html'
	subject_template_name ='account/auth/password_reset_subject.txt'	
	success_url = reverse_lazy('account:password_reset_done')

	def get_context_data(self, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
		context = super().get_context_data(**kwargs)
		context["site_setting"] = site_setting
		return context


class PasswordResetDone(PasswordResetDoneView):
	template_name ='account/auth/password_reset.html'

	def get_context_data(self, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
		context = super().get_context_data(**kwargs)
		context["site_setting"] = site_setting
		return context


class PasswordResetConfirm(PasswordResetConfirmView):
	template_name ='account/auth/password_reset_confirm.html'
	success_url = reverse_lazy('account:password_reset_complete')

	def get_context_data(self, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
		context = super().get_context_data(**kwargs)
		context["site_setting"] = site_setting
		return context


class PasswordResetComplete(PasswordResetCompleteView):
	template_name ='account/auth/password_reset_confirm.html'

	def get_context_data(self, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
		context = super().get_context_data(**kwargs)
		context["site_setting"] = site_setting
		return context
		

class EmailAlert(LoginRequiredMixin, EmailVerifyRedirectMixin, TemplateView):
	def get(self, request, *args, **kwargs):
		return render(request, 'account/auth/email_alert.html')


class SendEmailVerifyCode(LoginRequiredMixin, EmailVerifyRedirectMixin, 
						  TemplateView):
	"""Generate a random number as verify code and email it to user."""
	def get(self, request, *args, **kwargs):
		code = generate_random_number()

		user = self.request.user
		user.email_verify_code = code
		user.save()

		subject = 'کد تایید ایمیل'
		message = 'کد تایید ایمیل شما: {}'.format(code)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [self.request.user.email]
		send_mail(subject, message, email_from, recipient_list)		
		return redirect('account:email_verify')


class EmailVerify(LoginRequiredMixin, EmailVerifyRedirectMixin, TemplateView):
	def get(self, request, *args, **kwargs):
		return render(request, 'account/auth/email_verify.html')

	def post(self, request, *args, **kwargs):
		if request.POST['code'] == self.request.user.email_verify_code:
			user = self.request.user
			user.is_email_verified = True
			user.email_verify_code = None	
			user.save()	
			return render(request, 'account/auth/email_verify_done.html') 

		return render(request, 'account/auth/email_verify.html', 
					 {'code_is_not_valid': True})
