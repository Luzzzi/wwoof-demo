from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from core.blocks import StoryBlock
from wagtail.admin.panels import FieldPanel
from core.constants import SEASONS


class JournalIndexPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["journal.JournalPage"]


class JournalPage(Page):
    parent_page_types = ["journal.JournalIndexPage"]
    season = models.CharField(
        max_length=12,
        verbose_name="Saison",
        help_text="Définit la saison de l'article, cela permet le classement sur la page Journal de Bord.",
        choices=SEASONS,
    )
    is_cover_visible = models.BooleanField(
        verbose_name="Apparition de l'image de couverture",
        default=False,
        help_text="Si la case est cochée, la page de couverture s'affiche, sinon elle sert uniquement de miniature.",
    )
    cover = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = models.TextField(verbose_name="Introduction")
    body = StreamField(
        StoryBlock(),
        use_json_field=True,
        verbose_name="Corps de la page",
    )

    content_panels = Page.content_panels + [
        FieldPanel("season"),
        FieldPanel("cover"),
        FieldPanel("is_cover_visible"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
