from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import *
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# Create your views here.

User = get_user_model()

def landing_page(request):
	return render(request, 'portal/landing_page.html')

def student_signup(request):
	if request.method=='POST':
		form = student_signup_form(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_student = True
			user.save()
			return HttpResponseRedirect('/')
	else:
			form = student_signup_form()
	return render(request, 'portal/student_signup.html', {'form': form})

def teacher_signup(request):
	if request.method=='POST':
		form = teacher_signup_form(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_teacher = True
			user.save()
			return HttpResponseRedirect('/')		
	else:
			form = teacher_signup_form()
	return render(request, 'portal/teacher_signup.html', {'form': form})

def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				if user.is_student:
					login(request, user)
					return redirect('student_dashboard')
				if user.is_teacher:
					login(request, user)
					return redirect('teacher_dashboard')				
				else:
					return render(request, 'portal/inactiv_account.html')
			else:
				return render(request, 'portal/inactiv_account.html')
	else:
		form = UserLoginForm()
	context = {
		'form': form,
	}
	return render(request, 'portal/login.html', context)

def user_logout(request):
	django_logout(request)
	return redirect('/')

def student_dashboard(request):
	documents = Document.objects.all()
	
	return render(request, 'portal/student_dashboard.html', { 'documents':documents })

def teacher_dashboard(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return render(request, 'portal/teacher_dashboard.html')
	else:
		form = DocumentForm()
	return render(request, 'portal/teacher_dashboard.html', {
		'form': form
	})

def edit_profile(request):
    if request.method == 'POST':
        user_profile = UserEditForm(data=request.POST or None, instance=request.user)
        if user_profile.is_valid():
            user_profile.save()
            return redirect('/student_dashboard')
    else:
        user_profile = UserEditForm(instance=request.user)

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'portal/edit_profile.html', context)

def student_proctor(request):
    if request.method == 'POST':
        form = Student_Proctor_Form(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.created=request.user
            new_user.save()
            return redirect('/student_dashboard')
    else:
        form = Student_Proctor_Form()
    context = {
        'form': form,
    }
    return render(request, 'portal/student_proctorform.html', context)

def student_update(request):
    if request.method == 'POST':
        user_form = Stud(data=request.POST or None, instance=request.user.student)
        if user_form.is_valid():
            user_form.save()
            return redirect('/student_dashboard')
    else:
        user_form = Stud(instance=request.user.student)
    context = {
        'user_form': user_form,
    }
    return render(request, 'portal/student_updateform.html', context)

def teacher_viewproctor(request):
	obj=student.objects.all()
	query = request.GET.get('q')
	if query:
		obj = student.objects.filter(name__icontains=query)
	return render(request,'portal/teacher_viewproctor.html',{'obj':obj})

def index(request):
	if request.method == 'POST':
		user_form = Student_update_Form1(data=request.POST or None, instance=request.user.student)
		if user_form.is_valid():
			user_form.save()
			return redirect('student_dashboard')
	else:
		user_form = Student_update_Form1(instance=request.user.student)
	context = {
        'user_form': user_form,
    }
	return render(request, 'portal/teacher_viewform.html', context)
