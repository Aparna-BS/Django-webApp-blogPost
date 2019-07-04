from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm
from blog.models import BlogPost


def home_page(request):
	# INCLUDE WITH ARGUMENTS
	# context = {'title' : 'Hey there !!'}
	# if request.user.is_authenticated:
	#	context = {'title' : 'Hey there !!', 'my_list':[1,2,3,4,5,6]}
	my_title = 'Hey there..Welcome to Try Django'
	qs = BlogPost.objects.all()[:5]
	context = {'title' : my_title, 'blog_list': qs}
	return render(request, "home.html", context)

def about_page(request):
	return render(request, "about.html", {'title' : 'About Us'})

def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():	# Validates input data
		print(form.cleaned_data)
		form = ContactForm()	# Re-initialize the form
	context = {'title' : 'Contact Us', 'form' : form}
	return render(request, "form.html", context)

def example_page(request):
	#return render(request, "hello_world.html", {'title' : 'Example'})
	context = { 'title': 'Example'}
	template_name = "base.html"
	template_obj = get_template(template_name)
	return HttpResponse(template_obj.render(context))