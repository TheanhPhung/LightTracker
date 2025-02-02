from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("relapse/<int:act_code>/", views.relapse, name="relapse"),
    path("targets/", views.targets, name="targets"),
    path("set_target/<int:act_code>", views.set_target, name="set_target"),
]
