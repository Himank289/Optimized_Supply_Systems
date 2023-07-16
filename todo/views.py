from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import User_info,Order_info,product_inventry_info,raw_inventry_info
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random

def home(request):
    try:    
        user_info = User_info.objects.get(user_id = request.user.id)
        if user_info.verified == False:
            return render(request, 'todo/home.html',{'msg':'Your Account verification is pending from Admin'})
        else:
            return render(request, 'todo/home.html')
    except:
            return render(request, 'todo/home.html')


def about(request):
    return render(request,'todo/about.html')

def product(request):
    return render(request, 'todo/product.html')

def contact(request):
    return render(request, 'todo/contact.html')

def faq(request):
    return render(request, 'todo/faq.html')


@login_required
def raw_material_inventory(request):
    import numpy as np
    # from sklearn.linear_model import LinearRegression

    import xgboost as xgb
    y = []
    x = []
    Raw_inventry_info = raw_inventry_info.objects.all()

    print(Raw_inventry_info[0].product_qty)

    X11 = np.array([1,2,3]).reshape(-1,1)
    y11 = np.array([0.45,0.63,0.87]).reshape(-1,1) # (ideal, actual)
    # regsr=LinearRegression()
    regsr = xgb.XGBRegressor()
    regsr.fit(X11,y11)

    to_predict_x= [3]
    to_predict_x= np.array(to_predict_x).reshape(-1,1)
    # predicted_y1 = regsr.predict(to_predict_x)[0][0]
    predicted_y1 = regsr.predict(to_predict_x)

    to_predict_x= [6]
    to_predict_x= np.array(to_predict_x).reshape(-1,1)
    # predicted_y2 = regsr.predict(to_predict_x)[0][0]
    predicted_y2 = regsr.predict(to_predict_x)


    for p in Raw_inventry_info:
        if p.product_qty < (p.ideal_qty)*predicted_y1:
            p.comment = "Under inventory"
        elif p.product_qty > (p.ideal_qty)*predicted_y2:
            p.comment = "Over inventory"
        else:
            p.comment = "Perfect inventory"

        x.append(p.product_name + " {" + p.comment + "}")
        y.append(p.product_qty)

    return render(request, 'todo/raw_material_inventory.html',{'Raw_inventry_info':Raw_inventry_info,'x':x,'y':y})

@login_required
def product_inventory(request):
    import numpy as np
    from sklearn.linear_model import LinearRegression,LogisticRegression

    y = []
    x = []
    Product_inventry_info = product_inventry_info.objects.all()
    
    X11 = np.array([1,2,3]).reshape(-1,1)
    y11 = np.array([0.5,0.7,0.9]).reshape(-1,1) # (ideal, actual)
    regsr=LinearRegression()
    regsr.fit(X11,y11)

    to_predict_x= [3]
    to_predict_x= np.array(to_predict_x).reshape(-1,1)
    predicted_y1 = regsr.predict(to_predict_x)[0][0]

    to_predict_x= [6]
    to_predict_x= np.array(to_predict_x).reshape(-1,1)
    predicted_y2 = regsr.predict(to_predict_x)[0][0]
    
    for p in Product_inventry_info:
        if p.product_qty < (p.ideal_qty)*predicted_y1:
            p.comment = "Under inventory"
        elif p.product_qty > (p.ideal_qty)*predicted_y2:
            p.comment = "Over inventory"
        else:
            p.comment = "Perfect inventory"

        x.append(p.product_name + " {" + p.comment + "}")
        y.append(p.product_qty)

    return render(request, 'todo/product_inventory.html',{'Product_inventry_info':Product_inventry_info,'x':x,'y':y})

class convert_to_class:
    def __init__(self,a,b):
        self.product_name = a
        self.values = b


@login_required
def purchase_forcasting(request):
    import numpy as np
    # from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    import math 

    y = []
    x = []
    order_info = Order_info.objects.all()
    for p in order_info:
        x.append(p.papad_type.replace("_"," "))
        y.append(p.quantity)

    x2 = set(x)
    y1 = []
    x1 = []

    for xx in x2:
        x1.append(xx)

    num_of_entries = 0

    for i in range(len(x1)):
        val = 0
        for j in range(len(x)):
            num_of_entries += 1
            if x1[i] == x[j]:
                val = val + y[j] 
        y1.append(val)


    y2 = []

    for yy in y1:
        X_1 = [1]
        Y_1 = [int(len(x1))]
        X_1.append(2)
        Y_1.append(yy)
        X11 = np.array(X_1).reshape(-1,1)
        y11 = np.array(Y_1).reshape(-1,1)
        to_predict_x= [3]
        to_predict_x= np.array(to_predict_x).reshape(-1,1)
        # regsr=LinearRegression()
        regsr = RandomForestRegressor(n_estimators=100)
        regsr.fit(X11,y11)
        # predicted_y= regsr.predict(to_predict_x)[0][0]
        predicted_y= regsr.predict(to_predict_x)
        y2.append(abs(math.ceil(predicted_y)))

    data_information = []
    for i in range(len(y2)):
        data_information.append(convert_to_class(x1[i],y2[i]))


    return render(request, 'todo/purchase_forcasting.html',{'x':x1,'y':y1,'y2':y2,'data_information':data_information})


@login_required
def place_your_order(request):
    user_info = User_info.objects.get(user_id = request.user.id)
    if user_info.verified == False:
        return render(request, 'todo/home.html',{'msg':'Your Profile verification is pending from Admin'})
    else:
        if request.method == 'GET':
            return render(request, 'todo/place_your_order.html')
        else:
            user = User.objects.get(id = request.user.id)
            user1 = User_info.objects.get(user_id = user.id)
            user2 = User.objects.get(id = user1.assigned_distributor_id)

            order_info = Order_info()
            order_info.user = user
            order_info.responsible_firm_of_this_order = user2
            order_info.quantity = request.POST['quantity']
            order_info.papad_type = request.POST['papad_type'].replace('_',' ')
            order_info.comment = request.POST['comment']
            order_info.acknowledgement = False
            order_info.order_placed = False
            order_info.save()

            return render(request, 'todo/place_your_order.html',{'error':"Order placed Successfully"})


@login_required
def placed_orders(request):
    user_info = User_info.objects.get(user_id = request.user.id)
    if user_info.verified == False:
        return render(request, 'todo/placed_orders.html',{'msg':'Profile verification is pending from Admin'})
    else:
        user_info = Order_info.objects.all().filter(user_id = request.user.id).filter(order_placed = False).order_by('-date_time').values()
        return render(request, 'todo/placed_orders.html',{'placed_orders':user_info})

@login_required
def order_history(request):
    user_info = User_info.objects.get(user_id = request.user.id)
    if user_info.verified == False:
        return render(request, 'todo/order_history.html',{'msg':'Profile verification is pending from Admin'})
    else:
        user_info = Order_info.objects.all().filter(user_id = request.user.id).filter(order_placed = True).order_by('-date_time').values()
        return render(request, 'todo/order_history.html',{'placed_orders':user_info})


@login_required
def placed_orders_by_distributor(request):
    if request.method == 'GET':
        # user_ID = User.objects.get(user_id = request.user.id)
        user_info1 = User_info.objects.all()
        user_info2 = User.objects.all()
        user_info = Order_info.objects.all().filter(responsible_firm_of_this_order = request.user.id).filter(order_placed = False).order_by('-date_time').values()
        return render(request, 'todo/placed_orders_by_distributor.html',{'placed_orders':user_info,'user_info1':user_info1,'user_info2':user_info2})
    else:
        try:
            Acknowledge = request.POST['Acknowledge']
            order_info = Order_info.objects.get(id = Acknowledge)
            order_info.acknowledgement = True
            order_info.save()
        except:
            place_order = request.POST['place_order']
            order_info = Order_info.objects.get(id = place_order)
            order_info.order_placed = True
            order_info.save()
            
        user_info1 = User_info.objects.all()
        user_info2 = User.objects.all()
        user_info = Order_info.objects.all().filter(responsible_firm_of_this_order = request.user.id).order_by('-date_time').values()
        return render(request, 'todo/placed_orders_by_distributor.html',{'placed_orders':user_info,'user_info1':user_info1,'user_info2':user_info2})

@login_required
def placed_orders_history_of_distributor(request):
        user_info1 = User_info.objects.all()
        user_info2 = User.objects.all()
        user_info = Order_info.objects.all().filter(responsible_firm_of_this_order = request.user.id).filter(order_placed = True).order_by('-date_time').values()
        return render(request, 'todo/placed_orders_history_of_distributor.html',{'placed_orders':user_info,'user_info1':user_info1,'user_info2':user_info2})


@login_required
def placed_orders_by_retailer(request):
    if request.method == 'GET':
        user_info = User_info.objects.get(user_id = request.user.id)
        if user_info.verified == False:
            return render(request, 'todo/placed_orders_by_retailer.html',{'msg':'Profile verification is pending from Admin'})
        else:
            user_info1 = User_info.objects.all()
            user_info2 = User.objects.all()
            user_info = Order_info.objects.all().filter(responsible_firm_of_this_order = request.user.id).filter(order_placed = False).order_by('-date_time').values()
            return render(request, 'todo/placed_orders_by_retailer.html',{'placed_orders':user_info,'user_info1':user_info1,'user_info2':user_info2})
    else:
        try:
            Acknowledge = request.POST['Acknowledge']
            order_info = Order_info.objects.get(id = Acknowledge)
            order_info.acknowledgement = True
            order_info.save()
        except:
            place_order = request.POST['place_order']
            order_info = Order_info.objects.get(id = place_order)
            order_info.order_placed = True
            order_info.save()

        user_info1 = User_info.objects.all()
        user_info2 = User.objects.all()
        user_info = Order_info.objects.all().filter(responsible_firm_of_this_order = request.user.id).order_by('-date_time').values()
        return render(request, 'todo/placed_orders_by_retailer.html',{'placed_orders':user_info,'user_info1':user_info1,'user_info2':user_info2})



@login_required
def placed_orders_history_of_retailer(request):
    user_info = User_info.objects.get(user_id = request.user.id)
    if user_info.verified == False:
        return render(request, 'todo/placed_orders_by_retailer.html',{'msg':'Profile verification is pending from Admin'})
    else:
        user_info1 = User_info.objects.all()
        user_info2 = User.objects.all()
        user_info = Order_info.objects.all().filter(responsible_firm_of_this_order = request.user.id).filter(order_placed = True).order_by('-date_time').values()
        return render(request, 'todo/placed_orders_history_of_retailer.html',{'placed_orders':user_info,'user_info1':user_info1,'user_info2':user_info2})


@login_required
def your_profile(request):
    import numpy as np
    from sklearn.linear_model import LogisticRegression

    user_info = User_info.objects.all().filter(user_id = request.user.id)
    # user_info = Order_info.objects.all().filter(user_id = request.user.id).filter(order_placed = True).order_by('-date_time').values()
    y = [
        'Spl_Urad(100g)','Spl_Urad(200g)','Spl_Urad(1kg)',
        'Plain_Urad(100g)','Plain_Urad(200g)','Plain_Urad(1kg)',
        'Urad_Moong(100g)','Urad_Moong(200g)','Urad_Moong(1kg)',
        'Garlic_Green_Chilli(100g)','Garlic_Green_Chilli(200g)','Garlic_Green_Chilli(1kg)',
        'Spl_Green_Chilli(100g)','Spl_Green_Chilli(200g)','Spl_Green_Chilli(1kg)',
        'Spl_Garlic(100g)','Spl_Garlic(200g)','Spl_Garlic(1kg)',
        'Red_Chilli(100g)','Red_Chilli(200g)','Red_Chilli(1kg)',
        'Jeera(100g)','Jeera(200g)','Jeera(1kg)',
        'Spl_Panjabi(100g)','Spl_Panjabi(200g)','Spl_Panjabi(1kg)',
        'Chana_Mix(100g)','Chana_Mix(200g)','Chana_Mix(1kg)',
        'Whole_Moong(100g)','Whole_Moong(200g)','Whole_Moong(1kg)',
        'Jain(100g)','Jain(200g)','Jain(1kg)',
        'Coin(1kg)',
        ]
    x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
    X11 = np.array(x).reshape(-1,1)
    y11 = np.array(y).reshape(-1,1) # (ideal, actual)
    regsr=LogisticRegression()
    regsr.fit(X11,y11)
    to_predict_x= [len(user_info)]

    to_predict_x= np.array(to_predict_x).reshape(-1,1)
    predicted_y = regsr.predict(to_predict_x)[0]
    print(predicted_y)

    return render(request, 'todo/your_profile.html',{'user_info':user_info,'predicted_y':predicted_y})



def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['firm_name'], password=request.POST['password1'])
                user.save()

                user_info = User_info()
                user_info.user = user
                user_info.Proprietor_name = request.POST['proprietor_name']
                user_info.Mobile_Number = request.POST['Mobile_Number']
                user_info.Email_ID = request.POST['Email_ID']
                user_info.Address = request.POST['Address']
                user_info.role = request.POST['role']
                user_info.verified = False    
                user_info.assigned_distributor = user
                user_info.save()            

                return redirect('home')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            try:
                user_info = User_info.objects.get(user_id = user.id)
                if user_info.verified == False:
                    return render(request, 'todo/home.html',{'msg':'Your Account verification is pending from Admin'})
                else:
                    return render(request, 'todo/home.html')
            except:
                return render(request, 'todo/home.html')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
