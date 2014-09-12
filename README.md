gc_toolkit
========

<b>symlink_tracer</b>

DESCRIPTION

>get_link is used to get the trails of given symbolic links (other files are also valid) until reaching their targets.
It will skip dead links or non-existing targets.

FORMAT

>\> symlink_tracer target1 [target2, target3 ...]

>At least one target should be specified.

EXAMPLE

>\> symlink_tracer link1 link2 link3

>-----link1-----

>/home/gc/link1

>\>\>/home/gc/dir/link\_in\_dir

>\>\>\>\>/home/gc/dir2/target

>link2 does not exist, skipping ...

>-----link3-----

>/home/gc/link3

>\>\>/usr/bin/python
