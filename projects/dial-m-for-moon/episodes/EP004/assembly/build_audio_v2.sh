#!/bin/bash
# EP004 v2 sound design (synthesized, adapted from build_audio.sh).
# v2 timeline (103.5s):
# CO 0-2 | title 2-5.5 | A1 5.5-13.5 | A2 13.5-18.5 | A3 18.5-21.5 | A4 21.5-27.5 |
# B1 27.5-32.5 | B2 32.5-36.5 | B3 36.5-39.5 | S05R 39.5-47.5 | S06 47.5-57.5 |
# S07R 57.5-65.5 | S08 65.5-75.5 | C2 75.5-83.5 | S10R 83.5-89.5 (silence) |
# INS 89.5-93.5 (silence) | S11 93.5-103.5
#
# - Tape-hiss bed across all, ducked near-zero under title 2-5.5,
#   total silence 83.5-93.5, dipped to 20% at 79.5-81.5 (empty depression found),
#   faint return 93.5-103.5.
# - Spark burst + low thump at 1.3s (CO payoff).
# - Pencil scratch 5.5-21.0, hard stop at 21.0 (A3 pencil stops dead).
# - S08 electrical crack + thump + ring at 66.5s.
set -e
cd "$(dirname "$0")"
DUR=103.5
ffmpeg -v error -y \
 -f lavfi -i "anoisesrc=color=pink:duration=${DUR}:sample_rate=44100" \
 -f lavfi -i "anoisesrc=color=white:duration=0.4:sample_rate=44100" \
 -f lavfi -i "sine=frequency=55:duration=0.6:sample_rate=44100" \
 -f lavfi -i "anoisesrc=color=white:duration=15.5:sample_rate=44100" \
 -f lavfi -i "anoisesrc=color=white:duration=0.15:sample_rate=44100" \
 -f lavfi -i "sine=frequency=48:duration=0.8:sample_rate=44100" \
 -f lavfi -i "sine=frequency=2093:duration=3:sample_rate=44100" \
 -filter_complex "\
[0:a]lowpass=f=3000,volume='0.05*if(between(t,2,5.5),0.05,if(between(t,83.5,93.5),0,if(between(t,79.5,81.5),0.2,if(between(t,93.5,103.5),0.4,1))))':eval=frame[bed];\
[1:a]highpass=f=800,volume='exp(-8*t)':eval=frame,adelay=1300,aresample=44100[burst];\
[2:a]volume='0.8*exp(-6*t)':eval=frame,adelay=1300,aresample=44100[thump];\
[3:a]bandpass=f=2500:w=1.5,tremolo=f=9:d=0.6,volume=0.10,afade=t=out:st=15.35:d=0.15,adelay=5500,aresample=44100[pencil];\
[4:a]highpass=f=2000,volume='exp(-30*t)':eval=frame,adelay=66500,aresample=44100[crack];\
[5:a]volume='0.9*exp(-5*t)':eval=frame,adelay=66500,aresample=44100[thump2];\
[6:a]volume='0.12*exp(-1.5*t)':eval=frame,adelay=66650,aresample=44100[ring];\
[bed][burst][thump][pencil][crack][thump2][ring]amix=inputs=7:normalize=0,alimiter=limit=0.95[a]" \
 -map "[a]" -c:a pcm_s16le temp_audio_v2.wav
echo "audio built:"
ffprobe -v error -show_entries format=duration -of csv=p=0 temp_audio_v2.wav
