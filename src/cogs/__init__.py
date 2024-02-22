from pkgutil import iter_modules

EXTENSIONS = [e.name for e in iter_modules(__path__, f"{__package__}.")]