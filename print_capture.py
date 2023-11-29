import sys
import time
from threading import Thread
from io import StringIO
from contextlib import contextmanager


# 原始函数
def function_with_print():
    for i in range(5):
        print(f"Progress: {i+1}/5")
        time.sleep(1)
    assert False

# 线程安全的context manager用于捕获stdout和stderr
@contextmanager
def capture_output(stream):
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stream
    sys.stderr = stream
    try:
        yield stream
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# 在一个新的线程中执行function_with_print并实时捕获输出
def threaded_function_with_capture():
    stream = StringIO()
    with capture_output(stream):
        thread = Thread(target=function_with_print)
        thread.start()
        while thread.is_alive():
            time.sleep(0.1)  # 短暂休眠以免频繁锁定
            stream.seek(0)  # 前往当前流的开头
            output = stream.read()
            if output:  # 如果有新输出则打印
                sys.__stdout__.write("message: " + output)
                sys.__stdout__.flush()
                stream.truncate(0)  # 清空流以便再次捕获
                stream.seek(0)
        thread.join()
        # 打印剩余的输出
        output = stream.getvalue()
        if output:
            sys.__stdout__.write(output)
            sys.__stdout__.flush()

# 运行线程捕获函数
threaded_function_with_capture()
