from django.db import models

from wagtail.models import Page


class HomePage(Page):
    subpage_types = ["journal.JournalIndexPage"]
    max_count = 1
