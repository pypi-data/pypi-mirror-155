import signal
import time

def set_timeout(num):
    def wrap(func):
        def handle(
            signum, frame
        ):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
            signal.alarm(num)  # 设置 num 秒的闹钟
            print("start alarm signal.")
            r = func(*args, **kwargs)
            print("close alarm signal.")
            signal.alarm(0)  # 关闭闹钟
            return r

        return to_do

    return wrap

@set_timeout(1)
def test():
    print(1)
    time.sleep(2)
    print(2)

test()