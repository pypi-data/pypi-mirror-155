from enum import Enum


class Status(Enum):
    INIT = 0
    PREPARE_RECORDING = 2
    RECORDING = 3
    RECORDING_FINISH = 1
    ERROR = 4
    PREPARE_UPLOADING = 5
    UPLOADING = 6
    UPLOADING_FINISH = 7
