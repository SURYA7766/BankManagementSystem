from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserDetailsForm, TransactionsForm
from django.core.exceptions import ObjectDoesNotExist
from .models import models
from .models import UserDetails
from django.http import HttpResponse
from .models import UserDetails, Transactions

# Create your views here.


def Home(request):
    return render(request, 'home.html')


def loginuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('UserInterface1')
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if(user is None):
            return render(request, 'loginuser.html', {'form': AuthenticationForm(), 'error': "Sorry the User Doesn't Exists"})
        else:
            login(request, user)
            return redirect('UserInterface1')


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('Home')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('registerdata')
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': UserCreationForm, 'error': "* User Already Exists"})
        else:
            return render(request, 'signupuser.html', {'form': UserCreationForm, 'error': "* Password Mismatch"})


def registerdata(request):
    form = UserDetailsForm()
    if(request.method == "POST"):
        form = UserDetailsForm(request.POST)
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.user_id = request.user
            instance.save()
            return redirect('UserInterface1')
    return render(request, 'registerdata.html', {'form': form})


def UserInterface1(request):
    if request.method == "POST":
        return redirect('Transfer')
    else:
        try:
            vals1 = Transactions.objects.filter(
                UserName=request.user)  # debit
            vals2 = Transactions.objects.filter(
                ReceiptantName=request.user)  # credit
            user = UserDetails.objects.get(user_id_id=request.user)
            x = user.moneyAvailable
            if (x is None):
                x = 0
        except ObjectDoesNotExist:
            x = "0"
            return render(request, 'UserInterface1.html',
                          {'response': request, 'user': x})

    return render(request, 'UserInterface1.html', {'response': request, 'user': x, 'vals1': vals1, "vals2": vals2})


def Transfer(request):
    Transactions = TransactionsForm()
    if(request.method == "POST"):
        form = TransactionsForm(request.POST)
        user1 = UserDetails.objects.get(user_id_id=request.user)
        if (form.is_valid()):
            instance = form.save(commit=False)
            if(instance.Money > user1.moneyAvailable):
                return render(request, 'TransactionsForm.html', {"TransactionsForm": Transactions, "Error": "Sorry out of Pocket! No Money! to make transaction😑"})
            try:
                instance.UserName = request.user
                instance.UserId = request.user
                user3 = User.objects.get(username=instance.ReceiptantName)
                user2 = UserDetails.objects.get(user_id_id=user3.pk)
                x = user1.moneyAvailable
            except ObjectDoesNotExist:
                return render(request, 'TransactionsForm.html', {'error': "User Not found"})
            user1.moneyAvailable = user1.moneyAvailable - instance.Money
            user2.moneyAvailable = user2.moneyAvailable + instance.Money
            if (user1.pk == user2.pk):
                user1.moneyAvailable = x
                user2.moneyAvailable = x
            user1.save()
            user2.save()
            instance.save()
            return redirect('TransactionSuccess')
    return render(request, 'TransactionsForm.html', {"TransactionsForm": Transactions})


def TransactionSuccess(request):
    if request.method == "POST":
        return redirect("UserInterface1")
    user = UserDetails.objects.get(user_id_id=request.user)
    x = user.moneyAvailable
    return render(request, "TransactionDone.html", {'x': x})
