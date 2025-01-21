from wagtail.admin.panels import FieldPanel
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks

from journal.models import JournalPage


class JournalModelViewSet(ModelViewSet):
    model = JournalPage
    ordering = ("title",)
    search_fields = ("title",)
    icon = "globe"
    inspect_view_enabled = True
    form_fields = ["title"]
    exclude_form_fields = ["slug"]

    panels = [
        FieldPanel("title"),
    ]


@hooks.register("register_admin_viewset")
def register_journal_viewset():
    return JournalModelViewSet(name="Journal")
