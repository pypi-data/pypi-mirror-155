import argparse
import subprocess

import zcommons as zc


def main(args):

    @zc.timer(name=args.cmds[0], repeat=args.repeat, show=True)
    def run():
        subprocess.run(args.cmds, shell=False)

    run()


def parse_args():
    parser = argparse.ArgumentParser(description="timer")
    parser.add_argument("--repeat", type=int, default=1, help="exec times")
    parser.add_argument("cmds", metavar="N", type=str, nargs="*", help="exec commands")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
