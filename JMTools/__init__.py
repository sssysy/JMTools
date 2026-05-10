from gsuid_core.sv import Plugins
from gsuid_core.server import on_core_start
from gsuid_core.logger import logger
from .JMConfig import JMConfig
from .utils.nsfw import LoadNSFW

import jmcomic

Plugins(
    name="JMTools",
)

global JMClient
JMClient = jmcomic.JmOption.default().new_jm_client()
logger.info("[JMTools] 启动JM客户端成功")

@on_core_start
async def _LoadNSFW():
    if JMConfig.get_config("NSFWSwitch").data:
        try:
            LoadNSFW()
            logger.info("[JMTools] 启动 NSFW 检测成功")
        except Exception as e:
            logger.info(f"[JMTools] NSFW 启动失败: {repr(e)}。将自动关闭 NSFW 模块")
            JMConfig.set_config("NSFWSwitch",False)
            
    else:
        logger.info("[JMTools] 跳过 NSFW 检测模块")
    