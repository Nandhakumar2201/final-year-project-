from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Profile  # make sure this import points to where your Profile model is

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")

            if not all([name, email, password, role]):
                return JsonResponse({"error": "Missing fields"}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({"error": "User already exists"}, status=400)

            # Create the User
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()

            # Manually create the Profile with role
            profile = Profile.objects.create(user=user, role=role)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)



@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email and password required"}, status=400)

            user = authenticate(username=email, password=password)
            if user is not None:
                return JsonResponse({
                    "success": True,
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                    }
                })
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)