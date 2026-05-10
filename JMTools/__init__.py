from gsuid_core.sv import Plugins
from gsuid_core.server import on_core_start
from gsuid_core.logger import logger

import jmcomic

Plugins(
    name="JMTools",
)

@on_core_start
async def _LoadJMClient():
    global JMClient
    JMClient = jmcomic.JmOption.default().new_jm_client()
    logger.info("[JMTools] 启动JM客户端成功")


