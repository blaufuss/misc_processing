#!/bin/sh

jobbase='nofilt20_'
script="/data/user/blaufuss/no_filt_find/nofilt_hunt.py"
outdir="/data/user/blaufuss/NoFilt/2020/"
counter=100
### seq <min> <stepsize> <max>
#for a in `seq 0.1 0.01 1.0`; do
for infile in `ls -d /data/exp/IceCube/2020/filtered/PFFilt/[0-1]*`; do
    let counter=counter+1
    command="python ${script} ${infile} ${outdir}"
    jobname=$jobbase$counter
    JOBID=$jobbase$counter
    echo JOB $JOBID /data/user/blaufuss/no_filt_find/submit.sub
    echo VARS $JOBID JOBNAME=\"$jobname\" command=\"$command\"
done

