from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm

def home(request):
    # Получаем все транзакции
    transactions = Transaction.objects.all()

    # Начальный баланс
    balance = 0

    # Обновляем баланс, учитывая тип транзакции
    for transaction in transactions:
        if transaction.type == 'income':  # Для дохода увеличиваем баланс
            balance += transaction.amount
        elif transaction.type == 'expense':  # Для расхода уменьшаем баланс
            balance -= transaction.amount

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем транзакцию
            return redirect('home')  # Перенаправляем на главную страницу после добавления

    else:
        form = TransactionForm()

    return render(request, 'home.html', {
        'transactions': transactions,
        'balance': balance,
        'form': form
    })
