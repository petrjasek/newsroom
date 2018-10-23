import superdesk
from functools import wraps

from flask import Blueprint, abort, current_app as newsroom_app, request
from flask_babel import gettext
from newsroom.auth import get_user
from newsroom.auth.token import decode_jwt
from newsroom.template_filters import sidenavs
from superdesk.utc import utcnow

from .companies import CompaniesResource, CompaniesService

blueprint = Blueprint('companies', __name__)

from . import views   # noqa


def get_user_company(user):
    if user and user.get('company'):
        return superdesk.get_resource_service('companies').find_one(req=None, _id=user['company'])


def get_company_sections(company_id):
    """get the section configured for the company"""
    if not company_id:
        return newsroom_app.sections

    company = superdesk.get_resource_service('companies').find_one(req=None, _id=company_id)
    if not company or not company.get('sections'):
        return newsroom_app.sections

    return [s for s in newsroom_app.sections if company.get('sections').get(s['_id'])]


def get_user_company_name(user=None):
    if not user:
        user = get_user()
    company = get_user_company(user)
    if company:
        return company['name']
    return ''


def section_allowed(nav, sections):
    return not nav.get('section') or sections.get(nav['section'])


def get_company_sidenavs(blueprint=None):
    user = get_user()
    company = get_user_company(user)
    navs = sidenavs(blueprint)
    if company and company.get('sections'):
        return [nav for nav in navs if section_allowed(nav, company['sections'])]
    return navs


def section(_id):
    def section_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_user()
            company = get_user_company(user)
            if company and company.get('sections') and not company['sections'].get(_id):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return section_decorator


def get_company_by_token():
    if not request:
        return None
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return None
    payload = decode_jwt(auth_token)
    if not payload or not payload.get('company'):
        return None
    company = superdesk.get_resource_service('companies').find_one(req=None, _id=payload['company'])
    if not company:
        return None
    if company.get('expiry_date') and company['expiry_date'] < utcnow():
        return None
    return company


def init_app(app):
    superdesk.register_resource('companies', CompaniesResource, CompaniesService, _app=app)
    app.add_template_global(get_user_company_name)
    app.add_template_global(get_company_sidenavs, 'sidenavs')
    app.settings_app('companies', gettext('Company Management'), weight=100, data=views.get_settings_data)
