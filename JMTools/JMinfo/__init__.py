from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.data_store import get_res_path
from gsuid_core.segment import MessageSegment
from ..JMConfig import JMConfig
from ..utils.nsfw import DetectImage
from jmcomic import JmcomicText

from .. import JMClient

SV_JMInfo = SV("jm获取详情")

@SV_JMInfo.on_prefix(("jm","JM","禁漫"))
async def GetJMInfo(bot: Bot,ev: Event):
    id = ev.text.strip()
    path = get_res_path() / "JMTools" / "cover"
    file_path = path / f"{id}.jpg"

    path.mkdir(parents=True, exist_ok=True) # 防止文件夹不存在
    if not file_path.exists():# 封面本地不存在
        JMClient.download_album_cover(id,str(file_path))

    # 解析简介
    AlbumDetail = JMClient.get_album_detail(id)
    actors = AlbumDetail.actors
    desc = AlbumDetail.description
    tags = AlbumDetail.tags
    title = AlbumDetail.title
    img = MessageSegment.image(str(file_path))

    # 图片 NSFW 检测
    NSFWSwitch = JMConfig.get_config("NSFWSwitch").data
    if not DetectImage(str(file_path))[0] and NSFWSwitch:
        url = JmcomicText.get_album_cover_url(id)
        img = f"[图片尺度过大，请点击查看]({url})"

    # 文本合并
    msg_text = ["标题：" + title]
    if desc:
        msg_text.append("简介: " + str(desc).strip())
    msg_text.append("\n")
    if actors:
        msg_text.append("作者: " + ", ".join(actors))
    msg_text.append("\n")
    if tags:
        msg_text.append("TAGS: " + ", ".join(f"#{tag}" for tag in tags))
    msg_text = "".join(msg_text)

    # 发送逻辑
    if JMConfig.get_config("InfoSendType").data == "合并转发":
        send_msg = MessageSegment.node([msg_text] + [img])
        await bot.send([send_msg])
    elif JMConfig.get_config("InfoSendType").data == "直接发送":
        send_msg = [msg_text,"\n",img]
        await bot.send(send_msg)

    

# 检测到纯数字
@SV_JMInfo.on_message()
async def MSGIsdigit(bot: Bot,ev: Event):
    msg = ev.text.strip()
    if msg.isdigit() and len(msg)>=5 and len(msg)<=8:
        await GetJMInfo(bot,ev)