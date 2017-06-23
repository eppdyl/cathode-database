#!/bin/bash
FILE='phip_vs_x_TH8-TH15.csv'

cat $FILE | awk '/Curve1/{flag=1;next}/Curve3/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/8.24,2.47,/"
cat $FILE | awk '/Curve3/,!/./' | sed '/^$/d; /Curve3/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/13.3,3.7,/"
