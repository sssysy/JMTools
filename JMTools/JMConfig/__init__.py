from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsStrConfig,
    GsBoolConfig,
    GsListStrConfig,
    GsFloatConfig,
    GsIntConfig
)
from gsuid_core.utils.plugins_config.gs_config import StringConfig
from gsuid_core.data_store import get_res_path

CONFIG_PATH = get_res_path() / 'JMTools' / 'config.json'

CONFIG_DEFAULT: dict[str, GSC] = {
    "InfoSendType": GsStrConfig(
        "JM 作品简介发送方式",
        "",
        "直接发送",
        ["直接发送", "合并转发"],
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
    )
}

JMConfig = StringConfig("JMConfig",CONFIG_PATH,CONFIG_DEFAULT)