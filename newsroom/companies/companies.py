
import newsroom

from content_api import MONGO_PREFIX
from newsroom.auth.token import generate_jwt


class CompaniesResource(newsroom.Resource):
    """
    Company schema
    """

    schema = {
        'name': {
            'type': 'string',
            'unique': True,
            'required': True
        },
        'url': {
            'type': 'string'
        },
        'sd_subscriber_id': {
            'type': 'string'
        },
        'is_enabled': {
            'type': 'boolean',
            'default': True
        },
        'contact_name': {
            'type': 'string'
        },
        'contact_email': {
            'type': 'string'
        },
        'phone': {
            'type': 'string'
        },
        'country': {
            'type': 'string'
        },
        'expiry_date': {
            'type': 'datetime',
            'nullable': True,
            'required': False,
        },
        'sections': {
            'type': 'object',
        },
        'auth_token': {
            'type': 'string',
        },
    }
    datasource = {
        'source': 'companies',
        'default_sort': [('name', 1)]
    }
    item_methods = ['GET', 'PATCH', 'DELETE']
    resource_methods = ['GET', 'POST']
    mongo_prefix = MONGO_PREFIX
    mongo_indexes = {
        'auth_token': ([('auth_token', 1)], {'unique': True}),
    }


class CompaniesService(newsroom.Service):

    def _populate_auth_token(self, company):
        if not company.get('auth_token'):
            company['auth_token'] = generate_jwt(company=str(company['_id']))
            self.system_update(company['_id'], {'auth_token': company['auth_token']}, company)

    def get(self, req, lookup):
        res = super().get(req, lookup)
        for company in list(res):
            self._populate_auth_token(company)
        return res.clone()
