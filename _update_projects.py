import json

import requests

from _logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    try:
        url = "https://api.github.com/users/csr13/repos"
        resp = requests.get(url)
        if not resp.status_code in [200]:
            raise Exception("Unable to get repos") from None
        else:
            logger.info("Projects pulled from gh")
            repos = resp.json()

        clean_repos = []
        for repo in repos:
            name = repo["name"]
            if name == "csr13.github.io":
                continue
            language = repo["language"]
            licence = repo["license"]
            url = repo["url"]
            default_branch = repo["default_branch"]
            description = repo["description"]
            html_url = repo["html_url"]
            owner = repo["owner"]["login"]
            size = repo["size"]
            topics = repo["topics"]
            zipped_repo = "https://github.com/%s/%s/archive/refs/heads/%s.zip" % (
                owner, name, default_branch
            )
            clean_repos.append(
                dict(
                    name=name, 
                    language=language, 
                    licence=licence, 
                    url=url,
                    default_branch=default_branch,
                    description=description,
                    html_url=html_url,
                    owner=owner,
                    size=size,
                    topics=topics,
                    zipped_repo=zipped_repo
                )
            )
                    
        logger.info("Writing to  ./_data/_projects.json") 
        with open("_data/_projects.json", "w") as fs:
            json.dump(clean_repos, fs)

    except Exception as e:
        if os.getenv("DEBUG") is not None:
            raise e
