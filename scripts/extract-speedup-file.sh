#!/bin/bash
f=$1
type=$2
speedup=$3
tmpdir=$4
tmpdir=`mktemp -d --tmpdir="$tmpdir" -t extract-speedupXXXX`
result_file=$5

if [ "$type" == "mp4" ]; then
    mplayer "$f" -dumpaudio -dumpfile "$tmpdir/temp.mp4a" > /dev/null 2>&1
    rm "$f"
    if [ "$speedup" == "0" ]; then
        faad -w "$tmpdir/temp.mp4a" 2>/dev/null | lame --quiet -m a -cbr -b 64 --resample 24 - "$result_file" > /dev/null 2>&1
    else
        faad -f 1 -o "$tmpdir/temp.wav" "$tmpdir/temp.mp4a" 2>/dev/null
        rm "$tmpdir/temp.mp4a"
        soundstretch "$tmpdir/temp.wav" stdout -tempo="$speedup" -speech 2>/dev/null | lame -m a -cbr -b 64 --resample 24 - "$result_file"
    fi
fi

if [ "$type" == "flv" ]; then
    mplayer "$f" -dumpaudio -dumpfile "$tmpdir/temp.mp3" > /dev/null 2>&1
    rm "$f"
    if [ "$speedup" == "0" ]; then
        mpg123 -w - "$tmpdir/temp.mp3" 2>/dev/null | lame --quiet -m a -cbr -b 64 --resample 24 - "$result_file" > /dev/null 2>&1
    else
        mpg123 -w "$tmpdir/temp.waw" "$tmpdir/temp.mp3" 2>/dev/null
        rm "$tmpdir/temp.mp3"
        soundstretch "$tmpdir/temp.wav" stdout -tempo="$speedup" -speech 2>/dev/null | lame --quiet -m a -cbr -b 64 --resample 24 - "$result_file"
    fi
fi

rm -rf "$tmpdir" > /dev/null 2>&1
