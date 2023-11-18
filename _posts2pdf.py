import os

import pdfkit

from _logger import get_logger


logger = get_logger(__name__)

this_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def main():
    posts_dir = "pages/posts"
    pdf_posts_dir = "media/documentation/pdfs/posts"


    if not os.path.exists(pdf_posts_dir):
        os.makedirs(pdf_posts_dir)

    options = {
        "enable-local-file-access": None,
        "user-style-sheet" : "static/css/main.css",
        "user-style-sheet" : "static/css/code-styles.css"
    }
    for each in os.listdir(posts_dir):
        name = each.replace(".html", ".pdf")
        with open(os.path.join(posts_dir, each), "r") as ts:
            pdfkit.from_file(
                ts, 
                os.path.join(pdf_posts_dir, name), 
                options=options,
            )

    return True


if __name__ == "__main__":
    main()

