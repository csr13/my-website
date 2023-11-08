import json
import os

import requests
import markdown
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("_p", "_templates"),
    autoescape=select_autoescape()
)


def generate_projects_page():
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
    
    return True


def generate_posts():
    posts_dir = "_posts"
    for post in os.listdir(posts_dir):
        print(post)
        if not post.endswith(".md"): continue

        txt = None
        with open(os.path.join(posts_dir, post), "r") as ts: 
            txt = ts.read()

        mkdown = markdown.Markdown(
            extensions=[
                "meta", 
                "fenced_code"
            ]
        )
        html = mkdown.convert(txt)
        meta = mkdown.Meta

        name = post.replace(".md", ".html")

        template = env.get_template("post.html")
        post_html = template.render(
            note_title=meta["title"][0], 
            note_body=html
        )
        with open("pages/posts/%s" % name, "w") as ts: 
            ts.write(post_html)

    return True

def main():
    errors = []

    if not generate_posts():
        errors.append("Unable to generate posts")

    if not generate_projects_page():
        errors.append("Unable to generate projects page")

    for error in errors:
        print("[ERROR] %s" % error)

    return True


if __name__ == "__main__":
    main()
