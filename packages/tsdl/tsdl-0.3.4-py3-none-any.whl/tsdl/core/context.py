from tsdl.api import em
from tsdl.common import util, assist


class Context(object):
    """
    测试用例上下文
    """

    def __init__(self, script: str, url: str, *loops, **meters):
        self._script = script
        if script is None:
            raise Exception('Path of script file is null.')
        pfs = script.split('.')
        pfs[-1] = pfs[-1] + '.py'
        if not util.pathUtil.exist(*pfs):
            raise Exception('Script file[{}] is not exist.'.format(script))

        self._url = url
        if not util.is_valid_url(url):
            raise Exception('Format of app url is not right that should be http://IP:PORT/accept.')

        self._loops = []
        if len(loops) > 0:
            for data in loops:
                self._loops.append(self.Loop(data))

        self._meters = {}
        if meters is None or len(meters) <= 0:
            raise Exception('Meters is null.')
        for pos, data in meters.items():
            self._meters[pos] = self.Meter(pos, data)

        self._runtime = self.Runtime()

    @property
    def script(self):
        return self._script

    @property
    def url(self):
        return self._url

    @property
    def loops(self):
        return self._loops

    @property
    def meters(self):
        return self._meters

    @property
    def runtime(self):
        return self._runtime

    class Loop(object):
        def __init__(self, data: dict):
            r = data.get('range')
            if r is None:
                raise Exception('Can not find range in loops. It should be like "start:end".')
            if r.find(':') <= 0:
                raise Exception('Format of range value is not right. It should be like "start:end"')
            self._range = self.Range(r)

            self._count = data.get('count')
            if self._count is None:
                raise Exception('Can not find count in loops. It should be decimal like 1, 2...')
            if self._count <= 0:
                raise Exception('Count must be more then 0.')

        @property
        def range(self):
            return self._range

        @property
        def count(self):
            return self._count

        class Range(object):
            def __init__(self, value: str):
                self._list = value.split(':')
                if len(self._list) != 2:
                    raise Exception('Length of range value after split must be 2.')
                if not self._list[0].isdigit():
                    raise Exception('Fist number of range must be decimal.')
                self._start = int(self._list[0])
                if not self._list[1].isdigit():
                    raise Exception('Fist number of range must be decimal.')
                self._end = int(self._list[1])
                if self._start > self._end:
                    raise Exception('Fist number of range must be less than second number of range.')

            @property
            def start(self):
                return self._start

            @property
            def end(self):
                return self._end

    class Meter(object):
        def __init__(self, pos: str, data: dict):
            self._pos = pos
            self._addr = data.get('addr')
            self._no = data.get('no')
            self._protocol = data.get('protocol')
            self._channel = {}
            chl = data.get('channel')
            if chl is not None:
                for baudrate, v in chl.items():
                    self._channel[baudrate.upper()] = v

            self._session = self.Session(self.pos)

        def baudrate(self):
            return self.channel.get('baudrate'.upper())

        @property
        def pos(self):
            return self._pos

        @property
        def addr(self):
            return self._addr

        @property
        def no(self):
            return self._no

        @property
        def protocol(self):
            return self._protocol

        @property
        def channel(self):
            return self._channel

        @property
        def session(self):
            return self._session

        class Session(object):
            """
                会话 - 电表通讯加密参数
            """

            def __init__(self, pos: str):
                self._key = '{}:session'.format(pos)

                self._esam = self.ESAM()
                self._em = self.EM()

            def __cache(self):
                assist.cache.set(self._key, data=self.to_dict())

            def to_dict(self):
                return util.to_dict(esam=self.esam.to_dict(), em=self.em.to_dict())

            def negotiate(self, get_esam_return_result: dict):
                result = get_esam_return_result['parse']['link_data']['mission']['result']
                self.esam.sn = result['esam.serial_number']
                self.esam.counter = result['esam.current_counter[1]']

                e_result = em.negotiate(self.esam.sn, self.esam.counter)
                self.em.rn = e_result['rn']
                self.em.data = e_result['data']
                self.em.mac = e_result['mac']

                self.__cache()

            def verify_session(self, connect_return_result: dict):
                result = connect_return_result['parse']['link_data']['connect_response_info']['security_data']
                self.esam.rn = result['server_rn']
                self.esam.mac = result['server_signature']

                e_result = em.verify_session(self.em.rn, self.esam.sn, self.esam.rn, self.esam.mac)
                self.em.iv = e_result['iv']

                self.__cache()

            @property
            def esam(self):
                return self._esam

            @property
            def em(self):
                return self._em

            class ESAM(object):
                """
                    电表里的ESAM模块
                """

                def __init__(self):
                    self._sn = None
                    self._rn = None
                    self._mac = None
                    self._counter = None

                def to_dict(self):
                    return util.to_dict(sn=self.sn, counter=self.counter, rn=self.rn, mac=self.mac)

                @property
                def sn(self):
                    return self._sn

                @sn.setter
                def sn(self, value):
                    self._sn = value

                @property
                def counter(self):
                    return self._counter

                @counter.setter
                def counter(self, value):
                    self._counter = value

                @property
                def rn(self):
                    return self._rn

                @rn.setter
                def rn(self, value):
                    self._rn = value

                @property
                def mac(self):
                    return self._mac

                @mac.setter
                def mac(self, value):
                    self._mac = value

            class EM(object):
                """
                    加密机
                """

                def __init__(self):
                    self._rn = None
                    self._data = None
                    self._mac = None
                    self._iv = None  # 加密数据的密钥

                def to_dict(self):
                    return util.to_dict(rn=self.rn, data=self.data, mac=self.mac, iv=self.iv)

                @property
                def rn(self):
                    return self._rn

                @rn.setter
                def rn(self, value):
                    self._rn = value

                @property
                def data(self):
                    return self._data

                @data.setter
                def data(self, value):
                    self._data = value

                @property
                def mac(self):
                    return self._mac

                @mac.setter
                def mac(self, value):
                    self._mac = value

                @property
                def iv(self):
                    return self._iv

                @iv.setter
                def iv(self, value):
                    self._iv = value

    class Runtime(object):
        """
        运行时
        """

        def __init__(self):
            self._step = None
            self._loop_times = None
            self._total_loop_times = None
            self._last_result = None

        def reset_loop(self):
            self._loop_times = None
            self._total_loop_times = None

        @property
        def step(self):
            return self._step

        @step.setter
        def step(self, value):
            self._step = value

        @property
        def last_result(self):
            return self._last_result

        @last_result.setter
        def last_result(self, value):
            self._last_result = value

        @property
        def loop_times(self):
            return self._loop_times

        @loop_times.setter
        def loop_times(self, value):
            self._loop_times = value

        @property
        def total_loop_times(self):
            return self._total_loop_times

        @total_loop_times.setter
        def total_loop_times(self, value):
            self._total_loop_times = value
