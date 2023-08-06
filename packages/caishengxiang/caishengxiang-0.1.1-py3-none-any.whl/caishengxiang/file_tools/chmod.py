import os
import stat
import json
import pwd


def get_chmod_number(path: str) -> str:
    s = os.stat(path)
    mode = s[stat.ST_MODE]
    usr_num = 0
    if mode & stat.S_IRUSR > 0:
        usr_num += 4
    if mode & stat.S_IWUSR > 0:
        usr_num += 2
    if mode & stat.S_IXUSR > 0:
        usr_num += 1
    grp_num = 0
    if mode & stat.S_IRGRP > 0:
        grp_num += 4
    if mode & stat.S_IWGRP > 0:
        grp_num += 2
    if mode & stat.S_IXGRP > 0:
        grp_num += 1

    oth_num = 0
    if mode & stat.S_IROTH > 0:
        oth_num += 4
    if mode & stat.S_IWOTH > 0:
        oth_num += 2
    if mode & stat.S_IXOTH > 0:
        oth_num += 1
    chmod_num = str(usr_num) + str(grp_num) + str(oth_num)
    return chmod_num
