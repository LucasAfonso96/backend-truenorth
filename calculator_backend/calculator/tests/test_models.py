from django.test import TestCase
from calculator.models import CustomUser, Operation, Record
from django.contrib.auth import get_user_model

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.user_balance, 10.0)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.user_data)
        self.assertEqual(admin_user.email, self.user_data['email'])
        self.assertTrue(admin_user.check_password(self.user_data['password']))
        self.assertEqual(admin_user.user_balance, 10.0)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class OperationModelTest(TestCase):
    def test_create_operation(self):
        operation = Operation.objects.create(type='addition', cost=2.0)
        self.assertEqual(operation.type, 'addition')
        self.assertEqual(operation.cost, 2.0)

class RecordModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        self.operation = Operation.objects.create(type='addition', cost=2.0)
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_create_record(self):
        record = Record.objects.create(
            user=self.user,
            operation=self.operation,
            amount=2.0,
            operation_response='4.0',
        )
        self.assertEqual(record.user, self.user)
        self.assertEqual(record.operation, self.operation)
        self.assertEqual(record.amount, 2.0)
        self.assertEqual(record.operation_response, '4.0')
