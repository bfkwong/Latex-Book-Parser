import sys
import re
import json
import urllib
import os
import base64
import requests
import mistletoe
import pandas as pd
from mistletoe.latex_renderer import LaTeXRenderer

graphicsRE = r'(?P<pre>[\s\S]*)\\includegraphics{(?P<pngSrc>[\s\S]*?)}(?P<post>[\s\S]*)'
def parseIncludeGraphics(string):
    global OUTPUT_IMG_CNT
    res = re.search(graphicsRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseIncludeGraphics(res["pre"])
    postRE = parseIncludeGraphics(res["post"])

    if res["pngSrc"][0:4] == "http":
        urllib.request.urlretrieve(res["pngSrc"], "./LatexBook/image/" + str(OUTPUT_IMG_CNT) + ".png")
        body = "\\begin{figure}[h!]\\centering\\includegraphics[width=0.45\\paperwidth]{%s}\\end{figure}\n" % ("image/" + str(OUTPUT_IMG_CNT) + ".png")
        OUTPUT_IMG_CNT += 1
    else:
        with open(OPERATING_PATH + res["pngSrc"], "rb") as f:
            with open("./LatexBook/image/" + res["pngSrc"] + ".png", "wb") as f2:
                f2.write(f.read())
        body = "\\begin{figure}[h!]\\centering\\includegraphics[width=0.45\\paperwidth]{%s}\\end{figure}\n" % ("image/" + res["pngSrc"] + ".png")

    return preRE + body + postRE

sectionRE = r'(?P<pre>[\s\S]*)\\section{(?P<title>[\s\S]*?)}(?P<post>[\s\S]*)'
def parseSection(string):
    global OUTPUT_IMG_CNT
    res = re.search(sectionRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseSection(res["pre"])
    postRE = parseSection(res["post"])

    titleSplit = res["title"].split(" ")
    chLabel = titleSplit[0]
    chTag = " ".join(titleSplit[1:])
    body = "\\chapter{%s}\\label{%s}" % (chTag, chLabel)

    return preRE + body + postRE

subsectionRE = r'(?P<pre>[\s\S]*)\\subsection{(?P<title>[\s\S]*?)}(?P<post>[\s\S]*)'
def parseSubSection(string):
    global OUTPUT_IMG_CNT
    res = re.search(subsectionRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseSubSection(res["pre"])
    postRE = parseSubSection(res["post"])

    titleSplit = res["title"].split(" ")
    secLabel = titleSplit[0]
    secTag = " ".join(titleSplit[1:])
    body = "\\section{%s}\\label{%s}" % (secTag, secLabel)

    return preRE + body + postRE

subsubsectionRE = r'(?P<pre>[\s\S]*)\\subsubsection{(?P<title>[\s\S]*?)}(?P<post>[\s\S]*)'
def parseSubSubSection(string):
    global OUTPUT_IMG_CNT
    res = re.search(subsubsectionRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseSubSubSection(res["pre"])
    postRE = parseSubSubSection(res["post"])

    titleSplit = res["title"].split(" ")
    subsecLabel = titleSplit[0]
    subsecTag = " ".join(titleSplit[1:])
    body = "\\subsection{%s}\\label{%s}" % (subsecTag, subsecLabel)

    return preRE + body + postRE

quotationRE = r'(?P<pre>[\s\S]*)\\begin{displayquote}\n(?P<title>[\s\S]*?)\\end{displayquote}(?P<post>[\s\S]*)'
def parseQuotation(string):
    res = re.search(quotationRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseQuotation(res["pre"])
    postRE = parseQuotation(res["post"])
    body = "\\begin{displayquote}" + res["title"] + "\\end{displayquote}"

    return preRE + body + postRE

mathJaxAlignRE = r'(?P<pre>[\s\S]*)\$\$ *\n* *\\begin{align}(?P<title>[\s\S]*?) *\n* *\\end{align}\$\$(?P<post>[\s\S]*)'
def parseMathJaxTags(string):
    res = re.search(mathJaxAlignRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseMathJaxTags(res["pre"])
    postRE = parseMathJaxTags(res["post"])
    body = "\\begin{align}" + res["title"] + "\\end{align}"

    return preRE + body + postRE

tagRE = r'(?P<pre>[\s\S]*)\\tag{[\s\S]*?}(?P<post>[\s\S]*)'
def parseRemoveTag(string):
    res = re.search(tagRE, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseRemoveTag(res["pre"])
    postRE = parseRemoveTag(res["post"])

    return preRE + postRE

hrefTags = r'(?P<pre>[\s\S]*)\\href{(?P<link>[\s\S]*?)}{(?P<text>[\s\S]*?)}(?P<post>[\s\S]*)'
def parseFootNoteTag(string):
    res = re.search(hrefTags, string)

    if res == None:
        return string

    res = res.groupdict()

    preRE = parseFootNoteTag(res["pre"])
    postRE = parseFootNoteTag(res["post"])
    body = res["text"] + "\\footnote{" + res["link"] + "}"

    return preRE + body + postRE


def postParser(string):
    parsed = parseIncludeGraphics(string)
    parsed = parseSection(parsed)
    parsed = parseSubSection(parsed)
    parsed = parseSubSubSection(parsed)
    parsed = parseQuotation(parsed)
    parsed = parseMathJaxTags(parsed)
    parsed = parseRemoveTag(parsed)
    parsed = parseFootNoteTag(parsed)
    return parsed