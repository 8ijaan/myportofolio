from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<uuid:project_id>/update/", update_project, name="update_project"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_project_star,
        name="toggle_star",
    ),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("api/experience/", get_experiences_json, name="get_experience_json"),
    path("experience/", show_experiences, name="show_experiences"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path(
        "experience/<uuid:experience_id>/star/",
        toggle_experience_star,
        name="toggle_experience_star",
    ),
    path("experience/<uuid:experience_id>/update/", update_experience, name="update_experience"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]