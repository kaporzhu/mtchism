# -*- coding: utf-8 -*-
import os

from django.core.files.uploadedfile import SimpleUploadedFile


class FormFileMixin(object):
    """
    Mixin for form with FileField.
    """
    def create_file_data(self, file_name, field_name):
        """
        Load the file and create SimpleUploadedFile instance.

        :params file_name: Full file path
        :params fieldname: Form field name
        """
        if not os.path.exists(file_name):
            raise ValueError('Can\'t find test data file %s'.format(file_name))
        with open(file_name, 'rb') as f:
            return {field_name: SimpleUploadedFile(f.name, f.read())}
