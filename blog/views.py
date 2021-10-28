from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Topic, Post, Comment
from .forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'blog/signup.html'
    success_url = reverse_lazy('blog:login')
    form_class = SignUpForm


class PostCreationView(UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'blog/create-post.html'
    fields = ['title', 'body', 'status']

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        self.topic = get_object_or_404(Topic, title=self.kwargs['title'])
        self.obj.topic = self.topic
        self.obj.save()
        return HttpResponseRedirect(reverse('blog:post_list',
                                    args=[self.topic.title]))

    def test_func(self):
        return self.request.user.is_staff


class PostListView(ListView):
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        topic = get_object_or_404(Topic, title=self.kwargs['title'])
        return topic.posts.filter(status='published')


class PostDetailView(DetailView):
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def get_object(self):
        self.post_slug = self.kwargs['slug']
        return get_object_or_404(Post, slug=self.post_slug)

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, slug=self.post_slug)
        comments = post.comments.all()
        context = super().get_context_data(**kwargs)
        context['comments'] = comments
        return context


class PostUpdationView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'blog/update-post.html'

    def get_succes_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['slug']])

    def test_func(self):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return post.author == self.request.user


class PostDeletionView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/check_delete.html'
    slug_field = 'slug'

    def get_success_url(self):
        return reverse('main:home')

    def test_func(self):
        post = get_object_or_404(self.model, slug=self.kwargs['slug'])
        return post.author == self.request.user


class CommentCreationView(LoginRequiredMixin, View):
    def post(self, request, slug):
        blog = get_object_or_404(Post, slug=slug)
        comment_text = request.POST['text']
        comment = Comment(blog=blog, body=comment_text, user=request.user)
        comment.save()
        return HttpResponseRedirect(reverse('blog:post_detail',
                                    args=[slug]))
