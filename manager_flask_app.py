# coding:utf-8
from __future__ import absolute_import, unicode_literals
from flask_script import Manager, Shell, Server
from web.extension import db, mongo, redis
from web.app import create_app
import datetime
import decimal
import requests

__author__ = "golden"
__date__ = '2017/2/7'
app = create_app('web_config.Developer')
manager = Manager(app)

all_area = ['武侯区', '青羊区', '高新区', '天府新区', '金牛区', '锦江区', '成华区', '双流区', '温江区', '龙泉区', '郫县区', '新都区', '都江堰区', '高新西区', '成都周边']


def make_shell_context():
    return dict(mongo=mongo, app=app)


@manager.option('-d', '--date', dest='date', help=u'统计日期之后', required=False)
@manager.option('-s', '--site', dest='site', help=u'网站', required=False)
def day_increase(date=None, site=None):
    """统计每日新增数据"""
    if not date:
        date = str((datetime.datetime.now() - datetime.timedelta(days=3)).date())
    if site:
        sites = [site]
    else:
        sites = ['fang', 'lianjia', 'anjuke']
    for s in sites:
        mongo_db = getattr(mongo.db, s)
        datas = mongo_db.group(key={'publish_date': True}, initial={'count': 0},
                               reduce="function(doc,prev){prev.count++}",
                               condition={'publish_date': {'$gte': date}})
        for data in datas:
            mongo.db.day_increase.update({"publish_date": data['publish_date'],
                                          "domain": s}, {"$set": data},
                                         upsert=True)
        print("%s done!" % s)


@manager.option('-d', '--date', dest='date', help=u'统计日期之后', required=False)
@manager.option('-s', '--site', dest='site', help=u'网站', required=False)
def average_price_area(date=None, site=None):
    """按区域统计每平米平均价格"""
    if not date:
        date = str((datetime.datetime.now() - datetime.timedelta(days=3)).date())
    if site:
        sites = [site]
    else:
        sites = ['fang', 'lianjia', 'anjuke']
    for s in sites:
        mongo_db = getattr(mongo.db, s)
        datas = mongo_db.group(key={'publish_date': True, 'area': True}, initial={'count': 0, 'sum': 0},
                               reduce="function(doc,prev){prev.count++,prev.sum+=parseFloat(doc.m2_price)}",
                               condition={'m2_price': {'$exists': True}, 'publish_date': {'$gte': date}})
        for data in datas:
            if data['zone'] not in all_area and not data['zone'].endswith('区'):
                data['zone'] += '区'
            if data['zone'] in all_area:
                _avg = data['sum'] / data['count']
                avg = decimal.Decimal(_avg).quantize(decimal.Decimal('0.00'))
                data.pop('count')
                data.pop('sum')
                data['average'] = unicode(avg)
                mongo.db.average_price_area.update({"publish_date": data['publish_date'],
                                                    'zone': data['zone'],
                                                    'domain': s}, {"$set": data},
                                                   upsert=True)
        print("%s done!" % s)


@manager.option('-d', '--date', dest='date', help=u'统计日期之后', required=False)
@manager.option('-s', '--site', dest='site', help=u'网站', required=False)
def average_price_day(date=None, site=None):
    """每天平均数"""
    if not date:
        date = str((datetime.datetime.now() - datetime.timedelta(days=3)).date())

    if site:
        sites = [site]
    else:
        sites = ['fang', 'lianjia', 'anjuke']
    for s in sites:
        mongo_db = getattr(mongo.db, s)
        datas = mongo_db.group(key={'publish_date': True, }, initial={'count': 0, 'sum': 0},
                               reduce="function(doc,prev){prev.count++,prev.sum+=parseFloat(doc.m2_price)}",
                               condition={'m2_price': {'$exists': True}, 'publish_date': {'$gte': date}})
        for data in datas:
            _avg = data['sum'] / data['count']
            avg = decimal.Decimal(_avg).quantize(decimal.Decimal('0.00'))
            data.pop('count')
            data.pop('sum')
            data['average'] = unicode(avg)
            mongo.db.average_price_day.update({"publish_date": data['publish_date'],
                                               "domain": s}, {"$set": data},
                                              upsert=True)
        print("%s done!" % s)


@manager.command
def delete_history(before_date=None):
    """删除esf历史数据"""
    if not before_date:
        before_date = str((datetime.datetime.now() - datetime.timedelta(days=10)).date())
    for s in ['fang', 'lianjia', 'anjuke']:
        mongo_db = getattr(mongo.db, s)
        mongo_db.remove({"publish_date": {"$lt": before_date}})
    return 'success'


@manager.command
def check_proxy():
    all_proxy = mongo.db.proxy.find()
    for proxy in all_proxy:
        proxies = {"http": "http://%s:%s" % (proxy['ip'], proxy['port'])}
        try:
            res = requests.get('http://www.ip138.com/', proxies=proxies, timeout=2)
            if res.ok:
                proxy['check_time'] = str(datetime.datetime.now())
                proxy['checked'] = 1
                mongo.db.proxy.update({"_id": proxy['_id']}, {"$set": proxy},
                                      upsert=True)
            else:
                mongo.db.proxy.remove({"_id": proxy['_id']})
                print('delete : %s' % proxy['ip'])
        except:
            mongo.db.proxy.remove({"_id": proxy['_id']})
            print('delete : %s' % proxy['ip'])


manager.add_command("shell", Shell(make_context=make_shell_context, use_bpython=False))
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    port=5001,
    host="0.0.0.0"
))

if __name__ == "__main__":
    manager.run()
