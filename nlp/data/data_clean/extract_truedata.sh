
project=$1
if [ $project == 1 ];then
cat text |grep -v \# |sed '/^$/d'|awk '{if($2)print $0}'|sed 's/\r//g' |sed 's/  / /g' |sed 's///g' |sed -e 's/\xEF\xBB\xBF//' |sed 's///' |sed 's///'> new_wav_lab
cat new_wav_lab|awk '{print $1}' > wavlist
cat new_wav_lab|awk '{$1="";sub(" ", "");print}'|sed 's/+/加/g'|sed 's/-/减/g'|sed 's/\./点/g'|sed 's/\\t//g'|sed 's/\\n//g'|sed 's/[[:punct:]]/ /g' |tr a-z A-Z > label.text
paste -d " " wavlist label.text > final_wav_lab.text
fi

