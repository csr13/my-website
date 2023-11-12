import datetime
import json
import os

import requests
import markdown
from jinja2 import Environment, PackageLoader, select_autoescape

from _logger import get_logger


logger = get_logger(__name__)


env = Environment(
    loader=PackageLoader("_p", "_templates"),
    autoescape=select_autoescape()
)


def generate_index():
    try:
        posts_dir = "_posts"
        posts = []
        for post in os.listdir(posts_dir):
            if not post.endswith(".md"): continue
            txt = None
            with open(os.path.join(posts_dir, post), "r") as ts: 
                txt = ts.read()
            mkdown = markdown.Markdown(extensions=["meta"])
            html = mkdown.convert(txt)
            meta = mkdown.Meta
            name = post.replace(".md", ".html")
            title = meta.get("title")[0]
            date = meta.get("date")[0]
            year, month, day = [int(x) for x in date.split("-")]
            date = datetime.datetime(year=year, month=month, day=day)
            posts.append({
                "title" : title,
                "date" : date,
                "timestamp" : date.timestamp(),
                "href" : "/pages/posts/%s" % name 
            })
        
        posts = sorted(posts, key=lambda x: x["timestamp"], reverse=True)
        template = env.get_template("landing.html")
        index_html = template.render(posts=posts)
        with open("index.html", "w") as ts: 
            ts.write(index_html)
    except Exception as e:
        if os.getenv("DEBUG") is not None:
            raise e
        return False

    return True


def generate_projects_page():
    try:
        url = "https://api.github.com/users/csr13/repos"
        resp = requests.get(url)
        if not resp.status_code in [200]:
            raise Exception("Unable to get repos") from None
        else:
            repos = resp.json()

        clean_repos = []
        for repo in repos:
            name = repo["name"]
            language = repo["language"]
            licence = repo["license"]
            owner = repo["owner"]
            url = repo["url"]
            clean_repos.append(dict(
                name=name, 
                language=language, 
                licence=licence, 
                owner=owner,
                url=url
            ))
        
        template = env.get_template("projects.html")
        projects_template = template.render(
            repos=clean_repos
        )
        
        with open("pages/projects.html", "w") as fs:
            fs.write(projects_template)
    except Exception as e:
        if os.getenv("DEBUG") is not None:
            raise e
        return False

    return True


def generate_posts():
    try:
        posts_dir = "_posts"
        for post in os.listdir(posts_dir):
            if not post.endswith(".md"): continue
            txt = None
            with open(os.path.join(posts_dir, post), "r") as ts: 
                txt = ts.read()
            mkdown = markdown.Markdown(extensions=[
                "meta", 
                "fenced_code" # enable code snippets ``` ```
            ])
            html = mkdown.convert(txt)
            meta = mkdown.Meta
            name = post.replace(".md", ".html")
            template = env.get_template("post.html")
            date = meta.get("date")[0]
            title = meta.get("title")[0]
            author = meta.get("author")[0]
            post_html = template.render(
                note_title=meta["title"][0], 
                note_body=html,
                note_date=date,
                note_author=author
            )
            with open("pages/posts/%s" % name, "w") as ts: 
                ts.write(post_html)
    except Exception as e:
        if os.getenv("DEBUG") is not None:
            raise e
        return False

    return True


def main():
    errors = []
    if not generate_index():
        errors.append("Unable to generate index")
    if not generate_posts():
        errors.append("Unable to generate posts")
    #if not generate_projects_page():
    #    errors.append("Unable to generate projects page")

    if len(errors) > 0:
        for error in errors:
            print("[ERROR] %s" % error)
        exit(1)

    exit(0)


if __name__ == "__main__":
    main()
