import sys
from .app import Scrapyd


def main_loop():
    args = sys.argv[1:]
    main_thread = Scrapyd()
    if args:
        if args[0] == 'stop':
            return main_thread.stop()
        elif args[0] == 'start':
            return main_thread.start()
        elif args[0] == 'restart':
            return main_thread.restart()
        elif args[0] == 'status':
            return main_thread.status()
        else:
            return "option is stop|start|restart|status"
    else:
        return main_thread.start()
