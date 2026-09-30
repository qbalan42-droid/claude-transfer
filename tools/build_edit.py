#!/usr/bin/env python3
"""Fast-cut edit of a talking-head video: jump cuts on every pause, punch-in zoom per cut, word-by-word captions
with the live word in yellow, a hook card and chapter cards. Local tools only (ffmpeg, whisper.cpp).
Setup once:   brew install whisper-cpp ; download ggml-small.en.bin next to this script
Usage:        build_edit.py raw.mp4 plan|all [--preview SECONDS]   (writes into ./edit_work)
Optional edit_meta.json next to the raw file: {"hook": ["TEXT", seconds], "chapters": [[source_sec, "Title"], ...], "out": "final.mp4"}
"""
import json, os, re, subprocess, sys
FF, FP, WC = 'ffmpeg', 'ffprobe', 'whisper-cli'
RAW = os.path.abspath(sys.argv[1]); STEP = sys.argv[2] if len(sys.argv) > 2 else 'plan'
PREVIEW = float(sys.argv[sys.argv.index('--preview') + 1]) if '--preview' in sys.argv else None
W = os.path.join(os.path.dirname(RAW), 'edit_work'); SEG = os.path.join(W, 'seg'); os.makedirs(SEG, exist_ok=True)
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ggml-small.en.bin')
LEAD, TAIL = 0.06, 0.10; FILLERS = {'um', 'uh', 'umm', 'uhh', 'hmm', 'mm', 'ah', 'er'}; ZOOMS = [1.0, 1.10, 1.0, 1.06, 1.14, 1.0, 1.08]
FONTS = '/System/Library/Fonts/Supplemental'; ENC = ['-c:v', 'h264_videotoolbox', '-b:v', '12M', '-profile:v', 'high']
run = lambda cmd: subprocess.run(cmd, check=True)

def transcribe():
    wav = os.path.join(W, 'audio.wav'); tj = os.path.join(W, 'transcript.json')
    if not os.path.exists(tj):
        run([FF, '-v', 'error', '-y', '-i', RAW, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', wav])
        run([WC, '-m', MODEL, '-f', wav, '-l', 'en', '-oj', '-of', tj[:-5], '-ml', '1', '-sow', '-t', '8'])
    j = json.load(open(tj))['transcription']
    return [(x['offsets']['from'] / 1000.0, x['offsets']['to'] / 1000.0, x['text'].strip()) for x in j if x['text'].strip()], wav

def silences(wav):
    out = subprocess.run([FF, '-v', 'info', '-i', wav, '-af', 'silencedetect=noise=-30dB:d=0.25', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', out)]; es = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
    return list(zip(ss, es))

def plan(ws, sil):
    end = ws[-1][1] + 1.0; speech = []; t = 0.0
    for a, b in sil:
        if a - t >= 0.30: speech.append((t, a))
        t = b
    speech.append((t, end))
    fill = [(s, e) for s, e, w in ws if re.sub(r'[^a-z]', '', w.lower()) in FILLERS and e - s >= 0.18]
    out = []
    for a, b in speech:
        cur = a
        for fs, fe in fill:
            if fs > cur and fe < b and fs - cur >= 0.25: out.append((cur, fs)); cur = fe
        if b - cur >= 0.25: out.append((cur, b))
    rg = [(max(0, a - LEAD), b + TAIL) for a, b in out]; merged = []
    for a, b in rg:
        if merged and a <= merged[-1][1] + 0.05: merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else: merged.append((a, b))
    return [(a, min(b, PREVIEW)) for a, b in merged if a < PREVIEW] if PREVIEW else merged

def cut(rg):
    files = []
    for i, (a, b) in enumerate(rg):
        z = ZOOMS[i % len(ZOOMS)]; out = os.path.join(SEG, 'seg_%04d.mp4' % i); files.append(out)
        if os.path.exists(out) and os.path.getsize(out) > 1000: continue
        vf = 'crop=iw/%.3f:ih/%.3f:(iw-iw/%.3f)/2:(ih-ih/%.3f)*0.40,scale=1920:1080,fps=60,format=yuv420p' % (z, z, z, z)
        af = 'afade=t=in:st=0:d=0.012,afade=t=out:st=%.3f:d=0.012,aresample=48000' % max(0, b - a - 0.012)
        run([FF, '-v', 'error', '-y', '-hwaccel', 'videotoolbox', '-ss', '%.3f' % a, '-to', '%.3f' % b, '-i', RAW, '-vf', vf, '-af', af] + ENC + ['-c:a', 'aac', '-b:a', '192k', '-ac', '2', out])
    lst = os.path.join(W, 'concat.txt'); open(lst, 'w').write(''.join("file '%s'\n" % f for f in files))
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', os.path.join(W, 'cut.mp4')])

def remap(rg):
    offs = []; t = 0.0
    for a, b in rg: offs.append(t); t += b - a
    def f(x):
        for (a, b), o in zip(rg, offs):
            if a <= x <= b: return o + (x - a)
    return f

def T(t): return '%d:%02d:%05.2f' % (int(t // 3600), int(t % 3600 // 60), t % 60)

def captions(ws, rg, meta):
    f = remap(rg); kept = [(f(s), f(e), w) for s, e, w in ws if f(s) is not None and f(e) is not None and re.sub(r'[^a-z]', '', w.lower()) not in FILLERS]
    groups, g = [], []
    for s, e, w in kept:
        if g and (len(g) >= 3 or s - g[-1][1] > 0.6 or re.search(r'[.!?]$', g[-1][2])): groups.append(g); g = []
        g.append((s, e, w))
    if g: groups.append(g)
    ev = []
    for g in groups:
        ge = g[-1][1] + 0.12
        for k, (s, e, w) in enumerate(g):
            e2 = g[k + 1][0] if k + 1 < len(g) else ge
            txt = ' '.join(('{\\c&H00E5FF&}' if j == k else '{\\c&HFFFFFF&}') + ww.upper().replace('{', '').replace('}', '') for j, (_, _, ww) in enumerate(g))
            ev.append('Dialogue: 0,%s,%s,Caps,,0,0,0,,%s' % (T(s), T(max(e2, s + 0.05)), txt))
    if meta.get('hook'): ev.append('Dialogue: 1,%s,%s,Hook,,0,0,0,,%s' % (T(0), T(meta['hook'][1]), meta['hook'][0].replace('\n', '\\N')))
    for src, title in meta.get('chapters', []):
        t = f(src)
        if t is not None: ev.append('Dialogue: 1,%s,%s,Chapter,,0,0,0,,%s' % (T(t), T(t + 2.4), title.upper()))
    hdr = ('[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n[V4+ Styles]\n'
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
           'Style: Caps,Impact,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,7,3,2,80,80,170,1\n'
           'Style: Hook,Impact,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,8,4,5,120,120,60,1\n'
           'Style: Chapter,Impact,64,&H0000E5FF,&H00FFFFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,2,0,3,10,0,8,80,80,70,1\n\n[Events]\n'
           'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
    open(os.path.join(W, 'captions.ass'), 'w').write(hdr + '\n'.join(ev) + '\n')

def burn(meta):
    out = meta.get('out', os.path.join(W, 'final.mp4'))
    run([FF, '-v', 'error', '-y', '-i', os.path.join(W, 'cut.mp4'), '-vf', 'ass=%s:fontsdir=%s' % (os.path.join(W, 'captions.ass'), FONTS)] + ENC[:2] + ['-b:v', '14M', '-c:a', 'copy', '-movflags', '+faststart', out])
    print('final ->', out)

if __name__ == '__main__':
    ws, wav = transcribe(); rg = plan(ws, silences(wav))
    src = float(subprocess.check_output([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', RAW]))
    kept = sum(b - a for a, b in rg); print('words %d | cuts %d | kept %.1f of %.1f min (%.0f%% removed)' % (len(ws), len(rg), kept / 60, (PREVIEW or src) / 60, 100 * (1 - kept / (PREVIEW or src))))
    mp = os.path.join(os.path.dirname(RAW), 'edit_meta.json'); meta = json.load(open(mp)) if os.path.exists(mp) else {}
    if STEP == 'all': cut(rg); captions(ws, rg, meta); burn(meta)
