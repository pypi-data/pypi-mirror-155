import time
import random
from typing import Union

__all__ = "shuffle,drop".split(",")


def shuffle(string: str, times: int = 1, show_seed: bool = False) -> Union[str, tuple]:
    """
    打乱字符串

    :param string: 原始字符串
    :param times: 进行几次打乱
    :param show_seed: 是否输出种子
    :return: str
    """
    if not string:
        return ""
    for _ in range(times):
        seed = _get_seed()
        if show_seed:
            print(seed)
        string_list = list(string)
        for index, data in enumerate(string_list):
            tmp = string_list[(ord(data) + seed) % len(string_list)]
            string_list[(ord(data) + seed) % len(string_list)] = data
            string_list[index] = tmp
    if show_seed:
        return ''.join(string_list), seed
    else:
        return ''.join(string_list)


def drop(string: str, how_many: Union[int, float], show_seed: bool = False) -> Union[str, tuple]:
    """
    随机丢去字符串一些字符

    :param string: 原始字符串
    :param how_many: >=1为丢弃多少字符，,<1为丢去多少比例的字符，向下取整
    :param show_seed: 是否输出种子
    :return:
    """
    if not string:
        return ""
    if int(how_many) >= len(string):
        return ""
    seed = _get_seed()
    string_list = list(string)
    if how_many < 1:
        how_many = int(len(string_list) * how_many)
        if how_many == 0:
            return ''.join(string_list)
    for _ in range(how_many):
        string_list.remove(string_list[(how_many * seed) % len(string_list)])
    if show_seed:
        return ''.join(string_list), seed
    else:
        return ''.join(string_list)


def _get_seed() -> int:
    """
    生成种子

    :return: int
    """
    return int(time.time() + random.randint(0, 100_000_000))


if __name__ == "__main__":
    inp_string = input(":")
    for _ in range(10):
        print(shuffle(drop(inp_string, how_many=2)))
