from django.urls import path
from . import views
from django.contrib.auth.views import (PasswordResetView, 
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView
                                       )

urlpatterns = [
    path('cadastro/', views.cadastrar, name='cadastro'),
    path('login/', views.login, name='login'),
    path('sair/', views.sair, name='sair'),
    path('home/', views.home, name='home'),
    path('password_reset/', PasswordResetView.as_view(template_name = 'registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html'), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]



