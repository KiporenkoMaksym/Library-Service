from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"

    @property
    def first_last_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"


    class PaymentTypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"


    status = models.CharField(
        max_length=7,
        choices=PaymentStatusChoices.choices
    )
    type = models.CharField(
        max_length=7,
        choices=PaymentTypeChoices.choices
    )
    borrowing = models.ForeignKey(
        "borrowing.Borrowing",
        on_delete=models.CASCADE
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.status} - {self.borrowing.book.title}"
