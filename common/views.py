from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Draft, Post
import markdown

MD_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


@method_decorator(login_required, name='dispatch')
class EditorView(View):
    def get(self, request):
        draft, _ = Draft.objects.get_or_create(author=request.user)
        return render(request, "blog/editor.html", {"draft": draft})


@method_decorator([login_required, csrf_exempt], name='dispatch')
class AutosaveDraftView(View):
    def post(self, request):
        data = request.POST.get("content", "")
        draft, _ = Draft.objects.get_or_create(author=request.user)
        draft.content_md = data
        draft.save()
        return JsonResponse({"status": "ok", "updated_at": str(draft.updated_at)})

    def get(self, request):
        return JsonResponse({"status": "error"}, status=400)


@method_decorator(login_required, name='dispatch')
class PublishPostView(View):
    def get(self, request):
        return render(request, "blog/publish.html")

    def post(self, request):
        draft = get_object_or_404(Draft, author=request.user)
        title = request.POST.get("title", "Untitled")
        content_md = draft.content_md or ""
        content_html = markdown.markdown(content_md, extensions=MD_EXTENSIONS)

        post = Post.objects.create(
            author=draft.author,
            title=title,
            content_md=content_md,
            content_html=content_html
        )

        draft.delete()
        return redirect("blog:post_detail", pk=post.pk)


@method_decorator(login_required, name='dispatch')
class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, "blog/post_detail.html", {"post": post})
