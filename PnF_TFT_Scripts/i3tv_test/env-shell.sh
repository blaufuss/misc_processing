#!/usr/bin/env bash
#
# Icetray environment script for tarballs.  Sets everything relative
# to the directory that this shell runs in.  Different than the env-shell.sh
# which knows about values of I3_BUILD, etc.
#

if [[ "$1" = "help" ]]
    then
    echo "Usage: $0 [SHELL]"
    echo "Spawn a new shell with an Icetray environment loaded"
    echo ""
    echo "SHELL can specified with or without a full path.  If SHELL"
    echo "is omitted the login shell is used by default."
    echo "Examples:"
    echo "   $0"
    echo "   $0 tcsh"
    echo "   $0 /bin/tcsh"
    echo "   $0 /path/to/script.py"
    echo ""
    echo "To exit the Icetray environment simply exit the new shell."
    echo ""
    exit 1
fi

if [[ -z "$1" ]]
    then # user did not specify a shell
    NEW_SHELL=$SHELL 
    # only exit if no shell specified on command line *and* env already loaded 
    if [[ -n "$I3_SHELL" ]] 
	then  
	echo "****************************************************************"
	echo "You are currently in a shell with an Icetray environment loaded."
	echo "Please exit the current shell and re-run $0 from a clean shell."
	echo "****************************************************************"
	echo "Environment not (re)loaded."
	exit 2
    fi
else
    NEW_SHELL=$1
    shift
    ARGV=$*
fi

_I3_SHELL=$NEW_SHELL

#
# Determine directory that this shell lives in.
#
BASEDIR='/usr/local/pnf/i3tv/icerec-current'

_I3_SRC=$BASEDIR
_I3_BUILD=$BASEDIR

# Check for I3_BUILD mismatch
if [ -n "$I3_BUILD" -a "$I3_BUILD" != "$_I3_BUILD" ]
then
    echo "****************************************************************"
    echo "I3_BUILD CHANGED"
    echo "It appears that you are attempting to load an icetray environment different"
    echo "than the one already loaded"
    echo "          This I3_BUILD=$_I3_BUILD"
    echo "Already loaded I3_BUILD=$I3_BUILD"
    echo "****************************************************************"
    echo "Environment not (re)loaded."
    exit 2
fi

_ROOTSYS=$BASEDIR/cernroot

_LD_LIBRARY_PATH=$BASEDIR/lib:$_ROOTSYS/lib:$BASEDIR/lib/tools:$LD_LIBRARY_PATH
_DYLD_LIBRARY_PATH=$BASEDIR/lib:$_ROOTSYS/lib:$BASEDIR/lib/tools:$ROOTSYS:$DYLD_LIBRARY_PATH
_PYTHONPATH=$BASEDIR/lib:$PYTHONPATH
_PATH=$BASEDIR/bin:$PATH

TOPBAR="************************************************************************"
WIDTH=`echo "$TOPBAR" | wc -c`

WIDTH=$(( $WIDTH-2 ))

function printctr()
{
    LEN=`echo "$*" | wc -c`
    LOFFSET=$(( ($WIDTH-$LEN)/2 ))
    ROFFSET=$(( $WIDTH-$LOFFSET-$LEN ))

    FORMAT="*%${LOFFSET}s%s%${ROFFSET}s*\n"
    printf $FORMAT " " "$*" " "
}

if [[ -z "$ARGV" ]]
    then
    printf "$TOPBAR\n"
    printctr ""
    printctr "W E L C O M E  to  I C E T R A Y"
    printctr ""
    printctr "Version icerec.releases.V03-03-00     r69466"
    printctr ""
    printctr "You are welcome to visit our Web site"
    printctr "http://icecube.umd.edu"
    printctr ""
    printf "$TOPBAR\n"
    printf "\n"
    printf "Icetray environment has:\n"
    printf "   I3_SRC       = %s\n" $_I3_SRC
    printf "   I3_BUILD     = %s\n" $_I3_BUILD
    printf "   I3_PORTS     = %s\n" $_I3_PORTS
fi

if [[ -z "$I3_SHELL" ]] # a clean, first invocation
    then

    PATH=$_PATH \
	LD_LIBRARY_PATH=$_LD_LIBRARY_PATH \
	DYLD_LIBRARY_PATH=$_DYLD_LIBRARY_PATH \
	PYTHONPATH=$_PYTHONPATH \
	I3_SRC=$_I3_SRC \
	I3_BUILD=$_I3_BUILD \
	ROOTSYS=$_ROOTSYS \
	I3_SHELL=$_I3_SHELL \
	$NEW_SHELL $ARGV

else  # not clean, use previous environment
    $NEW_SHELL $ARGV
fi

STATUS=$?

if [ -z "$ARGV" ]
then
    echo "Exited Icetray Environment."
fi
exit $STATUS
