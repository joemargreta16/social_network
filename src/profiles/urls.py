from django.urls import path
from .views import (
    my_profile_views,
    invites_received_view,
    profile_lists_view,
    all_profile_to_invite_lists_view,
    ProfileDetailView,
    ProfileListView,
    send_invitation_request,
    remove_from_friends,
    accept_invitations,
    decline_invitations,
)

app_name = 'profiles'
urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_views, name='my-profile-views'),
    path('myinvites/', invites_received_view, name='my-invites-views'),
    path('to-invite/', all_profile_to_invite_lists_view, name='all-profiles-to-invite-view'),
    path('send-invite/', send_invitation_request, name='send-invite-view'),
    path('remove-friend/', remove_from_friends, name='remove_from_friends-view'),
    path('<slug>/', ProfileDetailView.as_view(), name='profiles-detail-view'),
    path('myinvites/accept', accept_invitations, name='accept-request'),
    path('myinvites/decline', decline_invitations, name='decline-request'),
]
