from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        # Изменение: форматируем сумму с двумя знаками после запятой
        return f"{self.type} - {self.amount:.2f} ({self.description})"
