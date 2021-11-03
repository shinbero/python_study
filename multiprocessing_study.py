import multiprocessing as mp
import os
import traceback
import sys

class MyProcess(mp.Process):
    def __init__(self, *args, **kwargs):
        self._p_conn, self._c_conn = mp.Pipe()
        self._exception = None

        super().__init__(*args, **kwargs)

    def run(self):
        try:
            mp.Process.run(self)
            self._c_conn.send(None)
        except Exception as err:
            tb = traceback.format_exc()
            self._c_conn.send((err, tb))

    @property
    def exception(self):
        if self._p_conn.poll():
            self._exception = self._p_conn.recv()
        return self._exception



def main():
    q = mp.Queue()
    parent_conn, child_conn = mp.Pipe()

    procs = []
    for i in range(1):
        # p = mp.Process(target=multi_procs_f, args=(i, q))
        p = MyProcess(target=multi_procs_f, args=(i, q, child_conn))
        p.start()
        print(f"i={i}, started !")
        procs.append(p)

    for p in procs:
        p.join()

    print("Hello")

    #     if p.exception:
    #         error, traceback = p.exception
    #         # print(traceback)
    #         # print(f"type(error)={type(error)}, error={error}")

    #         # raise ValueError(traceback) from error
    #         # raise ValueError from error
    #         raise ValueError(traceback)

    # # print("Hello, world")

    # print("Start getting msg from Pipe.")
    # for i in range(2):
    #     val = parent_conn.recv()
    #     print(f"Get from q: {val}, type={type(val)}")

    # print("hello in parent!!")

    # for i in range(6):
    #     val = q.get()
    #     print(f"Get from q: {val}, type={type(val)}")

def multi_procs_f(s, q, child_conn):
    print(f"Hello, {s} !")
    print(f"PPID={os.getppid()}, PID={os.getpid()}")
    raise RuntimeError(f"RTE in child process. s={s}")

    # print("Hello !! This is after exception.")

    child_conn.send(39)
    child_conn.send("Msg in child..")

    # q.put(s)
    # q.put(f"Put s in pid={os.getpid()}")

if __name__ == '__main__':
    main()
