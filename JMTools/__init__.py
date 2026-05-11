from gsuid_core.sv import Plugins
from gsuid_core.server import on_core_start
from gsuid_core.logger import logger
from .JMConfig import JMConfig
from .utils.nsfw import LoadNSFW
from .utils.shortlink import LoadShortLinkSettings

import jmcomic
import os

Plugins(
    name="JMTools",
)

global JMClient
JMClient = jmcomic.JmOption.default().new_jm_client()
logger.info("[JMTools] 启动JM客户端成功")

@on_core_start
async def _Load():

    # 检查 NSFW 配置项
    if JMConfig.get_config("NSFWSwitch").data:
        try:
            os.environ["NSFWPY_USE_CHINA_MIRROR"] = "0" # 关闭nsfwPy模型镜像下载（SSL错误）
            LoadNSFW()
            logger.info("[JMTools] 启动 NSFW 检测成功")
        except Exception as e:
            logger.warning(f"[JMTools] NSFW 启动失败: {repr(e)}。将自动关闭 NSFW 模块")
            JMConfig.set_config("NSFWSwitch",False)
            
    else:
        logger.info("[JMTools] 跳过 NSFW 检测模块")

    # 检查 Sink 配置项
    if JMConfig.get_config("SinkSwitch").data:
        SinkUrl = JMConfig.get_config("SinkUrl").data
        SinkToken = JMConfig.get_config("SinkToken").data
        SinCloaking = JMConfig.get_config("SinCloaking").data
        SinUnsafe = JMConfig.get_config("SinUnsafe").data
        SinExpireTime = JMConfig.get_config("SinExpireTime").data
        logger.debug(f"[JMTools] {SinCloaking},{SinUnsafe}")
        if SinkUrl is None or SinkToken is None:
            logger.warning("[JMTools] 短链接配置缺失，将自动关闭短链接功能")
            JMConfig.set_config("SinkSwitch",False)
        else:
            LoadShortLinkSettings(SinkUrl=SinkUrl,SinkToken=SinkToken,SinCloaking=SinCloaking,SinUnsafe=SinUnsafe,expire=SinExpireTime)
            logger.info("[JMTools] 启动短链接功能成功")
        