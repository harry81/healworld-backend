# -*- coding: utf-8 -*-


def update_extra(backend, details, user=None, *args, **kwargs):
    """
    """
    if user and not user.is_anonymous():
        user.update_picture_url()
