
from flask import json
from lxml import etree
from newsroom.utils import get_entity_or_404
from newsroom.agenda.formatters import EventsNewsmlG2Formatter

from .test_push_events import test_event

event = test_event.copy()


def test_eventsml_event_format(client, app):
    client.post('/push', data=json.dumps(event), content_type='application/json')
    parsed = get_entity_or_404(event['guid'], 'agenda')
    formatter = EventsNewsmlG2Formatter()

    assert 'foo.xml' == formatter.format_filename(parsed)

    xml = formatter.format_item(parsed, item_type='agenda')
    root = etree.fromstring(xml)

    assert 'newsMessage' in root.tag

    item_set = root.find('itemSet', root.nsmap)
    assert item_set is not None

    concept = item_set[0]
    assert 'conceptItem' in concept.tag