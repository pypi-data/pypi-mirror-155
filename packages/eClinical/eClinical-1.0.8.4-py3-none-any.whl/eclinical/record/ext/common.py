HOST = "200.200.101.113"
import json


def wash(func):
    def wrapper(*args, **kwargs):
        if args[1].request.host != HOST and not args[1].request.path.startswith("/api/"):
            return func(*args, **kwargs)

    return wrapper


def empty_string(content: str):
    return len(content.strip()) == 0


def disable_elements(*elements):
    for element in elements:
        element.Disable()


def enable_elements(*elements):
    for element in elements:
        element.Enable()


def read_parameter():
    with open('parameter.json', 'r') as f:
        return json.loads(f.read())


def write_parameter(**kwargs):
    with open('parameter.json', 'w') as f:
        f.write(json.dumps(kwargs))


if __name__ == '__main__':
    print(read_parameter().get("a"))
