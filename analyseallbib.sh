#!/bin/bash
echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
echo "xxxxxxxx Welcome to Steg analyzer. xxxxxxxx"
echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

echo "This is going to take a while. Why don't you take a coffee :) ?"
path=$1
clear
attack="trim"
echo "Comparing tag resistance to attack : ${attack}"

rm report.txt
nametag="watermarked"
# Listing all wav files (without extension nor path)
files=$(find ${path} -maxdepth 1 -name '*.wav' | awk -F'/' '{print $NF}' | sed -e "s/\.wav//")
# For all wav files
for file in $files
do
    echo "${file}.wav" >> report.txt
    echo "---- Processing file ${file}.wav ----"
    # For all algos
    for alg in "DSS" "LSB" "ECHO"
    do  
        echo "Algo $alg"
        # Writing a tag
        ./main.py -i ${path}$file -a $alg -w ../input w
        # Attacking the signal
        ./main.py -i ${path}output/${file}_${nametag}_$alg atk -t ${attack}
        # Reading from initial file
        ./main.py -i ${path}output/${file}_${nametag}_${alg} -a $alg r
        # Reading from attacked file
        ./main.py -i ${path}output/${file}_${nametag}_${alg}_atk -a $alg r
        # Comparing obtained tags
        ./main.py -fa ${path}output/${file}_${nametag}_${alg}.wmk -fb ${path}output/${file}_${nametag}_${alg}_atk.wmk cmp
    done
    echo "----" >> report.txt
done

echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
echo "xxxxx Job done ! Thanks for waiting ! xxxxx"
echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
