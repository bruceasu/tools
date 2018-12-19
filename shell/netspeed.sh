#!/bin/bash

#Description:show the net speed
#Author:kofj
#Mail: kfanjian#gmail.com(change # to @)
#AD:Building Website,please view kofj.net

interface=${1:-eth0}

typeset in in_old dif_in dif_in1 dif_out1
typeset out out_old dif_out


in_old=$(cat /proc/net/dev | grep wan1 | sed 's=^.*:==' | awk '{ print $1 }' )
out_old=$(cat /proc/net/dev | grep wan1 | sed 's=^.*:==' | awk '{ print $9 }')


while true
do
         sleep 1
         in=$(cat /proc/net/dev | grep $interface | sed 's=^.*:==' | awk '{ print $1 }')
         out=$(cat /proc/net/dev | grep $interface | sed 's=^.*:==' | awk '{ print $9 }')
         dif_in=$((in-in_old))
         #dif_in1=$((dif_in * 8 /1024))
         dif_in1=`echo "scale=3; ${dif_in} /1024" | bc`
         dif_out=$((out-out_old))
#         echo "IN: ${dif_in} bytes OUT: ${dif_out} bytes"
         #dif_out1=$((dif_out * 8 / 1024 / 1024 ))
         dif_out1=`echo "scale=3; ${dif_out} /1024" | bc`
         echo -e "IN: ${dif_in1} kBps\tOUT: ${dif_out1} kBps"
         in_old=${in}
         out_old=${out}
done
