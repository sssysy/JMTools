import httpx
import time

g_url = ""
g_token = ""
g_cloaking = ""
g_unsafe = ""
g_erxpire = 0

def LoadShortLinkSettings(SinkUrl:str,SinkToken:str,SinCloaking:bool,SinUnsafe:bool,expire:int=0):
    """
    参数：
        SinkUrl: 短链接生成域名
        SinkToken: 短链接生成Token
        SinCloaking: 短链接伪装
        SinUnsafe: 短链接跳转提示    
        expire: 有效时间(小时)
    """
    global g_url, g_token, g_cloaking, g_unsafe, g_erxpire
    g_url = SinkUrl
    g_token = SinkToken
    g_cloaking = SinCloaking
    g_unsafe = SinUnsafe
    g_erxpire = expire



async def CreateShortLink(link:str,title = None):
    url = f"{g_url}/api/link/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {g_token}"
    }
    data = {
        "url": link,
        "cloaking": g_cloaking,
        "unsafe": g_unsafe,
        "title": title or "",
        "": int(time.time()) + g_erxpire * 3600
    }
    print(data)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url,headers=headers,json=data)
            if response.status_code != 201:
                return {"code": response.status_code, "msg":response.text}
            else:
                return {"code": 201,"msg": "","link": response.json().get("shortLink")}
    except Exception as e:
        return {"code": -1,"msg": f"{repr(e)}|{data}|{headers}"}

