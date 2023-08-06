import time
import traceback
import signal
from typing import Any

from concurrent.futures import ThreadPoolExecutor
import function

from wdcmd.wdcmd_args_parse import Argv
from wdcmd.wdcmd_cmd_config import CmdConfig, CmdInfo
from wdcmd.wdcmd_context import CmdContext
from wdcmd.wdcmd_interface import CmdOption, TerminalArgv

EXIT_APPLICATION = "EXIT_APPLICATION"


class Entity:
    pool = ThreadPoolExecutor()
    status = True

    def __init__(self, opt: CmdOption = CmdConfig(), args: TerminalArgv = Argv()):
        self.opt = opt
        self.args = args
        self.funcs: dict[str, Any] = {EXIT_APPLICATION: []}

    def on_default(self, func):
        self.funcs[""] = func
        return self

    def register(self, info: CmdInfo, func):
        self.opt.register(info)
        self.funcs[info.name] = func
        return self

    def on_exits(self, *funcs):
        for i in funcs:
            if self.funcs.get(EXIT_APPLICATION) is None:
                self.funcs[EXIT_APPLICATION] = [i]
            else:
                self.funcs[EXIT_APPLICATION].append(i)
        return self

    def launch(self):
        try:
            if self.funcs.get("") is not None:
                map = self.opt.get("")
                map.update(self.args.get_command_args())
                self.funcs.get("")(CmdContext(map))
            elif len(self.args) == 0:
                self.opt.show()
                exit(2)
            for cmd, kv in self.args:
                map = self.opt.get(cmd)
                if map is None:
                    raise Exception(f"Unknown command:[{cmd}]")
                map.update(kv)
                ctx = CmdContext(map)
                func = self.funcs[cmd]

                def future(ctx):
                    nonlocal func, cmd
                    try:
                        func(ctx)
                    except Exception as err:
                        print(f"commend {cmd} panic:{err}")
                        traceback.print_exc()

                self.pool.submit(future, ctx)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            self.wait_exit()
        except Exception as err:
            print(f"application launch panic:{err}")
            # print(traceback.print_exc())
            traceback.print_exc()
        else:
            # print(f"application launch success,start game over")
            # finally:
            print("start stop application ......")
            self.funcs[EXIT_APPLICATION].reverse()
            for over in self.funcs[EXIT_APPLICATION]:
                over()
            print("stop application success")

    def wait_exit(self):
        def signal_wait_exit(s, f):
            self.status = False

        signal.signal(signal.SIGINT, signal_wait_exit)
        signal.signal(signal.SIGTERM, signal_wait_exit)
        while self.status:
            time.sleep(0.1)


# if __name__ == '__main__':
#     class TestServer:
#         config_path = 'config.yaml'
#         status = True
#
#         def info_run(self):
#             return CmdInfo("run", "run application") \
#                        .set_args("c", self.config_path, "配置文件地址"), self.run
#
#         def run(self, ctx):
#             print(f"配置文件地址：{ctx.get('c')}")
#             while self.status:
#                 print("test run ....")
#                 time.sleep(1)
#                 raise Exception("TEST PANIC")
#
#         def exit(self):
#             self.status = False
#             print("server stop over")
#
#
#     server = TestServer()
#     e = Entity().register(*server.info_run()).on_exits(server.exit)
#     e.launch()
