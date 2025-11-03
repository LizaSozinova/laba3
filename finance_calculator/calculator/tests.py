from django.test import TestCase
from django.urls import reverse
from .models import Transaction

class TransactionModelTest(TestCase):
    def test_create_transaction(self):
        # Создаем доход
        income = Transaction.objects.create(type='income', amount=1000, description='Salary')
        self.assertEqual(income.type, 'income')
        self.assertEqual(income.amount, 1000)
        self.assertEqual(income.description, 'Salary')

        # Создаем расход
        expense = Transaction.objects.create(type='expense', amount=500, description='Groceries')
        self.assertEqual(expense.type, 'expense')
        self.assertEqual(expense.amount, 500)
        self.assertEqual(expense.description, 'Groceries')

    def test_balance_calculation(self):
        # Создаем доходы и расходы
        Transaction.objects.create(type='income', amount=1000, description='Salary')
        Transaction.objects.create(type='expense', amount=500, description='Groceries')
        Transaction.objects.create(type='income', amount=1500, description='Bonus')

        # Проверяем баланс
        total_income = sum(t.amount for t in Transaction.objects.filter(type='income'))
        total_expense = sum(t.amount for t in Transaction.objects.filter(type='expense'))
        balance = total_income - total_expense

        # Ожидаемый баланс: 1000 + 1500 - 500 = 2000
        self.assertEqual(balance, 2000)

    def test_transaction_str(self):
        # Проверяем, что строковое представление транзакции правильное
        transaction = Transaction.objects.create(type='income', amount=1000, description='Salary')
        self.assertEqual(str(transaction), 'income - 1000.00 (Salary)')

    class TransactionViewsTest(TestCase):
        def test_home_page_loads(self):
            # Загружаем главную страницу
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Balance")

        def test_balance_calculation_on_home_page(self):
            # Создаем транзакции
            Transaction.objects.create(type='income', amount=1000, description='Salary')
            Transaction.objects.create(type='expense', amount=500, description='Groceries')

            # Проверяем, что баланс на главной странице корректно отображается
            response = self.client.get(reverse('home'))
            self.assertContains(response, "Balance: 500.00")

        def test_add_transaction(self):
            # Проверяем, что можно добавить транзакцию через форму
            data = {
                'type': 'income',
                'amount': 1000,
                'description': 'Salary'
            }
            response = self.client.post(reverse('home'), data)
            self.assertEqual(response.status_code, 302)  # После успешного добавления перенаправит

            # Проверяем, что транзакция была добавлена в базу данных
            transaction = Transaction.objects.last()
            self.assertEqual(transaction.type, 'income')
            self.assertEqual(transaction.amount, 1000)
            self.assertEqual(transaction.description, 'Salary')

