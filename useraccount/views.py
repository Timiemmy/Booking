from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Address
from .serializers import UserSerializer, AddressSerializer



class UserView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_address(self, obj):
        try:
            address = Address.objects.get(user=obj)
            # This is important - pass the context
            return AddressSerializer(address, context=self.context).data
        except Address.DoesNotExist:
            return None


class UserDeleteView(generics.RetrieveDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    
    def perform_create(self, serializer):
        user_id = self.kwargs.get('pk')
        user = CustomUser.objects.get(pk=user_id)
        serializer.save(user=user)


class AddressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()