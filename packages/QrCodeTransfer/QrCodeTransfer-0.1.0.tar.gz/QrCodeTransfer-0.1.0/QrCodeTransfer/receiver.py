
from ast import alias
import base64
from time import sleep
from PIL import Image
from PIL import ImageGrab
import os
import sys
import re
import argparse
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode

import packet


def log(level, *msg):
    if level<3:
        print(*msg)

class RecordConfig:
    '''record config'''
    def __init__(self, grab_size=1000, grab_topleft=(0,0), wait_time=0.01, save_image=False):
        self.grab_size = grab_size
        self.grab_topleft = grab_topleft
        self.wait_time = wait_time
        self.save_image = save_image

class Recorder:
    '''record qr code image and text'''

    def __init__(self, config:RecordConfig, save_file:str):
        self.config = config
        self._save_file = save_file
        self._symbols=[ZBarSymbol.QRCODE]

    def _record_one(self, record_id:str):
        log(3, 'recording %s' % record_id)
        topleft = self.config.grab_topleft
        img = ImageGrab.grab(bbox=(topleft[0], topleft[1],topleft[0]+self.config.grab_size,topleft[1]+self.config.grab_size))
        if self.config.save_image:
            img.save(os.path.join(os.path.dirname(self._save_file), record_id+'.png'))

        data = decode(img, self._symbols)
        if len(data) == 0:
            return
        
        text = data[0].data.decode('utf-8')
        frame_id, text = packet.unpack(text)
        if frame_id == self._last_frame_id:
            return

        self.write_file(text)
        self.write_file('\n')
        if text.startswith('>'):
            log(1, 'command %s' % text)

            if text == '>quit':
                self.stop()
            return

        pos = text.find(':')
        if pos != -1:
            new_index = int(text[0:pos])
            for i in range(self._cur_index, new_index-1):
                log(3, 'missing ', i)
            self._cur_index = new_index

    def write_file(self, data):
        '''write data to file'''
        self._file_handle.write(data)

    def start(self):
        '''record the image and the recognition text '''
        self._recording = True
        self._cur_index = 0
        self._file_handle = open(self._save_file, 'a')
        self._last_frame_id = -1
            
        record_id = 1
        while self._recording:
            try:
                self._record_one(str(record_id))
            except:
                pass
            record_id += 1
            sleep(self.config.wait_time)

    def stop(self):
        '''stop recording'''
        if self._recording:
            self._recording = False

            self._file_handle.close()
            self._file_handle = None

def merge_records(dir):
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                with open(os.path.join(dirpath, filename), 'r') as fin:
                    content = fin.read()

                index = content.find(':')
                if index != -1:
                    print(int(content[0:index]), content)
        break

def show_lost_indices(in_file):
    '''print missing indices'''
    indices, max_index = get_block_map(in_file)
    losts = get_lost_indices(indices, max_index)
    losts = [str(i) for i in losts]
    print(','.join(losts))

def get_block_map(in_file):
    lines = []
    with open(in_file, 'r') as fin:
        lines = fin.readlines()

    blocks_map = {}
    max_index = 0
    for line in lines:
        match = re.match('^([0-9]*):(.*)', line)
        if match and len(match.groups()) > 0:
            index = int(match.groups()[0])
            blocks_map[index] = match.groups()[1]
            if index > max_index:
                max_index = index
    return blocks_map, max_index

def get_lost_indices(indices, max_index):
    losts = []
    for i in range(0, max_index+1):
        if not i in indices:
            losts.append(i)
    return losts

def restore(record_file, save_file):
    '''restore the final file from record file'''
    indices, max_index = get_block_map(record_file)
    losts = get_lost_indices(indices, max_index)
    if len(losts):
        raise Exception('lost indices: %s' % losts)

    lines = []
    for i in range(0, max_index+1):
        lines.append(indices[i])

    lines_to_bytes = '\n'.join(lines).encode('utf-8')
    # with open(save_file+'.temp', 'wb') as fout:
    #     fout.write(lines_to_bytes)

    content = base64.b64decode(lines_to_bytes)
    with open(save_file, 'wb') as fout:
        fout.write(content)
    
def do_record(args):
    config = RecordConfig(save_image=args.save_image)
    Recorder(config, args.filename).start()

def do_restore(args):
    restore(args.filename, args.filename+'.7z')

def do_print_lost(args):
    show_lost_indices(args.filename)

def main():
    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers(help='sub-command help', dest='command')
    sub_parser = sub_parsers.add_parser('record', help='record the image and the recognition text')
    sub_parser.add_argument('filename', help='record file')
    sub_parser.add_argument('--save_image', help='is images saved', action='store_true')
    sub_parser.set_defaults(func=do_record)

    sub_parser = sub_parsers.add_parser('restore', help='restore file from the records file')
    sub_parser.add_argument('filename', help='restore file name')
    sub_parser.set_defaults(func=do_restore)

    sub_parser = sub_parsers.add_parser('print_lost', help='print the lost indices', aliases='lost')
    sub_parser.add_argument('filename', help='the record file')
    sub_parser.set_defaults(func=do_print_lost)

    args = parser.parse_args(sys.argv[1:])
    # print(args)
    args.func(args)

if __name__ == '__main__':
    main()