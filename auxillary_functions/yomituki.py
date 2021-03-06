# coding: utf-8

import itertools

import bs4
from janome.tokenizer import Tokenizer
from pykakasi import kakasi

to = Tokenizer()
kakasi = kakasi()
kakasi.setMode("K", "H")
conv = kakasi.getConverter()

def is_kana(character):
    if 12353 <= ord(character) <= 12542:
        return True
    return False

def hantei(word):
    org = word.surface
    kata = word.reading
    if org == kata or kata == '*':
        return (org,), False, None
    hira = conv.do(word.reading)
    if org == hira:
        return (org,), False, None
    else:
        return org, True, hira

def cut_end(org, hira):
    if org[-1] != hira[-1]:
        return (org, hira),
    for i in range(1, len(org)):
        if org[-i - 1] != hira[-i - 1]:
            return (org[:-i], hira[:-i]), hira[-i:]
    return org,


def yomituki(sentence):
    return (cut_end(source, yomi) if ruby else source for source, ruby, yomi in map(hantei, to.tokenize(sentence)))


def ruby_wrap(org, yomi):
    return '<ruby><rb>{}</rb><rp>（</rp><rt>{}</rt><rp>）</rp></ruby>'.format(org, yomi)


def ruby_text(text):
    yomi = yomituki(text)
    plain = ''
    for i in itertools.chain.from_iterable(yomi):
        if isinstance(i, str):
            plain += i
        else:
            plain += ruby_wrap(*i)
    return plain


def ruby_p(p):
    plain = '<p>'
    for i in p:
        if isinstance(i, bs4.element.NavigableString):
            plain += ruby_text(str(i))
        elif isinstance(i, bs4.element.Tag):
            plain += str(i)
    plain += '</p>'
    return plain

def ruby_div(div):
    plain = '<div>'
    for i in div:
        if isinstance(i, bs4.element.NavigableString):
            if i.strip():
                plain += ruby_text(str(i))
        elif isinstance(i, bs4.element.Tag):
            plain += ruby_p(i)
    plain += '</div>'
    return plain
