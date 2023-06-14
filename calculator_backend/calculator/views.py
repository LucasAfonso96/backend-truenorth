import requests
import json
import math

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from .models import Operation, Record, CustomUser
from .serializers import UserSerializer, OperationSerializer


class TokenObtainPairView(TokenObtainPairView):
    pass


class TokenRefreshView(TokenRefreshView):
    pass


User = get_user_model()


def index(request):
    return render(request, 'index.html')


@api_view(['PUT'])
def user_status_view(request, user_id):
    print('id', user_id)
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')

    if new_status not in ['active', 'inactive']:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    user.status = new_status
    user.save()

    return Response({'message': 'User status updated successfully'})


@api_view(['POST'])
@csrf_exempt
def register(request):
    print('REGISTEEEEEEEEEEEEEER')
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'error': 'email already exists.'}, status=400)

    user = CustomUser.objects.create_user(email=email, password=password)
    user.save()
    return JsonResponse({'message': 'User registered successfully.'}, status=201)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None and user.status == 'active':
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return Response({'token': f'Bearer {str(access_token)}'}, status=200)

    elif user is not None and user.status == 'inactive':
        return HttpResponse({'error': 'User is inactive. Contact the administrator for assistance'}, status=403)
    else:
        return HttpResponse({'error': 'Invalid email or password.'}, status=401)


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return JsonResponse({'success': True})


@api_view(['GET'])
def user_list(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def operation_list(request):
    queryset = Operation.objects.all()
    serializer = OperationSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_operation(request):
    print('entrando')
    operation_type = request.data.get('type')
    cost = request.data.get('cost')
    print(operation_type, cost)

    if not operation_type or not cost:
        return Response({'error': 'Operation type and cost are required.'}, status=400)

    operation, created = Operation.objects.get_or_create(type=operation_type, cost=cost)

    if created:
        return Response({'message': 'Operation created successfully.'}, status=201)
    else:
        return Response({'message': 'Operation already exists.'}, status=400)


@api_view(['POST'])
def calculate(request):
    number1 = request.data.get('number1')
    number2 = request.data.get('number2')
    operation_type = request.data.get('operationType')

    operation = get_object_or_404(Operation, type=operation_type)
    user = request.user
    if user.user_balance < operation.cost:
        return Response({'error': 'Insufficient balance.', 'user_balance': user.user_balance}, status=400)

    user.user_balance = float(user.user_balance) - operation.cost
    user.save()

    operations = {
        'addition': lambda x, y: x + y,
        'subtraction': lambda x, y: x - y,
        'multiplication': lambda x, y: x * y,
        'division': lambda x, y: x / y,
        'square_root': lambda x, y: math.sqrt(x),
        'random_string': lambda x, y: generate_random_string(x)
    }

    operation_func = operations.get(operation.type)
    if operation_func:
        result = operation_func(number1, number2)
        record = Record.objects.create(
            operation=operation,
            user=user,
            amount=operation.cost,
            operation_response=result
        )
        print('r', result)
        record.save()
        return Response({'result': result, 'user_balance': user.user_balance})

    else:
        return HttpResponse("Server Error", status=500)


def generate_random_string(num):
    response = requests.get(f'https://www.random.org/strings/?num={num}&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new')
    if response.status_code == 200:
        random_string = response.text.strip()
        return random_string
    else:
        return HttpResponse("Error occurred during random API call", status=500)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_user_records(request):
    print('recooords')
    user = request.user
    records = Record.objects.filter(user=user, is_deleted=False)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by in ['id', 'date', 'operation_response', 'amount', 'cost']:
        if sort_by == 'cost':
            records = records.order_by('operation__cost')
        elif sort_by == 'type':
            records = records.order_by('operation__type')
        else:
            records = records.order_by(sort_by)

    # Search by di
    search_query = request.GET.get('search')
    if search_query:
        records = records.filter(id__icontains=search_query)

    # Pagination
    paginator = Paginator(records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    # Delete record
    if request.method == 'POST':
        record_id = request.data.get('record_id')
        try:
            record = Record.objects.get(id=record_id, user=user)
            record.is_deleted = True
            record.save()
            return JsonResponse({'message': 'Record deleted successfully'})
        except Record.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)

    # Serialized records for the current page
    serialized_records = [
        record.serialize()
        for record in page]

    return JsonResponse({
        'records': serialized_records,
        'totalRecords': paginator.count,
        'currentPage': page.number,
    })
