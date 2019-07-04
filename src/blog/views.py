from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import BlogPost
from django.http import Http404
from .forms import BlogPostForm, BlogPostModelForm

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def blog_post_detail_page(request, slug):
	'''
	try:
		obj = BlogPost.objects.get(id=post_id)
	except BlogPost.DoesNotExist:
		raise Http404
	except ValueError:
		raise Http404
	'''
	''' QUERYSET LOOKUP
	queryset = BlogPost.objects.filter(slug=slug)
	if queryset.count() < 1:
		raise Http404
	else:
		obj = queryset.first()
	'''
	obj = get_object_or_404(BlogPost, slug=slug)

	template_name = 'blog_post_detail.html'
	context = {'object':obj}
	return render(request, template_name, context)


# Create Retrieve Update Delete
def blog_post_list_view(request):
    # list out objects 
    # could be search
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
    	my_qs = BlogPost.objects.filter(user=request.user)
    	qs = (qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {'object_list': qs}
    return render(request, template_name, context) 

#@login_required(login_url='/login')
#@login_required
@staff_member_required
def blog_post_create_view(request):
    # create objects
    # ? use a form
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
    	#print(form.cleaned_data)
    	#title = form.cleaned_data['title']
    	#obj = BlogPost.objects.create(title=title)
    	# MODEL FORM
    	#obj = BlogPost.objects.create(**form.cleaned_data)
    	obj = form.save()	# save() can be used only if it is a model
    	obj.title = form.cleaned_data.get("title") + "a" 	# To manipulate data if required
    	obj.user = request.user
    	obj.save()
    	form = BlogPostForm()
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)  


def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)   

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {'form': form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)  

@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'    
    if request.method == 'POST':	# call the method
    	obj.delete()				# and delete it.
    	return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)