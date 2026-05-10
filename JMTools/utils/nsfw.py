from nsfwpy import NSFW
from ..JMConfig import JMConfig

def LoadNSFW() -> None:
    global detector
    detector = NSFW()

def DetectImage(Path: str):
    """
    返回[True,result]: 安全；
    返回[False,result]: 危险。
    """
    result = detector.predict_image(Path)
    if result is not None:
        porn = result.get("porn",0) * 0.1
        if porn >= float(JMConfig.get_config("NSFWpersent").data):
            return [False,result]
        else:
            return [True,result]
    else:
        return [False,result]