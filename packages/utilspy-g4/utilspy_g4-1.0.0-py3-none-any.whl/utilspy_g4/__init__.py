import os


def addExt(path: str, ext: str) -> str:
    """
    Add ext to path

    :param path: Path to file
    :param ext: Added ext
    :rtype: str
    :return: Path with added ext
    """

    pathExt = os.path.splitext(path)
    return pathExt[0] + '.' + ext + pathExt[1]