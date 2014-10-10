#!/usr/bin/python

import os, sys, optparse

TOOL_VERSIONS_LIST = ['dev','2014.12','2014.06-SP2','2014.06-SP1','2014.06','2013.12','2013.06']

if __name__ == "__main__":
    usage = "%prog [options] caselist TOOL_version"
    description = "This is used to generate a shell script and case list to run regression robot to reproduce failed cases listed in daily work panel"
    parser = optparse.OptionParser(usage=usage, description=description)
    parser.add_option("-r", "--run", action="store_true", dest="run", default=False, help="It will run the generated script if -r is specified")
    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        parser.error("Wrong number of arguments")
    else:
        input_file = args[0]
        version = args[1]
	    # TODO sanity check of input_file
	    # checkCaselist()
	    # check TOOL version to run
        if version not in TOOL_VERSIONS_LIST:
            parser.error("The specified TOOL_version [%s] is not correct or unsupported."%version)
        try:
            case_list = [line.strip().split('/') for line in open(input_file,'r')]
        except IOError:
            parser.error("caselist file (arg1) does not exist!")

        case_dict={}
        for item in case_list:
            if len(item)==2:
                (suite, case) = item
                if suite not in case_dict.keys():
                    case_dict[suite]=[case]
                else:
                    case_dict[suite].append(case)
        if not os.path.exists("ready_to_go"):
            os.mkdir("ready_to_go") 
        os.chdir("ready_to_go")

        for suite in case_dict.keys():
            tmp_fh = open("%s.tl"%suite, 'w')
            for i in case_dict[suite]:
                tmp_fh.write(i+'\n')
            tmp_fh.close()
        print("[Bobby]: Finished generating .tl case lists")
        # Composing shell script        
        sh_fh=open("runme.sh",'w')
        sh_fh.write("""#!/bin/csh -f
set username = `id -u -n`
if -d results then
    rm -rf results
endif
mkdir results
cd results
mkdir logs
""")
        for suite in case_dict.keys():
            ca = "" # needs to reset the value of 'ca' each iteration
            if "_q" in suite:
                ca = ""
            elif "_32" in suite or "_64" in suite:
                if "err" in suite:
                    ca = "-64"
                else:
                    ca = "-ca -64"
            elif "-ndg" in suite:
                ca = "-ca -ndg"
            else:
                ca = ""
            sh_fh.write('echo "[Bobby]: Running suite: %s ..."\n'%suite)
            sh_fh.write("regression_robot -v %s -s %s -r %s -k %s >& logs/%s_reproduce.log\n"%(version, suite, os.path.realpath("%s.tl"%suite), ca, suite))
            sh_fh.write("sed '1,/==START==/d' /SCRATCH/$username/AMD.64/%s/%s/report.txt >& %s_results.txt\n"%(version,suite,suite))
        sh_fh.close()
        os.chmod("runme.sh", 0777)
        print "[Bobby]: Done. Source runme.sh to execute"
        if opts.run:
            print "[Bobby]: Now running runme.sh ..."
            result=os.system("runme.sh")
            if not result:
        	    print "[Bobby]: Successfully finished running"
            else:
                print "[Bobby]: Failed running the script"
