from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer





@api_view(['GET', 'POST'])
def account_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Destination
from .serializers import DestinationSerializer


@api_view(['GET', 'POST'])
def destination_list(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def destination_detail(request, pk):
    try:
        destination = Destination.objects.get(pk=pk)
    except Destination.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DestinationSerializer(destination)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DestinationSerializer(destination, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        destination.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer

@api_view(['POST'])
def incoming_data(request):
    # Logic to handle incoming data
    data = request.data
    app_secret_token = request.headers.get('CL-X-TOKEN')

    if not app_secret_token:
        return Response({"error": "Unauthenticated"}, status=401)

    try:
        account = Account.objects.get(app_secret_token=app_secret_token)
    except Account.DoesNotExist:
        return Response({"error": "Account not found"}, status=404)

    # Send data to destinations
    send_data_to_destinations(account, data)

    return Response({"message": "Data received and sent to destinations successfully"}, status=200)

def send_data_to_destinations(account, data):
    # Logic to send data to destinations based on account and destination configurations
    destinations = Destination.objects.filter(account=account)
    for destination in destinations:
        # Implement sending data to each destination
        pass  # Placeholder for sending data to destination




# data_handler/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Destination
import json

@csrf_exempt
def incoming_data_view(request):
    if request.method == 'POST':
        # Check if the request contains JSON data
        if not request.content_type == 'application/json':
            return JsonResponse({'message': 'Invalid Data'}, status=400)

        # Extract app secret token from request headers
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return JsonResponse({'message': 'Unauthenticated'}, status=401)

        # Find the account associated with the app secret token
        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'Unauthenticated'}, status=401)

        # Extract JSON data from request body
        data = json.loads(request.body)

        # Process the data and send it to destinations
        # Implement your logic here to send data to destinations

        return JsonResponse({'message': 'Data received and processed successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)
