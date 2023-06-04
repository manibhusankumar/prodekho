from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout

from Prop_dekho import settings
from main.forms import *
from main.models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout




# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepages'] = HomePage.objects.all()[:1]
        context['property'] = Listing.objects.all()
        context['genres'] = Navbar.objects.all()
        context['agents'] = UserProfile.objects.all()
        context['cities']= City.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['sports'] = CompanySupport.objects.all()
        # user = self.request.user
        # listing = Listing.objects.filter(user=user).count()
        # context['listing'] = listing
        usernames = []
        # for listing in context['property']:
        #     user = User.objects.get(id=listing.user_id)
        #     usernames.append(user.username)
        # context['listing_usernames'] = usernames
        return context




class SliderView(TemplateView):
    template_name = 'index2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepages'] = HomePage.objects.all()[:1]
        context['property'] = Listing.objects.all()
        context['sliders'] = Slider.objects.all()[:1]
        context['genres'] = Navbar.objects.all()
        context['agents'] = UserProfile.objects.all()
        context['cities'] = City.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        return context


class VideoView(TemplateView):
    template_name = 'index3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepages'] = HomePage.objects.all()[:1]
        context['property'] = Listing.objects.all()
        context['sliders'] = Slider.objects.all()[:1]
        context['genres'] = Navbar.objects.all()
        context['agents'] = UserProfile.objects.all()
        context['cities'] = City.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        return context


class SlideShowView(TemplateView):
    template_name = 'index4.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepages'] = HomePage.objects.order_by('-id')[:1]
        context['property'] = Listing.objects.all()
        context['sliders'] = Slider.objects.all()[:1]
        context['genres'] = Navbar.objects.all()
        context['agents'] = UserProfile.objects.all()
        context['cities'] = City.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()

        return context


class BlogView(TemplateView):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        context['blog'] = Blog.objects.all()
        context['news'] = News.objects.all()
        return context


class BlogSingleView(DetailView):
    model = Blog
    template_name = 'blog-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class AgentView(TemplateView):
    template_name = 'agent-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class AgencyView(TemplateView):
    template_name = 'agency-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context

# class AgentSingleView(DetailView):
#     model = Agent
#     template_name = 'agent-single.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['genres'] = Navbar.objects.all()
#         context['blogs'] = b.objects.all()
#         return context


class AgentListView(ListView):
    model = UserProfile
    template_name = 'dashboard-agents.html'
    paginate_by = 6


    def get_queryset(self):
        return UserProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        context['cities'] = City.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aboutus'] = AboutUs.objects.all()[:1]
        context['companystory'] = CompanyStory.objects.all()
        context['property'] = Listing.objects.all()
        context['genres'] = Navbar.objects.all()
        context['agents'] = UserProfile.objects.all()
        context['teams'] = Team.objects.all()
        context['sports'] = CompanySupport.objects.all()
        return context


class ContactView(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        user = self.request.user
        listing = Listing.objects.filter(user=user).count()
        context['listing'] = listing
        booking = Booking.objects.filter(is_booked=True).count()
        context['booking'] = booking
        return context



class MyPofile(TemplateView):
    template_name = 'dashboard-myprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class Dashboard_list(ListView):
    model = Listing
    template_name = 'dashboard-listing-table.html'
    paginate_by = 2

    def get_queryset(self):
        user = self.request.user
        qs = Listing.objects.filter(user=user)
        sort_by = self.request.GET.get('sort_by')
        search_query = self.request.GET.get('search_query')
        if sort_by == 'oldes':
            qs = qs.order_by('-id')
        # elif sort_by == 'average_rating':
        #     qs = qs.order_by('-average_rating')
        elif sort_by == 'name_az':
            qs = qs.order_by('title')
        elif sort_by == 'name_za':
            qs = qs.order_by('-title')
        if search_query:
            qs = qs.filter(title__icontains=search_query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['selected_sort_option'] = self.request.GET.get('sort_by')
        context['search_query'] = self.request.GET.get('search_query')
        return context


class PageNotFoundView(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


# class UserRegistrationView(CreateView):
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy('index')
#     template_name = 'footer.html'


class AddListingView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard-add-listing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        context['category'] = Category.objects.all()
        context['cities'] = City.objects.all()
        context['genres'] = Navbar.objects.all()

        return context



class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'footer.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid(request):  # pass the request argument to is_valid()
            form.save()
            return redirect('index')
        return super().post(request, *args, **kwargs)



# @csrf_exempt
# def Login(request):
#     if request.method == 'POST':
#
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             genres = Navbar.objects.all()
#             context = {'genres': genres}
#             login(request, user)
#             if user.is_agent:
#                 return render(request,'agent-profile.html',context)
#             return render(request, 'dashboard.html',context)
#     genres = Navbar.objects.all()
#     context = {'genres': genres}
#     return render(request, 'index.html',context)
# @csrf_exempt
# def Login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             if user.is_agent:
#                 return redirect('agent-dashboard') # assumes 'agent-profile' is a named URL pattern
#             return redirect('dashboard') # assumes 'dashboard' is a named URL pattern
#     genres = Navbar.objects.all()
#     context = {'genres': genres}
#     return render(request, 'index.html', context)

class LoginView(TemplateView):
    template_name = 'index.html'
    # genres = Navbar.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['genres'] = self.genres
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == "agent":
                return redirect('dashboard')
            if user.user_type == "customer":
                return redirect('user_profile')
        else:
            return JsonResponse({'is_authenticated': False, 'error': 'Invalid email or password'}, status=401)


class LogoutView(View):
    def get(self, request):
        logout(request)
        genres = Navbar.objects.all()
        homepages = HomePage.objects.all()
        context = {'genres': genres,'homepages':homepages}
        return render(request, 'index.html',context)


class UserNavbar(TemplateView):
    template_name = 'user-navbar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context

class UpdateProfileView(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'dashboard-myprofile.html'
    success_url = reverse_lazy('my_profile')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        else:
            return response

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if 'image' in self.request.FILES:
                user.image = self.request.FILES['image']
                user.save()
            if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                data = {'success': True}
                return JsonResponse(data)
            else:
                return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class ChangePasswordView(View):
    form_class = ResetPasswordForm
    template_name = 'dashboard-myprofile.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                data = {'error': False, 'message': 'password  did not match'}
                return JsonResponse(data)
            password=form.cleaned_data.get('password')
            if len(password) < 4:
                data = {'error': False, 'message': 'password  length must be greater than 4'}
                return JsonResponse(data)
            else:
                user = self.request.user
                if user and user.is_authenticated:
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    login(request, user)
                    data = {'success': True}
                    return JsonResponse(data)
        data = {'success': False, 'message': 'There was an error'}
        return JsonResponse(data)


@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(request.POST or None, instance=user_profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        data = {'success': True}
        return JsonResponse(data)
    genres = Navbar.objects.all()
    return render(request, 'dashboard-myprofile.html', {'form': form, 'genres': genres})

@login_required
def socialmedia(request):
    social = get_object_or_404(SocialMedia,user=request.user)
    form = SocialMediaForm(request.POST or None, instance=social)
    if request.method == "POST" and form.is_valid():
        form.save()
        data = {'success': True}
        return JsonResponse(data)
    genres = Navbar.objects.all()
    return render(request, 'dashboard-myprofile.html', {'form': form, 'genres': genres})



# def create_listing(request):
#     if request.method == 'POST':
#         form = ListingForm(request.POST)
#         if form.is_valid():
#             # Save the listing object
#             listing = form.save()
#             # Redirect to the listing detail page
#             return redirect('index')
#     else:
#         form = ListingForm()
#     return render(request, 'dashboard-add-listing.html', {'form': form})


# class ListingCreateView(generic.CreateView):
#     form_class = ListingForm
#     template_name = 'dashboard-add-listing.html'
#     success_url = reverse_lazy('index')
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             data = {'success': True}
#             return JsonResponse(data)
#         else:
#             # Display form errors to the user
#             print(form.errors)
#             return super().post(request, *args, **kwargs)
#

class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ListingForm
    template_name = 'dashboard-add-listing.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



def listing_update(request, id):
    band = Listing.objects.get(id=id)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=band)
        if form.is_valid():
            form.save()
            data = {'success': True}
            return JsonResponse(data)
            # return redirect('listing_update', band.id)
    else:
        form = ListingForm(instance=band)

    cities = City.objects.all()
    category = Category.objects.all()
    types = Type.objects.all()
    genres = Navbar.objects.all()
    context = {'cities': cities, 'category': category,'genres':genres,'types':types, 'form': form}
    return render(request, 'dashboard-update-listing.html',context)

class ListingSingleView(DetailView):
    model = Listing
    template_name = 'listing-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context

# class AgentPofile(TemplateView):
#     template_name = 'agent-profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['genres'] = Navbar.objects.all()
#         return context

# class AgentProfileView(UpdateView):
#     model = User
#     form_class = UpdateForm
#     template_name = 'agent-profile.html'
#     success_url = reverse_lazy('agent_profile')
#
#     def form_invalid(self, form):
#         response = super().form_invalid(form)
#         if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#             return JsonResponse({'errors': form.errors}, status=400)
#         else:
#             return response
#
#     def form_valid(self, form):
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             if 'image' in self.request.FILES:
#                 user.image = self.request.FILES['image']
#                 user.save()
#             if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                 data = {'success': True}
#                 return JsonResponse(data)
#             else:
#                 return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['genres'] = Navbar.objects.all()
#         return context

# @login_required
# def edit_agent_profile(request):
#     agent_profile = get_object_or_404(Agent, user=request.user)
#     form = AgentProfileForm(request.POST or None, instance=agent_profile)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         data = {'success': True}
#         return JsonResponse(data)
#     genres = Navbar.objects.all()
#     return render(request, 'agent-profile.html', {'form': form, 'genres': genres})
#

class AgentDashboard(TemplateView):
    template_name = 'agent-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


def search_results(request):
    query = request.GET.get('query')
    type_id = request.GET.get('type')
    city_id = request.GET.get('city')
    category_id = request.GET.get('category')
    price = request.GET.get('price')


    # Filter the YourModel objects based on the search criteria
    results = Listing.objects.filter(title__icontains=query)
    if type_id:
        results = results.filter(type_id=type_id)
        if city_id:
            results = results.filter(city_id=city_id)

    if category_id:
        results = results.filter(category_id=category_id)

    if price:
        price_min, price_max = price.split('-')
        results = results.filter(price__gte=price_min, price__lte=price_max)

    # Render the search results page
    genres = Navbar.objects.all()
    return render(request, 'search_results.html', {'results': results,'genres':genres})



# def create_book(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         listing_id = request.POST.get('listing')
#         listing = Listing.objects.get(id=listing_id)
#         book = Booking.objects.create(name=name, email=email, phone=phone, listing=listing)
#         genres = Navbar.objects.all()
#         return render(request, 'index.html', {'book': book,'genres':genres})

class CreateBookView(CreateView):
    model = Booking
    fields = ['name', 'email', 'phone', 'listing']
    template_name = 'index.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    #         data = {'success': True}
    #         return JsonResponse(data)
    #     return response

class BookingListView(ListView):
    model = Booking
    template_name = 'dashboard-bookings.html'
    paginate_by = 2
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user
        listings = Listing.objects.filter(user=user)
        if listings.exists():
            qs = Booking.objects.filter(listing__in=listings)
        else:
            qs = Booking.objects.none()
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'oldes':
            qs = qs.order_by('-id')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['selected_sort_option'] = self.request.GET.get('sort_by')

        return context


