import asyncio
from typing import Any, Tuple

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot import on_regex, on_command
from nonebot.adapters.qqguild import Bot, MessageEvent

from ..config import priority
from .get_meme_card import get_meme_img
from ..utils.nonebot2.rule import FullCommand
from ..utils.nonebot2.send import local_image
from .get_mys_data import get_region_task, get_task_detail
from ..utils.exception.handle_exception import handle_exception

get_task_adv = on_regex(
    '(原神任务|任务|任务详情|任务攻略)( )?([\u4e00-\u9fa5]+)( )?', priority=priority
)
get_meme = on_command('抽表情', priority=priority, rule=FullCommand())


@get_task_adv.handle()
@handle_exception('任务攻略')
async def send_task_adv(
    bot: Bot,
    event: MessageEvent,
    matcher: Matcher,
    args: Tuple[Any, ...] = RegexGroup(),
):
    if str(args[2]) in ['须弥', '层岩', '海岛']:
        pass
        '''
        im = await get_region_task(str(args[2]))
        for i in im:
            await bot.call_api(
                'send_group_forward_msg', group_id=event.group_id, messages=i
            )
            await asyncio.sleep(1)
        await matcher.finish()
        '''
    else:
        im = await get_task_detail(str(args[2]))
        await matcher.finish(im)


@get_meme.handle()
@handle_exception('抽表情')
async def send_primogems_data(matcher: Matcher):
    logger.info('开始执行[抽表情]')
    img = await get_meme_img()
    await matcher.finish(local_image(img))
