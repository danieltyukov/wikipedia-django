from django.shortcuts import render, redirect
from random import choice
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    page = util.get_entry(title)
    if (not page):
        return redirect(request, "encyclopedia/error.html", {
            "message": "Page Not Found",
            "status": 404
        })

    text = Markdown()
    markdown_page = text.convert(page)
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "html_page": markdown_page,
    })


def search(request):
    search_id = request.POST.get("q", "")
    entries = util.list_entries()
    exist = search_id in entries

    if exist:
        return redirect('title', title=search_id)

    checked_entries = [
        entry for entry in entries if not entry.find(search_id) == -1]

    return render(request, "encyclopedia/index.html", {
        "entries": checked_entries
    })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html")

    if request.method == "POST":
        new_content = request.POST.get("content", "")
        new_title = request.POST.get("title", "")

    if (len(new_content) == 0 or len(new_title) == 0):
        return render(request, "encyclopedia/error.html", {
            "message": "Please Fill In All Fields",
            "description": "You Must Fill In The Fields Before Submitting",
            "status": 400
        })

    if util.get_entry(new_title):
        return render(request, "encyclopedia/error.html", {
            "message": "Page Already Exists",
            "description": "This Page Already Exists",
            "status": 400
        })

    util.save_entry(new_title, new_content)

    return redirect('title', title=new_title)


def edit_page(request, title):
    if request.method == "GET":

        entry_page = util.get_entry(title)
        if (not entry_page):
            return render(request, "encyclopedia/error.html", {
                "message": "Page Not Found",
                "status": 404
            })

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": entry_page
        })

    if request.method == "POST":
        new_content = request.POST.get("content", "")
        new_title = request.POST.get("title", "")

        if (len(new_content) == 0 or len(new_title) == 0):
            return render(request, "encyclopedia/error.html", {
                "message": "Please Fill In All Fields",
                "description": "You Must Fill In The Fields Before Submitting",
                "status": 400
            })

        util.save_entry(new_title, new_content)
        return redirect('title', title=new_title)


def random(request):
    entries = util.list_entries()
    choices = choice(entries)

    return redirect('title', title=choices)


def delete_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/delete.html")

    if request.method == "POST":
        delete_title = request.POST.get("title", "")

        if (len(delete_title) == 0):
            return render(request, "encyclopedia/error.html", {
                "message": "Please Fill In The Field",
                "description": "You Must Fill In The Field Before Submitting",
                "status": 400
            })

        util.delete_entry(delete_title)
        return redirect('index')


def handler404(request, exception):
    return render(request, "encyclopedia/handler404.html", {})


def handler500(request, exception=None):
    return render(request, "encyclopedia/handler500.html", {})


def handler403(request, exception=None):
    return render(request, "encyclopedia/handler403.html", {})


def handler400(request, exception=None):
    return render(request, "encyclopedia/handler400.html", {})
