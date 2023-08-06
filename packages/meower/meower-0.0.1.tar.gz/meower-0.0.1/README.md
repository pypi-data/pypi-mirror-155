# meower.py
Python library for interacting with the Meower API
## Commands
- `meower.repair()` - Checks if the server is in repair mode
- `meower.post_id(num)` - A very misleading name. Downloads home, then finds the post number
- `meower.home()` - Downloads home
- `meower.home_len()` - Shows the number of posts on home
- `meower.get_post(str)` - Gets the specified post, and shows in `username: post` format
- `meower.page_len()` - Shows the number of home pages
- `meower.current_page()` - Returns the current page number
- `meower.change_page(num)` - Changes the page
- `meower.ping()` - "Pings" the Meower API, by fetching