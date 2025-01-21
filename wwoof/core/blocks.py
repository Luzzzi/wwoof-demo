from wagtail.blocks import (
    RichTextBlock,
    StreamBlock,
    PageChooserBlock,
    StructBlock,
    URLBlock,
    CharBlock,
    EmailBlock,
    ListBlock,
    TextBlock,
    BooleanBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds import embeds
from wagtail.embeds.blocks import EmbedBlock, EmbedValue
from django.core.validators import validate_unicode_slug
from core.constants import BASE_ITEMS_GROUP, MEDIA_ITEMS_GROUP, EDITORIAL_ITEMS_GROUP


class EmbedValueEnhanced(EmbedValue):
    """
    Override default EmbedValue class in order to add some properties that are
    part of the Embed object (thumbnail_url, title...).
    """

    def __init__(self, url, max_width=None, max_height=None):
        embed = embeds.get_embed(url)
        self.thumbnail_url = embed.thumbnail_url
        self.provider_name = embed.provider_name
        self.title = embed.title
        self.url = url
        self.max_width = max_width
        self.max_height = max_height


class EmbedBlockEnhanced(EmbedBlock):
    def get_default(self):
        # Allow specifying the default for an EmbedBlock as either an EmbedValue or a string (or None).
        if not self.meta.default:
            return None
        elif isinstance(self.meta.default, EmbedValue):
            return self.meta.default
        else:
            # assume default has been passed as a string
            return EmbedValueEnhanced(
                self.meta.default,
                getattr(self.meta, "max_width", None),
                getattr(self.meta, "max_height", None),
            )

    def to_python(self, value):
        # The JSON representation of an EmbedBlock's value is a URL string;
        # this should be converted to an EmbedValue (or None).
        if not value:
            return None
        else:
            return EmbedValueEnhanced(
                value,
                getattr(self.meta, "max_width", None),
                getattr(self.meta, "max_height", None),
            )

    def value_from_form(self, value):
        # convert the value returned from the form (a URL string) to an EmbedValue (or None)
        if not value:
            return None
        else:
            return EmbedValueEnhanced(
                value,
                getattr(self.meta, "max_width", None),
                getattr(self.meta, "max_height", None),
            )


class VideoItemBlock(StructBlock):
    embed = EmbedBlockEnhanced(label="Lien de la vidéo")
    caption = CharBlock(label="Légende", required=False)

    class Meta:
        icon = "media"


class LinksBlock(StreamBlock):
    internal = PageChooserBlock(label="Lien interne")
    external = URLBlock(label="Lien externe")
    email = EmailBlock(label="Email")

    class Meta:
        max_num = 1


class ButtonBlock(StructBlock):
    cta_text = CharBlock(label="Texte du bouton")
    cta_link = LinksBlock(label="Lien du bouton")


class EngagementBlock(StructBlock):
    image = ImageChooserBlock(label="Image")
    title = CharBlock(label="Titre", required=False)
    cta = ButtonBlock(label="Bouton")


class ImageBlock(StructBlock):
    image = ImageChooserBlock(label="Image")
    caption_text = CharBlock(label="Légende", required=False)
    link = LinksBlock(label="Lien", required=False)


class QuoteBlock(StructBlock):
    quote = TextBlock(
        label="Citation",
        help_text="Les guillemets seront ajoutés automatiquement.",
    )
    author = CharBlock(label="Auteur", required=False)
    image = ImageChooserBlock(required=False, label="Image de profil")

    class Meta:
        icon = "openquote"


class AnchorBlock(StructBlock):
    id = CharBlock(
        validators=[validate_unicode_slug],
        label="Nom de l'ancre",
        help_text="Ce texte sera le texte utilisé pour le lien de l'ancre, et le texte affiché dans l'url au clic sur l'ancre. Il est invisible dans la page. Il peut utiliser tout caractère sauf les espaces, les accents et les majuscules.",
    )


class DoublePortraitImages(StructBlock):
    imageA = ImageBlock(label="Image de gauche")
    imageB = ImageBlock(label="Image de droite")


class CallToActionBlock(StructBlock):
    title = TextBlock(label="Titre")
    cta = ButtonBlock(label="Bouton")
    with_background = BooleanBlock(
        label="Souhaitez-vous un fond clair ?",
        help_text="Si cette case est coché, le bloc est entouré d'un fond clair et le texte change de couleur.",
    )


class StoryBlock(StreamBlock):
    rich_text = RichTextBlock(
        label="Texte riche",
        features=["h2", "h3", "h4", "bold", "hr", "italic", "link", "ol", "ul"],
        group=BASE_ITEMS_GROUP,
    )
    engagement = EngagementBlock(label="Bloc d'engagement", group=EDITORIAL_ITEMS_GROUP)
    anchor = AnchorBlock(label="Ancre", group=EDITORIAL_ITEMS_GROUP)
    quote = QuoteBlock(label="Citation", group=EDITORIAL_ITEMS_GROUP)
    carousel = ListBlock(
        ImageBlock,
        label="Carousel",
        group=MEDIA_ITEMS_GROUP,
        icon="image",
    )
    image = ImageBlock(label="Image", group=MEDIA_ITEMS_GROUP)
    double_portrait = DoublePortraitImages(
        label="Bloc d'images format portrait", group=MEDIA_ITEMS_GROUP
    )
    row_images = ListBlock(
        ImageBlock,
        label="Bloc d'images en ligne",
        group=MEDIA_ITEMS_GROUP,
        min=2,
        max=3,
        help_text="Il est possible d'ajouter 2 ou 3 images en lignes.",
    )
    cta_block = CallToActionBlock(label="Bloc d'appel à action")
