from django.urls import path

# import views
from documents import views



urlpatterns = [
    # profile picture
    path("profile-picture/", views.UserProfilePictureAPI.as_view(), name="get_user_profile")

]
