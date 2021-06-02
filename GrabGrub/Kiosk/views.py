from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Account, Food, Customer, Order
from datetime import datetime

# LOGIN AND SIGN UP
def login(request):
    if(request.method == "POST"):
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        accountList = Account.objects.filter(username = uname)
        if(len(accountList)>0):
            verifyAccount = Account.objects.get(username = uname)
            if(pword == verifyAccount.getPassword()):
                messages.info(request, "Successfully logged in account " + str(verifyAccount.getUsername()))
                return redirect("homepage")
            else:
                messages.error(request, "Invalid Login")
                return render(request, "Kiosk/login.html")
        else:
            messages.error(request, "Invalid Login")
            return render(request, "Kiosk/login.html")
    else:
        return render(request, 'Kiosk/login.html')

def create_account(request):
    if(request.method == "POST"):
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        accountList = Account.objects.filter(username = uname)
        if(len(accountList) > 0):
            messages.error( request, "Username is taken")
            return render(request, "Kiosk/create_account.html")
        else:
            messages.info(request, "Successfully created account!")
            Account.objects.create(username = uname, password = pword)
            return redirect("login")
    else:
        return render(request, "Kiosk/create_account.html")

# ORDER-CENTERED
def homepage(request):
    order_objects = Order.objects.all()
    return render(request, "Kiosk/homepage.html", {'orders':order_objects})

def add_order(request):
    customer_objects = Customer.objects.all()
    food_objects = Food.objects.all()
    now = datetime.now()
    if(request.method == "POST"):
        foodpk = request.POST.get("food")
        qty = request.POST.get("quantity")
        ordered_at = now
        cust_orderpk = request.POST.get("customer")
        payment_mode = request.POST.get("payment")

        food = Food.objects.get(pk=foodpk)
        cust_order = Customer.objects.get(pk=cust_orderpk)

        Order.objects.create(food=food,qty=qty,ordered_at=ordered_at,cust_order=cust_order,payment_mode=payment_mode)
        messages.info(request, "Successfully added order")
        return redirect("homepage")

    else:
        return render(request, "Kiosk/add_order.html", {'customers':customer_objects, 'food':food_objects})

def view_order_details(request, pk):
    
    o = get_object_or_404(Order, pk=pk)

    list = []
    pk_list = Order.objects.filter().values('pk')
    for number in pk_list:
        list.append(number['pk'])
        list.sort()
    currentValue = list.index(pk)
    if currentValue != len(list)-1:
        nextValue = list[currentValue+1]
    else:
        nextValue = 0
    prevValue = list[currentValue-1]
    start = list[0]
    end = list[-1]
    return render(request, "Kiosk/view_order_details.html", {'o':o,'nextValue':nextValue, 'prevValue':prevValue, 'start':start, 'end':end})

def update_order_details(request, pk):
    if(request.method == "POST"):
        qty = request.POST.get("qty")
        payment_mode = request.POST.get("payment")

        oldOrder = get_object_or_404(Order, pk=pk)

        if(qty == str(int(oldOrder.getQuantity())) and payment_mode == oldOrder.getMode()):
            o = get_object_or_404(Order, pk=pk)
            messages.error(request, "Supplied details are identical")
            return render(request, "Kiosk/update_order_details.html", {'o':o})

        else:
            Order.objects.filter(pk=pk).update(qty=qty,payment_mode=payment_mode)
            messages.info(request, "Successfully updated order details")
            return redirect("view_order_details", pk=pk)

    else:
        o = get_object_or_404(Order, pk=pk)
        return render(request, "Kiosk/update_order_details.html", {'o':o})
        
def confirm_delete_order(request, pk):
    o = get_object_or_404(Order, pk=pk)
    return render(request, "Kiosk/confirm_delete_order.html", {'o':o})

def delete_order(request, pk):
    Order.objects.get(pk=pk).delete()
    messages.info(request, "Successfully deleted order")
    return redirect('homepage')

# FOOD-CENTERED
def view_food_items(request):
    food_objects = Food.objects.all()
    return render(request, "Kiosk/view_food_items.html", {'foods':food_objects})

def update_food_item(request, pk):
    if(request.method == "POST"):
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")

        #Make a list of all Food objects, lowercase each object and append to flistlower if it is equal to lowercase of name
        namelower = name.lower()
        flist = Food.objects.filter()
        flistlower = []
        for fobject in flist:
            fobjectlower = fobject.getName().lower()
            flistlower.append(fobjectlower)

        oldFood = get_object_or_404(Food, pk=pk)

        #If name is the same
        if(namelower == oldFood.getName().lower()):
            #If descrption, and price are the same
            if(description == oldFood.getDesc() and price == str(oldFood.getPrice())):
                f = get_object_or_404(Food, pk=pk)
                messages.error(request, 'Supplied details are identical')
                return render(request, "Kiosk/update_food_item.html", {'f':f})
            #If description and price are not the same
            else:
                Food.objects.filter(pk=pk).update(description=description, price=price)
                messages.info(request, "Successfully updated food item")
                return redirect('view_food_items')

        #If name already exists in flistlower
        elif(namelower in flistlower):
            f = get_object_or_404(Food, pk=pk)
            messages.error(request, 'Food item already exists')
            return render(request, "Kiosk/update_food_item.html", {'f':f})
        
        #If name does not exist in flistlower
        else:
            Food.objects.filter(pk=pk).update(name=name, description=description, price=price)
            messages.info(request, 'Successfully updated food item')
            return redirect('view_food_items')

    else:
        f = get_object_or_404(Food, pk=pk)
        return render(request, "Kiosk/update_food_item.html", {'f':f})

def confirm_delete_food(request, pk):
    f = get_object_or_404(Food, pk=pk)
    return render(request, "Kiosk/confirm_delete_food.html", {'f':f})

def delete_food(request, pk):
    messages.info(request, "Successfully deleted food item")
    Food.objects.filter(pk=pk).delete()
    return redirect('view_food_items')

def add_food_item(request):
    now = datetime.now()
    if(request.method=="POST"):
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        created_at = now
        
        namelower = name.lower()
        flist = Food.objects.filter()
        flistlower = []
        for fobject in flist:
            fobjectlower = fobject.getName().lower()
            if(fobjectlower==namelower):
                flistlower.append(fobjectlower)
        
        if(len(flistlower) > 0):
            messages.error(request, "Dish already exists")
            return render(request, "Kiosk/add_food_item.html")
        
        else:
            Food.objects.create(name=name, description=description, price=price, created_at=created_at)
            return redirect('view_food_items')

    else:
        return render(request, 'Kiosk/add_food_item.html')

# CUSTOMER-CENTERED
def view_customers(request):
    customer_objects = Customer.objects.all()
    return render(request, "Kiosk/view_customers.html", {'customers':customer_objects})

def update_customer_details(request, pk):
    if(request.method == "POST"):
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        
        #Make a list of all Customer objects, lowercase each object and append to clistlower if it is equal to lowercase of name
        namelower = name.lower()
        clist = Customer.objects.filter()
        clistlower = []
        for cobject in clist:
            cobjectlower = cobject.getName().lower()
            clistlower.append(cobjectlower)

        oldCustomer = get_object_or_404(Customer, pk=pk)
        
        #If name is the same
        if(namelower == oldCustomer.getName().lower()):
            #If address and city are the same
            if(address == oldCustomer.getAddress() and city == oldCustomer.getCity()):
                messages.error(request, "Supplied details are identical")
                c = get_object_or_404(Customer, pk=pk)
                return render(request, "Kiosk/update_customer_details.html", {'c':c})
            #If address and city are not the same
            else:
                Customer.objects.filter(pk=pk).update(address=address, city=city)
                messages.info(request, 'Successfully updated customer details')
                return redirect('view_customers')

        #If name already exists in clistlower
        elif(namelower in clistlower):
            messages.error(request, 'Customer name is taken')
            c = get_object_or_404(Customer, pk=pk)
            return render(request, "Kiosk/update_customer_details.html", {'c':c})

        #If name does not exist in clistlower
        else:
            Customer.objects.filter(pk=pk).update(name=name, address=address, city=city)
            messages.info(request, 'Successfully updated customer details')
            return redirect('view_customers')
    
    else:
        c = get_object_or_404(Customer, pk=pk)
        return render(request, 'Kiosk/update_customer_details.html', {'c':c})

def confirm_delete_customer(request, pk):
    c = get_object_or_404(Customer, pk=pk)
    return render(request, "Kiosk/confirm_delete_customer.html", {'c':c})    

def delete_customer(request, pk):
    messages.info(request, 'Successfully deleted customer')
    Customer.objects.filter(pk=pk).delete()
    return redirect('view_customers')