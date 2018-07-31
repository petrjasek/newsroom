
from newsroom.wire.formatters import NewsMLG2Formatter


class EventsNewsmlG2Formatter(NewsMLG2Formatter):

    def format_item(self, item, item_type=None):
        agenda = item.copy()
        agenda.setdefault('type', 'event')
        return super().format_item(agenda, item_type)