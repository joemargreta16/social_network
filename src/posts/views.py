from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def post_comment_views(request):
    ques = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # Initials
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_added = False

    # Post form and Comment form
    if 'submit_post_form' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm
            post_added = True

    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm

    context = {
        'ques': ques,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,
    }
    return render(request, 'posts/main.html', context)


# --------------------------------------------------------------------
@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data,safe=False)

    return redirect('posts:post-comment-views')


# --------------------------------------------------------------------
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update_post.html'
    success_url = reverse_lazy('posts:post-comment-views')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You're not the author of this post...")
            return super().form_invalid(form)


# --------------------------------------------------------------------
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:post-comment-views')

    # success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, "You're not the author of this post...")
        return obj
