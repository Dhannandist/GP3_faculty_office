from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# login
def login_view(req):
    # cek kalo udah login
    if req.user.is_authenticated:
        return redirect("dashboard")
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        user = authenticate(req, username=username, password=password)
        # buat sementara redirect ke admin panel
        if user is not None:
            login(req, user)
            # return redirect("admin:index")
            return redirect("dashboard")
        else:
            messages.error(req, "Masukan username dan password yang benar!")

    return render(req, "login.html")


def logout_view(req):
    logout(req)
    messages.success(req, "Berhasil logout!")
    return redirect("login")
