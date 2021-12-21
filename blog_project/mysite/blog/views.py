from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin   #for class based views
from django.contrib.auth.decorators import login_required   #for function based views
from django.urls import reverse_lazy



# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    #login_url = '/login/'  #kullanıcı giris yapamazsa buraya yonlendirilir
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

    # You have used LoginRequiredMixin for class-based-view and login_required for function-based-view.
    # Both are working same. In class-base-view, you have made sure the user is authenticated by inheriting the LoginRequiredMixin class.
    # And in function-based-view, you have put it above the function.


class UpdatePostView(UpdateView):
    login_url = '/login/'  # kullanıcı giris yapamazsa buraya yonlendirilir
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'  # kullanıcı giris yapamazsa buraya yonlendirilir
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            asd = form.save(commit=False)
            asd.post = post #post var in Commentmodel which is s foreign key in Post model
            asd.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})


@login_required()
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required()
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required()
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)











