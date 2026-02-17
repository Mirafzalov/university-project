from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from .models import CategoryUni, Faculty, University, Major, Program, Comment, ProfileUser, Ip
from .forms import LoginForm, RegisterForm, CommentForm, EditAccountForm, EditProfileUserForm


# Create your views here.
from .tests import get_client_ip


def main_page(request):
    # categories = CategoryUni.objects.all()
    # faculties = Faculty.objects.all()
    universities = University.objects.all()

    context = {
        'title': 'MyFutureUni найди свой институт',
        # 'categories': categories,
        # 'faculties': faculties,
        'universities': universities
    }

    return render(request, 'MyFutureUni/index.html', context)


def university_by_cat_fac(request, cat_pk, fac_pk):
    universities = University.objects.filter(category_uni=cat_pk, faculty=fac_pk)
    # categories = CategoryUni.objects.all()
    # faculties = Faculty.objects.all()
    category = CategoryUni.objects.get(pk=cat_pk)
    faculty = Faculty.objects.get(pk=fac_pk)


    context = {
        'title': f'MyFutureUni {category.title}/{faculty.title}',
        'universities': universities,
        # 'categories': categories,
        # 'faculties': faculties,

    }
    return render(request, 'MyFutureUni/index.html', context)



# Все университеты определенного катетегория
def university_by_category(request, cat_pk):
    universities = University.objects.filter(category_uni=cat_pk)
    # categories = CategoryUni.objects.all()
    # faculties = Faculty.objects.all()

    context = {
        'title': 'MyFutureUni категория',
        'universities': universities,
        # 'categories': categories,
        # 'faculties': faculties,
    }

    return render(request, 'MyFutureUni/index.html', context)



##############################################

class UniversityDetail(DetailView):
    model = University
    context_object_name = 'university'

    def get_context_data(self, **kwargs):
        context = super(UniversityDetail, self).get_context_data()
        university = context['university']
        majors = Major.objects.filter(university=university)
        programs = Program.objects.filter(university=university)
        same_universities = University.objects.filter(category_uni=university.category_uni, faculty__in=university.faculty.all())

        context['same_universities'] = same_universities.exclude(pk=university.pk).distinct()[:5]
        context['majors'] = majors
        context['programs'] = programs
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(university=university)


        ip = get_client_ip(self.request)
        if Ip.objects.filter(ip=ip).exists():
            university.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            university.views.add(Ip.objects.get(ip=ip))

        return context



# def university_detail(request, uni_pk):
#     university = University.objects.get(pk=uni_pk)
#     majors = Major.objects.filter(university=university)
#     programs = Program.objects.filter(university=university)
#     same_universities = University.objects.filter(category_uni=university.category_uni, faculty__in=university.faculty.all())
#
#
#     context = {
#         'university': university,
#         'title': f'MyFutureUni {university.title}',
#         'majors': majors,
#         'programs': programs,
#         'same_universities': same_universities.exclude(pk=university.pk).distinct(),
#         'form': CommentForm()
#     }
#
#     return render(request, 'MyFutureUni/university_detail.html', context)

##################################################################################################33333

# def login_user_view(request):
#     if request.user.is_authenticated:
#         return redirect('main')
#
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             profile = ProfileUser.objects.get_or_create(user=user)
#             profile.save()
#             if user:
#                 login(request, user)
#                 redirect('main')
#     else:
#         form = LoginForm()
#
#     context = {
#         'title': 'Авторизация',
#         'form': form
#     }
#     return render(request, 'MyFutureUni/login.html', context)
##########################################################

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'MyFutureUni/login.html'
    next_page = 'main'
    redirect_authenticated_user = 'main'
    extra_context = {
        'title': 'Авторизация'
    }





def logout_user_view(request):
    logout(request)
    return redirect('main')



def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    else:
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
        else:
            form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'MyFutureUni/register.html', context)






class SearchUniversity(ListView):
    model = University
    template_name = 'MyFutureUni/index.html'
    context_object_name = 'universities'

    def get_queryset(self):
        word = self.request.GET.get('q')
        return University.objects.filter(title__iregex=word)





def save_comment(request, pk):
    if request.user.is_authenticated and request.method == 'POST':
        try:
            university = University.objects.get(pk=pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.university = university
                comment.save()

            return redirect('university', university.pk)
        except Exception as e:
            print(e)
            return redirect('main')
    else:
        return redirect('login')







class CommentUpdate(UpdateView):
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse('university', kwargs={'pk': comment.university.pk})

    def form_valid(self, form):
        try:
            comment = Comment.objects.get(pk=self.kwargs['pk'])
            if self.request.user == comment.author and self.request.user.is_authenticated:
                return super(CommentUpdate, self).form_valid(form)
            else:
                return redirect('main')
        except Exception as e:
            return redirect('main')


def comment_delete(request, pk):
    if request.user.is_authenticated:
        try:
            comment = Comment.objects.get(pk=pk, author=request.user)
            comment.delete()
            return redirect('university', comment.university.pk)
        except Exception as e:
            return redirect('main')
    else:
        return redirect('main')



def profile_user(request, pk):
    if request.user.is_authenticated:
        try:
            profile = ProfileUser.objects.get(user=pk)
            context = {
                'title': f'Профиль {profile.user.username}',
                'profile': profile,
                'account_form': EditAccountForm(instance=request.user),
                'profile_form': EditProfileUserForm(instance=request.user.profileuser)
            }
            return render(request, 'MyFutureUni/profile.html', context)
        except:
            return redirect('main')
    else:
        return redirect('login')




def edit_account_profile(request):
    if request.user.is_authenticated and request.method == 'POST':
        account_form = EditAccountForm(request.POST, instance=request.user)
        profile_form = EditProfileUserForm(request.POST, request.FILES, instance=request.user.profileuser)
        if account_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            account_form.save()

            data = account_form.cleaned_data
            user = User.objects.get(id=request.user.id)
            if user.check_password(data['old_password']):
                if data['old_password'] != data['new_password'] and data['new_password'] == data['new_password2']:
                    user.set_password(data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)

            return redirect('profile', user.pk)

    else:
        return redirect('login')
