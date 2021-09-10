from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import ContactUsForm
from site_setting.models import SiteSetting


class ContactUs(TemplateView):
	def get(self, request, *args, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0]         
		return render(request, 'contact_us/contact_us.html',
					  {'site_setting': site_setting})

	def post(self, request, *args, **kwargs):
		# Save the message if form is valid.
		form = ContactUsForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'پیام شما با موفقیت ارسال شد.')
		return redirect('contact_us:contact_us')
