from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('predict/', views.predict, name='predict'),
    path('result/', views.result, name='result'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('researcher/', views.researcher, name='researcher'),
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback-list/', views.feedback_list, name='feedback_list'),
]


    

    
    
    # Logout
'''path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),'''

