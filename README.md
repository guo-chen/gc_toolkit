gc_toolkit
========

##symlink_tracer

#####DESCRIPTION
<code>symlink_tracer</code> is used to get the trails of given symbolic links (other files are also valid) until reaching their targets. It will skip dead links or non-existing targets.

#####SYNOPSIS
<pre>
> symlink_tracer target1 [target2, target3 ...]
At least one target should be specified.
</pre>

#####EXAMPLE
<pre>
> symlink_tracer link1 link2 link3
-----link1-----
/home/gc/link1
>>/home/gc/dir/link_in_dir
>>>>/home/gc/dir2/target
link2 does not exist, skipping ...
-----link3-----
/home/gc/link3
>>/usr/bin/python
</pre>


##qa_auto_reproduce

#####STATEMENT OF CONFIDENTIALITY
In this tool the actual name of the product name and the regression robot name is modified in case of potential violations of company regulations.

#####DESCRIPTION
<code>qa_auto_reproduce</code> is used for reproducing failed cases in different suite automatically for the daily work. This is subject to the testing framework which is confidential to public. 

#####SYNOPSIS
<pre>
> qa_auto_reproduce --help
usage: qa_auto_reproduce [options] caselist TOOL_version

This is used to generate a shell script and case list to run regression
framework robot to reproduce failed cases listed in daily work panel

options:
  -h, --help  show this help message and exit
  -r, --run   It will run the generated script if -r is specified
usage: qa_auto_reproduce [options] caselist TOOL_version
</pre>
