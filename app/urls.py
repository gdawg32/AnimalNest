from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("pets/", views.pets, name="pets"),
    path("employee_login/", views.employee_login, name="employee_login"),
    path('logout/', views.employee_logout, name='employee_logout'),
    path("employee_portal", views.employee_portal, name="employee_portal"),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('adopter_signup', views.adopter_signup, name='adopter_signup'),
    path('adopter_login', views.adopter_login, name="adopter_login"),
    path('adopter_portal', views.adopter_portal, name="adopter_portal"),
    path('adopter_logout', views.adopter_logout, name="adopter_logout"),
    path('edit_pet/<str:pet_id>/', views.edit_pet, name='edit_pet'),
    path('delete_pet/<str:pet_id>/', views.delete_pet, name='delete_pet'),
    path('pet/<str:pet_id>/', views.pet_profile, name='pet_profile'),
    path('pet/<str:pet_id>/adopt/', views.adopt_pet, name='adopt_pet'),
    path('approve-adoption/<str:appointment_id>/', views.approve_adoption, name="approve_adoption"),
    path('reject-adoption/<str:appointment_id>/', views.reject_adoption, name="reject_adoption"),

]