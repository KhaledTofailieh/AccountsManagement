from django.contrib.auth import user_logged_in
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.handlers import error_handler
from accounts.models import User
from accounts.serializers import UserAuthSerializer


# class based view, this time contain post method.
class SignUpView(APIView):
    def post(self, request):
        email = request.data.get('email')

        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'This email is not available.'}, status=status.HTTP_400_BAD_REQUEST)
        # UserAuthentication serializer
        serializer = UserAuthSerializer(data=request.data)

        # validate fields with serializers.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
@error_handler
# functional view that responsible on authenticate user(give him token)
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']
        # this will raise an error if criteria doesn't meet.
        user = User.objects.get(email=email, password=password, status=User.Status.ACTIVE)

        # if user is fetched correctly with requested criteria.
        if user:
            try:
                serializer = UserAuthSerializer(user)
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)
