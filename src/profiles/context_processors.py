from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        image = profile_obj.avatar
        return {'picture': image}
    return {}


def invitations_received_count(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        query_set_count = Relationship.objects.invitations_received(profile_obj).count()
        return {'qs_count': query_set_count}
    return {}
