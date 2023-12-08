from django.shortcuts import render, redirect
import csv
from .forms import UserDataForm
from .models import UserData
from io import TextIOWrapper 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'fundapp/index.html')

@login_required
def crm(request):
    if request.user.is_superuser:
        # For admin users, display all data
        users_data = UserData.objects.all()
    else:
        # For non-admin users, filter data based on the logged-in user
        users_data = UserData.objects.filter(user=request.user)

    return render(request, 'fundapp/crm.html', {'users_data': users_data})

@login_required
def upload(request):
    if request.method == 'POST':
        if request.user.is_superuser:  # Only allow admin users to upload data
            if 'file' in request.FILES:
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    return HttpResponseRedirect(reverse('crm') + '?error=Please+upload+a+CSV+file')

                try:
                    csv_data = csv.reader(TextIOWrapper(csv_file.file, encoding='utf-8'), delimiter=',')
                    users = User.objects.filter(is_superuser=False)  # Exclude admin users
                    total_users = users.count()
                    user_records = [[] for _ in range(total_users)]
                    current_user_index = 0
                    
                    for row in csv_data:
                        user_records[current_user_index].append(UserData(
                            user=users[current_user_index],
                            name=row[0],
                            country=row[1],
                            phone=row[2],
                            email=row[3],
                            source=row[4]
                        ))
                        # Move to the next user for the next record
                        current_user_index = (current_user_index + 1) % total_users
                    
                    # Bulk create user data objects for each user
                    for index, records in enumerate(user_records):
                        UserData.objects.bulk_create(records)

                    return HttpResponseRedirect(reverse('crm') + '?success=CSV+uploaded+successfully!')
                
                except Exception as e:
                    return HttpResponseRedirect(reverse('crm') + f'?error=Error+uploading+CSV:+{str(e)}')

        else:
            return HttpResponseRedirect(reverse('crm') + '?error=Only+admin+can+upload+data')

    return render(request, 'crm.html')


@login_required
def edit(request, id):
    user = UserData.objects.get(id=id)
    if request.method == 'POST':
        # update fields
        user.name = request.POST['name']
        user.country = request.POST['country']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.source = request.POST['source']
        user.save()
        return redirect('crm')
    return render(request, 'fundapp/edit.html', {'user': user})

@login_required
def delete(request, id):
    user = UserData.objects.get(id=id)
    user.delete()
    user = UserData.objects.all()
    return redirect('crm')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user) 
            messages.success(request, "Logged in successfully")
            
            # Pass data to the template
            return redirect("crm")
        else:
            messages.error(request, "Bad credentials")
            return redirect('login')  
    return render(request, "fundapp/crm.html")


def login_user(request):
    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')  # Redirect to registration page

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')  # Redirect to registration page

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')  # Redirect to registration page

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "You are now registered. Please log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'registration.html')


def signout(request):
    logout(request)
    return redirect('crm')