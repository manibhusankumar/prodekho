from django.urls import path

from main import views
from main.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('slider/', SliderView.as_view(), name='slider'),
    path('video/', VideoView.as_view(), name='video'),
    path('slide-show/', SlideShowView.as_view(), name='slide-show'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('agent-list', AgentView.as_view(), name='agent-list'),
    path('agency_list/', AgencyView.as_view(), name='agency-list'),
    path('single-blog/<slug:slug>/', views.BlogSingleView.as_view(), name='single-blog'),
    path('about/', AboutView.as_view(), name='about'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('my-profile', MyPofile.as_view(), name='my_profile'),
    path('not_fount', PageNotFoundView.as_view(), name='not_fount'),
    path('add', AddListingView.as_view(), name='add'),
    path("register/", SignUpView.as_view(), name='signup'),
    path('login/', views.Login, name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('user/<int:pk>/edit/', UpdateProfileView.as_view(), name='edit_user'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

]