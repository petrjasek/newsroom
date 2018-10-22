
import feedparser
import datetime

from newsroom.auth.token import generate_jwt
from superdesk.utc import utcnow

from .fixtures import items, init_company, init_items  # noqa


def test_rss(client, app):
    res = client.get('wire/rss')
    assert 401 == res.status_code

    company = app.data.find_one('companies', req=None, _id=1)
    assert company

    # add products matching 1 item
    app.data.insert('products', [{
        '_id': 10,
        'name': 'product test',
        'companies': ['1'],
        'is_enabled': True,
        'query': 'amazon',
    }])

    TOKEN = generate_jwt(company=1)
    assert generate_jwt(company=1) == TOKEN, \
        'when this fails we should check in auth if company.auth_token == request.auth_token'
    app.data.update('companies', 1, {'auth_token': TOKEN}, company)

    res = client.get('wire/rss?auth_token=%s' % TOKEN)
    assert 200 == res.status_code

    feed = feedparser.parse(res.get_data())
    assert 'Newshub' in feed.feed.title
    assert 1 == len(feed.entries)
    assert items[0]['_id'] == feed.entries[0].guid
    assert items[0]['headline'] == feed.entries[0].title

    # no rss for expired companies
    company = app.data.find_one('companies', req=None, _id=1)
    app.data.update('companies', 1, {'expiry_date': utcnow() - datetime.timedelta(hours=1)}, company)
    res = client.get('wire/rss?auth_token=%s' % TOKEN)
    assert 401 == res.status_code, 'no rss for expired companies'


def test_rss_bad_token(client):
    res = client.get('wire/rss?auth_token=foo')
    assert res.status_code == 401
