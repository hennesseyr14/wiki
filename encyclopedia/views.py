from django.http import Http404
from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    entry = util.get_entry(title)
    if entry is None:
        raise Http404("Entry not found")

    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": markdown(entry)
    })
