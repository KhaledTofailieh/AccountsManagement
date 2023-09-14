import time

from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
import re


# UserAuthSerializer used for authentication process.
class UserAuthSerializer(serializers.ModelSerializer):
    TYPE_CHOICES = ('Ad', 'St', 'Cu')
    STATUS_CHOICES = ('Ac', 'Di')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'birth_date', 'last_name', 'email', 'type', 'status', 'tokens']

    email = serializers.EmailField()
    type = serializers.ChoiceField(choices=User.Type.choices, default='Cu')
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='Ac')
    birth_date = serializers.DateField(default=None)

    tokens = serializers.SerializerMethodField()

    # validators on input.
    def validate_email(self, value):
        # Custom email validation logic
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_type(self, value):
        if value not in self.TYPE_CHOICES:
            raise serializers.ValidationError("Invalid 'type' value")
        return value

    def validate_birth_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be greater that present")
        return value

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        data = {
            'name': f'{user.first_name} {user.last_name}',
            "access": access
        }
        return data
