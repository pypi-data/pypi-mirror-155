from requests import get
import json
from stopwatch import Stopwatch

page = 1
stopwatch = Stopwatch()

def repair():
    status = get("https://api.meower.org/status").text
    try:
        load = json.loads(status)
        return load["isRepairMode"]
    except json.decoder.JSONDecodeError:
        pass

def find_post(id):
    global page
    home = get(f"https://api.meower.org/home?page={page}").text
    try:
        load = json.loads(home)
        return load["index"][id]
    except json.decoder.JSONDecodeError:
        pass

def get_home():
    global page
    home = get(f"https://api.meower.org/home?page={page}").text
    try:
        load = json.loads(home)
        return json.loads(load["index"])
    except json.decoder.JSONDecodeError:
        pass

def home_len():
    global page
    home = get(f"https://api.meower.org/home?page={page}").text
    try:
        load = json.loads(home)
        return len(load["index"])
    except json.decoder.JSONDecodeError:
        pass

def get_post(id):
    post = get(f"https://api.meower.org/posts?id={id}").text
    try:
        load = json.loads(post)
        return load["u"] + ": " + load["p"]
    except json.decoder.JSONDecodeError:
        pass

def page_len():
    global page
    home = get(f"https://api.meower.org/home?page={page}").text
    try:
        load = json.loads(home)
        return load["pages"]
    except json.decoder.JSONDecodeError:
        pass

def current_page():
    global page
    home = get(f"https://api.meower.org/home?page={page}").text
    try:
        load = json.loads(home)
        if (page != load["page#"]):
            page = load["page#"]
        return load["page#"]
    except json.decoder.JSONDecodeError:
        pass

def change_page(page_num):
    global page
    page = page_num

def ping():
    stopwatch.start()
    get("https://api.meower.org/")
    stopwatch.stop()
    return stopwatch.elapsed