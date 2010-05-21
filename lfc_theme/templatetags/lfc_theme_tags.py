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
        obj = context.get("lfc_context")

        if obj:
            cache_key = "slots-information-%s-%s" % (obj.content_type, obj.id)
        else:
            cache_key = "slots-information-portal"

        info = cache.get(cache_key)
        if info:
            context["content_class"] = info["content_class"]
            context["SlotLeft"] = info["SlotLeft"]
            context["SlotRight"] = info["SlotRight"]
            return ''

        if obj:
            obj = obj.get_content_object()

        for slot in Slot.objects.all():
            context["Slot%s" % slot.name] = portlets.utils.has_portlets(slot, obj)

        if context["SlotLeft"] and context["SlotRight"]:
            content_class = "span-13 append-1"
        elif context["SlotLeft"]:
            content_class = "span-18 last"
        elif context["SlotRight"]:
            content_class = "span-18 append-1"
        else:
            content_class = "span-24 last"

        cache.set(cache_key, {
            "content_class" : content_class,
            "SlotRight" : context["SlotLeft"],
            "SlotLeft" : context["SlotLeft"],
        })

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