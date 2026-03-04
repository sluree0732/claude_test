from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import PostForm
from . import sheets


class BoardListView(View):
    def get(self, request):
        posts = sheets.get_all_posts()
        return render(request, 'board/list.html', {'posts': posts})


@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'board/create.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            sheets.create_post(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                author=request.user.username,
            )
            return redirect('board:list')
        return render(request, 'board/create.html', {'form': form})


class PostDetailView(View):
    def get(self, request, pk):
        post = sheets.get_post(pk)
        if post is None:
            from django.http import Http404
            raise Http404('게시글을 찾을 수 없습니다.')
        return render(request, 'board/detail.html', {'post': post})
