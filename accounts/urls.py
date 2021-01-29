from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginPage,name="loginPage"),
    path('register/',views.registerPage,name="registerPage"),
    path('logout/',views.logoutUser,name='logoutUser'),

    path('user/',views.userPage,name="userPage"),
    path('product/',views.product,name="product"),
    path('customer/<pk>/',views.customer,name="customer"),
    path('setting/',views.accountSetting,name="accountSetting"),

    path('create_order/<pk>',views.createOrder,name="createOrder"),
    path('update_order/<pk>',views.updateOrder,name="updateOrder"),
    path('delete_order/<pk>',views.delete,name="delete"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),
]


# submit email form                             PasswordResetView.as_view()
# Email sent succes message                     PasswordResetDoneView.as_view()
# link to passworde reset form in email         PasswordResetConfirmView.as_view()
# password successfully change message          PasswordResetCompleteView.as_view()