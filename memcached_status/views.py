# Copyright (c) Fredrik Lundh.  Take from http://effbot.org/zone/django-memcached-view.htm

from django import http
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings

import datetime, re

@login_required
def summary(request):
    try:
        import memcache
    except ImportError:
        raise http.Http404

    if not (request.user.is_authenticated() and
            request.user.is_staff):
        raise http.Http404

    if (settings.MEMCACHED_SERVERS is None) or (len(settings.MEMCACHED_SERVERS) == 0):
        raise http.Http404

    host = memcache._Host(settings.MEMCACHED_SERVERS)
    host.connect()
    host.send_cmd("stats")

    class Stats:
        pass

    stats = Stats()

    while 1:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = datetime.timedelta(seconds=value)
            elif key == "time":
                value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()

    if stats.cmd_get > 0:
        hit_rate = 100 * stats.get_hits / stats.cmd_get
    else:
        hit_rate = 0

    return render_to_response(
        'memcached_status/summary.html', dict(
            stats=stats,
            hit_rate=hit_rate,
            time=datetime.datetime.now(), # server time
        ))
