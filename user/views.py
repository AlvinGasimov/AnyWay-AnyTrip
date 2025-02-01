from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from booking.models import Order
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "user/register.html", {"error": "Bu email artıq qeydiyyatdan keçib!"})

        CustomUser.objects.create(full_name=full_name, email=email, phone=phone)
        return redirect("login")
    return render(request, "user/register.html")



def login(request):
    if request.method == "POST":
        email = request.POST.get("username")


        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return render(request, "user/login.html", {"error": "Bu email ilə istifadəçi tapılmadı!"})
            
        verification_code = random.randint(100000, 999999)
        
        send_mail(
            "Daxil olma üçün təsdiq kodu",
            f"Sizin təsdiq kodunuz: {verification_code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        request.session["user_email"] = email
        request.session["user_id"] = user.id
        request.session["user_full_name"] = user.full_name
        request.session["verification_code"] = verification_code

        return redirect("submitemail")  # Kodu daxil etmə səhifəsinə yönləndiririk

    return render(request, "user/login.html")


def submitemail(request):
    if request.method == "POST":
        entered_code = int(request.POST.get("number"))
        correct_code = request.session.get("verification_code")
        
        if entered_code == correct_code:
            return redirect("home")
        else:
            return render(request, "user/submitemail.html", {"error": "Yanlış kod daxil etdiniz. Yenidən cəhd edin."})

    return render(request, "user/submitemail.html")

def account(request):
    user_id = request.session.get("user_id")
    user = CustomUser.objects.get(id=user_id)
    orders = Order.objects.filter(user=user)
    context = {
        "orders": orders,
    }
    return render(request, 'user/account.html', context)


def logout(request):
    auth_logout(request)
    request.session.flush()

    return redirect("login")