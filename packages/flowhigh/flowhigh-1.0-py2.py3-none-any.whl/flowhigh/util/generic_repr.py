def generic_repr(cls):
    """ Injects a generic repr function """

    def generic_repr_func(that):
        class_items = [f'{k}={v}' for k, v in vars(that).items()]
        return f'<{that.__class__.__name__} ' + ', '.join(class_items) + '>'

    cls.__repr__ = generic_repr_func
    return cls
