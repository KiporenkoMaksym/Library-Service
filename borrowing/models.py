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
