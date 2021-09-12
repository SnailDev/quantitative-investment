import contextlib
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from util import logger

HOT_SEARCH_URL = "https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=30&only_count=0&current=5_30&pct=&chgpct=7_12&tr=15_25&pettm=10_80&mc=5000000000_20000000000&pct10=20_50&_=1631011206501"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

RETRIES = Retry(total=3,
                backoff_factor=1,
                status_forcelist=[k for k in range(400, 600)])


@contextlib.contextmanager
def request_session():
    s = requests.session()
    try:
        s.headers.update(HEADERS)
        s.mount("http://", HTTPAdapter(max_retries=RETRIES))
        s.mount("https://", HTTPAdapter(max_retries=RETRIES))
        yield s
    finally:
        s.close()


class Core:

    def get_hot_stock(self):
        """热门股票
        """
        resp = None
        try:
            with request_session() as s:
                resp = s.get(HOT_SEARCH_URL)
        except:
            logger.exception('get hot search failed')
        return (json.loads(resp.text), resp)


if __name__ == "__main__":
    core = Core()
    searches, resp = core.get_hot_stock()
    logger.info('%s', searches)
