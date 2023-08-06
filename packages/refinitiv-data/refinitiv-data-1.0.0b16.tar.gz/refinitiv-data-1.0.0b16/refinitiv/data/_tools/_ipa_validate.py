def do_all_elements_have_error(data: dict, elements: list) -> bool:
    counter = len(elements) or 1
    for element in elements:

        if not hasattr(element, "get"):
            counter -= 1
            data["error_message"] = f"Invalid data type={type(element)}, data={element}"
            continue

        error = element.get("error")

        if error:
            counter -= 1
            error_codes = data.setdefault("error_code", [])
            error_code = error.get("code")
            error_codes.append(error_code)
            error_messages = data.setdefault("error_message", [])
            error_message = error.get("message")
            error_messages.append(error_message)

    if counter == 0:
        return True

    return False
