from django.urls import path

from Users.views import Register, LogIn, LogOutView

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', LogIn.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout")
]
