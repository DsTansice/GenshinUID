from typing import Optional

from ..message.error_reply import VERIFY_HINT
from ..db_operation.db_operation import cache_db, error_db
from ..mhy_api.get_mhy_data import get_info, get_spiral_abyss_info


class GetCookies:
    def __init__(self) -> None:
        self.useable_cookies: Optional[str] = None
        self.uid: Optional[str] = None
        self.raw_data: Optional[dict] = None

    async def get_useable_cookies(self, uid: str) -> str:
        self.uid = uid
        while True:
            cache = await cache_db(uid)
            if isinstance(cache, str):
                return cache
            else:
                self.useable_cookies = cache.CK
            await self.get_uid_data()
            msg = await self.check_cookies_useable()
            if isinstance(msg, str):
                return msg
            else:
                if msg:
                    return ''

    async def get_uid_data(self):
        self.raw_data = await get_info(self.uid, self.useable_cookies)

    async def get_spiral_abyss_data(self, schedule_type: str = '1'):
        return await get_spiral_abyss_info(
            self.uid, self.useable_cookies, schedule_type
        )

    async def check_cookies_useable(self):
        if self.raw_data:
            retcode = self.raw_data['retcode']
            if retcode != 0:
                if retcode == 10001:
                    if self.useable_cookies:
                        await error_db(self.useable_cookies, 'error')
                        return False
                elif retcode == 10101:
                    if self.useable_cookies:
                        await error_db(self.useable_cookies, 'limit30')
                        return False
                elif retcode == 10102:
                    return '当前查询id已经设置了隐私，无法查询！'
                elif retcode == 1034:
                    return VERIFY_HINT
                else:
                    return (
                        'Api报错，返回内容为：\r\n'
                        + str(self.raw_data)
                        + '\r\n出现这种情况可能的UID输入错误 or 不存在'
                    )
            else:
                return True
        else:
            return '没有可以使用的Cookies！'
