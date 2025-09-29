#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys, argparse
from collections import Counter

STOPWORDS = set("病 人 患 者 今日 今晚 今早".split())

def sent_split(text):
    parts = re.split(r'(?<=[。！？；;.!?])\s*', text.strip())
    return [s.strip() for s in parts if s.strip()]

def tokenize(text):
    return re.findall(r'[A-Za-z]+|\d+|[\u4e00-\u9fff]', text.lower())

def summarize(text, top_k=3):
    sents = sent_split(text)
    words = [w for s in sents for w in tokenize(s) if w not in STOPWORDS]
    freqs = Counter(words)
    scores = {i: sum(freqs.get(w,0) for w in tokenize(s)) for i,s in enumerate(sents)}
    top_idx = sorted(sorted(scores, key=scores.get, reverse=True)[:top_k])
    return [sents[i] for i in top_idx]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=str)
    ap.add_argument("--top_k", type=int, default=3)
    args = ap.parse_args()
    text = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    for i, s in enumerate(summarize(text, args.top_k), 1):
        print(f"{i}) {s}")
