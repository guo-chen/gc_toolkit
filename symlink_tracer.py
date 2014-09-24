#!/usr/bin/python
import os, sys

# For colourful fancy outputs
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
        if self.check_path.endswith(os.sep):
            self.check_path=self.check_path.rstrip(os.sep) # Right strip the os.sep if the check_path ends with it. In case of the link is created as 'ln -s xx/xx/ xx'
        eval_path, valid = validatePath(self.check_path)
        # print eval_path, valid # for debugging
        if valid == False:
            print("%sOne of the parent directories is a symbolic link, retracing from it.%s"%(bcolors.WARNING,bcolors.ENDC))
            self.check_path=eval_path
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
    last=""
    arrow=">>"
    count=0
    while(test!=target and last!=test):
        list.append(arrow*count+" "+test)
        last=test
        test=iter.next()
        count+=1
    list.append(arrow*count+" "+bcolors.CYAN+test+bcolors.ENDC)
    for path in list:
       print path
    os.chdir(cwd_save)  # returning original path

def validatePath(input_path):
    """
    validatePath() is to check if any parent directories of
    given path is a symbolic link. If so, return the eldest 
    path and False, otherwise return input path and True.
    """
    parent=os.path.dirname(os.path.abspath(input_path))
    path_ancestry_list=[]
    while(parent!=os.sep):
        if os.path.islink(parent):
            path_ancestry_list.append((parent,True))
        else:
            path_ancestry_list.append((parent,False))
        parent=os.path.dirname(parent)
    #    print path_ancestry_list[-1]       # for debugging
    eldest=path_ancestry_list[0][0]
    if True not in [i[1] for i in path_ancestry_list]:
        return os.path.abspath(input_path), True
    else:
        for i in range(len(path_ancestry_list)):
            if path_ancestry_list[i][1] == True:
                eldest=path_ancestry_list[i][0]
        return eldest, False

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
