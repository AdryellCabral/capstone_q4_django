from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.serializers import UserSerializer, CustomerSerializer, CustomerUpdateSerializer,\
     PartnerResponseSerializer, AddressPartnerSerializer, ServiceTypePartnerSerializer,\
          PartnerCheckSerializer
from accounts.models import User, Customer, Partner 
from orders.models import ServiceType, Address
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class AccountCustomerView(APIView):

    def post(self, request):

        data = request.data
        data['username'] = data['email']

        data_serializer = UserSerializer(data=request.data)
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
               
        try:        
            new_user = User.objects.create_user(**data)
            new_customer = Customer.objects.create(user_customer=new_user)
            serialized = CustomerSerializer(new_customer)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)


class LoginCustomerView(APIView):

    def post(self, request):

        data = request.data

        try:
            username = data['email']
            password = data ['password']
        except KeyError:
            return Response({'message': 'You must inform the email and the password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username = data['email'],
            password = data ['password']
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Email or password invalid.'}, status=status.HTTP_400_BAD_REQUEST)


class AccountCustomerByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
       
    def get(self, request, customer_id=''):

        try:        
            customer = Customer.objects.get(id=customer_id)
            serialized = CustomerSerializer(customer)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except:               
            return Response({'message': 'Invalid customer_id'}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, customer_id=''):

        user = request.user
        update_data = request.data

        try:
            customer = Customer.objects.get(id=customer_id)                
        except:
            return Response({'message': 'Invalid customer_id'}, status=status.HTTP_404_NOT_FOUND)


        if user.id == customer.user_customer.id:
            try:
                data_serializer = CustomerUpdateSerializer(customer, data=update_data)
                if not data_serializer.is_valid():
                    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
                data_serializer.save()

                updated_customer = Customer.objects.get(id=customer_id)
                serialized = CustomerSerializer(updated_customer)

                return Response(serialized.data, status=status.HTTP_200_OK)
            except IntegrityError as e:
                return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'message': 'You can update only your own data.'}, status=status.HTTP_403_FORBIDDEN)
          

class AccountPartnerView(APIView):

    def post(self, request):

        data = request.data
        data['username'] = data['email']
        data_gender = data.pop('gender')
        data_birthday = data.pop('birthday')
        data_describe = data.pop('describe')
        data_service = data.pop('services')
        data_address = data.pop('address')  
        
        data_user_serializer = UserSerializer(data=request.data)
        if not data_user_serializer.is_valid():
            return Response(data_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
               
        try:        
            data_address_serializer = AddressPartnerSerializer(data=data_address)
            if not data_address_serializer.is_valid():
                return Response(data_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data_service_serializer = ServiceTypePartnerSerializer(data={'name': data_service})
            if not data_service_serializer.is_valid():
                return Response(data_service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
                        
            new_user = User.objects.create_user(**data)
            service = ServiceType.objects.get(name=data_service)
            address = Address.objects.get_or_create(**data_address)
            
            partner_data_to_check ={
                'user_partner': data,
                'gender': data_gender,
                'birthday': data_birthday,
                'describe': data_describe
            }

            data_partner_serializer = PartnerCheckSerializer(data=partner_data_to_check)
            if not data_partner_serializer.is_valid():
                return Response(data_partner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

            partner_data ={
                'user_partner': new_user,
                'gender': data_gender,
                'birthday': data_birthday,
                'describe': data_describe,
                'service': service,
                'address': address[0]
            }

            new_partner = Partner.objects.create(**partner_data)
            serialized = PartnerResponseSerializer(new_partner)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)


class LoginPartnerView(APIView):

    def post(self, request):

        data = request.data

        try:
            username = data['email']
            password = data ['password']
        except KeyError:
            return Response({'message': 'You must inform the email and the password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username = data['email'],
            password = data ['password']
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Email or password invalid.'}, status=status.HTTP_400_BAD_REQUEST)

