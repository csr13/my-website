import json

import requests
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("p", "_templates"),
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


def main():
    if not generate_projects_page():
        return False
    return True


if __name__ == "__main__":
    main()
