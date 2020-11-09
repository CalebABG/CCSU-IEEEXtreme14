BREAK_CHARS = {'\n', '\r', ' ', ',', '.', '?', '!'}


def get_all_lines(file_name=None):
    lines = []
    if file_name is not None:
        with open(file_name) as file:
            lines = file.readlines()[2:]
    else:
        while True:
            try:
                line = input()
                if line is None or len(line) == 0:
                    break
                lines.append(line)
            except:
                break

    return lines


def _split(value: str, delimiter: str):
    return value.replace("\n", "").split(delimiter)


def get_stops_and_indexes(file_name=None):
    _tuple = None
    if file_name is not None:
        with open(file_name) as file:
            stop_words = set(_split(file.readline(), ';'))
            index_terms = set(_split(file.readline(), ';'))
            _tuple = (stop_words, index_terms)
    else:
        stop_words = set(_split(input(), ';'))
        index_terms = set(_split(input(), ';'))
        _tuple = (stop_words, index_terms)

    return _tuple


def break_char_found(c):
    return c in BREAK_CHARS
