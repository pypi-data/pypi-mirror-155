#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

__all__ = [
    "get_cached_value",
]

def get_cached_value(holder_object, cache_key, getter, *args, **kwargs):
    """Get cached value from an holder_object and set the cache value at the first request.

    @Returns:
        (Any): The cahced value or the getter returned value.
    
    @Parameters:
        holder_object(Any): The holder object which holds the cache property.
        cache_key(str): The cache property which will attach to the holder object.
        getter(Callable): The callable object which will be called if there is no cache value.
        *args(Any): Place holder parameters which will be used by getter.
        **kwargs(Any): Keyword parameters which will be used by getter.

    @Example:
        token = request.GET.get("token")
        value = get_cached_value(request, "cache_key_for_get_user_info", services.get_user_info, token=token)
    """
    cache_key = force_text(cache_key)
    if not hasattr(holder_object, cache_key):
        setattr(holder_object, cache_key, getter(*args, **kwargs))
    return getattr(holder_object, cache_key)
