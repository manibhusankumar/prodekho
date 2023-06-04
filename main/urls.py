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
    path('single-listing/<slug:slug>/', views.ListingSingleView.as_view(), name='single-listing'),

    # path('single-agent/<slug:slug>/', views.AgentSingleView.as_view(), name='single-agent'), ListingSingleView
    path('agent_list', AgentListView.as_view(), name='lis'),
    path('about/', AboutView.as_view(), name='about'),
    path('my-profile', MyPofile.as_view(), name='my_profile'),
    path('not_fount', PageNotFoundView.as_view(), name='not_fount'),
    path('add-listing', AddListingView.as_view(), name='add_listing'),
    path("register/", SignUpView.as_view(), name='signup'),
    # path('login/', views.Login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('user/<int:pk>/edit/', UpdateProfileView.as_view(), name='edit_user'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path('use_profile',views.edit_profile,name='user_profile'),
    path('social', views.socialmedia, name='social'),
    # path('create_listing', views.create_listing,name='create_listing'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('create_listing', ListingCreateView.as_view(),name='create_listing'),
    path('dashboard_list', Dashboard_list.as_view(), name='dashboard_list'),
    path('listing/<int:id>/band_update/', views.listing_update, name='listing_update'),
    # path('agent-profile',AgentPofile.as_view(), name='agent_profile'),
    # path('agent/<int:pk>/edit/', AgentProfileView.as_view(), name='edit_agent'),
    # path('edit-agent', views.edit_agent_profile, name='edit_agent_profile'),
    path('agent_dashboard',AgentDashboard.as_view(), name='agent-dashboard'),
    path('search/', search_results, name='search_results'),
    path('booking', CreateBookView.as_view(), name='create_book'),
    path('booking-listing', BookingListView.as_view(), name='booking_listing'),
    # path('book', views.create_book, name='create_book'),


]