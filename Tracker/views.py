from django.shortcuts import render, redirect
from .models import TrackingHistory, CurrentBalance, UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login/')

    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture') 

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            profile_picture=profile_picture if profile_picture else 'default.jpg'
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('/login/')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="login_view")
def base(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))

        
        current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)

        if amount == 0:
            messages.warning(request, "Amount cannot be zero")
            return redirect('/')

        expense_type = "CREDIT" if amount > 0 else "DEBIT"

        TrackingHistory.objects.create(
            user=request.user,
            current_balance=current_balance,
            amount=amount,
            expense_type=expense_type,
            description=description
        )

        current_balance.current_balance += amount
        current_balance.save()

        return redirect('/')

    
    current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)
    transactions = TrackingHistory.objects.filter(user=request.user)
    income = sum(t.amount for t in transactions if t.expense_type == "CREDIT")
    expense = sum(t.amount for t in transactions if t.expense_type == "DEBIT")

    
    


    context = {
        'income': income,
        'expense': expense,
        'transactions': transactions,
        'current_balance': current_balance,
        'profile': user_profile,   
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


