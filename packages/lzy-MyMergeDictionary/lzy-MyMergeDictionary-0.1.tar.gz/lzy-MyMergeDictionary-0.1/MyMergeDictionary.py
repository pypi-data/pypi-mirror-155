def MyMergeDictionary(*args):
    for dict in args[1:]:
        for key, value in dict.items():
            if key in args[0]:
                args[0][key] += value
            else:
                args[0][key] = value
    return args[0]