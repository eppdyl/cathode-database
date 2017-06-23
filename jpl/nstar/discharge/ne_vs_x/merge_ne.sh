#!/bin/bash
FILE='ne_vs_position_TH8-TH15.csv'

cat $FILE | awk '/Curve1/{flag=1;next}/Curve2/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/8.24,2.47,/"
cat $FILE | awk '/Curve2/,!/./' | sed '/^$/d; /Curve2/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/13.3,3.7,/"
