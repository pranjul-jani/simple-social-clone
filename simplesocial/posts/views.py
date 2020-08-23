from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

# this allows us to access some convenient Mixin's to use with class Based views

from braces.views import SelectRelatedMixin

from django.contrib import messages

from posts.models import Post

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class PostList(SelectRelatedMixin, generic.ListView):
    model = Post

    # mixin that allows us to provide a tuple of related models i.e basically Foreign keys
    select_related = ('user', 'group')


class UserPost(generic.ListView):
    model = Post
    template_name = 'posts/user_post_list.html'


    def get_queryset(self):
        try:
            # taken from User object created above
            self.post_user = User.objects.prefetch_related("posts").get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ['message', 'group']
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # initialise the user/writer of the post to the current user
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        quertset = super().get_queryset()
        return quertset.filter(user_id = self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)



















