# coding:utf-8
from __future__ import absolute_import, unicode_literals
import sys
import tempfile
from contextlib import contextmanager
import os, pkg_resources
import time
import base64
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import inside_project, get_project_settings

__author__ = "golden"
__date__ = '2017/5/27'


def activate_egg(eggpath):
    """Activate a Scrapy egg file. This is meant to be used from egg runners
    to activate a Scrapy egg file. Don't use it from other code as it may
    leave unwanted side effects.
    """
    try:
        d = pkg_resources.find_distributions(eggpath).next()
    except StopIteration:
        raise ValueError("Unknown or corrupt egg")
    d.activate()
    settings_module = d.get_entry_info('scrapy', 'settings').module_name
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_module)


@contextmanager
def project_environment(project, egg):
    """
    
    :param project: 
    :param egg: egg的二进制字符串
    :return: 
    """
    version = str(int(time.time()))
    if egg:
        prefix = '%s-%s-' % (project, version)
        fd, eggpath = tempfile.mkstemp(prefix=prefix, suffix='.egg')
        lf = os.fdopen(fd, 'wb')
        lf.write(base64.decodestring((egg)))
        lf.close()
        activate_egg(eggpath)
    else:
        eggpath = None
    try:
        assert 'scrapy.conf' not in sys.modules, "Scrapy settings already loaded"
        yield
    finally:
        if eggpath:
            os.remove(eggpath)


def run_spider(egg, project, spider, task_id, minion_id):
    os.environ['SCRAPY_PROJECT'] = project
    argv = ['', 'crawl', spider]
    if task_id:
        argv.append('--logfile=%s.log' % task_id)
        argv.append('--set=TASK_ID=%s' % task_id)
        argv.append('--set=PROJECT_NAME=%s' % project)
        argv.append('--set=MINION_ID=%s' % minion_id)
    with project_environment(project, egg):
        from scrapy.cmdline import execute
        execute(argv)


def get_crawler_process(argv=None, settings=None):
    if argv is None:
        argv = sys.argv

    # --- backwards compatibility for scrapy.conf.settings singleton ---
    if settings is None and 'scrapy.conf' in sys.modules:
        from scrapy import conf
        if hasattr(conf, 'settings'):
            settings = conf.settings
    # ------------------------------------------------------------------

    if settings is None:
        settings = get_project_settings()

    import warnings
    from scrapy.exceptions import ScrapyDeprecationWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ScrapyDeprecationWarning)
        from scrapy import conf
        conf.settings = settings
    # ------------------------------------------------------------------
    return CrawlerProcess(settings)


def list_spider(egg, project):
    os.environ['SCRAPY_PROJECT'] = project
    argv = ['', 'list']
    with project_environment(project, egg):
        return get_crawler_process(argv).spider_loader.list()
