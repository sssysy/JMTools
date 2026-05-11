from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsStrConfig,
    GsBoolConfig,
    GsListStrConfig,
    GsFloatConfig,
    GsIntConfig
)
from gsuid_core.utils.plugins_config.gs_config import StringConfig
from gsuid_core.logger import logger
from gsuid_core.data_store import get_res_path

import os

CONFIG_PATH = get_res_path() / 'JMTools'

CONFIG_DEFAULT: dict[str, GSC] = {
    "InfoSendType": GsStrConfig(
        "JM 作品简介发送方式",
        "",
        "直接发送",
        ["直接发送", "合并转发"],
    ),
    "CoverSendUrl": GsStrConfig(
        "JM 作品封面发送方式",
        "发图可能会卡 QQ 风控导致无法发出",
        "发送链接",
        ["发送链接", "发送图片"],
    ),
    "DetailErrorText": GsStrConfig(
        "JM 作品不存在发送文本",
        "作品不存在时发送的消息前缀",
        "不是哥们，你这 JM 号有问题啊？",
    ),
    "NSFWSwitch": GsBoolConfig(
        "NSFW 检测",
        "[需重启] 对发送的作品封面图进行 NSFW 检测以避免图片文件发送失败",
        False
    ),
    "NSFWpersent": GsIntConfig(
        "NSFW 识别强度",
        "1~10",
        7,
        max_value = 10
    ),
    "SinkSwitch": GsBoolConfig(
        "生成短链接",
        "[需重启] 发送URL时套用短链接",
        False
    ),
    "SinkUrl": GsStrConfig(
        "[需重启] 短链接生成域名",
        "Sink(https://github.com/miantiao-me/Sink) 查看部署教程",
        "https://example.com",
    ),
    "SinkToken": GsStrConfig(
        "[需重启] 短链接生成Token",
        "Workers 中的 SITE_TOKEN 变量",
        "",
    ),
    "SinCloaking": GsBoolConfig(
        "[需重启] 短链接伪装",
        "开启后访问网站将不会跳转到源网址",
        False,
    ),
    "SinUnsafe": GsBoolConfig(
        "[需重启] 短链接跳转提示",
        "开启后访问网站将会先显示跳转提示而不直接显示图片",
        True,
    ),
    "SinExpireTime": GsIntConfig(
        "[需重启] 短链接过期时间",
        "0则长期有效(单位：小时)",
        1,
    ),
    "NumberDetect": GsBoolConfig(
        "自动识别群内数字当作 jm 号",
        "满足条件 (5<=长度<=8 & 纯数字消息) 后自动触发 jm 识别",
        False,
    ),
}
CONFIG_PATH.mkdir(parents=True, exist_ok=True)
JMConfig = StringConfig("JMConfig",CONFIG_PATH / 'config.json',CONFIG_DEFAULT)