from django.core.cache import cache
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

# portlets imports
import portlets.utils
from portlets.models import Slot

register = Library()

class SlotsInformationNode(Node):
    """
    """
    def render(self, context):
        page = context.get("lfc_context")

        if page:
            cache_key = "slots-information-%s-%s" % (page.content_type, page.id)
            context["content_class"] = cache.get(cache_key)
        else:
            cache_key = "slots-information-portal"
            context["content_class"] = cache.get(cache_key)

        if context["content_class"]:
            return ""

        if page:
            page = page.get_content_object()

        for slot in Slot.objects.all():
            context["Slot%s" % slot.name] = portlets.utils.has_portlets(slot, page)

        if context["SlotLeft"] and context["SlotRight"]:
            content_class = "span-13 append-1"
        elif context["SlotLeft"]:
            content_class = "span-18 last"
        elif context["SlotRight"]:
            content_class = "span-18 append-1"
        else:
            content_class = "span-24 last"

        cache.set(cache_key, content_class)
        context["content_class"] = content_class
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