from django.shortcuts import render, redirect
import csv
from .forms import UserDataForm
from .models import UserData
from io import TextIOWrapper 
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'fundapp/index.html')

def crm(request):
    users = UserData.objects.all()
    return render(request, 'fundapp/crm.html', {'users': users}) 

def upload(request):
    return render(request, 'fundapp/upload.html') 


def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            # Ensure the file is a CSV file
            if not csv_file.name.endswith('.csv'):
                return HttpResponseRedirect(reverse('crm') + '?error=Please+upload+a+CSV+file')
            
            # Process the uploaded CSV file
            csv_data = csv.reader(TextIOWrapper(csv_file.file, encoding='utf-8'), delimiter=',')
            for row in csv_data:
                UserData.objects.create(
                    name=row[0],
                    country=row[1],
                    phone=row[2],
                    email=row[3],
                    source=row[4]
                )
                # Add more fields as needed based on the CSV columns and model fields
            
            # Redirect with success message in query parameter
            return HttpResponseRedirect(reverse('crm') + '?success=CSV+uploaded+successfully!')

    return render(request, 'crm.html')

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


def delete(request, id):
    user = UserData.objects.get(id=id)
    user.delete()
    user = UserData.objects.all()
    return redirect('crm')