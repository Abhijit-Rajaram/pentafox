from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from app.models import UserDetails, Role 
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def user_creation(request):
    if request.method == "POST":
        id = request.POST.get('id', None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        role = request.POST.get('role', None)

        print(id, name, email, role)

        if not name or not email or not role:
            return JsonResponse({'data': 'Invalid Data'})
        
        if not id:
            try:
                with transaction.atomic():
                    user: User = User(username=name.strip(), email=email.strip())
                    user.password = make_password('password')
                    user.save()
                    
                    UserDetails.objects.create(role_id = role, user = user)
            except Exception as e:
                print(str(e))
                return JsonResponse({'data': 'Error'})
        else:
            try:
                user: UserDetails = UserDetails.objects.get(id=id)
                auth_user: User = user.user
                user.role_id = role
                user.save()

                auth_user.username = name.strip()
                auth_user.email = email.strip()
                auth_user.save()
            except UserDetails.DoesNotExist:
                return JsonResponse({'data': 'Invalid Data'})
        return JsonResponse({'data': 'Success'})
    
    roles = Role.objects.values('id', 'role')
    users = UserDetails.objects.values('id','user_id','user__username', 'user__first_name', 'user__email', 'user__is_active', 'role__role', 'role_id')
    return render(request,'user_details.html', {'roles':roles,'users':users})

def toggle_status(request):
    if request.method == "POST":
        id = request.POST.get('id', None)
        status = request.POST.get('status', None)

        if not id or not status:
            return JsonResponse({'data': 'Invalid Data'})
        try:
            user: User = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({'data': 'Invalid Data'})

        user.is_active = status
        user.save()

        print(user.is_active)
        return JsonResponse({'data': 'Success'})
    return JsonResponse({'data': 'Invalid request'})

def role(request):
    if request.method == "POST":
        id = request.POST.get('id', None)
        role = request.POST.get('role', None)

        if not role:
            return JsonResponse({'data': 'Invalid Data'})
        
        if not id:
            Role.objects.create(role=role.strip().upper())
        else:
            Role.objects.filter(id=id).update(role=role.strip().upper())

        return JsonResponse({'data': 'Success'})
def delete_user(request):
    if request.method == "POST":
        id = request.POST.get('id', None)

        if not id:
            return JsonResponse({'data': 'Invalid Data'})
        
        try:
            with transaction.atomic():
                user: UserDetails = UserDetails.objects.get(id = id)
                auth_user_id = user.user.id
                UserDetails.objects.filter(id=id).delete()
                User.objects.filter(id = auth_user_id).delete()
        except Exception as e:
            print(str(e))
            return JsonResponse({'data': 'Error'})
        return JsonResponse({'data': 'Success'})
        