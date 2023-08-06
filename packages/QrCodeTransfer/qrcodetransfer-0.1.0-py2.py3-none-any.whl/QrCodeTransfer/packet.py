

def pack(frame_id, data):
    return '%d %s' % (frame_id, data)

def unpack(data):
    frame_id, data = data.split(' ', 1)
    return int(frame_id), data
