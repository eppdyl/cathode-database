#!/bin/bash
for mdot in 8 10 12; do
	FILE='ne_vs_x_Id-multiple_mdot-'$mdot'sccm_1.5cm-cathode-raw.csv'

	cat $FILE | awk '/Curve1/{flag=1;next}/Curve2/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/20,$mdot,/"
	cat $FILE | awk '/Curve2/{flag=1;next}/Curve3/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//' | sed "s/^/30,$mdot,/"
	cat $FILE | awk '/Curve3/{flag=1;next}/Curve4/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/40,$mdot,/"
	cat $FILE | awk '/Curve4/{flag=1;next}/Curve5/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/50,$mdot,/"



	if [[ $mdot -eq 8 ]]; then 
		cat $FILE | awk '/Curve5/{flag=1;next}/Curve6/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/60,$mdot,/"
		cat $FILE | awk '/Curve6/{flag=1;next}/Curve7/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/70,$mdot,/"
		cat $FILE | awk '/Curve7/{flag=1;next}/Curve8/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/80,$mdot,/"
		cat $FILE | awk '/Curve9/,!/./' | sed '/^$/d; /Curve9/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/90,$mdot,/"
		cat $FILE | awk '/Curve8/{flag=1;next}/Curve9/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/100,$mdot,/"
	fi

	if [[ $mdot -eq 10 ]]; then
		cat $FILE | awk '/Curve5/{flag=1;next}/Curve6/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/60,$mdot,/"
			cat $FILE | awk '/Curve6/{flag=1;next}/Curve7/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/70,$mdot,/"
			cat $FILE | awk '/Curve7/{flag=1;next}/Curve8/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/80,$mdot,/"
			cat $FILE | awk '/Curve8/{flag=1;next}/Curve9/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/90,$mdot,/"
			cat $FILE | awk '/Curve9/,!/./' | sed '/^$/d; /Curve9/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/100,$mdot,/"
	fi

	if [[ $mdot -eq 12 ]]; then 
		cat $FILE | awk '/Curve6/{flag=1;next}/Curve7/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/60,$mdot,/"
		cat $FILE | awk '/Curve7/{flag=1;next}/Curve8/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/70,$mdot,/"
		cat $FILE | awk '/Curve8/{flag=1;next}/Curve9/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/80,$mdot,/"
		cat $FILE | awk '/Curve9/,!/./' | sed '/^$/d; /Curve9/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/90,$mdot,/"
		cat $FILE | awk '/Curve5/{flag=1;next}/Curve6/{flag=0}flag' | sed '/^$/d' | awk -F',' '{print "\""$1"\",\""$2"\""}'  | awk -f transpose.awk | sed 's/^/[/; s/$/],/' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' | sed 's/,$//'| sed "s/^/100,$mdot,/"
	fi
done
