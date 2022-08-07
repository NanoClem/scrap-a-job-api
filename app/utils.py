from http.cookies import SimpleCookie


def parse_cookies(raw_cookie: str) -> dict[str, str]:
    cookie_parser = SimpleCookie()
    cookie_parser.load(raw_cookie)
    return {k: v.value for k, v in cookie_parser.items()}