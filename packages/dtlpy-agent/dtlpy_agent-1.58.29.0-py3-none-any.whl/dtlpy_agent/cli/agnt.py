import datetime
from .executor import run_agent
from .parser import get_parser


def main():
    try:
        parser = get_parser()
        args, _ = parser.parse_known_args()
        run_agent(args=args)

    except Exception as err:
        print(datetime.datetime.utcnow())
        print("[ERROR]\t%s" % err)
    print("Dataloop.ai Agent CLI. Type agnt --help for options")


if __name__ == "__main__":
    main()
