import os


def path_join(*args):
    path_ = os.path.abspath(__file__)
    path_ = path_[:path_.find('bin')]
    path_ = os.path.join(path_, *args)
    return path_
