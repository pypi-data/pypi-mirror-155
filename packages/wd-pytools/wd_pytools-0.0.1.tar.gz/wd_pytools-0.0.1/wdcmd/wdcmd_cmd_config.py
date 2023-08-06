import sys


class CmdInfo:
    def __init__(self, name: str = "", des: str = ""):
        self.name = name
        self.describe = des
        self.args = []

    def set_name(self, name=""):
        self.name = name
        return self

    def set_description(self, des=""):
        self.describe = des
        return self

    def set_args(self, *kvd):
        if len(kvd) == 0:
            pass
        elif len(kvd) == 1:
            self.args.append((kvd[0], "", ""))
        elif len(kvd) == 2:
            self.args.append((kvd[0], kvd[1], ""))
        elif len(kvd) == 3:
            self.args.append((kvd[0], kvd[1], kvd[2]))
        else:
            self.args.append((kvd[0], kvd[1], format(kvd[2:])))
        return self

    def get_args(self, k: str):
        k = k.lstrip("-")
        for x in self.args:
            if x[0] == k:
                return x[1]
        return None

    def show(self):
        if self.name != "":
            print(f"{self.name} : {self.describe}")
        for x in self.args:
            print(f"    -> {x[0]} default:({x[1]}) description:{x[2]}")

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        i = self.i
        self.i += 1
        if i >= len(self.args):
            raise StopIteration
        return self.args[i][0], self.args[i][1], self.args[i][2]


class CmdConfig:
    cmds = list[CmdInfo]()
    name = sys.argv[0]
    description = "programmers are too lazy to write descriptions"

    def __init__(self, name=None, des=None):
        if name is not None:
            self.name = name
        if des is not None:
            self.description = des

    def register(self, *args, **kv):
        info = CmdInfo()
        for i, k in enumerate(args):
            if i == 0:
                if type(k) is CmdInfo:
                    info = k
                    break
                info.set_name(k)
            elif i == 1:
                info.set_description(k)
        for k, v in kv.items():
            info.set_args(k, v)
        self.cmds.append(info)
        return self

    def show(self):
        print(f"application:{self.name}")
        print(f"description:{self.description}")
        for i in self.cmds:
            i.show()

    def get(self, key: str) -> dict:
        map = {}
        for i in self.cmds:
            if i.name != key:
                continue
            for k, v, _ in i:
                map[k] = v
            return map
        return None


if __name__ == "__main__":
    CmdConfig().register("run", "run application", aaaa="hello").show()
