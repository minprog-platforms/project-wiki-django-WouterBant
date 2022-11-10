from django.shortcuts import render
from markdown2 import Markdown
from random import choice

from . import util

def edit(request):
    if request.method == 'POST':
        title = request.POST['page']
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "page": page
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def MD_2_HTML(title):
    page = util.get_entry(title)
    if not page:
        return None
    markdowner = Markdown()
    return markdowner.convert(page)

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")

    title = request.POST['title_of_article']
    if util.get_entry(title):
        return render(request, "encyclopedia/page_exists.html")

    text = request.POST['article']
    util.save_entry(title, text)
    page = MD_2_HTML(title)
    if not page:
        return render(request, "encyclopedia/notfound.html")
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": page
    })

def present_page(request, title):
    page = MD_2_HTML(title)
    if not page:
        return render(request, "encyclopedia/notfound.html")
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": page
    })

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    page = MD_2_HTML(title)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": page
    })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title_of_article']
        text = request.POST['article']
        util.save_entry(title, text)
        page = MD_2_HTML(title)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": page
        })

def search(request):
    if request.method == "POST":
        title = request.POST['q']
        page = MD_2_HTML(title)
        if page:
            return render(request, "encyclopedia/page.html", {
                "title": title,
                "page": page
            })
        entries = util.list_entries()
        res = []
        for entry in entries:
            if title.lower() in entry.lower():
                res.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": res
        })