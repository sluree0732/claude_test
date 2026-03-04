from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import PostForm
from .models import Post


class BoardListView(View):
    def get(self, request):
        posts = Post.objects.select_related('author').all()
        return render(request, 'board/list.html', {'posts': posts})


@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'board/create.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board:list')
        return render(request, 'board/create.html', {'form': form})


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'board/detail.html', {'post': post})
