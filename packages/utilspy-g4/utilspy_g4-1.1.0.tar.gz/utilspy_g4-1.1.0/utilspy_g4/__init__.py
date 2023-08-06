import os
import cv2


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


def compareFrames(framePath_1: str, framePath_2: str) -> bool:
    """
    Compare 2 frames
    :param framePath_1: Path to frame 1
    :param framePath_2: Path to frame 2
    :return: bool
    """

    # TODO: Check different frames size

    frame_1 = cv2.imread(framePath_1)
    frame_2 = cv2.imread(framePath_2)
    diff = cv2.norm(frame_1, frame_2, cv2.NORM_L2)

    if diff == 0.0:
        return True

    return False
