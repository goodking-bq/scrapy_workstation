# coding:utf-8
from __future__ import absolute_import, unicode_literals
import sys, os, time, atexit
from signal import SIGTERM
import logging
import yaml

__author__ = "golden"
__date__ = '2017/2/21'

logger = logging.getLogger(__name__)


class Daemon(object):
    """
    基本的守护进程类

    使用方法: 继承然后该写run 函数
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                logger.debug("第一个父进程退出")
                sys.exit(0)
        except OSError as e:
            logger.warning("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                logger.debug("第二个父进程退出")
                sys.exit(0)
        except OSError as e:
            logger.warning("第一个父进程退出")("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        yaml.dump({'main_pid': pid, 'subprocess_pid': []}, open(self.pidfile, 'w+'))

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pid = self.main_pid
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()
        return "start success.run as pid %s" % pid

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pid = self.main_pid
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            return message % self.pidfile
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                os.remove(self.pidfile)
                return 'stop success. pid %s is killed' % pid
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                    return 'stop success. pid %s is killed==' % pid
            else:
                return err

    def restart(self):
        """
        重启
        """
        msg = ''
        msg += self.stop() + '\n'
        time.sleep(2)
        msg += self.start()
        return msg

    def run(self):
        """
        运行的代码
        """
        pass

    def status(self):
        try:
            pid = self.main_pid
        except IOError:
            pid = None
        if pid:
            return "is running as pid %s" % pid
        else:
            return "is not running"

    def append_pid(self, pid):
        try:
            all_pid = yaml.load(open(self.pidfile, 'r'))
            if all_pid['subprocess_pid']:
                all_pid['subprocess_pid'] = list(set(all_pid['subprocess_pid'].append(pid)))
            else:
                all_pid['subprocess_pid'] = [pid]
            yaml.dump(all_pid, open(self.pidfile, 'w+'))
        except Exception as e:
            logger.error(e.__repr__())

    def remove_pid(self, pid):
        all_pid = yaml.load(open(self.pidfile, 'r'))
        all_pid['subprocess_pid'].pop(pid)
        yaml.dump(all_pid, open(self.pidfile, 'w+'))

    @property
    def main_pid(self):
        try:
            all_pid = yaml.load(open(self.pidfile, 'r'))
            pid = int(all_pid.get('main_pid'))
        except IOError:
            pid = None
        return pid

    @property
    def subprocess_pids(self):
        try:
            all_pid = yaml.load(open(self.pidfile, 'r'))
            pid = all_pid.get('subprocess_pid')
        except IOError:
            pid = None
        return pid

    def kill_pid(self, pid):
        os.kill(int(pid), SIGTERM)
        time.sleep(0.1)
        return '子进程PID: %s killed sucess\n' % pid
