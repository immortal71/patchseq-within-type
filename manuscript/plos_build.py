"""Build the PLOS Computational Biology version of the manuscript.

Numbered Vancouver references, author summary after the abstract, figure and
table captions after the paragraph that first cites them, italic gene names,
double spacing, continuous line numbers, page numbers. Output: plos/ folder.
"""
import os, re, subprocess, shutil, zipfile
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
OUT = os.path.join(HERE, "plos")
os.makedirs(OUT, exist_ok=True)

REFS = {
    "Cadwell et al. 2016": "Cadwell CR, Palasantza A, Jiang X, Berens P, Deng Q, Yilmaz M, et al. Electrophysiological, transcriptomic and morphologic profiling of single neurons using Patch-seq. Nat Biotechnol. 2016;34(2):199-203. doi:10.1038/nbt.3445",
    "Fuzik et al. 2016": "Fuzik J, Zeisel A, Máté Z, Calvigioni D, Yanagawa Y, Szabó G, et al. Integration of electrophysiological recordings with single-cell RNA-seq data identifies neuronal subtypes. Nat Biotechnol. 2016;34(2):175-83. doi:10.1038/nbt.3443",
    "Lipovsek et al. 2021": "Lipovsek M, Bardy C, Cadwell CR, Hadley K, Kobak D, Tripathy SJ. Patch-seq: past, present, and future. J Neurosci. 2021;41(5):937-46. doi:10.1523/JNEUROSCI.1653-20.2020",
    "Tripathy et al. 2017": "Tripathy SJ, Toker L, Li B, Crichlow CL, Tebaykin D, Mancarci BO, et al. Transcriptomic correlates of neuron electrophysiological diversity. PLoS Comput Biol. 2017;13(10):e1005814. doi:10.1371/journal.pcbi.1005814",
    "Gouwens et al. 2020": "Gouwens NW, Sorensen SA, Baftizadeh F, Budzillo A, Lee BR, Jarsky T, et al. Integrated morphoelectric and transcriptomic classification of cortical GABAergic cells. Cell. 2020;183(4):935-53.e19. doi:10.1016/j.cell.2020.09.057",
    "Bernaerts et al. 2025": "Bernaerts Y, Deistler M, Gonçalves PJ, Beck J, Stimberg M, Scala F, et al. Combined statistical-biophysical modeling links ion channel genes to physiology of cortical neuron types. Patterns (N Y). 2025;6(10):101323. doi:10.1016/j.patter.2025.101323",
    "Huang et al. 2025": "Huang W, Xu Q, Liu S. Linking ion channel gene expression to neuronal firing patterns through a statistical-biophysical model. Patterns (N Y). 2025;6(10):101390. doi:10.1016/j.patter.2025.101390",
    "Schulz et al. 2006": "Schulz DJ, Goaillard JM, Marder E. Variable channel expression in identified single and electrically coupled neurons in different animals. Nat Neurosci. 2006;9(3):356-62. doi:10.1038/nn1639",
    "Prinz et al. 2004": "Prinz AA, Bucher D, Marder E. Similar network activity from disparate circuit parameters. Nat Neurosci. 2004;7(12):1345-52. doi:10.1038/nn1352",
    "Marder & Goaillard 2006": "Marder E, Goaillard JM. Variability, compensation and homeostasis in neuron and network function. Nat Rev Neurosci. 2006;7(7):563-74. doi:10.1038/nrn1949",
    "Goaillard & Marder 2021": "Goaillard JM, Marder E. Ion channel degeneracy, variability, and covariation in neuron and circuit resilience. Annu Rev Neurosci. 2021;44:335-57. doi:10.1146/annurev-neuro-092920-121538",
    "Scala et al. 2021": "Scala F, Kobak D, Bernabucci M, Bernaerts Y, Cadwell CR, Castro JR, et al. Phenotypic variation of transcriptomic cell types in mouse motor cortex. Nature. 2021;598(7879):144-50. doi:10.1038/s41586-020-2907-3",
    "Bomkamp et al. 2019": "Bomkamp C, Tripathy SJ, Bengtsson Gonzales C, Hjerling-Leffler J, Craig AM, Pavlidis P. Transcriptomic correlates of electrophysiological and morphological diversity within and across excitatory and inhibitory neuron classes. PLoS Comput Biol. 2019;15(6):e1007113. doi:10.1371/journal.pcbi.1007113",
    "Kobak et al. 2021": "Kobak D, Bernaerts Y, Weis MA, Scala F, Tolias AS, Berens P. Sparse reduced-rank regression for exploratory visualisation of paired multivariate data. J R Stat Soc Ser C Appl Stat. 2021;70(4):980-1000. doi:10.1111/rssc.12494",
    "Reva et al. 2025": "Reva M, Arnaudon A, Zbili M, Makkeh A, Markram H, Goaillard JM, et al. Higher-order interactions in neuronal function: from genes to ionic currents in biophysical models. Proc Natl Acad Sci U S A. 2025;122(40):e2500048122. doi:10.1073/pnas.2500048122",
    "Benjamini & Hochberg 1995": "Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57(1):289-300. doi:10.1111/j.2517-6161.1995.tb02031.x",
}
KEYRE = "|".join(re.escape(k).replace(r"\ (?=\d)", " ") for k in REFS)
NAMES = {k: k.rsplit(" ", 1)[0] for k in REFS}
YEARS = {k: k.rsplit(" ", 1)[1] for k in REFS}

def read(p):
    return open(p, encoding="utf-8").read().strip()

front = read("front.md")
title = front.splitlines()[0].lstrip("# ").strip()
abstract = front.split("## Abstract")[1].split("Keywords:")[0].strip()
summary = read("author_summary.md").split("## Author summary")[1].split("\n\n", 1)[1].split("\n## ")[0].strip()

body = "\n\n".join(read(p + ".md") for p in ["intro", "results", "discussion", "methods"])
table = read("table1.md")
back = read("back.md")
ack = back.split("## Acknowledgements")[1].split("\n## ")[0].strip()
legends = {}
for m in re.finditer(r"\*\*Figure (\d)\. (.+?)\*\* (.+)", back):
    legends[int(m.group(1))] = (m.group(2), m.group(3))

# ---- citations to numbers, in order of first appearance ----
order = []
def num(k):
    if k not in order:
        order.append(k)
    return order.index(k) + 1

def fmt(nums):
    nums = sorted(set(nums))
    return "[" + ",".join(str(n) for n in nums) + "]"

def convert(text):
    # parenthetical groups: (A et al. 2016; B & C 2006)
    def paren(m):
        inner = m.group(1)
        parts = [p.strip() for p in inner.split(";")]
        if all(p in REFS for p in parts):
            return fmt([num(p) for p in parts])
        return m.group(0)
    text = re.sub(r"\(([^()]*?\d{4}[^()]*?)\)", paren, text)
    # narrative: Name et al. (2025)
    for k in REFS:
        n, y = NAMES[k], YEARS[k]
        text = re.sub(re.escape(n) + r" \(" + y + r"\)", lambda m, k=k: f"{NAMES[k]} {fmt([num(k)])}", text)
    # inside other parentheses: "(..., Kobak et al. 2021)" or "(Scala et al. 2021)" leftovers
    for k in REFS:
        text = re.sub(re.escape(k) + r"(?![\d])", lambda m, k=k: fmt([num(k)]), text)
    return text

# fix numbering order by first appearance in the reading order before converting
_full = body + "\n\n" + table + "\n\n" + "\n\n".join(t + " " + l for t, l in legends.values())
_pos = {}
for k in REFS:
    n, y = NAMES[k], YEARS[k]
    m = re.search(re.escape(n) + r" \(?" + y, _full)
    _pos[k] = m.start() if m else 10**9
for k in sorted(REFS, key=lambda k: _pos[k]):
    num(k)
body = convert(body)
table = convert(table)
legends = {i: (convert(t), convert(l)) for i, (t, l) in legends.items()}
ack = convert(ack)
missing = [k for k in REFS if k not in order]
assert not missing, missing
assert not re.search(r"et al\. \d{4}|et al\. \(\d{4}\)|& [A-Z][a-z]+ \d{4}", body), "unconverted citation"

# ---- figure and table labels ----
def figlabels(t):
    t = re.sub(r"Figure (\d)([a-d])\b", lambda m: f"Fig {m.group(1)}{m.group(2).upper()}", t)
    t = re.sub(r"Figure (\d)", r"Fig \1", t)
    return t
body = figlabels(body)
legends = {i: (tt, re.sub(r"\(([a-d])\)", lambda m: f"({m.group(1).upper()})", figlabels(l))) for i, (tt, l) in legends.items()}

# ---- place captions after the paragraph that first cites them ----
paras = body.split("\n\n")
placed = set()
out = []
tab_title, tab_rest = table.split("**", 2)[1], table.split("**", 2)[2]
tab_legend, tab_md = tab_rest.split("\n\n", 1)
for p in paras:
    out.append(p)
    for i in range(1, 6):
        if i not in placed and re.search(rf"Fig {i}[A-D]?\b", p) and not p.startswith("#"):
            t, l = legends[i]
            out.append(f"**Fig {i}. {t}** {l}")
            placed.add(i)
    if "T1" not in placed and "Table 1" in p and not p.startswith("#"):
        out.append(f"**{tab_title.strip()}**\n\n{tab_md.strip()}\n\n{tab_legend.strip()}")
        placed.add("T1")
assert placed == {1, 2, 3, 4, 5, "T1"}, placed
body = "\n\n".join(out)

# ---- italic mouse gene symbols ----
GENE = r"(?<![\w*/.])(Hcn[1-4]|Pvalb|Lamp5|Vip|Sst)(?![\w*])"
body = re.sub(GENE, r"*\1*", body)
summary_i = summary
body = body.replace("Mouse primary motor cortex Patch-seq data", "Mouse (*Mus musculus*) primary motor cortex Patch-seq data")

refs = "\n\n".join(f"{i+1}. {REFS[k]}" for i, k in enumerate(order))
short = "Channel expression and within-type neuronal electrophysiology"
assert len(short) <= 70 and len(title) <= 200
assert len(abstract.split()) <= 300
sw = len(summary.split())
assert 150 <= sw <= 200, sw

md = f"""# {title}

Short title: {short}

Aashish Kharel^1\\*^

^1^ Independent researcher, Kathmandu, Nepal

\\* Corresponding author: aashishkharel7@gmail.com

## Abstract

{abstract}

## Author summary

{summary}

{body}

## Acknowledgments

{ack}

## References

{refs}
"""
md = md.replace("## Introduction", "## Introduction", 1)
open(os.path.join(OUT, "plos_manuscript.md"), "w", encoding="utf-8").write(md)

bad = re.findall(r"[\u2012-\u2015\u200b-\u200f\u202a-\u202e\u2060\ufeff\u00a0]", md)
assert not bad, set(bad)

# ---- docx via pandoc, reusing the black reference doc ----
ref = "reference.docx"
subprocess.run(["python3", "build.py", "black"], check=True, capture_output=True)
docx_path = os.path.join(OUT, "Kharel_PLOSCB_manuscript.docx")
subprocess.run(["pandoc", os.path.join(OUT, "plos_manuscript.md"), "-o", docx_path,
                "--reference-doc", ref], check=True)

d = Document(docx_path)
for p in d.paragraphs:
    p.paragraph_format.line_spacing = 2.0
    for r in p.runs:
        r.font.color.rgb = RGBColor(0, 0, 0)
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                for r in p.runs:
                    r.font.size = Pt(8)
                    r.font.color.rgb = RGBColor(0, 0, 0)
for s in d.sections:
    s.left_margin = s.right_margin = Cm(2.5)
    s.top_margin = s.bottom_margin = Cm(2.5)
    sp = s._sectPr
    ln = OxmlElement("w:lnNumType")
    ln.set(qn("w:countBy"), "1")
    ln.set(qn("w:restart"), "continuous")
    ln.set(qn("w:distance"), "360")
    sp.append(ln)
    # page number in footer
    fp = s.footer.paragraphs[0]
    fp.alignment = 1
    run = fp.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind); run._r.append(el)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = txt; run._r.append(el)
cp = d.core_properties
cp.author = cp.last_modified_by = "Aashish Kharel"
cp.title = title
cp.comments = cp.keywords = cp.subject = ""
d.save(docx_path)

# strip generator name in app.xml
tmp = docx_path + ".tmp"
with zipfile.ZipFile(docx_path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in ("word/styles.xml", "word/document.xml"):
            s = data.decode("utf-8")
            s = re.sub(r'<w:rFonts [^>]*/>', '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/>', s)
            s = re.sub(r'w:color w:val="[0-9A-Fa-f]{6}"', 'w:color w:val="000000"', s)
            data = s.encode("utf-8")
        if item.filename == "docProps/app.xml":
            data = re.sub(rb"<Application>.*?</Application>", b"<Application>Microsoft Office Word</Application>", data)
        zout.writestr(item, data)
shutil.move(tmp, docx_path)

subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, docx_path],
               check=True, capture_output=True)

# figures as TIFF named Fig1.tif ... for revision stage
from PIL import Image
for i, f in enumerate(["fig1_raw_vs_within", "fig2_calibration", "fig3_hh_parameters",
                       "fig4_partitions", "fig5_hcn"], 1):
    im = Image.open(f"../figures/{f}.png").convert("RGB")
    im.save(os.path.join(OUT, f"Fig{i}.tif"), compression="tiff_lzw", dpi=(300, 300))
print("refs in order:", [k for k in order])
print("summary words", sw, "abstract words", len(abstract.split()))
