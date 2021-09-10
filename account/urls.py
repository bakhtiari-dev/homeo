from django.urls import path
from django.contrib.auth.views import (
	LogoutView, PasswordChangeDoneView,
)

from .views import (
	UserList, UserDetail, ArticleList, ArticleCreate, ArticlePreview, 
	ArticleUpdate, ArticleDelete, EstateList, EstateCreate, EstateUpdate, 
	EstateDelete, EstatePreview, EstateImageDelete, SubscriptionList,
	LogIn, Register, PasswordChange, UserUpdate, PasswordReset, 
	PasswordResetDone, PasswordResetConfirm, PasswordResetComplete, EmailAlert,
	SendEmailVerifyCode, EmailVerify
)


app_name = 'account'

urlpatterns = [
	path('', UserList.as_view(), name='user_list'),
	path('<int:id>/', UserDetail.as_view(), name='user_detail'),

	path('article_list/', ArticleList.as_view(), name='article_list'),
	path('article_list/<slug:status>/', ArticleList.as_view(), 
		 name='article_list_by_status'
	),
	path('article_create/', ArticleCreate.as_view(), name="article_create"),
	path('article_update/<int:pk>/', ArticleUpdate.as_view(), 
		 name="article_update"),
	path('article_delete/<int:pk>/', ArticleDelete.as_view(), 
		 name="article_delete"),
	path('article_preview/<int:article_id>/', ArticlePreview.as_view(), 
		 name="article_preview"),
	
	path('estate_list/', EstateList.as_view(), name='estate_list'),
	path('estate_list/<slug:status>/', EstateList.as_view(), 
		 name='estate_list_by_status'),
	path('estate_create/', EstateCreate.as_view(), name="estate_create"),
	path('estate_update/<int:pk>/', EstateUpdate.as_view(), 
		 name="estate_update"),
	path('estate_delete/<int:pk>/', EstateDelete.as_view(), 
		 name="estate_delete"),
	path('estate_preview/<int:estate_id>/', EstatePreview.as_view(), 
		 name="estate_preview"),
	path('estate_image_delete/<int:image_id>/', EstateImageDelete.as_view(), 
		 name="estate_image_delete"), 

	path('subscription_list/', SubscriptionList.as_view(), 
		 name='subscription_list'),

	path('user_update/', UserUpdate.as_view(), name="user_update"),

	path('login/', LogIn.as_view(), name="login"),
	path('logout/', LogoutView.as_view(), name="logout"),
	path('register/', Register.as_view(), name="register"),

	path('password_change/', PasswordChange.as_view(), name='password_change'),
	path('password_change/done/', PasswordChangeDoneView.as_view(
		 template_name='account/auth/password_change_done.html'), 
		 name='password_change_done'),

	path('password_reset/', PasswordReset.as_view(), name='password_reset'),
	path('password_reset/done/', PasswordResetDone.as_view(), 
		 name='password_reset_done'),
	path('password_reset_confirm/<uidb64>/<token>/', 
		 PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('password_reset_complete/',
		  PasswordResetComplete.as_view(), name='password_reset_complete'),

	path('email_alert/', EmailAlert.as_view(), name="email_alert"),
	path('send_email_verify_code/', 
		SendEmailVerifyCode.as_view(), name="send_email_verify_code"),
	path('email_verify/', EmailVerify.as_view(), name="email_verify"),
]
