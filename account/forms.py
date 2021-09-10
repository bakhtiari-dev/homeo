from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ('first_name', 'email', 'phone', 
				  'password1', 'password2', 'image')

	error_messages = {
		'password_mismatch': 'رمزهای عبور با یک‌دیگر تفاوت دارند.',
	}
