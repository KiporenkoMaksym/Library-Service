from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE)


class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"


    class PaymentTypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"


    status = models.CharField(max_length=7, choices=PaymentStatusChoices.choices)
    type = models.CharField(max_length=7, choices=PaymentTypeChoices.choices)
    borrowing = models.ForeignKey("borrowing.Borrowing", on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
