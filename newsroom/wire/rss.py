
import flask
from feedgen import feed


def generate_rss(items):
    fg = feed.FeedGenerator()
    fg.title('Newshub feed')
    fg.link(href=flask.url_for('wire.rss', _external=True), rel='self')
    fg.link(href=flask.url_for('wire.wire', _external=True), rel='alternate')
    fg.description('foo')
    for item in items:
        entry = fg.add_entry()
        entry.id(item['_id'])
        entry.title(item.get('headline', item.get('name', item.get('slugline', ''))))
        entry.link(href=flask.url_for('wire.wire', _external=True) + '?item=%s' % item['_id'])
        entry.description(item.get('description_text'))
        entry.published(item['_created'])
        entry.updated(item['versioncreated'])
        entry.content(item.get('body_html'), type='text/html')
    return fg.rss_str(pretty=True)
