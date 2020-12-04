clear
echo "This will take a while. Why don't you go take a coffee :) ?"
./main.py -i ../data/music -a LSB -k ../key -w ../input w
./main.py -i ../data/music_watermarked_LSB atk
./main.py -i ../data/music_watermarked_LSB -a LSB -k ../key r
./main.py -i ../data/music_watermarked_LSB_atk_echo -a LSB -k ../key r
echo "Computing differences"
python3 diff.py ../data/music_watermarked_lsb.wmk ../data/music_watermarked_LSB_atk_echo.wmk
echo "Thank you for waiting !"