import traceback
import time
from MonolithTime import MonolithTime
from SearchResult import SearchResult
from playsound import playsound
from PIL import ImageGrab
import cv2
import win32gui
import win32api
import numpy as np

# edit this, set your resolution
myResolution = (2560, 1386)

REFERENCE_RESOLUTION = (2560, 1386)  # do not change
multiplier = myResolution[0] / REFERENCE_RESOLUTION[0]

searchingPos = [
    (int(1200 * multiplier), int(60 * multiplier)),
    (int(1370 * multiplier), int(130 * multiplier)),
]
# value at [1] should be size, not point
searchingPos[1] = (
    searchingPos[1][0] - searchingPos[0][0],
    searchingPos[1][1] - searchingPos[0][1],
)

numbers = [cv2.imread(f"./img/{i}.bmp", cv2.IMREAD_GRAYSCALE) for i in range(0, 10)]
if multiplier < 1:
    for i in range(0, len(numbers)):
        width = int(numbers[i].shape[1] * multiplier)
        height = int(numbers[i].shape[0] * multiplier)
        dim = (width, height)
        numbers[i] = cv2.resize(numbers[i], dim, interpolation=cv2.INTER_AREA)

mainWindow = None


def getScreenshot():
    global mainWindow

    def rect(hwnd):
        _left, _top, _right, _bottom = win32gui.GetClientRect(hwnd)
        left, top = win32gui.ClientToScreen(hwnd, (_left, _top))
        right, bottom = win32gui.ClientToScreen(hwnd, (_right, _bottom))
        return left, top, right, bottom

    desktop = ImageGrab.grab(rect(mainWindow))
    frame = cv2.cvtColor(np.array(desktop), cv2.COLOR_BGR2GRAY)
    return frame
    # return cv2.imread("./img/poe.bmp", cv2.IMREAD_GRAYSCALE)


def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(
            idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0]))
        )
    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")


def getTimer():
    res: list[SearchResult] = []

    refSm = getScreenshot()[
        searchingPos[0][1] : searchingPos[0][1] + searchingPos[1][1],
        searchingPos[0][0] : searchingPos[0][0] + searchingPos[1][0],
    ]

    for i in range(0, 10):
        result = cv2.matchTemplate(refSm, numbers[i], cv2.TM_CCOEFF_NORMED)

        h, w = numbers[i].shape[:2]

        result = np.where(result >= 0.81)
        boxes = np.array(
            [
                *map(
                    lambda x: np.concatenate((x, np.array([x[0] + w, x[1] + h]))),
                    np.column_stack(result),
                )
            ]
        )
        for point in non_max_suppression_fast(boxes, 0.1):
            try:
                MPx, *_ = point
                res.append(SearchResult(MPx, i))
            except Exception:
                print(
                    "EXCEPTION ",
                    traceback.format_exc(),
                    "\n",
                    f"{point=} {h=} {w=}"
                )

    res.sort(key=lambda x: x.pos)

    if len(res) == 4:
        return MonolithTime(res[1].num, res[2].num * 10 + res[3].num)
    else:
        return MonolithTime(0, 0)


print("Focus main window, then press END")
while win32api.GetKeyState(0x23) >= 0:
    time.sleep(1 / 1000)
mainWindow = win32gui.GetForegroundWindow()

nextReset = None

print("Starting")
while True:
    timer = getTimer()
    if not timer.isStarted():
        time.sleep(1)
        continue
    print(timer)
    if not nextReset:
        nextReset = timer.getNextReset()
        continue

    if nextReset == timer:
        nextReset = timer.getNextReset()
        playsound("./audio/notification.mp3", block=False)
        time.sleep(2)
    else:
        time.sleep(0.1)
