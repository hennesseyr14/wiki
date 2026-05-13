from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "header": "All Pages",
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

def search(request):
    query = request.POST.get("q")

    if util.get_entry(query):
        return HttpResponseRedirect(reverse("wiki", kwargs={"title": query}))

    results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
    return render(request, "encyclopedia/index.html", {
        "header": f"Results for \"{query}\"",
        "entries": results,
    })