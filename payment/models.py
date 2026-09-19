from django.db import models



class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        PENDING = "PENDING", "Pending"

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(max_length=7, choices=PaymentStatus.choices)
    type = models.CharField(max_length=7, choices=PaymentType.choices)
    borrowing = models.ForeignKey("borrowing.Borrowing", on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment #{self.id} for Borrowing #{self.borrowing_id}"