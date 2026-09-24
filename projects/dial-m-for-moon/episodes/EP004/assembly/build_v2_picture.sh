#!/bin/bash
# EP004 v2 picture assembly — 17 segments, hard cuts, captions burned in.
set -e
cd ~/workspace/jevmax/projects/dial-m-for-moon/episodes/EP004
S=shots
ffmpeg -v error -y \
 -i assembly/EP004_video_only.mp4 \
 -i assembly/title.mp4 \
 -i "$S/v2_SEQA/media-generation-seqa-a1-wide-pan-0-2533ede0-ae5d-4e5f-87f4-7b254e2a58d9.mp4" \
 -i "$S/v2_SEQA/media-generation-seqa-a2-ots-nocap-0-4ec1f711-44ef-428e-8519-282cdaf4dabe.mp4" \
 -i "$S/v2_SEQA/media-generation-seqa-a3-pencil-stop-0-e5a3a27b-0139-46f9-8d63-6bfcc815792d.mp4" \
 -i "$S/v2_SEQA/media-generation-seqa-a4-file-pan-r2-0-a98051de-0010-4fad-b60a-dae3dd763b52.mp4" \
 -i "$S/v2_SEQB/B1_winner.mp4" \
 -i "$S/v2_SEQB/B2_winner.mp4" \
 -i "$S/v2_SEQB/B3_winner.mp4" \
 -i "$S/v2_S05R/media-generation-ep004-s05r-drift-r1-0-f03f28e3-b2bc-4032-abe2-0391029744f4.mp4" \
 -i assembly/EP004_video_only.mp4 \
 -i "$S/v2_S07R/media-generation-ep004-s07r-push-r1-0-b504330d-2a45-4f3f-9aaa-24937fe18c1e.mp4" \
 -i assembly/EP004_video_only.mp4 \
 -i "$S/v2_SEQC/media-generation-seqc-c2-anim-r3-0-b571cb71-c42d-42e5-a492-afd599509500.mp4" \
 -i "$S/v2_S10R/media-generation-ep004-s10r-arc-r2-0-425d24b4-c314-4a60-83ae-601c04958805.mp4" \
 -i "$S/v2_S10R/media-generation-ep004-ins-s10b-r2-0-3fbfcef9-93cf-404b-a574-6948696de061.mp4" \
 -i assembly/EP004_video_only.mp4 \
 -filter_complex "\
[0:v]trim=start=0:end=2,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v0];\
[1:v]trim=start=0:end=3.5,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v1];\
[2:v]trim=start=0:end=8,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v2];\
[3:v]trim=start=0:end=5,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v3];\
[4:v]trim=start=2.5:end=5.5,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v4];\
[5:v]trim=start=0:end=6,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v5];\
[6:v]trim=start=5:end=10,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v6];\
[7:v]trim=start=0:end=4,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v7];\
[8:v]trim=start=0:end=3,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v8];\
[9:v]trim=start=1:end=9,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v9];\
[10:v]trim=start=45.5:end=55.5,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v10];\
[11:v]trim=start=0:end=8,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v11];\
[12:v]trim=start=65.5:end=75.5,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v12];\
[13:v]trim=start=1:end=9,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v13];\
[14:v]trim=start=0:end=6,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v14];\
[15:v]trim=start=0:end=4,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v15];\
[16:v]trim=start=95.5:end=105.5,setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v16];\
[v0][v1][v2][v3][v4][v5][v6][v7][v8][v9][v10][v11][v12][v13][v14][v15][v16]concat=n=17:v=1:a=0[cat];\
[cat]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:text='He never flew.':fontsize=44:fontcolor=white:shadowcolor=black@0.6:shadowx=2:shadowy=2:x=(w-text_w)/2:y=h*0.80:enable='between(t,25.5,27.5)',\
drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:text='Gone.':fontsize=44:fontcolor=white:shadowcolor=black@0.6:shadowx=2:shadowy=2:x=(w-text_w)/2:y=h*0.80:enable='between(t,79.5,82.5)'[v]" \
 -map "[v]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 \
 assembly/EP004_assembly_v2_video.mp4
echo "picture done:"
ffprobe -v error -show_entries format=duration -show_entries stream=width,height,codec_name,r_frame_rate -of default=noprint_wrappers=1 assembly/EP004_assembly_v2_video.mp4
