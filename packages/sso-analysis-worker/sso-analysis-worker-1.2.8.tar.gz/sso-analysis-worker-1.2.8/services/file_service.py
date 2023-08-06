from os import path


def read_line_from_file(filename: str, line_number: int) -> str:
    return_line = None
    with open(filename) as file:
        for i, line in enumerate(file):
            if i == line_number:
                return_line = line
                break
    return return_line


def save_to_file(file_path: str, base_page: str, ids: list) -> bool:
    if not path.isfile(file_path):
        with open(file_path, "w") as file:
            file.write("Site,Found Google,Found Facebook,Found Apple\n")
    with open(file_path, "a") as file:
        file.write(base_page)
        google_found = None
        facebook_found = None
        apple_found = None
        for id in ids:
            if google_found is None and id[0] == 1:
                google_found = id
            if facebook_found is None and id[0] == 2:
                facebook_found = id
            if apple_found is None and id[0] == 3:
                apple_found = id
        file.write("," + ("\"" + str(google_found) + "\"" if google_found is not None else "False"))
        file.write("," + ("\"" + str(facebook_found) + "\"" if facebook_found is not None else "False"))
        file.write("," + ("\"" + str(apple_found) + "\"" if apple_found is not None else "False"))
        file.write("\n")
    return True
