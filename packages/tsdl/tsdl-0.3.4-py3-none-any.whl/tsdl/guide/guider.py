from tsdl.common import util, assist
from tsdl.core import command
from tsdl.core.context import Context


def handle_session_negotiate(context: Context, esam_return_parses: dict):
    """
    处理会话协商
    """
    for pos, parse in esam_return_parses.items():
        context.meters.get(pos).session.negotiate(parse)


def handle_session_verify(context: Context, connect_return_parses: dict):
    """
    处理会话验证
    """
    for pos, parse in connect_return_parses.items():
        context.meters.get(pos).session.verify_session(parse)


def handle_meter_channels(context: Context):
    """
    处理通道
    """
    pos_channel = {}
    for pos, meter in context.meters.items():
        pos_channel[pos] = meter.baudrate()

    return pos_channel


def handle_encode_frames(context: Context, encode_frame_parse: dict, **session):
    """
    处理组帧
    """
    parses = {}
    for pos, meter in context.meters.items():
        parses[pos] = util.replace(encode_frame_parse, comm_addr=meter.addr)
        sd = {}
        for k, v in session.items():
            sd[k] = eval('context.meters.get(pos).session.{}'.format(v.lower().replace('_', '.')))

        if len(sd) > 0:
            parses[pos] = util.replace(parses[pos], **sd)

    frames = {} if len(parses) > 0 else None
    for pos, parse in parses.items():
        fr = command.encode(context, parse, cache='{}#{}'.format(assist.cache.name, pos))
        frames[pos] = fr.get('frame')

    return frames


def handle_decode_frames(context: Context, app_return_result: dict):
    """
    处理解帧
    """
    parses = {}
    for pos, frame in app_return_result['result'].items():
        parses[pos] = command.decode(context, frame, cache='{}#{}'.format(assist.cache.name, pos))

    # 分帧处理开始
    framing_frames = {} if len(parses) > 0 else None
    for pos, parse in parses.items():
        next_frame = __handle_framing(context, pos, parse)
        if next_frame is not None:
            framing_frames[pos] = next_frame

    if framing_frames is not None and len(framing_frames) > 0:
        parses = handle_decode_frames(context, __send_next(context, framing_frames))
    # 分帧处理结束

    return parses


def __handle_framing(context: Context, pos: str, parse: dict):
    """
    处理分帧
    """
    part_frame_key = '{}:part:frame'.format(pos)

    protocol = parse['meta']['name']
    comm_addr = parse['parse']['address']['server']['value']
    link_data = parse['parse']['link_data']

    framing = link_data.get('framing')

    get_next_frame = None
    if framing is not None:
        if framing.get('type') != 'FINAL':
            """
                缓存分帧
            """
            parts = assist.cache.get(part_frame_key)
            if parts is None or parts == 'NULL':
                assist.cache.set(part_frame_key, link_data.get('part_frame', '').strip())
            else:
                assist.cache.set(part_frame_key, (parts + ' ' + link_data.get('part_frame', '')).strip())

            """
                获取读取下一帧
            """
            get_next = assist.manual.protocol(protocol, 'get:next', comm_addr=comm_addr)
            get_next_frame = command.encode(context, get_next, cache='{}#{}'.format(assist.cache.name, pos))
        else:
            assist.cache.delete(part_frame_key)

    return get_next_frame


def __send_next(context: Context, next_frames: dict):
    """
    发送抄读分帧
    """
    meter_comm = assist.manual.app('meter:comm', step_id=context.runtime.step,
                                   message='Read Next Frame', frame=next_frames)
    return command.send(context, meter_comm)
