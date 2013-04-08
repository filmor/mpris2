def enum(name='Enum', *args, **kwargs):
    items = {}

    for index, item in enumerate(args):
        items[item] = index

    items.update(**kwargs)

    return type(name, (), items)