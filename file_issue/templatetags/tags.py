#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/12/26 14:26
# @Author  : WangKang


from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def dd_display(request, selected):
    # print(str(request.path), str(selected))
    a = str(request.path)
    b = str(selected)

    if b in a:
        return "display: block;"

@register.simple_tag
def li_selected(request, selected):
    #print(str(request.path), str(selected))
    a = str(request.path)
    b = str(selected)

    if b in a:
        return "se"

@register.simple_tag
def display_name(obj):
    print(obj)
    # return eval('value.get_' + arg + '_display')()
    return "11"
    # return apply(eval(‘value.get_’ + arg + ‘_display’), ())