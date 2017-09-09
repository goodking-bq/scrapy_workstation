# coding:utf-8
from __future__ import absolute_import, unicode_literals
from web.models import Project, Spider, Task, TaskUrl, TaskLog, Minion
from flask import render_template, current_app, redirect, url_for, request
import os, sys
import subprocess
import base64

__author__ = "golden"
__date__ = '2017/6/22'


# TODO 项目列表
def project():
    projects = Project.objects.all()
    return render_template('scrapy/project.html', projects=projects)


# TODO 刷新项目
def refresh_project():
    app = current_app._get_current_object()
    spiderdir = app.config.get('SPIDERDIR')
    projects = os.listdir(spiderdir)
    for name in projects:
        _project = Project.objects.filter(name=name).first()

        if not _project:
            _project = Project()
        _project.name = name
        _project.alias = name
        _project.description = ''
        _project.save()
        # spider
        _spiderpath = os.path.join(spiderdir, name)
        scrapyexe = app.config.get('SCRAPY_EXE')
        p = subprocess.Popen([scrapyexe, 'list'], cwd=_spiderpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        stdout = p.stdout.readlines()
        spiders = []
        for spider_name in stdout:
            spider_name = spider_name.strip()
            spider = Spider.objects.filter(name=spider_name, project=_project).first()
            if not spider:
                spider = Spider()
            spider.name = spider_name
            spider.project = _project
            spider.save()
            spiders.append(spider)
        _project.spiders = spiders
        _project.save()
    return redirect(url_for('.project'))


# TODO 添加项目
def add_project():
    pass


# TODO 爬虫列表
def spider():
    spiders = Spider.objects.all()
    return render_template('scrapy/spider.html', spiders=spiders)


# TODO 添加 start_urls
def add_start_url():
    form = request.form
    url = form.get('url')
    object_id = form.get('object_id')
    _spider = Spider.objects.filter(id=object_id).first()
    _spider.start_urls.append(url)
    _spider.save()
    return redirect(url_for('.spider'))


# TODO 添加start_urls 到队列
def push_start_url():
    url = request.args.get('url')
    spider_id = request.args.get('spider_id')
    _spider = Spider.objects(id=spider_id).first()
    if url:
        urls = [url]
    else:
        urls = _spider.start_urls
    task = Task()
    task.spider = _spider
    task.start_urls = urls
    task.save()
    for url in urls:
        tu = TaskUrl()
        tu.url = url
        tu.task_id = task.id
        tu.save()
    return redirect(url_for('.spider'))


def project_manager():
    form = request.form
    project_id = form.get('project_id')
    if project_id:
        _project = Project.objects.filter(id=project_id).first()
    else:
        _project = Project()
    _project.name = form.get('name')
    _project.alias = form.get('alias')
    _project.description = form.get('description')
    _project.egg = base64.encodestring(request.files['egg'].stream.read())
    _project.save()
    return redirect(url_for('.project'))


def tasks():
    spider_id = request.args.get('spider_id')
    if spider_id:
        _spider = Spider.objects(id=spider_id).first()
        _tasks = Task.objects(spider=_spider).order_by('-start_time').all()
    else:
        _tasks = Task.objects().order_by('-start_time').all()
    return render_template('scrapy/tasks.html', tasks=_tasks)


def spider_logs():
    task_id = request.args.get('task_id')
    minion_id = request.args.get('minion_id')
    minions = Minion.objects.all()
    logs = TaskLog.objects
    if task_id:
        _task = Task.objects(id=task_id).first()
        logs = logs.filter(task=_task)
    if minion_id:
        _minion = Minion.objects(id=minion_id).first()
        logs = logs.filter(minion=_minion)
    logs = logs.order_by('-log_time').limit(20)
    logs = reversed(logs)
    return render_template('scrapy/spider_logs.html', logs=logs, minions=minions)
