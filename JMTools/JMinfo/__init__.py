from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.data_store import get_res_path
from gsuid_core.segment import MessageSegment

from .. import JMClient

SV_JMInfo = SV("jm获取详情")

@SV_JMInfo.on_prefix("jm")
async def GetJMInfo(bot: Bot,ev: Event):
    id = ev.text.strip()
    path = get_res_path() / "JMTools" / "cover"
    JMClient.download_album_cover(id,f"{path}/{id}.png")
    AlbumDetail = JMClient.get_album_detail(id)
    actors = AlbumDetail.actors
    desc = AlbumDetail.description
    tags = AlbumDetail.tags
    title = AlbumDetail.title
    img = MessageSegment.image(f"{path}/{id}.png")
    msg = f"《{title}》\n<{desc}>\n作者：{actors}\n#{tags}\n{img}"
    await bot.send(msg)