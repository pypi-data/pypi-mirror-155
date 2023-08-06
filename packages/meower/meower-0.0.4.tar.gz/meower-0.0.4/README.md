# meower.py
Python library for interacting with the Meower API
## Commands
- `meower.repair()` - Checks if the server is in repair mode
- `meower.find_post(num)` - Downloads home, then finds the post number
- `meower.get_home()` - Downloads home
- `meower.home_len()` - Shows the number of posts on home
- `meower.get_post(str)` - Gets the specified post, and shows in `username: post` format
- `meower.page_len()` - Shows the number of home pages
- `meower.current_page()` - Returns the current page number
- `meower.change_page(num)` - Changes the page
- `meower.ping()` - "Pings" the Meower API, by timing `requests` to fetch the root page
## Installing
`meower.py` is now on PyPI (Python Package Index)! That means that you can use `pip3`, or `pip` to install it now!
### Linux
```
pip3 install meower
```
### Windows
```
py -m pip install meower
```
## Usage
For some reason (maybe because of the lack of a class), you can't use the traditional `import meower` method. Instead, use:
```python
from meower import meower
```
## Building
You can use the following commands corresponding to your OS:
### Linux
```
python3 -m build
```
### Windows
```
py -m build
```
## Upgrading
`meower.py` is a ongoing project, so you'd might want to check for updates regularly. You can update the package like this:
### Linux
```
pip3 install meower==[latest version]
```
### Windows
```
py -m pip install meower==[latest version]
```