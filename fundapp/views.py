from django.shortcuts import render
import csv
from .forms import UserDataForm
from .models import UserData
from io import TextIOWrapper 

# Create your views here.
def home(request):
    return render(request, 'fundapp/index.html')

def crm(request):
    users = UserData.objects.all()
    return render(request, 'fundapp/crm.html', {'users': users}) 

def upload(request):
    return render(request, 'fundapp/upload.html') 


def upload_csv(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            # Ensure the file is a CSV file
            if not csv_file.name.endswith('.csv'):
                return render(request, 'fundapp/upload_csv.html', {'error': 'Please upload a CSV file'})
            
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
            
            # Redirect or return a success message after file upload
            return render(request, 'fundapp/upload_csv.html', {'success': 'CSV uploaded successfully!'})
        
    # Display the form for file upload and form submission
    form = UserDataForm(request.POST or None)
    if form.is_valid():
        form.save()
        # Redirect or return a success message after form data submission
        return render(request, 'fundapp/upload_csv.html', {'success': 'Form data submitted successfully!'})
    
    return render(request, 'fundapp/upload_csv.html', {'form': form})