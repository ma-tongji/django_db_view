# -*- coding: utf-8 -*-
# @Author: martin
# @Date:   2018-01-14 22:44:57
# @Last Modified by:   martin
# @Last Modified time: 2018-01-14 22:50:10

import sys
from django.utils.http import urlencode
from django import template

register = template.Library()

# @register.simple_tag(takes_context=True)
# def get_standard_tag_name(obj_tag):
#     while 1:
#         parent_tag = obj_tag.parent_tag
#         if parent_tag:
# 
#         else:
#         if obj_tag.parent
#     query = context['request'].GET.dict()
#     query.update(kwargs)
#     query_utf8 = {}
#     for k, v in query.iteritems():
#         if isinstance(v, unicode):
#             v = v.encode('utf8')
#         query_utf8[k] = v
#     return urlencode(query_utf8)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    query_utf8 = {}
    for k, v in query.items():
        if isinstance(v, str):
            v = v.encode('utf8')
        query_utf8[k] = v
    return urlencode(query_utf8)

