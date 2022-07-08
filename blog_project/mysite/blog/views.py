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
#Used by ListViews - it determines the list of objects that you want to display.
#By default, it will just give you all for the model you specify.
#By overriding this method you can extend or completely replace this logic

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post_dt' #Normalde bu attribute tanıml değildi ve post_detail.html'de
                                    # post_dt yerine post kullanılıyordu.

#'context_object_name' :This helps anyone else reading the code to understand what is variable in the template context, plus it is much easier to read and understand.



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
    postal = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)  #dolu form gönderiyor
        if form.is_valid():
            post_atr = form.save(commit=False)  #egitimde, comment = form.save(commit=False)
            post_atr.post = postal #post var in Commentmodel which is a foreign key in Post model
            post_atr.save()
            return redirect('post_detail', pk=postal.pk)
#post_atr.post = postal. This connects the Comment model's post attribute to the current post that the user is on (so the connection between the comment and the post can happen)
# Comment'in post attribute'ünü (Foreign Key ile Post model'a baglıdır) formla gelen Post model object(burada postal)'e eşitliyor.

    else:
        form = CommentForm()  #bos form gönderiyor
        return render(request, 'blog/comment_form.html', {'form_me': form})
#{'form': form}'daki value olan form, yukarıdaki form instance'dan geliyor.

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


#push için deneme








