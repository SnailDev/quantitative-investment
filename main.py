import os

import util
from util import logger
from core import Core


def generate_archive_md(searches):
    """生成归档readme
    """
    def search(item):
        return '|[{}](https://xueqiu.com/S/{})|{}|{}%|{}%|{}%|{}|{}亿|{}%|'.format(item['name'], item['symbol'], item['current'], item['pct'], item['chgpct'], item['tr'], round(item['pettm'],2), round(item['mc']/100000000,2), round(item['pct10'],2))

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)

    return readme


def generate_readme(searches):
    """生成今日readme
    """
    def search(item):
        return '|[{}](https://xueqiu.com/S/{})|{}|{}%|{}%|{}%|{}|{}亿|{}%|'.format(item['name'], item['symbol'], item['current'], item['pct'], item['chgpct'], item['tr'], round(item['pettm'],2), round(item['mc']/100000000,2), round(item['pct10'],2))

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)

    return readme


def save_readme(md):
    logger.debug('readme:%s', md)
    util.write_text('README.md', md)


def save_archive_md(md):
    logger.debug('archive md:%s', md)
    name = '{}.md'.format(util.current_date())
    file = os.path.join('archives', name)
    util.write_text(file, md)


def save_raw_content(content: str, filePrefix: str):
    filename = '{}-{}.json'.format(filePrefix, util.current_date())
    file = os.path.join('raw', filename)
    util.write_text(file, content)


def run():
    core = Core()
    # 热搜
    stocks, resp = core.get_hot_stock()
    if resp:
        save_raw_content(resp.text, 'hot-stock')

    # 最新数据
    readme = generate_readme(stocks['data']['list'])
    save_readme(readme)
    # 归档
    archiveMd = generate_archive_md(stocks['data']['list'])
    save_archive_md(archiveMd)


if __name__ == "__main__":
    run()
