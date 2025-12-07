from django.urls import path
from .views import SignupView, CustomLoginView, UserDetailView, SpeakerListView, UserListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('speakers/', SpeakerListView.as_view(), name='speaker_list'),
]
