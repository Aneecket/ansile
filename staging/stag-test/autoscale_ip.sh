scaling_group=stag-pnlmanager
ags_details=$(python count.py $scaling_group)
ip_list=$(echo  $ags_details | jq -r '.ip' | tr "," " " | tr -d "'" | xargs -n1 )
#echo "$ip_list"
#sed '2a $ip_list' hosts
#(echo 2a; echo $ip_list; echo .; echo w) | ed - hosts
awk "NR==3 {print $ip_list} 2" hosts1 > hosts2 
