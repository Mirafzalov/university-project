from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main'),
    path('category_uni/<int:cat_pk>/faculty/<int:fac_pk>/', university_by_cat_fac, name='category_and_faculty'),
    path('category_uni/<int:cat_pk>/', university_by_category, name='category'),
    # path('university/<int:uni_pk>/', UniversityDetail, name='university'),
    path('university/<int:pk>/', UniversityDetail.as_view(), name='university'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('register/', register_user_view, name='register'),
    path('search/', SearchUniversity.as_view(), name='search'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('change_comment/<int:pk>/', CommentUpdate.as_view(), name='change_comment'),
    path('comment_delete/<int:pk>/', comment_delete, name='comment_delete'),
    path('profile/<int:pk>/', profile_user, name='profile'),
    path('edit_account_profile/', edit_account_profile, name='edit'),
]
