import sys

DEFAULT_GLOBAL = "DEFAULT_GLOBAL"


class Argv:
    orders = {DEFAULT_GLOBAL: {}}
    vector = []

    def __init__(self):
        self.application_name = sys.argv[0]
        i = 1
        order = DEFAULT_GLOBAL
        while i < len(sys.argv):
            cmd = sys.argv[i]
            if cmd[0] == '-':
                cmd = cmd.lstrip('-')
                value = None
                if i + 1 < len(sys.argv) and sys.argv[i + 1][0] != "-":
                    value = sys.argv[i + 1]
                    i += 1
                self.orders[order][cmd] = value
            else:
                self.orders[cmd] = {}
                self.vector.append(cmd)
                order = cmd
            i += 1

    def get_args(self, cmd=DEFAULT_GLOBAL):
        return self.orders.get(cmd)

    def get_command_args(self, cmd=DEFAULT_GLOBAL):
        args = dict(self.get_args())
        if cmd != DEFAULT_GLOBAL:
            if type(self.get_args(cmd)) is dict:
                args.update(self.get_args(cmd))
        return args

    def commands(self):
        return self.vector

    # def show(self):
    #     for k, v in self.orders.items():
    #         print(k, v)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.vector):
            raise StopIteration
        cmd = self.vector[self.i]
        self.i += 1
        return cmd, self.get_command_args(cmd)

    def __len__(self):
        return len(self.vector)


if __name__ == '__main__':
    for k, v in Argv():
        print(k, v)
