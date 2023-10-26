from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False)
        )
        user.set_password(validated_data['password'])  # Set the password
        user.save()  # Save the user without returning the password
        return user

    def to_representation(self, instance):
        # Exclude the 'password' field from the serialized data
        data = super().to_representation(instance)
        data.pop('password', None)
        return data






