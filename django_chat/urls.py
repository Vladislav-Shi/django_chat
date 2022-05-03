from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include
from chat.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
    path('signin/',
         LoginView.as_view(template_name='auth/login.html',
                           next_page='chat:index'),
         name='signin_page'),
    path('exit/', LogoutView.as_view(next_page='chat:index'),
         name='signout_page'),
    path('signup/', RegisterView.as_view(), name='signup_page')
]