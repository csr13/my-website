import datetime
import json
import os
import pprint

import requests
import markdown
from jinja2 import Environment, PackageLoader, select_autoescape

from _logger import get_logger

THIS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

PAGES_DIR = os.path.join(THIS_DIR, "pages")

POSTS_DIR = os.path.join(PAGES_DIR, "posts")

CATEGORIES_DIR = os.path.join(POSTS_DIR, "categories")

logger = get_logger(__name__)

env = Environment(
    loader=PackageLoader("_p", "_templates"),
    autoescape=select_autoescape()
)


def get_posts():
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
        categories = meta.get("categories")
        year, month, day = [int(x) for x in date.split("-")]
        date = datetime.datetime(year=year, month=month, day=day)
        posts.append({
            "title" : title,
            "date" : date,
            "timestamp" : date.timestamp(),
            "href" : "/pages/posts/%s" % name,
            "post_name" : post, 
            "categories" : categories
        })
    return posts


def get_categories():
    categories = []
    for cat in os.listdir(CATEGORIES_DIR):
        abs_path = os.path.join(CATEGORIES_DIR, cat)
        if not os.path.isdir(abs_path):
            continue
        posts_num = len([x for x in os.listdir(abs_path) if x != 'list.html'])
        categories.append([cat, posts_num])
    return sorted(categories, key=lambda x: x[0].lower())


def generate_index():
    try:
        posts = get_posts()

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

        with open("keybase.txt", "r") as ts: 
            proof_lines = ts.readlines()
            proof_lines = proof_lines[4:-2]
            proof = ''
            for each in proof_lines:
                proof += each

        posts = sorted(posts, key=lambda x: x["timestamp"], reverse=True)
        template = env.get_template("landing.html")
        index_html = template.render(
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
        posts_dir = os.path.join(THIS_DIR, "_posts")
        cats_path = os.path.join(THIS_DIR, "pages", "posts", "categories")
        if not os.path.exists(cats_path):
            os.makedirs(cats_path)

        for post in os.listdir(posts_dir):
            if not post.endswith(".md"): 
                continue
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
            categories = meta.get("categories")
            post_html = template.render(
                note_title=meta["title"][0], 
                note_body=html,
                note_date=date,
                note_author=author,
                note_permalink=permalink,
                note_description=description,
                note_categories=categories,
                name=post
            )
            with open("pages/posts/%s" % name, "w") as ts: 
                ts.write(post_html)

            for cat in categories:
                cat = cat.replace(" ", "-")
                cat = "-".join([c.lower() for c in cat.split("-")])
                if not os.path.exists(os.path.join(cats_path, cat)):
                    os.makedirs(os.path.join(cats_path, cat))
                with open(os.path.join(cats_path, cat, name), "w") as ts:
                    ts.write(post_html)

        posts = get_posts()
        cat_posts = {cat: [] for cat in os.listdir(cats_path)}
        for cat in cat_posts.keys():
            for post in posts:
                post_categories = post["categories"]
                post_categories = [c.replace(" ", "-").lower() for c in post_categories]
                if cat in post_categories:
                    cat_posts[cat].append(post)

        for cat, posts in cat_posts.items():
            abs_path = os.path.join(cats_path, cat)
            if not os.path.isdir(abs_path):
                continue
            template = env.get_template("category.html")
            cat_html = template.render(cat=cat, posts=posts)
            cat_index = os.path.join(abs_path, "list.html")
            with open(cat_index, "w") as ts:
                ts.write(cat_html)
        
        template = env.get_template("categories.html")
        cats_html = template.render()

        with open(os.path.join(PAGES_DIR, "categories.html"), "w") as ts:
            ts.write(cats_html)

    except Exception as e:
        if os.getenv("DEBUG") is not None:
            raise e
        return False

    return True

def generate_projects():
    try:
        with open("_data/_projects.json", "r") as fs:
            projects = json.load(fs)

        template = env.get_template("projects-archive.html")
        projects_html = template.render(projects=projects)
        
        with open(os.path.join(PAGES_DIR, "projects.html"), "w") as ts:
            ts.write(projects_html)
            ts.close()

    except Exception as error:
        if os.getenv("DEBUG") is not None:
            logger.info(str(error))
        return False
    return True


def set_template_globals(env: Environment):
    env.globals["site_repo"] = "https://github.com/csr13/csr13.github.io"
    env.globals["https_site"] = "https://www.csr13.me"
    env.globals["http_site"] = "http://www.csr13.me"
    env.globals["github_site"] = "https://csr13.github.io"
    env.globals["media_posts_pdf_root"] = "/media/documentation/pdfs/posts/"
    env.globals["categories_path"] = "/pages/posts/categories"
    env.globals["all_posts"] = get_posts()
    env.globals["categories"] = get_categories()
    env.globals["system_status"] = "In progress - online"
    return True


def generate_sitemap():
    try:
        url = "https://www.csr13.me"
        home = "https://www.csr13.me/"
        date = datetime.datetime.today().__str__()[:10]
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>%s</loc>
        <lastmod>%s</lastmod>
        <changefreq>always</changefreq>
        <priority>1.0</priority>
    </url>
        ''' % (url, date)
        
        pages = []
        for root, dirs, files in os.walk(PAGES_DIR):
            for d in dirs:
                _files = os.path.join(root, d)
                for _file in os.listdir(_files):
                    path = os.path.join(root, d, _file)
                    if not (os.path.isfile(path) and path.endswith(".html")):
                        continue
                    pages.append("%s/%s" % (url, path.strip("/root/site/")))

        for page in pages:
            xml += '''
    <url>
        <loc>%s</loc>
        <lastmod>%s</lastmod>
        <changefreq>always</changefreq>
        <priority>0.5</priority>
    </url>
            ''' % (page, date)

        xml += '''
</urlset>
        '''

        with open(os.path.join(THIS_DIR, "sitemap.xml"), "w") as ts:
            ts.write(xml)
            ts.close()

    except Exception as error:
        if os.getenv("DEBUG") is not None:
            logger.info(str(error))
        return False
    return True


        
def main():
    set_template_globals(env)
    errors = []
    if not generate_index():
        errors.append("Unable to generate index")
    if not generate_posts():
        errors.append("Unable to generate posts")
    if not generate_projects():
        errors.append("Unable to generate projects")
    if not generate_sitemap():
        errors.append("Unable to generate sitemap")
    if len(errors) > 0:
        for error in errors:
            print("[ERROR] %s" % error)
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
