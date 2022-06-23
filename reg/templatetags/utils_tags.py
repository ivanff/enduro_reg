from random import shuffle

from django import template
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.urls.base import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.tag()
def admin_url(obj, action='change'):
    if not action in ('add', 'change', 'delete'):
        raise ValueError
    if action == 'add':
        url = reverse(admin_urlname(obj.__class__._meta, action))
    elif action in ('change', 'delete'):
        url = reverse(admin_urlname(obj.__class__._meta, action), args=(obj.id,))
    else:
        raise ValueError
    return url


@register.filter
def obfuscate(value, prefix='""'):
    arr = list(random_chunk(value))
    a = len(arr)
    
    rnd = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    shuffle(rnd)
    rnd = rnd[:a]
    z = []
    em = "%s" % '+'.join(rnd)
    for num, v in enumerate(rnd):
        if num == 0:
            z.append('%s="%s"' % (v, ''.join(arr[num])))
        else:
            z.append('%s+="%s"' % (v, ''.join(arr[num])))
    
    shuffle(z)
    func_name = "rnd_%s_chunk" % get_random_string(length=5)
    return mark_safe("""
<script id="%s">
   function %s(el) {
    var %s="";
    var em;
    %s
    em=%s;
    if (el) {
        var link = el.parentElement;
        link.setAttribute("href", %s+em);
        link.text = em;
    }
    return
    }
    %s(document.querySelector('#%s'));
</script>
""" % (func_name, func_name, '="";'.join(unique_everseen(rnd)), ';\n'.join(z), em, prefix, func_name, func_name))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
