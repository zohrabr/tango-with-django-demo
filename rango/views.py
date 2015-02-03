from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from rango.models import Category, Page
from rango.forms import categoryform, pageform, userform, profiluserform
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required





def index(request):
	
	context = RequestContext(request)
	request.session.set_test_cookie()
	category_list = Category.objects.order_by('-likes')[:5]
	dictionary = {'categories' : category_list}
	for c in category_list :
		c.name = c.name.replace(' ','_')
	return render_to_response('rango/index.html',dictionary,context)





def about(request):
	context = RequestContext(request)
	dic={'about' : "rango says: here is the about page (^_^) "  }
	return render_to_response('rango/about.html',dic,context)





def category(request,category_url):
	context = RequestContext(request)
	category_name = category_url.replace('_',' ')
	dic = {'category_name' : category_name,'category_url':category_url}
	try:
		category = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=category)
		dic['pages'] = pages
		dic['category'] = category
	except Category.DoesNotExist:
		pass
	return render_to_response('rango/category.html', dic , context)	







def add_category(request):
	context=RequestContext(request)
	if request.method == 'POST':
		form= categoryform(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = categoryform()
	return render_to_response('rango/add_category.html',{'form' : form }, context)




def add_page(request, category_url):
    context = RequestContext(request)

    category_name = category_url.replace('_',' ')
    if request.method == 'POST':
        form = pageform(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_url)
        else:
            print form.errors
    else:
        form = pageform()

    return render_to_response( 'rango/add_page.html',
            {'category_url': category_url,
             'category_name': category_name, 'form': form},
             context)









def register(request):
	context = RequestContext(request)
	if request.session.test_cookie_worked():
    		print ">>>> TEST COOKIE WORKED!"
   		request.session.delete_test_cookie()
	
	
	registred = False
	if request.method =='POST' :
		user_form =userform(data= request.POST)
		profil_form = profiluserform(data = request.POST)
		if user_form.is_valid() and profil_form.is_valid() :
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profil = profil_form.save(commit = False)
			profil.user =user
			if 'picture' in request.FILES :
				profil.picture = request.FILES['picture']
			profil.save()
			registred = True 
		else :
			print user_form.errors, profil_form.errors
	else:
		user_form= userform()
		profil_form= profiluserform()
	return render_to_response('rango/register.html',{'user_form': user_form,'profil_form': profil_form, 'reg': registred}, context)









def user_login(request):
	context= RequestContext(request)
	if request.method == 'POST':	
		username= request.POST['username']
		userpass = request.POST['password']
		user = authenticate(username=username,password=userpass)
		if user :
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username,userpass)	
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('rango/login.html', {}, context)




@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")




@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')






		




