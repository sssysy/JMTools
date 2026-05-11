from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.data_store import get_res_path
from gsuid_core.segment import MessageSegment
from ..JMConfig import JMConfig
from ..utils.nsfw import DetectImage
from jmcomic import JmcomicText,MissingAlbumPhotoException

from .. import JMClient
from ..utils.shortlink import CreateShortLink

SV_JMInfo = SV("jm获取详情")

@SV_JMInfo.on_prefix(("jm","JM","禁漫"))
async def GetJMInfo(bot: Bot,ev: Event):

    id = ev.text.strip().lstrip("0") # 删除左侧多的0
    path = get_res_path() / "JMTools" / "cover"
    file_path = path / f"{id}.jpg"
    url = ""
    img = ""


    # 解析简介
    try:
        AlbumDetail = JMClient.get_album_detail(id)
        logger.debug(f"[JMTools] 获取到的本子标题：{AlbumDetail.title}")
    except MissingAlbumPhotoException as e: # 本子不存在
        logger.error(f"[JMTools] jm号不存在")
        ErrorText = JMConfig.get_config("DetailErrorText").data
        await bot.send(f"\n{ErrorText}(jm{e.error_jmid} 不存在)",True)
        return
    except Exception as e:
        logger.error(f"[JMTools] 获取jm详情失败：{repr(e)}")
        await bot.send(f"jm号解析失败，详见控制台")
        return
    
    actors = AlbumDetail.actors
    desc = AlbumDetail.description
    tags = AlbumDetail.tags
    title = AlbumDetail.title
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


    # 解析图片
    path.mkdir(parents=True, exist_ok=True) # 防止文件夹不存在

    CoverSendUrl = JMConfig.get_config("CoverSendUrl").data
    ShortLink = JMConfig.get_config("SinkSwitch").data

    
    if not file_path.exists():# 封面本地不存在
        JMClient.download_album_cover(id,str(file_path))

    if CoverSendUrl == "发送图片":# 发送图片
        img = MessageSegment.image(str(file_path))

        # 图片 NSFW 检测
        NSFWSwitch = JMConfig.get_config("NSFWSwitch").data
        if not DetectImage(str(file_path))[0] and NSFWSwitch:
            img = MessageSegment.text(f"[图片尺度过大，请点击查看]({url})")

    elif CoverSendUrl == "发送链接":
        url = JmcomicText.get_album_cover_url(id)
        img = MessageSegment.text(url)

        # 判断是否短链接
        if ShortLink:# 开启短链接
            text = await CreateShortLink(url)
            if text["code"] == 201: # 生成成功
                logger.debug(f"[JMTools] 网页返回201，网址{text["link"]}")
                url = MessageSegment.text(text["link"])
                img = url
            else:# 生成失败，保持原样
                logger.warning(f"短链接生成失败: {text}，将直接发送源网址")


    # 发送逻辑
    if JMConfig.get_config("InfoSendType").data == "合并转发":
        send_msg = MessageSegment.node([msg_text] + [img])
        logger.debug(send_msg)
        await bot.send([send_msg])
    elif JMConfig.get_config("InfoSendType").data == "直接发送":
        send_msg = [msg_text,"\n",img]
        logger.debug(send_msg)
        await bot.send(send_msg)

    

# 检测到纯数字
@SV_JMInfo.on_message()
async def MSGIsdigit(bot: Bot,ev: Event):
    msg = ev.text.strip()
    NumberDetect = JMConfig.get_config("NumberDetect").data
    if msg.isdigit() and len(msg)>=5 and len(msg)<=8 and NumberDetect:
        await GetJMInfo(bot,ev)