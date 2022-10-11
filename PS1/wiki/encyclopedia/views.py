# -*- coding: utf-8 -*-

from http.client import HTTPResponse
import re, os
from tkinter import Widget
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import markdown2
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    data = util.get_entry(entry)
    data = markdown2.markdown(data) if data else None
    return render(request, "encyclopedia/entry.html", {
        "entry": data,
        "title": str(entry)
    })
    
def search(request):
    title = request.GET['q']
    entries = util.list_entries()
    found = []
    for page in entries:
        if title.lower() == str(page).lower():
            return HttpResponseRedirect(reverse("entry", args=(page,)))
        elif str(title).lower() in str(page).lower():
            found.append(page) 
    return render(request, "encyclopedia/search.html",{
        "found": found,
        "title": title
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page title")
    contents = forms.CharField(label="Contents", widget=forms.Textarea)

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.entry_name_is_taken(title):
                    return render(request, 'encyclopedia/new_page.html', {
                        "form": form,
                        "name_taken_alert": True
                    })
            else:
                util.save_entry(title, util.purge_CR(form.cleaned_data["contents"]))
                return HttpResponseRedirect(reverse("entry", args=(title,)))
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })

class EditPageForm(forms.Form):
    contents = forms.CharField(label="Contents", widget=forms.Textarea)

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(title, util.purge_CR(form.cleaned_data['contents']))
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:

            return render(request, "encyclopedia/edit.html", {
                "initial_value": form.cleaned_data['contents'],
                "title": title
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "initial_value": util.get_entry(title),
            "title": title
    })

def random(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect(reverse("entry", args=(title,)))
