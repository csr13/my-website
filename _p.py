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

###################################################
# Set global variables for templates
###################################################

env.globals["site_repo"] = "https://github.com/csr13/csr13.github.io"
env.globals["https_site"] = "https://www.csr13.me"
env.globals["http_site"] = "http://www.csr13.me"
env.globals["github_site"] = "https://csr13.github.io"


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
                "href" : "/pages/posts/%s" % name,
            })
        
        #############################################################
        # Generate pdfs and research
        ############################################################

        pdfs = []
        research = []
        for pdf in os.listdir("media/documentation/pdfs"):
            if not pdf.endswith(".pdf"): 
                continue
            if pdf.endswith("research.pdf"):
                research.append({
                    "href": os.path.join(
                        "/", 
                        "media", 
                        "documentation", 
                        "pdfs", 
                        pdf
                    ),
                    "title" : " ".join(
                        [x.capitalize() for x in pdf.split("_")]
                    ).strip(".pdf"),
                    "type" : "research"
                })
            else:
                pdfs.append({
                    "href": os.path.join(
                        "/", 
                        "media", 
                        "documentation", 
                        "pdfs", 
                        pdf
                    ),
                    "title" : " ".join(
                        [x.capitalize() for x in pdf.split("_")]
                    ).strip(".pdf"),
                    "type" : "documentation"
                })

        pdfs = {
            "research" : research, 
            "pdfs" : pdfs
        }
        
        rd_template = env.get_template("documentation-research-archive.html")
        objects = pdfs["research"] + pdfs["pdfs"]
        rd_html = rd_template.render(objects=objects)

        with open("pages/documentation-research-archive.html", "w") as ts:
            ts.write(rd_html)
            
        #############################################################
        # Generate proof of ownershio
        ############################################################

        with open("_data/_projects.json", "r") as fs:
            projects = json.load(fs)

        with open("keybase.txt", "r") as ts: 
            proof_lines = ts.readlines()
            proof_lines = proof_lines[4:-2]
            proof = ''
            for each in proof_lines:
                proof += each

        posts = sorted(posts, key=lambda x: x["timestamp"], reverse=True)
        template = env.get_template("landing.html")
        index_html = template.render(
            projects=projects, 
            posts=posts[:5], # latest
            pdfs=pdfs,
            proof=proof
        )

        with open("index.html", "w") as ts: 
            ts.write(index_html)
       
        template = env.get_template("notes-archive.html")
        archive_html = template.render(posts=posts) # all posts

        with open("pages/notes-archive.html", "w") as ts:
            ts.write(archive_html)
        
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
                "codehilite",
                "fenced_code" # enable code snippets ``` ```
            ])
            html = mkdown.convert(txt)
            meta = mkdown.Meta
            name = post.replace(".md", ".html")
            template = env.get_template("post.html")
            date = meta.get("date")[0]
            title = meta.get("title")[0]
            author = meta.get("author")[0]
            permalink = meta.get("permalink")[0]
            description = meta.get("description")[0]
            post_html = template.render(
                note_title=meta["title"][0], 
                note_body=html,
                note_date=date,
                note_author=author,
                note_permalink=permalink,
                note_description=description
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

    if len(errors) > 0:
        for error in errors:
            print("[ERROR] %s" % error)
        exit(1)

    exit(0)


if __name__ == "__main__":
    main()
