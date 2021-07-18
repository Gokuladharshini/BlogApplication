from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import PostView,ArticleDetailView,AddPostView,UpdatePostView,DeletePostView,CategoryView,LikeView,UserEditView,PasswordsChangeView,ShowProfilePageView,EditProfilePageView,CreateProfilePageView,AddCommentView,subscription

urlpatterns = [
   
    path('',views.home,name="home"),
    path('register/',views.register, name="register"),
    path('login/', auth_view.LoginView.as_view(template_name='Sblogs/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='Sblogs/logout.html'), name="logout"),
    path('posts/',PostView.as_view(template_name='Sblogs/posts.html'),name='posts'),
    path('article/<int:pk>',ArticleDetailView.as_view(template_name='Sblogs/articles_detail.html'),name='articles_detail'),
    path('add_post/',AddPostView.as_view(template_name='Sblogs/add_post.html'),name='add_post'),
    path('article/edit/<int:pk>',UpdatePostView.as_view(template_name='Sblogs/update_post.html'),name='update_post'),
    path('article/<int:pk>/remove',DeletePostView.as_view(template_name='Sblogs/delete_post.html'),name='delete_post'),
    path('category/<str:cats>/',views.CategoryView,name='category'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('edit_profile/', UserEditView.as_view(template_name='Sblogs/edit_profile.html'),name='edit_profile'),
    path('password/',PasswordsChangeView.as_view(template_name='Sblogs/change_password.html')),
    path('password_success',views.password_success,name="password_success"),
    path('<int:pk>/profile/',ShowProfilePageView.as_view(template_name='Sblogs/user_profile.html'),name='show_profile_page'),
    path('<int:pk>/edit_profile/',EditProfilePageView.as_view(),name='edit_profile_page'),
    path('create_profile_page/',CreateProfilePageView.as_view(),name='create_profile_page'),
    path('article/<int:pk>/comment/',AddCommentView.as_view(),name="add_comment"),
    path('search/',views.search,name='search'),
    path("", views.subscription, name="subscription"),
   
]