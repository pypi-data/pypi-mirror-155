# wd_pytools

### Introduce

This is the tools for python.

### wdcmd
```python
import time

from wdcmd import Info, entity


class TestServer:
    config_path = 'config.yaml'
    status = True

    def info_run(self):
        return Info("run", "run application") \
                   .set_args("c", self.config_path, "配置文件地址"), self.run

    def run(self, ctx):
        print(f"配置文件地址：{ctx.get('c')}")
        while self.status:
            print("test run ....")
            time.sleep(1)

    def exit(self):
        self.status = False
        print("server stop over")


if __name__ == "__main__":
    server = TestServer()
    entity.register(*server.info_run()).on_exits(server.exit).launch()
```
