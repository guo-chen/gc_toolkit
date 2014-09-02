#!/usr/bin/python
import os, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[36m'


class PathIter(object):
    def __init__(self,check_path):
        self.check_path = check_path
    def __iter__(self):
        return self
    def next(self):
        out=os.path.abspath(self.check_path)
        tmp_path=os.path.dirname(self.check_path)
        if not tmp_path:
            tmp_path=os.getcwd()
        os.chdir(tmp_path)
        to_check=os.path.basename(self.check_path)
        if os.path.islink(to_check):
            self.check_path=os.readlink(to_check)
        return out


      
def getLinks(link_name):
    cwd_save=os.getcwd()
    target=os.path.realpath(link_name)
    iter=PathIter(link_name)
    list=[]
    test= iter.next()
    arrow=">>"
    count=0
    while(test!=target):
        list.append(arrow*count+" "+test)
        test=iter.next()
        count+=1
    list.append(arrow*count+" "+bcolors.CYAN+test+bcolors.ENDC)
    for i in list:
       print i
    os.chdir(cwd_save)


if __name__ == "__main__":
    argv_list = sys.argv[1:]
    if argv_list:
        for link in argv_list:
            if os.path.exists(link):
                print("-----%s-----"%link)
                getLinks(link.rstrip(os.sep))
            else:
                print("%s does not exist, skipping ..."%link)
    else:
        print("Error: At least one path needs to be specified.")
        sys.exit(-1)

