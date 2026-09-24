#!/bin/bash
# EP004 temp sound design (synthesized). Timeline:
# CO 0-2 | title 2-5.5 | S02 5.5-15.5 | S03 15.5-25.5 | S04 25.5-35.5 |
# S05 35.5-45.5 | S06 45.5-55.5 | S07 55.5-65.5 | S08 65.5-75.5 |
# S09 75.5-85.5 | S10 85.5-95.5 (total silence) | S11 95.5-105.5
set -e
cd "$(dirname "$0")"
DUR=105.5
ffmpeg -v error -y \
 -f lavfi -i "anoisesrc=color=pink:duration=${DUR}:sample_rate=44100" \
 -f lavfi -i "anoisesrc=color=white:duration=0.4:sample_rate=44100" \
 -f lavfi -i "sine=frequency=55:duration=0.6:sample_rate=44100" \
 -f lavfi -i "anoisesrc=color=white:duration=5:sample_rate=44100" \
 -f lavfi -i "anoisesrc=color=white:duration=0.15:sample_rate=44100" \
 -f lavfi -i "sine=frequency=48:duration=0.8:sample_rate=44100" \
 -f lavfi -i "sine=frequency=2093:duration=3:sample_rate=44100" \
 -filter_complex "\
[0:a]lowpass=f=3000,volume='0.05*if(between(t,2,5.5),0,if(between(t,85.5,95.5),0,1))':eval=frame[bed];\
[1:a]highpass=f=800,volume='exp(-8*t)':eval=frame,adelay=1300,aresample=44100[burst];\
[2:a]volume='0.8*exp(-6*t)':eval=frame,adelay=1300,aresample=44100[thump];\
[3:a]bandpass=f=2500:w=1.5,tremolo=f=9:d=0.6,volume=0.10,adelay=5500,aresample=44100[pencil];\
[4:a]highpass=f=2000,volume='exp(-30*t)':eval=frame,adelay=66000,aresample=44100[crack];\
[5:a]volume='0.9*exp(-5*t)':eval=frame,adelay=66000,aresample=44100[thump2];\
[6:a]volume='0.12*exp(-1.5*t)':eval=frame,adelay=66150,aresample=44100[ring];\
[bed][burst][thump][pencil][crack][thump2][ring]amix=inputs=7:normalize=0,alimiter=limit=0.95[a]" \
 -map "[a]" -c:a pcm_s16le temp_audio_v1.wav
echo "audio built:"
ffprobe -v error -show_entries format=duration -of csv=p=0 temp_audio_v1.wav
