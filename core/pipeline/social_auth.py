# -*- coding: utf-8 -*-
from social.exceptions import AuthAlreadyAssociated, AuthException, \
                              AuthForbidden

def update_extra(backend, details, user=None, *args, **kwargs):
    """
    """
    if user:
        user.update_picture_url()
    return None
