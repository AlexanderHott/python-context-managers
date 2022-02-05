# Python Context Managers

Using a context manager in python can help you manage resources that need to be manually closed. For example, you might want to open a file, read it, and then close it. Using a context manager allows you to skip calling the `file.close()` method.

## Without context manager

```py
file = open("file.txt", "r")
print(file.read())
file.close()
```

## With context manager

```py
with open("file.txt", "r") as f:
    print(f.read())
```

# Creating Custom Context Managers

You can create your own context managers by creating a class that implements the `__enter__` and `__exit__` (or `__aenter__` and `__aexit__` for asnyc) methods.

```py
class Ctx:
    def __init__(self, resource):
        self.resource = resource

    def __enter__(self):
        return self.resource.open()

    def __exit__(self, *_):
        self.resource.close()

with Ctx(...) as ctx:
    print(ctx)
```

You can also use `contextlib.contextmanager`.

```py
@contextlib.contextmanager
def manage_context(resource):
    try:
        yield resource.open():
    finally:
        resource.close()

with manage_context(...) as ctx:
    print(ctx) 
```