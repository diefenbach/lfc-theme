# django imports
from django.conf import settings
from django.core.cache import cache
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

# portlets imports
import portlets.utils
from portlets.models import Slot

register = Library()


class SlotsInformationNode(Node):
    def render(self, context):
        obj = context.get("lfc_context")
        request = context.get("request")

        if obj:
            cache_key = "%s-slots-information-%s-%s-%s" % \
                (settings.CACHE_MIDDLEWARE_KEY_PREFIX, obj.content_type, obj.id, request.user.id)
        else:
            cache_key = "%s-slots-information-portal-%s" % \
                (settings.CACHE_MIDDLEWARE_KEY_PREFIX, request.user.id)

        info = cache.get(cache_key)

        info = False
        if info:
            context["content_class"] = info["content_class"]
            context["left_class"] = info["left_class"]
            context["right_class"] = info["right_class"]
            context["SlotLeft"] = info["SlotLeft"]
            context["SlotRight"] = info["SlotRight"]
            return ''

        if obj:
            obj = obj.get_content_object()

        for slot in Slot.objects.all():
            context["Slot%s" % slot.name] = slot.has_portlets(obj)

        max_width = 24
        left_width = getattr(settings, "LFC_THEME_WIDTH_SLOT_LEFT", 5)
        right_width = getattr(settings, "LFC_THEME_WIDTH_SLOT_RIGHT", 5)

        if context["SlotLeft"] and context["SlotRight"]:
            content_class = "span-%s append-1" % (max_width - left_width - right_width - 1)
        elif context["SlotLeft"]:
            content_class = "span-%s last" % (max_width - left_width)
        elif context["SlotRight"]:
            content_class = "span-%s append-1" % (max_width - right_width - 1)
        else:
            content_class = "span-%s last" % max_width

        left_class = "span-%s" % left_width
        right_class = "span-%s last" % right_width

        cache.set(cache_key, {
            "content_class": content_class,
            "left_class": left_class,
            "right_class": right_class,
            "SlotLeft": context["SlotLeft"],
            "SlotRight": context["SlotRight"],
        })

        context["content_class"] = content_class
        context["left_class"] = left_class
        context["right_class"] = right_class
        return ''


def do_slots_information(parser, token):
    """Calculates some context variables based on displayed slots.
    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 1:
        raise TemplateSyntaxError(_('%s tag needs no argument') % bits[0])

    return SlotsInformationNode()

register.tag('slots_information', do_slots_information)
