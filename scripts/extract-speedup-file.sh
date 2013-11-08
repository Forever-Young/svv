#!/bin/bash
f=$1
type=$2
speedup=$3
tmpdir=$4
tmpdir=`mktemp -d --tmpdir="$tmpdir" -t extract-speedupXXXX`
result_file=$5

if [ "$type" == "mp4" ]; then
    mplayer "$1" -dumpaudio -dumpfile "$tmpdir/temp.mp4a" > /dev/null 2>&1
    faad "$tmpdir/temp.mp4a" > /dev/null 2>&1
fi

if [ "$type" == "flv" ]; then
    mplayer "$1" -dumpaudio -dumpfile "$tmpdir/temp.mp3" > /dev/null 2>&1
    mpg123 -w "$tmpdir/temp.wav" "$tmpdir/temp.mp3" > /dev/null 2>&1
fi
if [ "$speedup" == "0" ]; then
    lame --quiet -m a -cbr -b 64 --resample 24 "$tmpdir/temp.wav" "$result_file" > /dev/null 2>&1
else
    soundstretch "$tmpdir/temp.wav" stdout -tempo="$speedup" -speech 2>/dev/null | lame --quiet -m a -cbr -b 64 --resample 24 - "$result_file"
fi

rm -rf "$tmpdir" > /dev/null 2>&1
