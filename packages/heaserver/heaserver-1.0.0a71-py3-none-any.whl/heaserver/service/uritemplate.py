import regex as re
from contextlib import suppress

TEMPLATE_NAMES_PATTERN = re.compile("\\{([\\w\\?;][-\\w\\.,]*)\\}")


def tvars(route: str, url: str) -> dict[str, str]:
    pattern = _to_regex(route)
    match = pattern.fullmatch(url, partial=True)
    while match and match.partial:
        route = route[:-1]
        with suppress(Exception):
            match = _to_regex(route).fullmatch(url, partial=True)
    return match.groupdict() if match else {}


def _to_regex(route: str) -> re.Pattern:
    metadata_ = _metadata(route)
    l = []
    for m in metadata_:
        if m[3]:
            l.append(r'(?P<' + m[0] + r'>.+)')
        else:
            l.append(m[0])
    return re.compile(''.join(l))


def _metadata(route: str):
    if route is None:
        raise ValueError('route cannot be None')
    m = {match.group(): (match.start(), match.end()) for match in
         TEMPLATE_NAMES_PATTERN.finditer(route)}
    split_ = TEMPLATE_NAMES_PATTERN.split(route)
    start = 0
    i = 0
    for k, v in m.items():
        if v[0] > start:
            yield split_[i], start, v[0], False
            start = v[1]
            i += 1
        yield split_[i], v[0], v[1], True
        i += 1
    else:
        route_len = len(route)
        if route_len > start:
            yield split_[i], start, route_len, False
