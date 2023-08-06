from collections import OrderedDict
import threading
from typing import Dict
import json
import os

trans: Dict[str, str] = {}
with open(os.path.join(os.path.dirname(__file__), "trans", "trans.zh.json"), "r", encoding="utf-8") as f:
    trans  = json.load(f)

LANG = "zh"
untranslated: Dict[str, str] = {}


def _trans(str_to_trans: str) -> str:
    if str_to_trans in trans and trans[str_to_trans] != "":
        return trans[str_to_trans]
    else:
        untranslated[str_to_trans] = ""
        return str_to_trans


def write_to_translation_file():
    global timer, untranslated, trans
    with open(os.path.join(os.path.dirname(__file__), "trans", "trans.zh.json"), "w", encoding="utf8") as f:
        untranslated.update(trans)
        
        items = sorted(untranslated.items(), key=lambda obj: obj[0])
        # 创建一个新的空字典
        new_dict = OrderedDict()
        # 遍历 items 列表
        for item in items:
            # item[0] 存的是 key 值
            new_dict[item[0]] = untranslated[item[0]]
        json.dump(new_dict, f, indent=4, ensure_ascii=False)
    with open(os.path.join(os.path.dirname(__file__), "trans", "trans.zh.json"), "r", encoding="utf-8") as f:
        trans = json.load(f)
    untranslated = {}
    timer = threading.Timer(3, write_to_translation_file)
    timer.setDaemon(True)
    timer.start()

timer = threading.Timer(3, write_to_translation_file)
timer.start()
