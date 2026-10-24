"""Render the course notebooks as tutorial web pages for the site.

  concepts/NN-name/notebook.ipynb      ->  concepts/NN-name/notebook.html
  reference/reading-maths-symbols.ipynb ->  reference/reading-maths-symbols.html

Run after adding or editing a notebook:   python tools/build_tutorials.py
Needs:  pip install nbconvert
"""
import glob, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(REPO, "quantum-foundations")
GH = "https://github.com/Sathisha/quantum-learning-lab/blob/main/quantum-foundations/"

BAR = """<nav style="font:14px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif;background:#f5f7fb;border-bottom:1px solid #d3dae4;
padding:9px max(16px,env(safe-area-inset-left,0px));display:flex;flex-wrap:wrap;gap:4px 18px;justify-content:space-between">
<span><a href="{home}" style="color:#1d5bbd">Home</a> · <a href="{page}" style="color:#1d5bbd">{label}</a></span>
<span style="color:#566275">Tutorial notebook · <a href="{ipynb}" style="color:#1d5bbd">download .ipynb</a></span></nav>"""

def fix_links(html, in_concept):
    up = "../../reference/" if in_concept else ""
    html = html.replace(f'href="{up}reading-maths-symbols.ipynb"', f'href="{up}reading-maths-symbols.html"')
    html = re.sub(r'href="(?:\.\./\.\./reference/)?prep-plan\.md"', f'href="{GH}reference/prep-plan.md"', html)
    return html

def build(nb, in_concept):
    out = nb[:-len(".ipynb")] + ".html"
    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "html", "--template", "lab",
                    "--log-level", "WARN", "--output", os.path.basename(out), nb], check=True)
    html = fix_links(open(out, encoding="utf-8").read(), in_concept)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    name = re.sub(r"<[^>]+>|¶", "", h1.group(1)).strip() if h1 else "Tutorial"
    html = re.sub(r"<title>.*?</title>", f"<title>{name}: tutorial</title>", html, count=1, flags=re.S)
    html = html.replace('<img alt="No description has been provided for this image"', '<img alt="Plot produced by the cell above"')
    if in_concept:
        bar = BAR.format(home="../../../", page="./", label="Back to the concept page", ipynb=os.path.basename(nb))
    else:
        bar = BAR.format(home="../../", page="../../", label="All concepts", ipynb=os.path.basename(nb))
    html = re.sub(r"(<body[^>]*>)", r"\1" + bar.replace("\\", "\\\\"), html, count=1)
    open(out, "w", encoding="utf-8").write(html)
    print("built", os.path.relpath(out, REPO))

for nb in sorted(glob.glob(os.path.join(COURSE, "concepts", "*", "notebook.ipynb"))):
    build(nb, True)
build(os.path.join(COURSE, "reference", "reading-maths-symbols.ipynb"), False)
