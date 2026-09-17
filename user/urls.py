from django.urls import path

from user.views import CreateUserView, ManageUserView


urlpatterns = [
    path("", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
