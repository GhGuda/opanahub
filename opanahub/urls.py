from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('password_reset', views.password_reset_request, name="reset"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="passworddone.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="passwordconfirm.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="resetd.html"), name="password_reset_complete"),



    path('savethis', views.savethis, name="savethis"),
    path('savethiss', views.savethiss, name="savethiss"),
    path('savethissinprofile/<user>', views.savethissinprofile, name="savethissinprofile"),
    path('savedthissinyo/<user>', views.savedthissinyo, name="savedthissinyo"),
    path('savedthissinyou/<user>', views.savedthissinyou, name="savedthissinyou"),




    path('frontpage', views.frontpage, name="frontpage"),
    path('new_pana', views.pana, name="pana"),
    path('search', views.search, name="search"),
    path('likethis', views.likethis, name="likethis"),
    path('likecomment/<post_id>', views.likecomment, name="likecomment"),
    path('likethiss', views.likethiss, name="likethiss"),
    path('likethissinprofile/<user>', views.likethissinprofile, name="likethissinprofile"),
    path('likethissinyo/<user>', views.likethissinyo, name="likethissinyo"),
    path('likethissinyou/<user>', views.likethissinyou, name="likethissinyou"),
    path('pana_details/<post_id>', views.pana_details, name="pana_details"),
    path('edit/<pana>', views.edit, name="edit"),
    path('delpost/<pana>', views.delpost, name="delpost"),
    path('delthiss/<pana>/<user>', views.delthiss, name="delthiss"),



    path('profile/<user>', views.profile, name="profile"),
    path('follower/<user>', views.follower, name="follower"),
    path('following/<user>', views.following, name="following"),
    # path('follow/<userad>', views.f4f, name="f4f"),
    path('follow', views.follow, name="follow"),
    path('addup', views.addup, name="addup"),




    path('userliked/<user>', views.userliked, name="userliked"),
    path('savedpost/<user>', views.savedpost, name="savedpost"),




    path('remove/comment_del/<comment_id>/<post_id>', views.comment_del, name="comment_del"),

    





    path('setting', views.setting, name="setting"),
]
