#!/bin/bash

case $# in
 1      ) python3 /opt/python/ntrace.py x.x.x.x $1 2>/dev/null;;
 2      ) python3 /opt/python/ntrace.py $1 $2 2>/dev/null;;
 *      ) echo "need at least one arg";;
esac

exit 0