from ast import Not
from multiprocessing import context
from re import M
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate

from .forms import  UserRegisterForm, NewUserForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from add_road_user.models import User as use  
from add_road_user.forms import AddRoadUserForm  
from add_road_user.models import create_roadUser  
import os
from . models import OffenceList, Crime,create_roadUser,Challan
from django.shortcuts import get_object_or_404
import datetime
from django.db.models import Sum
import re

def chellan():
    last = Challan.objects.last()
    if last == None:
        last = 0
    else:
        last = last.id
    last+=1
    return ( "TNTRC" "%05d" % last)

def last_months():   
    todays = datetime.date.today()
    months = [todays.strftime("%m")]
    for i in range(4):
        first = todays.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        lastMonths =  lastMonth.strftime("%m")
        months.append(lastMonths)
        todays = lastMonth
    return months

def vehicle_check(v_number):
    x = re.search("^[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{1,2}[0-9]{4}$", v_number)
    if x is None:
        return False
    if x:
        return True
    


last_months = last_months()
offencelist = OffenceList.objects.all()


def index(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=use.objects.get(email=username), password=password)
        except:
            messages.error(request,"Invalid Email or password.")
            return redirect('/')
        if user is None:
            messages.error(request,"Invalid Email or password.")
            return redirect('/')
        elif user.is_admin:
            login(request, user)
            messages.success(request, f"You are now logged in as {username}.")
            return redirect("dashboard")
        
        elif user.is_employee:
            login(request, user)
            messages.success(request, f"You are now logged in as {username}.")
            return redirect("dashboard")
        
        elif user.is_customer:
            login(request, user)
            messages.success(request, f"You are now logged in as {username}.")
            return redirect("userfine_search")
            # return redirect("dashboard")
        else:
            messages.error(request,"Invalid Email or password.")
            return redirect('/')
    else:
            return render(request,'index.html')


def register(request):
    
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            username = request.POST.get('username')
            print(username)
            if form.is_valid():
                user =form.save()
                messages.success(request, f"{username}, Your account has been created.")
                return redirect('index')
                
            else:
                err=form.errors
                messages.error(request,"Registration Failed")
                return render(request,'index.html',{'form':form})
        else:
            return render(request,'index.html'); 

def logout_request(request):
	logout(request)
	return redirect("index")  

@login_required(login_url='index')
def add_fine(request):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        challan = Challan.objects.filter( created_at__range=(today_min, today_max))        
        return render(request, 'addfine.html',{'nbar': 'add_fine',"unique":chellan(),"challan":challan})

@login_required(login_url='index')
def dashboard(request):
    if request.user.is_admin or request.user.is_employee:
        datapoints = []
        offences = OffenceList.objects.all()
        for offence in offences:
            data = {}
            data['label']=offence.offence
            no = Crime.objects.filter(offence=offence).count()
            data["y"]=no
            datapoints.append(data)
        year = 2022
        paid = []
        for month in last_months:
            done = Challan.objects.filter(created_at__month=month).filter(payment_status=True).aggregate(Sum('total_penalty'))["total_penalty__sum"]
            if done is None:
                done = 0 
            d = {}
            d["month"] = month
            d["paid"] = done
            paid.append(d)
            
        print(paid)
        unpaid = []
        for month in last_months:
            notdone = Challan.objects.filter(created_at__month=month).filter(payment_status=False).aggregate(Sum('total_penalty'))["total_penalty__sum"]
            if notdone is None:
                notdone = 0 
            d = {}
            d["month"] = month
            d["unpaid"] = notdone
            unpaid.append(d)
        print(unpaid)

        paid_due = Challan.objects.filter(payment_status=True).aggregate(Sum('total_penalty'))
        unpaid_due = Challan.objects.filter(payment_status=False).aggregate(Sum('total_penalty'))
        
        road_user = create_roadUser.objects.all().count()
        total_chellan = Challan.objects.all().count()
        
        
        return render(request, 'dashboard.html',{'nbar': 'dashboard',"datapoints":datapoints,"paid":paid,"unpaid":unpaid,"unpaid_due":unpaid_due,"paid_due":paid_due,"road_user":road_user,"total_chellan":total_chellan })
    else:
        return redirect("userfine_search")


@login_required(login_url='index')    
def add(request):
    return render(request, 'add.html',{'nbar': 'add'})

@login_required(login_url='index')
def newuser(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = NewUserForm(request.POST,request.FILES)
            if form.is_valid():
                username = request.POST.get('username')
                form.save()
                messages.success(request, f"{username}, Your account has been created.")
                return redirect('newuser')   
            else:
                err=form.errors
                messages.error(request, "Registration Failed.")

                return render(request, 'newuser.html',{'form': form,'nbar': 'newuser'});
        else:
            return render(request, 'newuser.html', {'nbar': 'newuser'}); 
    else:
        return redirect("dashboard")


@login_required(login_url='index')
def viewuser(request):
    return render(request, 'viewuser.html',{'nbar': 'view_users'});   

@login_required(login_url='index')
def create_onroadUser(request):
    if request.user.is_admin or request.user.is_employee:
        if request.method == "POST":  
            form = AddRoadUserForm(request.POST,request.FILES)  
            print(form)
            if form.is_valid():  
                    form.save()  
                    firstName = form.cleaned_data['first_name']
                    lastName = form.cleaned_data['last_name']
                    messages.success(request,f'{firstName} {lastName} Profile Created Successfully! ')
                    return redirect('add')  
            else:
                    messages.error(request,'User Registration Failed')
                
                    return render(request,'add.html',{'form': form,'nbar': 'add'})        
        else:  
            messages.error(request,'file NotSaved ')
            return render(request,'add.html',{'nbar': 'add'})  
    else:
        return redirect("index")
    
    
@login_required(login_url='index')  
def view_users(request):
    if request.user.is_admin or request.user.is_employee:
        users = create_roadUser.objects.all()
        if request.method == "POST":   
            userdata = request.POST["userdata"]    
            if not userdata:
                messages.error(request,'Please Enter the Datails for Search')
                return redirect('view_users') 
            else:
                print(userdata)
                users1 = create_roadUser.objects.filter(aadhar_number__iexact = userdata)
                users2 = create_roadUser.objects.filter(license_number__iexact = userdata)
                if users1:
                    users=users1
                elif users2:
                    users=users2
                else:
                        # userdata = request.POST["userdata"]
                    messages.error(request,'Entered data was Invalid')

                    return render(request, 'view_users.html',{'userdata':userdata,'nbar': 'view_users'});
                if users:

                    return render(request, 'view_users.html',{'users':users,'userdata':userdata,'nbar': 'view_users',});
                else:
                    # userdata = request.POST["userdata"]    
                    messages.error(request,'Not Match')
                    return render(request, 'view_users.html',{'userdata':userdata,'nbar': 'view_users'});
        else :  

            return render(request, 'view_users.html',{'users':users,'nbar': 'view_users'});
    else:
        return redirect("index")
            


    
@login_required(login_url='index')   
def getuser_details(request):
    if request.user.is_admin or request.user.is_employee:
  
        if request.method == "POST":   
            userdata = request.POST["userdata"]    
            if not userdata:
                messages.error(request,'Please Enter the Datails for Search ')
                return redirect('add_fine') 
            else:
                print(userdata)
                users1 = create_roadUser.objects.filter(aadhar_number__iexact =userdata).first()
                users2 = create_roadUser.objects.filter(license_number__iexact =userdata).first()
                if users1:
                    users=users1
                elif users2:
                    users=users2
                else:
                        # userdata = request.POST["userdata"]    
                    messages.error(request,'Entered data was Invalid')
                    return render(request, 'addfine.html',{'userdata':userdata,'nbar': 'add_fine'});    
                if users:
                    cc = Challan.objects.filter(offender=users)
                    return render(request, 'addfine.html',{'users':users,'userdata':userdata,'nbar': 'add_fine','offencelist':offencelist,"challan": cc,"unique":chellan()});
                else:
                    # userdata = request.POST["userdata"]    
                    messages.error(request,'Not Match')
                    return render(request, 'addfine.html',{'userdata':userdata,'nbar': 'add_fine'});
        else:
            return HttpResponse("error occured ")
    else:
        return redirect("index")
            
        


@login_required(login_url='index')   
def penalty(request):
    if request.user.is_admin or request.user.is_employee:
        if request.method == "POST":  
    
            checklist = request.POST.getlist('checks')
            offender_id = request.POST.get("road_user")
            offender = create_roadUser.objects.get(pk=offender_id)     
            vehicle = request.POST.get("vehicle_number")
            payment_status = request.POST.get("payment")
            total_penalty = request.POST.get("penalty")
            print(total_penalty)
            
            if total_penalty == "0":
                messages.error(request,'please choose offence before submit')
                challan = Challan.objects.filter(offender=offender) 
                
                return render(request, 'addfine.html',{'users':offender,'nbar': 'add_fine','offencelist':offencelist,'challan':challan,'vehicle':vehicle,"unique":chellan()})
            
            if vehicle_check(vehicle):                 
                unique = request.POST.get("challan")
                if payment_status == "paid":
                    payment_status = True
                else:
                    payment_status = False   
                
                cc = Challan.objects.create(refrence=unique,total_penalty=total_penalty, vehicle_number=vehicle,offender=offender,officer=request.user,payment_status=payment_status,)
   
                for o in checklist:
                    offence = OffenceList.objects.get(pk=int(o))            
                    offence =  Crime( offence=offence,penalty=offence.offence_fine,challan = cc)
                    offence.save()   
                messages.info(request,'offence filed')
                             
                cc = Challan.objects.filter(offender=offender) 
                
                return render(request, 'addfine.html',{'users':offender,'nbar': 'add_fine','offencelist':offencelist,"challan": cc,"unique":chellan()})
            else:
                messages.error(request,'please enter a valid vehicle number')
                return render(request, 'addfine.html',{'users':offender,'nbar': 'add_fine','offencelist':offencelist,"unique":chellan()})    
    else:
        return redirect("index")    
    
    
@login_required(login_url='index')   
def view_challan(request,id):
    challan = get_object_or_404( Challan, pk=id)
    offences = Crime.objects.filter(challan=challan)
    return render(request, 'addfine_view.html',{'nbar': 'add_fine',"challan": challan,"offences":offences});
          
    
@login_required(login_url='index')   
def delete_RegUser(request,id):
        if request.user.is_admin or request.user.is_employee:  
            pi = create_roadUser.objects.get(pk = id)
            pi.delete()
            return redirect('view_users')   
        else:
            return redirect("index")  
   

# Edit Road User         
@login_required(login_url='index')
def edit_road_user(request, pk):
    
    if request.user.is_admin or request.user.is_employee:
        user = create_roadUser.objects.get(id = pk)
        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(user.profile) > 0:
                    os.remove(user.profile.path)
                user.profile = request.FILES['profile']
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.aadhar_number = request.POST.get('aadhar_number')
            user.gender = request.POST.get('gender')
            user.mobile_number = request.POST.get('mobile_number')
            user.email = request.POST.get('email')
            user.license_number = request.POST.get('license_number')
            user.save()
            username = user.first_name + user.last_name
            messages.success(request,f'{username} Profile Updated Successfully! ')
            return redirect('view_users')
        context ={
            'user':user,
            'nbar': 'view_users'
        }
        return render(request, 'edit_view_users.html', context);   
    else:
        return redirect("index")


@login_required(login_url='index')  
def userfine_search(request):
    if request.method == "POST":  
        userdata = request.POST.get("userdata")
        userdata1 = request.POST.get("userdata1")
        print(userdata,userdata1)
        
        try:
            if userdata and userdata1 :
                users = create_roadUser.objects.get(aadhar_number = userdata)

                challan = Challan.objects.filter(offender=users).filter( vehicle_number__iexact=userdata1 )
                return render(request, 'user_view_search.html',{'userdata':userdata,"challan":challan,"userdata":userdata,"userdata1":userdata1})
            if userdata:
                users = create_roadUser.objects.get(aadhar_number = userdata)
                challan = Challan.objects.filter(offender=users)
                return render(request, 'user_view_search.html',{'userdata':userdata,"challan":challan,"userdata":userdata,"userdata1":userdata1})
            if userdata1:
                challan = Challan.objects.filter( vehicle_number__iexact=userdata1 )
                print(challan)
                messages.error(request,'Vehicle number is invalid')
                
                return render(request, 'user_view_search.html',{'userdata':userdata,"challan":challan,"userdata":userdata,"userdata1":userdata1})
            else:
                messages.error(request,'Enter a data for Search')
                
                return render(request, 'user_view_search.html',)
                
        except:
            messages.error(request,'Entered data was invalid')
            return render(request, 'user_view_search.html',{'userdata':userdata,"userdata1":userdata1} )
    else :  
        return render(request, 'user_view_search.html',)
    
        
@login_required(login_url='index')
def user_payment(request,id):
    if request.method == "POST":
        o = request.POST.get("id")
        challan = Challan.objects.get(id=o)
        offence = Crime.objects.filter(challan=challan)
        challan.payment_status = True 
        challan.save() 
        return render(request, 'user_payment.html',{"challan":challan,"offences":offence})
    challan = Challan.objects.get(id=id)
    offence = Crime.objects.filter(challan=challan)
    return render(request, 'user_payment.html',{"challan":challan,"offences":offence})




    
    