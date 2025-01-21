from wagtail.admin.viewsets.base import ViewSet


class CalendarViewSet(ViewSet):
    add_to_admin_menu = True
    menu_label = "Calendar"
    icon = "date"
    # The `name` will be used for both the URL prefix and the URL namespace.
    # They can be customized individually via `url_prefix` and `url_namespace`.
    name = "calendar"
