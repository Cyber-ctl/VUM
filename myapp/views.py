from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import quotes
from django.views import View
from .forms import ExcelUploadForm
import pandas as pd
import datetime as dt
from django.conf import settings
import os ,  pywhatkit ,time
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password


from django.contrib import messages

# Create your views here.

def home(request):
    
    return render(request, "index.html", {'name': 'index'})

def header(request):

    return render(request, "header.html", {'name': 'header'})

def footer(request):
    return render(request, "footer.html", {'name': 'footer'})

def StudentView(request):
    stu_data = Student.objects.all()
    total_count = Student.objects.count()  # Get the total count of students

    return render(request, "student.html", {'stu_data': stu_data, 'total_count': total_count})

def books_view(request):
    return render(request, "books.html", {'name': 'books'})

def register_books_view(request):
    return render(request, "register.html", {'name': 'register_books_view'})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == "POST":
        student.delete()
        return redirect(StudentView)
        
    return redirect(StudentView)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == "POST":
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.password = request.POST.get('password')
        student.save()
        return redirect(StudentView)
    
    return render(request, 'edit_student.html', {'student': student})

def stud_add(request):
    excel_form = ExcelUploadForm()
    
    if request.method == "POST":
        if 'upload_excel' in request.POST:
            excel_form = ExcelUploadForm(request.POST, request.FILES)
            if excel_form.is_valid():
                excel_file = request.FILES['file']
                df = pd.read_excel(excel_file)

                # Validate required columns
                required_columns = {'name', 'email', 'password'}
                if not required_columns.issubset(df.columns):
                    return render(request, 'stud_reg.html', {
                        'excel_form': excel_form,
                        'error': 'Missing required columns: name, email, password'
                    })

                for _, row in df.iterrows():
                    if pd.isnull(row['name']) or pd.isnull(row['email']):
                        continue  # Skip incomplete rows
                    Student.objects.create(
                        name=row['name'],
                        email=row['email'],
                        password=row['password']
                    )
                return redirect('student')  # Adjust this to your actual redirect URL name

        elif 'stud_reg' in request.POST:
            name = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
             
            if name and email and password:
                Student.objects.create(
                    name=name,
                    email=email,
                    password=password
                    
                )
                return redirect('student')

    return render(request, 'stud_reg.html', { 'excel_form': excel_form, })

def welcome_view(request):
    admin_name = request.session.get('admin_name')
    return render(request, "welcome.html", {'admin_name': admin_name})


def Logged_view(request):
    items = quotes.objects.filter(active=1)
    
    if request.method == 'POST':
        identifier = request.POST.get('namevum')  # Can be username or email
        password = request.POST.get('passvum')
        
        try:
            # Try to find the admin by username or email, and ensure status=1 (active)
            admin_user = Admin_reg.objects.get(
                Q(name=identifier) | Q(email=identifier),
                status=1
            )
            
            # Use check_password to verify the hashed password
            if check_password(password, admin_user.password):
                # Set session and redirect to welcome page
                request.session['admin_name'] = admin_user.name
                return redirect('welcome')
            else:
                messages.error(request, "Incorrect password.")
        
        except Admin_reg.DoesNotExist:
            messages.error(request, "Admin user does not exist or inactive.")
        
    return render(request, "logged.html", {'items': items})

def Logged_in(request):
    
    return redirect(Logged_view)

def admin_status_change(request, user_id, action):
    if request.method == "POST":
        admin = get_object_or_404(Admin_reg, id=user_id)
        admin.modifiedat = dt.date.today()

        if action == 'enable':
            admin.status = 1
        elif action == 'disable':
            admin.status = 0
        else:
            return redirect('Admin_list')  # invalid action

        admin.save()

    return redirect('Admin_list')


def edit_admin(request, user_id):
#    admin_reg = get_object_or_404(Admin_reg, id=user_id)
    #import pdb; pdb.set_trace()
    admin = get_object_or_404(Admin_reg, id=user_id)
    
    if request.method == "POST":
        admin.email = request.POST.get('email')
        admin.name = request.POST.get('name')
        admin.modifiedat = dt.date.today()
        admin.save()
    #    return redirect(StudentView)
        return redirect('Admin_list')
        
    return render(request, 'admin_modify.html', {'admin': admin})

def Admin_reg_view(request):
        name = request.POST.get('username')
        status = request.POST.get('status')
        password = request.POST.get('password')
        email = request.POST.get('email')
        createdby= dt.date.today()
        hashed_password = make_password(password)

        if name and status and hashed_password:
            Admin_reg.objects.create(
            name=name,
            status=status,
            password=hashed_password,
            email=email,
            createdat=createdby
        )
            return redirect('Admin_list')
        
        return render(request, "admin_reg.html")
        

def admin_delete(request, user_id):
    admin = get_object_or_404(Admin_reg, id=user_id)
    
    if request.method == "POST":
        admin.delete()
        return redirect(Admin_view)
        
    return redirect(Admin_view)

def Admin_view(request):
    user=Admin_reg.objects.all()

    return render(request, "admin.html",{'user':user})

def admin_password(request):

    return render(request,"admin_password.html")

def quotes_view(request):
    #all_items = quotes.objects.all()
    items = quotes.objects.all
    
    return render(request, "quotes_view.html", {'items': items })

def delete_quotes(request, id):
    quote = get_object_or_404(quotes, id=id)
   
    if request.method == "POST":
        quote.delete()
        return redirect(quotes_view)
        
    return redirect(quotes_view)
    

def modify_quotes(request):
    #all_items = quotes.objects.all()
    items = quotes.objects.all
    
    return render(request, "modify_quotes.html", {'items': items })


def quotes_new(request):
    if request.method == "POST":
        quote_text = request.POST.get("quotes")  # Fixed variable name
        status = request.POST.get("status")
        # Optional fields
        author=request.POST.get("author")
        createdby= dt.date.today()
        #createdby = ("2025-09-10","%Y-%m-%d")

        if quote_text and status:  # Fixed variable name
            quotes.objects.create(  # Use correct model name
                quotes_a=quote_text,  # Match your model field names
                active=status,
                author=author,
                createdat=createdby
            )
        else:
           print("Missing required fields") 

        return redirect('quotes_view')
            
    return render(request, "new_quotes.html", {'name': 'quotes_new'})

def modify_quotes(request, quote_id):
    quote = get_object_or_404(quotes, id=quote_id)
    
    if request.method == "POST":
        quote.quotes_a = request.POST.get('quotes_a')
        quote.active = request.POST.get('status')
        quote.author = request.POST.get('author')
        quote.modifiedat=dt.date.today()
        quote.save()
        return redirect(quotes_view)
    
    return render(request, 'modify_quotes.html', {'quote': quote})

#Sabhasad
def Sabhasad_view(request):
    Sabhasad_list = Sabhasad.objects.all()
    total_count = Sabhasad.objects.count()  # Get the total count of students

    return render(request, "sabhasad.html",{'Sabhasad':Sabhasad_list,'total_count':total_count})


def Sabhasad_reg(request):
    excel_form = ExcelUploadForm()
    div_list = Div.objects.all()
    last_reg_no = Sabhasad.objects.order_by('-reg_no').values_list('reg_no', flat=True).first()
    new_reg_no = last_reg_no + 1
    
    
    if request.method == "POST":
        if 'upload_excel' in request.POST:
            excel_form = ExcelUploadForm(request.POST, request.FILES)
            if excel_form.is_valid():
                excel_file = request.FILES.get('File')
                
                if not excel_file:
                    return render(request, 'sabhasad_reg.html', {
                        'excel_form': excel_form,
                        'error': 'No file uploaded.'
                    })

                try:
                    df = pd.read_excel(excel_file)
                    #import pdb; pdb.set_trace() to debug the code
                except Exception as e:
                    return render(request, 'sabhasad_reg.html', {
                        'excel_form': excel_form,
                        'error': f'Error reading Excel file: {e}'
                    })
                
                # Check for required columns
                required_columns = {'Reg_no', 'Name', 'Division', 'Contact_no', 'Reg_date', 'Dob', 'Email_id', 'Address'}
                if not required_columns.issubset(df.columns):
                    return render(request, 'sabhasad_reg.html', {
                        'excel_form': excel_form,
                        'error': f'Missing required columns: {required_columns - set(df.columns)}'
                    })

                for _, row in df.iterrows():
                    reg_no = row['Reg_no']
                    name = row['Name']
                    division = row['Division'].upper()
                    contact_no = row['Contact_no']
                    reg_date = row['Reg_date']
                    dob = row['Dob']
                    email_id = row['Email_id']
                    address = row['Address']
                    active= True
                    createdat = dt.date.today()

                    
                    Sabhasad.objects.create(
                        reg_no=reg_no,
                        name=name,
                        division=division,
                        contact_no=contact_no,
                        reg_date=reg_date,
                        dob=dob,
                        active= active,
                        email_id=email_id,
                        address=address,
                        createdat=createdat
                    )
                #import pdb; pdb.set_trace()
                return redirect('Sabhasad')  # Adjust this to your actual redirect URL name

        elif 'stud_reg' in request.POST:
            
            reg_no = request.POST.get('Reg_no')
            name = request.POST.get('Name')
            division= request.POST.get('Division').upper()
            contact_no= request.POST.get('Contact')
            reg_date= request.POST.get('Reg_date')
            dob = request.POST.get('Dob')
            email_id= request.POST.get('Email_id')
            address= request.POST.get('Address')
            #import pdb; pdb.set_trace()
            print("Request method:", reg_no)
            if name and email_id :
                Sabhasad.objects.create (
                    reg_no = reg_no,
                    name = name,
                    division = division,
                    contact_no = contact_no,
                    reg_date = reg_date,
                    dob = dob,
                    active = 1,
                    email_id = email_id,
                    address = address,
                    createdat=dt.date.today()
                )
                return redirect('Sabhasad')

    #import pdb; pdb.set_trace()
    return render(request, 'sabhasad_reg.html', { 'excel_form': excel_form,'data':div_list,'new_reg_no':new_reg_no  })


def delete_Sabhasad(request, id):
    quote = get_object_or_404(Sabhasad, id=id)
   
    if request.method == "POST":
        quote.delete()
        return redirect(Sabhasad_view)
        
    return redirect(Sabhasad_view)


def sabhasad_modify(request, id):
    data = get_object_or_404(Sabhasad, id=id)
    date_dob = data.dob.strftime('%Y-%m-%d')
    date_reg = data.reg_date.strftime('%Y-%m-%d') 
    div=Div.objects.all()

    if request.method == "POST":
        data.reg_no = request.POST.get('Reg_no')
        data.name = request.POST.get('Name')
        data.division = request.POST.get('Division')
        data.contact_no= request.POST.get('Contact')
        data.reg_date = request.POST.get('Reg_date')
        data.dob = request.POST.get('Dob')
        data.email_id = request.POST.get('Email_id')
        data.address = request.POST.get('Address')
        data.modifiedat=dt.date.today()
        data.save()
        return redirect('Sabhasad')
   
    return render(request,'sabhasad_modify.html', {'data': data,'dob_n':date_dob,'date_reg':date_reg,'div':div})

def send_single_message(request, sabhasad_id):
    """Handle single message sends from anchor tags"""
    if request.method == "GET":
        messageBox = request.session.get('messageBox', '')
        
        try:
            #import pdb; pdb.set_trace()
            sabhasad = get_object_or_404(Sabhasad, id=sabhasad_id)
            whatsapp_number = f"+91{sabhasad.contact_no}"
            now = dt.datetime.now()
            hour = now.hour
            minute = now.minute + 1

            # Adjust in case minute goes over 59
            if minute >= 60:
                minute = 0
                hour = (hour + 1) % 24

            message = f"Hi {sabhasad.name}, {messageBox}"
            pywhatkit.sendwhatmsg(whatsapp_number, message,  hour, minute ,wait_time=25, tab_close=True)
            messages.success(request, f"Message sent to {sabhasad.name}")
        except Exception as e:
            messages.error(request, f"Error sending to {sabhasad.name}: {e}")
            
    return redirect('best_wish')

def sabhasad_filter(request):
    Sabhasad_list = Sabhasad.objects.all()
    #total_count = Sabhasad.objects.count()  # Get the total count of students
    #import pdb; pdb.set_trace()
    from_reg=request.GET.get('from_reg')
    to_reg=request.GET.get('to_reg')

    if from_reg and to_reg:
            Sabhasad_list = Sabhasad_list.filter(reg_no__range = [from_reg, to_reg])
    elif from_reg:
            Sabhasad_list = Sabhasad_list.filter(reg_no__gte=from_reg)
    elif to_reg:
            Sabhasad_list = Sabhasad_list.filter(reg_no__lte=to_reg)
        
    # Get filtered count
    filtered_count = Sabhasad_list.count()

    return render(request, "best_wish.html",{'Sabhasad':Sabhasad_list,'total_count':filtered_count})


def best_wish_view(request):
    if request.method == "POST":
        messageBox = request.session.get('messageBox', '')
        # Check which button was clicked      
        if 'send_bulk' in request.POST:
            # ----- BULK SEND -----
            selected_ids = request.POST.getlist('selected_ids')
            if not selected_ids:
                messages.warning(request, "No Sabhasad members selected for bulk send.")
                return redirect('best_wish')

            success_count = 0
            error_count = 0
            
            for sabhasad_id in selected_ids:
                try:
                    sabhasad = get_object_or_404(Sabhasad, id=sabhasad_id)
                    whatsapp_number = f"+91{sabhasad.contact_no}"
                    message = f"Hi {sabhasad.name}, {messageBox}"
                    now = dt.datetime.now()
                    import pdb; pdb.set_trace()
                    hour = now.hour
                    minute = now.minute + 1
                    value=30
                    # Adjust in case minute goes over 59
                    if minute >= 60:
                        minute = 0
                        hour = (hour + 1) % 24

                    pywhatkit.sendwhatmsg(whatsapp_number, message,  hour, minute ,wait_time=value, tab_close=True)
                    #pywhatkit.sendwhatmsg_instantly(whatsapp_number, message, wait_time=10, tab_close=True)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    messages.error(request, f"Error sending to ID {sabhasad_id}: {e}")

            messages.success(request, f"Bulk send completed. Successful: {success_count}, Failed: {error_count}")

        return redirect('best_wish')
    
    # For GET requests, show the form with Sabha members
    sabhasad_list = Sabhasad.objects.all()
    return render(request, "best_wish.html",{'Sabhasad':sabhasad_list})

def store_message(request):
    
    if request.method == "POST":
       #import pdb; pdb.set_trace()
       request.session['messageBox'] = request.POST.get('messageBox', '')
  
    return redirect('best_wish')

def card_view(request):

    return render(request,"card.html")

def fetch_by_id(request):
    #import pdb; pdb.set_trace()
    # Get the 'id' from GET parameters
    object_id = request.GET.get('userid2')

    if object_id:
        try:
            # Fetch the object by id
            my_object = Sabhasad.objects.get(reg_no=object_id)
        except Sabhasad.DoesNotExist:
            my_object = None  # If not found, set to None
    else:
        my_object = None

    # Pass the object to the template context
    return render(request,"card.html", {'object': my_object})



def Event_view(request):
    
    return render(request, "Event.html")

def Birth_view(request):
    sabhasad_list = Sabhasad.objects.all()
    today = dt.date.today()
    filter_type = request.GET.get("filter")

    if filter_type == "today":
        sabhasad_list = sabhasad_list.filter(dob__day=today.day, dob__month=today.month)
    elif filter_type == "monthly":
        sabhasad_list = sabhasad_list.filter(dob__month=today.month)

    return render(request, "best_wish.html",{'Sabhasad':sabhasad_list})
    #return render(request, "dob.html",{'sabhasad_list':sabhasad_list})

