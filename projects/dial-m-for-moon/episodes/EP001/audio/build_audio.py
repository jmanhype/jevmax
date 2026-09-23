#!/usr/bin/env python3
"""EP001 final audio mix — all foley synthesized with numpy, dialogue from TTS.
Timeline matches EP001_video_1055.mp4 (105.5s). Missing dialogue files are
skipped with a warning so the bed can be built before the RU TTS lands."""
import numpy as np, wave, os, sys

SR = 48000
T = 105.5
N = int(SR * T)
BASE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(1959)

mix = np.zeros(N, dtype=np.float32)

def add(clip, t, gain=1.0, fi=0.005, fo=0.005):
    s = int(t * SR)
    c = np.asarray(clip, dtype=np.float32) * gain
    n = len(c)
    if fi > 0:
        k = min(int(fi * SR), n)
        c[:k] *= np.linspace(0, 1, k)
    if fo > 0:
        k = min(int(fo * SR), n)
        c[-k:] *= np.linspace(1, 0, k)
    e = min(s + n, N)
    if s < N and e > s:
        mix[s:e] += c[:e - s]

def dur(sec):
    return int(sec * SR)

def white(sec, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng
    return r.standard_normal(dur(sec)).astype(np.float32)

def fft_bandpass(x, lo, hi, sr=SR):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / sr)
    m = ((f >= lo) & (f <= hi)).astype(np.float32)
    edge = int(len(m) * 0.02) + 1
    m = np.convolve(m, np.ones(edge) / edge, mode='same')
    return np.fft.irfft(X * m, len(x)).astype(np.float32)

def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = acc * a + x[i] * (1 - a)
        y[i] = acc
    return y

def decay_burst(sec, freq, q_bw=800, decay=0.03, seed=1):
    n = dur(sec)
    t = np.arange(n) / SR
    env = np.exp(-t / decay)
    nse = fft_bandpass(white(sec, seed), freq - q_bw / 2, freq + q_bw / 2)
    nse /= (np.abs(nse).max() + 1e-9)
    return (nse * env).astype(np.float32)

def thump(freq=65, sec=0.25, decay=0.06):
    n = dur(sec); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * freq * t) * np.exp(-t / decay)
    click = decay_burst(0.03, 2500, 2000, 0.008, seed=7) * 0.4
    out = np.zeros(n, dtype=np.float32); out += body.astype(np.float32)
    out[:len(click)] += click
    return out / (np.abs(out).max() + 1e-9)

def creak(sec, f0, f1, seed=3):
    n = dur(sec); t = np.arange(n) / SR
    sweep = f0 + (f1 - f0) * (t / sec)
    ph = 2 * np.pi * np.cumsum(sweep) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    wob = 0.5 + 0.5 * np.sin(2 * np.pi * 9 * t + 1)
    x = saw * wob * np.sin(np.pi * t / sec) ** 2
    return fft_bandpass(x.astype(np.float32), 150, 900, SR) * 0.5

def load_wav(path):
    if not os.path.exists(path):
        print(f"WARN: missing dialogue {path} — skipped", flush=True)
        return None
    w = wave.open(path, 'rb')
    n = w.getnframes()
    raw = w.readframes(n)
    w.close()
    ch = w.getnchannels(); sw = w.getsampwidth(); fr = w.getframerate()
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    if fr != SR:
        idx = (np.arange(int(len(a) * SR / fr)) * fr / SR).astype(int)
        a = a[np.clip(idx, 0, len(a) - 1)]
    return a

# ---------- beds ----------
room = onepole_lp(white(T, 11), 320) * 0.020
hum_t = np.arange(N) / SR
hum = (np.sin(2*np.pi*100*hum_t)*0.006 + np.sin(2*np.pi*200*hum_t)*0.003).astype(np.float32)
add(room + hum, 0, fi=1.0, fo=2.0)

# board hiss S01 (6-14) with slow wander, drops out at S02
h = fft_bandpass(white(8.5, 12), 2200, 9000)
wander = 0.6 + 0.4 * onepole_lp(white(8.5, 13), 2)
add(h * wander * 0.055, 6.0, fi=0.5, fo=0.4)

# corridor bed S05 (32-40): muffled, slightly present
corr = onepole_lp(white(8, 14), 500) * 0.028
add(corr, 32.0, fi=1.0, fo=1.5)

# ---------- S01 events ----------
add(decay_burst(0.07, 1800, 1600, 0.012, seed=21), 8.5, gain=0.5)          # plug click
crk = np.zeros(dur(4.5), dtype=np.float32)                                 # crackle builds 9-13.5
for i, tt in enumerate(np.sort(rng.uniform(0, 4.5, 90))):
    dens = 0.3 + 0.7 * (tt / 4.5)
    if rng.random() < dens:
        b = decay_burst(0.02, 3500, 3000, 0.004, seed=100+i) * (0.3+0.7*rng.random())
        s = int(tt*SR); e = min(s+len(b), len(crk)); crk[s:e] += b[:e-s]
add(crk, 9.0, gain=0.35, fi=0.8, fo=0.5)
st = load_wav(os.path.join(BASE, 'tts/seven_three_s01_radio.wav'))
if st is not None:
    add(st, 10.2, gain=0.11, fi=0.4, fo=0.8)                                # buried mayday
br = fft_bandpass(white(0.9, 22), 400, 1400)                               # sharp intake
add(br * np.sin(np.pi*np.linspace(0,1,dur(0.9)))**0.5 * 0.5, 13.2, gain=0.30, fi=0.35, fo=0.1)

# ---------- S02: hiss drops at 14, hum returns 15.5 ----------
add((np.sin(2*np.pi*100*np.arange(dur(3.5))/SR)*0.010).astype(np.float32), 15.5, fi=1.2)

# ---------- S03: SEVEN-THREE Russian line ----------
s3 = load_wav(os.path.join(BASE, 'tts/seven_three_s03_radio.wav'))
if s3 is not None:
    add(s3, 21.5, gain=0.38, fi=0.05, fo=0.3)

# ---------- S04: pencil knock ----------
add(decay_burst(0.06, 1900, 1400, 0.010, seed=23), 30.5, gain=0.45)          # dry knock

# ---------- S05: pencil scratch 33-38 ----------
scr = fft_bandpass(white(5, 24), 3000, 7500)
am = 0.5 + 0.5*np.abs(np.sin(2*np.pi*7*np.arange(dur(5))/SR + rng.random()*6))
am *= 0.7 + 0.3*rng.random(dur(5))
add(scr*am*0.05, 33.0, fi=0.3, fo=0.6)

# ---------- S06: door, boots, creak ----------
add(creak(1.1, 150, 95, seed=31), 43.5, gain=0.30, fi=0.1, fo=0.3)           # hinges
add(thump(62, 0.22, 0.05), 45.0, gain=0.55)                                 # boot 1
add(thump(58, 0.22, 0.05), 45.5, gain=0.50)                                 # boot 2
add(creak(0.7, 200, 130, seed=32), 47.2, gain=0.16, fi=0.1, fo=0.2)          # floor

# ---------- S07: dialogue over hum ----------
k7 = load_wav(os.path.join(BASE, 'tts/korabelnikov_s07.wav'))
if k7 is not None: add(k7, 53.0, gain=0.50, fi=0.03, fo=0.25)
v7 = load_wav(os.path.join(BASE, 'tts/valya_s07.wav'))
if v7 is not None: add(v7, 56.8, gain=0.46, fi=0.03, fo=0.25)

# ---------- S08: paper 61.5-65.5, then true silence ----------
pap = fft_bandpass(white(4, 25), 900, 4500)
gust = 0.4 + 0.6*np.abs(onepole_lp(white(4, 26), 3))
add(pap*gust*0.09, 61.5, fi=0.2, fo=0.4)
sil = np.ones(N, dtype=np.float32)
for a, b, v in [(65.5, 71.5, 0.03), (89.5, 105.5, 0.02)]:
    s, e = int(a*SR), int(b*SR)
    ramp = int(0.8*SR)
    sil[s:s+ramp] *= np.linspace(1, v, ramp)
    sil[s+ramp:e] *= v
    r2 = min(ramp, N - e)
    if r2 > 0:
        sil[e:e+r2] *= np.linspace(v, 1, r2)
mix *= sil

# ---------- S09: quiet line + stove tick ----------
k9 = load_wav(os.path.join(BASE, 'tts/korabelnikov_s09.wav'))
if k9 is not None: add(k9, 74.0, gain=0.30, fi=0.05, fo=0.4)                # quiet
add(decay_burst(0.035, 4400, 2500, 0.006, seed=27), 76.8, gain=0.10)         # stove tick

# ---------- S10: latch, knocks, silence ----------
add(thump(95, 0.16, 0.04), 82.0, gain=0.45)                                 # door latch
add(decay_burst(0.05, 2600, 1800, 0.010, seed=28), 82.0, gain=0.25)
for kt in (87.0, 88.5):                                                    # two flat static knocks
    k = fft_bandpass(white(0.15, 29), 700, 2600)
    k *= np.minimum(1, np.arange(len(k))/(0.01*SR))
    add(k, kt, gain=0.30, fi=0.005, fo=0.02)

# ---------- finalize ----------
peak = np.abs(mix).max()
print(f"peak before norm: {peak:.3f}", flush=True)
mix = np.tanh(mix * 1.1) * 0.89
out = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
path = os.path.join(BASE, 'EP001_audio_mix.wav')
w = wave.open(path, 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(out.tobytes()); w.close()
print(f"wrote {path} ({os.path.getsize(path)} bytes)", flush=True)
