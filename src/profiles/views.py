from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.contrib.auth.models import User


# Create your views here.
@login_required
def my_profile_views(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/myprofile.html', context)


# --------------------------------------------------------------------
@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    query_set = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, query_set))

    is_empty = False

    if len(results) == 0:
        is_empty = True

    context = {
        'query_set': results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/myinvites.html', context)


# --------------------------------------------------------------------
@login_required
def accept_invitations(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-views')


# --------------------------------------------------------------------
@login_required
def decline_invitations(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-views')


# --------------------------------------------------------------------
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # context['username'] = profile
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_r = Relationship.objects.filter(sender=profile)

        rel_sender = []
        rel_receiver = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_sender'] = rel_sender
        context['rel_receiver'] = rel_receiver
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False

        return context


# --------------------------------------------------------------------
@login_required
def profile_lists_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles(user)

    context = {
        'query_set': query_set,
    }
    return render(request, 'profiles/profile_list.html', context)


# The  "class ProfileListView(ListView)" and def profile_lists_view(request) are the same

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    # context_object_name = 'query_set'

    def get_queryset(self):
        query_set = Profile.objects.get_all_profiles(self.request.user)
        return query_set

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['hello'] = "Hello World!!!"
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # context['username'] = profile
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_r = Relationship.objects.filter(sender=profile)

        rel_sender = []
        rel_receiver = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_sender'] = rel_sender
        context['rel_receiver'] = rel_receiver
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


# --------------------------------------------------------------------
@login_required
def all_profile_to_invite_lists_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'query_set': query_set,
    }
    return render(request, 'profiles/profile_to_invite.html', context)


# --------------------------------------------------------------------
@login_required
def send_invitation_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-views')


# --------------------------------------------------------------------
@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-views')
