from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import authenticate, login, logout

from Prop_dekho import settings
from main.forms import RegistrationForm, LoginForm, UpdateForm, ResetPasswordForm
from main.models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
# from .forms import UserRegistrationForm
from django.contrib import messages


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepages'] = HomePage.objects.all()
        context['property'] = Property.objects.all()
        context['genres'] = Navbar.objects.all()
        return context


class SliderView(TemplateView):
    template_name = 'index2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class VideoView(TemplateView):
    template_name = 'index3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context


class SlideShowView(TemplateView):
    template_name = 'index4.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
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


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
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
        return context


class MyPofile(TemplateView):
    template_name = 'dashboard-myprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
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


class AddListingView(TemplateView):
    template_name = "dashboard-add-listing.html"


class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'footer.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid(request):
            form.save()
            return redirect('login')
        return super().post(request, *args, **kwargs)



def Login(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        email = request.POST['email']
        message = 'Login failed!'
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            genres = Navbar.objects.all()
            context = {'genres': genres}
            # messages.success(request, f' welcome {email} !!')
            return render(request, 'dashboard.html',context)
            # return redirect('dashboard')
        else:
            messages.info(request, f'account done not exit plz sign in')
    genres = Navbar.objects.all()
    context = {'genres': genres}
    return render(request, 'index.html',context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        genres = Navbar.objects.all()
        context = {'genres': genres}
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

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, 'User updated successfully')
            return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Navbar.objects.all()
        return context

class ChangePasswordView(View):
    form_class = ResetPasswordForm
    template_name = 'dashboard-myprofile.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(self.request, 'Password Did Not match')
            password=form.cleaned_data.get('password')
            if len(password) < 4:
                messages.error(self.request, 'Password must be at least 4 characters long')
            else:
                user = self.request.user
                if user and user.is_authenticated:
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    login(request, user)
                    messages.success(self.request, 'Password Change Successfully')
                    return redirect("my_profile")
                else:
                    messages.error(self.request, 'You are Not Login')
        else:
            messages.error(self.request, 'Password Change Failed!')
        genres = Navbar.objects.all()
        return render(request, self.template_name, context={'form': form, 'genres':genres})


