from typing import Any


class CmdContext:
    kv = {}

    # def __init__(self, **kwargs):
    #     for k, v in kwargs:
    #         self.kv[k] = v

    def __init__(self, *kv: dict):
        for x in kv:
            if type(x) is not dict:
                continue
            for k, v in x.items():
                self.kv[k] = v

    def get(self, k: str) -> Any:
        return self.kv.get(k.lstrip("-"))

    def set(self, k, v: str):
        self.kv[k] = v
