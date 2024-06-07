import time
from PyQt5.QtCore import QThread, pyqtSignal

class BackgroundWorkThread(QThread):
    task_finished = pyqtSignal()

    def __init__(self, work_function=None, items=None):
        super().__init__()
        self.work_function = work_function
        self.items = items

    def run(self):
        if self.items:
            self.work_function(*self.items)
        else:
            self.work_function()
        self.task_finished.emit()


class ProgressBar(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, total_time, total_items):
        super().__init__()
        self.total_time = total_time * total_items
        self.start_time = time.time()

    def run(self):
        while time.time() - self.start_time < self.total_time:
            elapsed_time = time.time() - self.start_time
            progress = int((elapsed_time / self.total_time) * 100)
            self.update_progress.emit(progress)
            time.sleep(0.5)