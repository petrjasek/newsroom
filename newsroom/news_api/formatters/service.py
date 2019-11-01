from newsroom.wire.formatters import get_all_formatters
from superdesk.utils import ListCursor
from superdesk.services import BaseService
from flask import abort
from superdesk import get_resource_service
from flask import current_app as app
from eve.versioning import versioned_id_field


class APIFormattersService(BaseService):
    """
    Internal service the will format the requested item in the requested format
    """

    def get(self, req, lookup):
        formatters = get_all_formatters()
        return ListCursor([{'name': type(f).__name__} for f in formatters])

    def _get_formatter(self, name):
        formatters = get_all_formatters()
        return next((f for f in formatters if type(f).__name__ == name), None)

    def get_version(self, id, version, formatter_name):
        formatter = self._get_formatter(formatter_name)
        if not formatter:
            abort(404)
        if version:
            item = get_resource_service('items_versions').find_one(req=None, _id_document=id, version=version)
            if not item:
                abort(404)
            resource_def = app.config['DOMAIN']['items']
            id_field = versioned_id_field(resource_def)
            item['_id'] = item[id_field]
        else:
            item = get_resource_service('items').find_one(req=None, _id=id)
        if not item:
            abort(404)
        ret = formatter.format_item(item)
        return {'formatted_item': ret, 'mimetype': formatter.MIMETYPE}
