from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from useraccount.models import CustomUser, Address
from useraccount.serializers import CustomUserSerializer, AddressSerializer


class UserView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_address(self, obj):
        try:
            address = Address.objects.get(user=obj)
            # This is important - pass the context
            return AddressSerializer(address, context=self.context).data
        except Address.DoesNotExist:
            return None


class UserDeleteView(generics.RetrieveDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


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
