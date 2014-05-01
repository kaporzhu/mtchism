# -*- coding: utf-8 -*-
import urllib


class PaginationMixin(object):
    """
    Mixin for Django Pagination
    """
    def get_context_data(self, *args, **kwargs):
        """
        Remove page param from request GET and add to context
        """
        data = super(PaginationMixin, self).get_context_data(*args, **kwargs)
        params = self.request.GET.dict()
        params.pop('page', None)
        data.update({'query_string': urllib.urlencode(params)})
        return data
