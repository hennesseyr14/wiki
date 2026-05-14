from django import forms
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from random import choice

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


class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def edit(request, title):
    if request.method == "POST":
        # Get submitted data from form
        form = EditPageForm(request.POST)

        # Save the information, if valid
        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki", kwargs={"title": title}))

        # Re-render page with existing information
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditPageForm(initial={"content": util.get_entry(title)}),
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


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

def create(request):
    if request.method == "POST":
        # Get submitted data from form
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # If the entry does not already exist, save it to disk and redirect to the new page's entry
            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki", kwargs={"title": title}))

            # Otherwise, display an error message and redirect back to the list of entries
            messages.error(request, f"Entry '{title}' already exists!")
            return HttpResponseRedirect(reverse("index"))

        # Re-render page with existing information
        return render(request, "encyclopedia/create.html", {
            "form": form
        })

    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm(),
    })


def random(request):
    title = choice(util.list_entries())
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })