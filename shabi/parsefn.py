import re


BRACKETS = re.compile(r'\[([^\]]+)\]|\(([^()]+)\)')


class FileInfo:
    name: str
    episode: str
    group: str
    extra: set[str]

    def __init__(self, name, episode, group, extra):
        self.name = name
        self.episode = episode
        self.group = group
        self.extra = extra

    def __repr__(self):
        return f'FileInfo(name={self.name!r}, episode={self.episode!r}, group={self.group!r}, extra={self.extra!r})'

    def __str__(self):
        return repr(self)

    @classmethod
    def parsefn(cls, fn: str) -> 'FileInfo':
        tokens = list(filter(None, map(str.strip, filter(None, BRACKETS.split(fn)))))

        if re.match('(1|4|7|10)月新番', tokens[1]):
            tokens[1:2] = []

        if tokens[0] == 'Lilith-Raws' or 'LoliHouse' in tokens[0] or tokens[0] == 'Haruhana':
            tokens[1:2] = re.split(r' +- +', tokens[1])
        # elif 'ANK-Raws' in tokens[0]:


        group = tokens[0]
        name = tokens[1]
        episode = tokens[2].rsplit('v',1)[0]
        extra = set(tokens[3:])
        return cls(name, episode, group, extra)


def main():
    import sys, os
    import getopt
    from rich import print
    opts, args = getopt.getopt(sys.argv[1:], 'e', ['error'])
    error_only = False
    for o,a in  opts:
        if o in ('-e', '--error'):
            error_only = True
    for arg in args:
        for r, ds, fs in os.walk(arg):
            for f in fs:
                if f.rsplit('.', 1)[-1] in ['mkv', 'mp4']:
                    ff = os.path.join(r, f)
                    try:
                        x = FileInfo.parsefn(f)
                        if not error_only:
                            print(repr(ff))
                            print(x)
                    except Exception as e:
                        print(repr(ff))
                        print(e)

if __name__ == '__main__':
    main()
