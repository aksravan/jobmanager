from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import StudentForm, CreateUserForm, CompanyForm
from .models import Company, CompanyStudents, StudentData

# home page
def home(request):
    companies = [str(c.usrname) for c in Company.objects.all()]
    error = []
    #if user is already logged in
    if request.user.is_authenticated:
    	return redirect('success')
    else:
        if request.method == 'POST':
            #if login button is clicked
            if "login-form" in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    #if admin is to be logged
                    if username == 'youareadmin' or str(request.user) == 'youareadmin':
                        login(request, user)
                        return redirect('superuser')
                    #comapny login
                    if username in companies:
                        login(request, user)
                        return redirect('company')
                    #student login
                    login(request, user)
                    context = {
                        'user' : request.user
                    }
                    return redirect('success')
                else:
                    messages.info(request, 'Username or Password is incorrect.')
            #if student data button is clicked
            elif "register-form" in request.POST:
                if request.method == 'POST':
                    form = CreateUserForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.info(request, 'You\'re successfully registered.')
                    else:
                        error = list(form.error_messages.values())
    
    context = {
        'error' : error
    }
    return render(request, 'jobmanager/home.html', context)

#screen after student login
@login_required(login_url='home')
def success(request):
    data = Company.objects.all().order_by('company_name')
    user = str(request.user)
    appliedcompany = []
    status_dict = {}
    
    #here we get the all companies for which the user has applied
    try:
        stu = CompanyStudents.objects.filter(student_id=user).order_by('company')
        for c in stu:
            appliedcompany.append(str(c.company))
            status_dict[str(c.company)] = c.isselected
    except:
        pass
    
    
    #here we get the status that the student has 
    #filled his details or not
    try:
        StudentData.objects.get(roll_no=user)
        status = True
    except:
        status = False

    context = {
        'user' : request.user,
        'company' : data,
        'student' : status,
        'appliedcompany' : appliedcompany,
        'student_status' : status_dict
    }

    return render(request, 'jobmanager/success.html', context)

#adminlogin
@login_required(login_url='home')
def superuser(request):
    #this status is used as a acknowlegment which shows 
    # if the company is registered or not and displaying error if any
    status = ''
    if str(request.user) != 'youareadmin':
        logout(request)
        return redirect('/')
    
    if request.method == 'POST':
        if 'add-company' in request.POST:
            form = CompanyForm(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, 'Company is added.')
            else:
                ch = str(request.POST.get("company_name"))
                status = Company.objects.filter(ch)
                if not status:
                    messages.info(request, 'Company already exists.')
                messages.info(request, 'Something went wrong, reload and try again.')
        
        elif 'register-company' in request.POST:
            if request.method == 'POST':
                    form = CreateUserForm(request.POST)
                    if form.is_valid():
                        form.save()
                        status = 'Company successfully registered.'
                    else:
                        status = 'Something went wrong. Please reload webpage and try again.'

    context = {
        'user' : request.user,
        'status' : status
    }
    return render(request, 'jobmanager/superuser.html', context)

#for logout
@login_required(login_url='home')
def adminlogout(request):
    logout(request)
    return redirect('home')

#for showing all the companies
@login_required(login_url='home')
def allcompanies(request):
    if str(request.user) != 'youareadmin':
        logout(request)
        return redirect('/')

    try:
        data = Company.objects.order_by('company_name')
    except:
        data = []
    context = {
        'company' : data
    }
    return render(request, 'jobmanager/companies.html', context)

#for showing all the students
@login_required(login_url='home')
def allstudents(request):
    if str(request.user) != 'youareadmin':
        logout(request)
        return redirect('/')
    try:
        data = StudentData.objects.order_by('name')
    except:
        data = []
    context = {
        'students' : data
    }
    return render(request, 'jobmanager/students.html', context)

#for showing all the student profile or to edit 
@login_required(login_url='home')
def profile(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'You\'r data is successfully saved with us.')

    id = request.user
    student = StudentData.objects.filter(roll_no=id)
    if student:
        resume = str(student[0].resume).split('/')
        context = {
            'user' : id,
            'student' : student[0],
            'resume' : '/'.join(resume[1:])
        }
    else:
        context= {
            'user' : id
        }
    return render(request, 'jobmanager/profile.html', context)

#deleting the student data 
@login_required(login_url='home')
def deleteallStudents(request):
    student = StudentData.objects.all()

    if len(student) == 0:
        messages.info(request, 'No student data is available. Database is empty.')
        return redirect('superuser')
    #this will delete the student as user 
    for s in student:
        try:
            s = User.objects.get(username=s.roll_no)
            s.delete()
        except:
            pass
    #this will delete the studentdata from database
    student.delete()
    messages.success(request, 'Successfully deleted.')
    return redirect('superuser')

#deleting all companies
@login_required(login_url='home')
def deleteallCompanies(request):
    company = Company.objects.all()
    if len(company) == 0:
        messages.info(request, 'No company is available. Database is empty.')
        return redirect('superuser')
    #this will delete the company as user
    try:
        for usr in company:
            try:
                u = User.objects.get(username=usr.usrname)
                u.delete()
            except:
                pass
        #this will delete the companies data
        company.delete()
        CompanyStudents.objects.all().delete()

    except:
        messages.error(request, "Something went wrong. Contact the developer.")
        return redirect('superuser')
    
    messages.success(request, 'Successfully deleted.')
    return redirect('superuser')

#apply student for the particular company
@login_required(login_url='home')
def applycompany(request, company):
    if request.method == 'POST':
        user = str(request.user)
        instance = Company.objects.get(company_name=company)
        cs = CompanyStudents(company=instance, student_id=user)
        cs.save()
        return redirect('success')

#here we will see list of the applied students to a 
#particular company
@login_required(login_url='home')
def appliedstudents(request):
    comp = Company.objects.all()
    data = [str(c.company_name) for c in comp]
    students = {}
    for c in comp:
        stu = CompanyStudents.objects.filter(company=c).order_by('student_id')
        students[str(c)] = [s.student_id for s in stu]
        
    context ={
        'students' : students,
        'company' : data
    }
    return render(request, 'jobmanager/appliedstudents.html', context)

#displaying the company view when company login
@login_required(login_url='home')
def company(request):
    user = str(request.user)
    students = []
    stu_dict = {}
    try:
        stu_obj = CompanyStudents.objects.filter(company=Company.objects.get(usrname=user)).order_by('student_id')
        
        for i in stu_obj:
            students.append(StudentData.objects.get(roll_no=i.student_id))
            stu_dict[str(i.student_id)] = i.isselected
    except:
        messages.info(request, 'No student Found.')
        
    context = {
        'user' : str(Company.objects.get(usrname=user).company_name),
        'students' : students,
        'status' : stu_dict
    }
    return render(request, 'jobmanager/company.html', context)

#selecting student as per company
@login_required(login_url='home')
def selectstudent(request):
    user = Company.objects.get(usrname=str(request.user))
    if request.method == 'POST':
        roll_no = request.POST.get('student-roll')
        CompanyStudents.objects.filter(company=user, student_id=roll_no).update(isselected=True)

    return redirect('company')

#displaying selected student as per company
@login_required(login_url='home')
def selectedstudents(request):
    #getting all the companies
    try:
        company = Company.objects.all().order_by('company_name')
    except:
        company = []
    
    try:
        student_dict = {}
        student = {}

        for obj in company:
            stu = CompanyStudents.objects.filter(company=obj).order_by('student_id')
            student[str(obj.company_name)] = [s.student_id for s in stu]
            student_dict[str(obj.company_name)] = [s.isselected for s in stu]
            
    except:
        student = []
        student_dict = []
    
    context = {
        'company' : company,
        'students' : student,
        'status' : student_dict
    }
    return render(request, 'jobmanager/selectedstudents.html', context)

