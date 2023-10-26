from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .serializers import CustomUserSerializer  # Import your user serializer
from .models import CustomUser
from .permissions import IsAdminOrReadOnly

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            
            date_of_birth = serializer.validated_data.get('date_of_birth')
            min_age = 15  
            user_age = (timezone.now().date() - date_of_birth).days // 365  

            
            if user_age < min_age:
                raise ValidationError({'date_of_birth': 'You must be at least 15 years old to register.'})

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrReadOnly]
