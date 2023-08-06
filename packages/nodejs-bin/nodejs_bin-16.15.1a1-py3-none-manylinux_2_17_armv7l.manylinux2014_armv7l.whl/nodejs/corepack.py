import os, sys
from .node import run as run_node
def run(args):
    return run_node([
        os.path.join(os.path.dirname(__file__), "lib/node_modules/corepack/dist/corepack.js"),
        *args
    ])
def main():
    sys.exit(run(sys.argv[1:]))
if __name__ == '__main__':
    main()
