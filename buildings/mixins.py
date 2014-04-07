# -*- coding: utf-8 -*-
from .models import Tag


class NewTagMixin(object):
    """
    Mixin for create and update Building.
    When new tag is added in the client, we try to save it to the database
    before process the form.
    """

    def get_form_kwargs(self):
        """
        Check the tags posted from the client.
        If it's not a tag id, we create a new tag for it.
        """
        kwargs = super(NewTagMixin, self).get_form_kwargs()
        if 'data' in kwargs:
            for tag_id in kwargs['data'].getlist('tags'):
                try:
                    Tag.objects.get(id=tag_id)
                except:
                    # tag_id is actually new tag, treat as new tag
                    # name(check the building.js)
                    tag_name = tag_id
                    tag = Tag(name=tag_name)
                    tag.save()
                    kwargs['data'].getlist('tags').remove(tag_name)
                    kwargs['data'].getlist('tags').append(tag.id)
        return kwargs
