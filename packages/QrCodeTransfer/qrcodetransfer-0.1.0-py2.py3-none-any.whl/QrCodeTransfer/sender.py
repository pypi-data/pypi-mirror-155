import base64
import logging
import math
import sys
import argparse
from time import sleep

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqrcode

tempfile = 'temp.png'

class SendConfig:
    def __init__(self, interval=100, data_maxlen=2000, window_pos=(0,0)):
        self.send_interval = interval
        self.send_len = data_maxlen
        self._window_pos = window_pos

class MainWindow(QMainWindow):
    def __init__(self, config:SendConfig) -> None:
        QMainWindow.__init__(self)
        self.config = config
        self._lost_indices = None
        self._send_file = None

        self._label = QLabel(self)
        self.show_qrcode('x'*self.config.send_len, True)
        self._label.setText(' ')

        self._timer=QTimer()
        self._timer.timeout.connect(self.on_send_timer)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        action = QAction(QIcon('open.png'), '&Start Send', self)
        action.setShortcut('Ctrl+S')
        action.setStatusTip('Start send')
        action.triggered.connect(self.on_start_send)
        file_menu.addAction(action)
        self._start_menu = action

        action = QAction(QIcon('open.png'), 'S&top Send', self)
        action.setShortcut('Ctrl+E')
        action.setStatusTip('stop send')
        action.triggered.connect(self.on_stop_send)
        file_menu.addAction(action)
        self._stop_menu = action
        self._stop_menu.setEnabled(False)

        action = QAction(QIcon('open.png'), 'Demo Qr', self)
        action.triggered.connect(self.demo_qr)
        file_menu.addAction(action)

    def demo_qr(self):
        data = open(self._send_file, 'rb').read()
        encode_data = base64.b64encode(data).decode('utf8')
        print(len(data), ' encode data len=', len(encode_data))
        self.show_qrcode(encode_data[0:2000])

    def set_lost_indices(self, lostIndices):
        self._lost_indices = lostIndices

    def set_send_file(self, send_file):
        self._send_file = send_file

    def show_qrcode(self, data, resize=False):
        pyqrcode.create(data, error='L', encoding=None).png(tempfile, scale=6)
        pixmap = QPixmap(tempfile)
        self._label.setPixmap(pixmap)
        self._label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        if resize:
            print(self.geometry())
            self.resize(pixmap.width(), pixmap.height())

    def on_start_send(self):
        pos = self.config._window_pos
        self.move(pos[0], pos[1])

        if self._send_file is None:
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self,"select file", "","All Files (*);;Python Files (*.py)", options=options)
            if not file_name:
                return

            self._send_file = file_name

        self._send_data = base64.b64encode(open(self._send_file, 'rb').read()).decode('utf8')
        max = math.ceil(len(self._send_data)/self.config.send_len)
        indices = range(0, max)
        if not self._lost_indices is None:
            indices = self._lost_indices
        self._indices_iter = iter(indices)
        self._cur_count = 0
        self._max_count = len(indices)
        self._stop_menu.setEnabled(True)
        self._start_menu.setEnabled(False)
        self._frame_id = 0

        self.send(">meta max=%d"%max)
        self._timer.start(self.config.send_interval)

    def on_stop_send(self):
        self.send('>quit')
        self._timer.stop()
        self._stop_menu.setEnabled(False)
        self._start_menu.setEnabled(True)

    def on_send_timer(self):
        try:
            cur_index = next(self._indices_iter)
        except StopIteration:
            self.on_stop_send()
            return

        self._cur_count += 1
        data_maxlen = self.config.send_len
        if cur_index*data_maxlen >= len(self._send_data):
            print('invalid index', cur_index)
            return

        data = self._send_data[cur_index*data_maxlen:(cur_index+1)*data_maxlen]
        self.show_status('send cur=%d max=%d curLen=%d' % (self._cur_count, self._max_count, len(data)))
        self.send('%d:%s' % (cur_index, data))
        
    def send(self, data):
        self._frame_id += 1
        self.show_qrcode(str(self._frame_id) + " " + data)

    def show_status(self, text):
        self.setWindowTitle(text)

def parse_indices(filename):
    with open(filename, 'r') as f:
        content = f.read()
        return [int(x) for x in content.split(',')]

def split_file(config:SendConfig, filename):
    send_data = base64.b64encode(open(filename, 'rb').read()).decode('utf-8')
    max = math.ceil(len(send_data)/config.send_len)
    with open(filename + '.split', 'w') as f:
        for i in range(0, max):
            f.write(send_data[i*config.send_len:(i+1)*config.send_len])
            f.write("\n")
    print('split to file {}'.format(filename + '.split'))

def show_main(send_file=None, lost_indices_file=None):
    app = QtWidgets.QApplication([])
    main_win = MainWindow(SendConfig())
    main_win.set_send_file(send_file)
    if lost_indices_file:
        main_win.set_lost_indices(parse_indices(lost_indices_file))

    main_win.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    main_win.show()
    sys.exit( app.exec_() )

def main():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')

    sub_parser = sub_parsers.add_parser('split', help='split file, for debug purpose (diff)')
    sub_parser.add_argument('filename', help='file to split')
    sub_parser.set_defaults(func=lambda args: split_file(SendConfig(), args.filename))

    sub_parser = sub_parsers.add_parser('ui', help='show main ui')
    sub_parser.add_argument('--filename', help='file to send')
    sub_parser.add_argument('--lost_indices_file', help='file contain lost indices, separated by comma')
    sub_parser.set_defaults(func=lambda args: show_main(args.filename, args.lost_indices_file))

    args = parser.parse_args(sys.argv[1:])
    # print(args)
    args.func(args)

if __name__ == '__main__':
    main()