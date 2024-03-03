from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import MyUserCreationForm, CSVUploadForm
from django.contrib.auth.decorators import login_required, user_passes_test
import paho.mqtt.publish as publish
from .models import ValidStudentID
import csv

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # ตรงนี้คือการใช้งานที่ถูกต้อง
            auth_login(request, user)  # ใช้ auth_login แทน login และส่งทั้ง request และ user
            # ทำการ redirect หรือแสดงข้อความสำเร็จตามที่ต้องการ
            return redirect('login')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"login_form": form})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("login")


@login_required
def unlock_door_SC252(request):
    # Define which user levels are allowed to unlock SC252
    if request.user.level in ['4']:
        publish.single("SC252/doorLock", "unlock", hostname="192.168.1.15")
        return HttpResponse('Door unlocked successfully!')
    else:
        return HttpResponse('Access denied.', status=403)

@login_required
def unlock_door_SC251(request):
    # Define which user levels are allowed to unlock SC251
    if request.user.level in ['3']:
        publish.single("SC251/doorLock", "unlock", hostname="192.168.1.15")
        return HttpResponse('Door unlocked successfully!')
    else:
        return HttpResponse('Access denied.', status=403)

@login_required
def unlock_door_SC250(request):
    # Define which user levels are allowed to unlock SC250
    if request.user.level in ['1', '2']:
        publish.single("SC250/doorLock", "unlock", hostname="192.168.1.15")
        return HttpResponse('Door unlocked successfully!')
    else:
        return HttpResponse('Access denied.', status=403)

def index(request):
    return render(request, 'index.html')

@login_required
# @user_passes_test(lambda u: u.is_staff)
def add_user(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                for row in reader:
                    student_id = row['StudentID']
                    # Avoid duplicates
                    if not ValidStudentID.objects.filter(student_id=student_id).exists():
                        ValidStudentID.objects.create(student_id=student_id)

                return redirect('index')
        else:
            form = CSVUploadForm()
        return render(request, 'csv_upload.html', {'form': form})
    else:
        return HttpResponse('Access denied.', status=403)