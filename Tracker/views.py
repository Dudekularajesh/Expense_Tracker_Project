from django.shortcuts import render, redirect
from .models import TrackingHistory, CurrentBalance
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.success(request, "Username not found") 
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)
        if not user:
            messages.success(request, "Incorrect password") 
            return redirect('/login/')
        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.success(request, "Username is already taken") 
            return redirect('/register/')
        
        user = User.objects.create(
            username = username,
            first_name = first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created") 
        return redirect('/register/')
    return render(request , 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="login_view")
def base(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))

        # Each user gets their own CurrentBalance
        current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)

        if amount == 0:
            messages.warning(request, "Amount cannot be zero")
            return redirect('/')

        expense_type = "CREDIT" if amount > 0 else "DEBIT"

        tracking_history = TrackingHistory.objects.create(
            user=request.user,
            current_balance=current_balance,
            amount=amount,
            expense_type=expense_type,
            description=description
        )

        current_balance.current_balance += amount
        current_balance.save()

        return redirect('/')

    # Fetch user-specific data only
    current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)
    transactions = TrackingHistory.objects.filter(user=request.user)
    income = sum(t.amount for t in transactions if t.expense_type == "CREDIT")
    expense = sum(t.amount for t in transactions if t.expense_type == "DEBIT")

    context = {
        'income': income,
        'expense': expense,
        'transactions': transactions,
        'current_balance': current_balance,
    }
    return render(request, 'base.html', context)


@login_required(login_url="login_view")
def delete_transaction(request, id):
    tracking_history = TrackingHistory.objects.filter(id=id, user=request.user).first()

    if tracking_history:
        current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)
        current_balance.current_balance -= tracking_history.amount
        current_balance.save()
        tracking_history.delete()

    return redirect('/')

