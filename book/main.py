import bs4
import requests

MAIN_PAGE = "https://comp24.sci2u.dk/book/"
BASE = "https://comp24.sci2u.dk"
LOGIN = "https://comp24.sci2u.dk/user/login/?next=/book/"

CLASSES_REMOVE = [
        "alert-warning",
        "btn",
        "btn-group",
        "modal-fade",
        "modal-content"
        ]

session = requests.session()

response = session.get(MAIN_PAGE)
cookies = response.cookies

csrf_token = cookies["csrftoken"]
print("Token gained.")


def get_creds():
    with open(".pass") as f:
        return f.read().splitlines()

username, password = get_creds()

resp = session.post(LOGIN, data={"csrfmiddlewaretoken": csrf_token, "username": username, "password": password})

assert "Invalid username or password" not in resp.text

def get_booklet(booklet_number):
    return session.get(f"https://comp24.sci2u.dk/book/booklet/{booklet_number}/")


def get_exercises_links(booklet_number):
    booklet = get_booklet(booklet_number)
    bs4_booklet = bs4.BeautifulSoup(booklet.text, "html.parser")

    # Find all 'a' tags that contain text with "Exercise"

    # exercises = bs4_booklet.find_all("a", text=lambda text: text and "Exercise" in text)

    # Find all with class 'nav-link' and 'text-dark' and id contains 'sidebar_collection'
    exercises = bs4_booklet.find_all("a", class_="nav-link", id=lambda id_: id_ and "sidebar_collection" in id_)

    links = [BASE + exercise["href"] for exercise in exercises]

    return links

# booklets go in increments of 2 from 4 to 16
def get_exercise(exercise_link: str):
    return session.get(exercise_link)


IMAGE_COUNT = 0
def handle_images(exercise):
    """
    Download images, then change url to local computer
    """

    global IMAGE_COUNT

    for img in exercise.find_all("img"):
        link = BASE + img["src"]

        session.get(link)

        with open("images/" + str(IMAGE_COUNT) + ".png", "wb") as f:
            f.write(session.get(link).content)

        img["src"] = "images/" + str(IMAGE_COUNT) + ".png"

    IMAGE_COUNT += 1

    return exercise


def remove_unnecessary_classes(exercise):
    for class_ in CLASSES_REMOVE:
        for tag in exercise.find_all(class_=class_):
            tag.decompose()

    return exercise


combined_html = bs4.BeautifulSoup()

katex_load_tag = combined_html.new_tag("script")
katex_load_tag["src"] = "render_katex.js"

combined_html.append(combined_html.new_tag("html"))
combined_html.html.append(combined_html.new_tag("body"))
combined_html.html.append(combined_html.new_tag("head"))
combined_html.head.append(katex_load_tag)

code_prettifier_tag = combined_html.new_tag("link")
code_prettifier_tag["rel"] = "stylesheet"
code_prettifier_tag["type"] = "text/css"
code_prettifier_tag["href"] = "https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/prettify.css"

head_appended = False

for booklet in range(4, 20, 2):
    print("fetching booklet " + str(booklet))
    for link in get_exercises_links(booklet):
        exercise = bs4.BeautifulSoup(get_exercise(link).text, "html.parser")

        # handle images
        exercise = handle_images(exercise)

        # remove unnecessary classes
        exercise = remove_unnecessary_classes(exercise)

        # From exercise.body only append the div with class "book-padding"
        exercise_body_add = exercise.body.find("div", class_="book-padding")

        combined_html.body.append(exercise_body_add)

        if head_appended == False:
            combined_html.head.append(exercise.head)
            head_appended = True


# link = get_exercises_links(4)[0]
# exercise = get_exercise(link)
# print(exercise)

with open("output.html", "w") as f:
    f.write("<!DOCTYPE html>\n" + combined_html.prettify())
