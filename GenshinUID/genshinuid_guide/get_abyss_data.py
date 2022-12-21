import json
from pathlib import Path
from typing import Dict, List, Union

from nonebot.log import logger

from .abyss_history import history_data
from ..utils.hhw_api.get_hhw_data import get_abyss_review, get_hhw_abyss_raw

REVIEW_PATH = Path(__file__).parent / "review.json"


async def generate_data():
    raw_data = await get_hhw_abyss_raw()
    result = {}
    for version in history_data:
        for floor in history_data[version]:
            _id = history_data[version][floor]
            data = await get_abyss_review(raw_data, _id, floor)
            if version not in result:
                result[version] = {}
            result[version][floor] = data

    with open(REVIEW_PATH, 'w', encoding='UTF-8') as file:
        json.dump(result, file, ensure_ascii=False)

    logger.info('[深渊预览] 数据已刷新！')


async def get_review(version: Union[str, float]) -> Union[List, str]:
    if not REVIEW_PATH.exists():
        return '请等待数据加载完成...'

    with open(REVIEW_PATH, "r", encoding='UTF-8') as f:
        review: Dict[str, Dict[str, Dict[str, List[str]]]] = json.load(f)

    if isinstance(version, float):
        version = str(version)

    im_list = []
    if version in review:
        im_list.append(f'{version}版本深渊阵容')
        for floor in review[version]:
            for half in review[version][floor]:
                im_list.append(
                    '\n'.join([half] + review[version][floor][half])
                )
        return im_list
    else:
        return '暂无该版本的深渊阵容...'
