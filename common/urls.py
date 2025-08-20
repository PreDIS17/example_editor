from django.urls import path
from .views import EditorView, AutosaveDraftView, PublishPostView, PostDetailView

app_name = "blog"

urlpatterns = [
    path("editor/", EditorView.as_view(), name="editor"),
    path("autosave/", AutosaveDraftView.as_view(), name="autosave"),
    path("publish/", PublishPostView.as_view(), name="publish"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
