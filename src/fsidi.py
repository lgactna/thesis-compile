from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent, indent

import re
import subprocess
import shutil

# absolute path to the markdown files to copy here
SOURCE_MD_DIR = Path(
    "C:/Users/Kisun/Desktop/Obsidian/Academic research/30 - Research topics/39 - By chapter"
)
SOURCE_ASSET_DIR = SOURCE_MD_DIR / "Assets"

# absolute path to the directory where the markdown files will be copied
TARGET_MD_DIR = Path("./md")
# absolute path to the directory where stuff to include like images should go
TARGET_ASSET_DIR = Path("./assets")

TARGET_TEX_DIR = Path("./tex")

def process_md_file(md_file: Path):
    """
    Pre-process a markdown file.
    
    Unlike main.py, you are responsible for the following:
    - Ensuring bulleted/numbered lists have sufficient line breaks
    - Ensuring section headings have sufficient line breaks
    - Manually linking URLs
    """
    # Read the file
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Remove all blockquotes
    text = re.sub(r"^>.*", "", text, flags=re.MULTILINE)
    
    # Ensure that bulleted lists have two line breaks before
    text = re.sub(r"(.)\n{1,2}((- .*$\n)+)", r"\1\n\n\2", text, flags=re.MULTILINE)

    # Ensure that numbered lists have two line breaks before
    text = re.sub(r"(.)\n{1,2}((\d\. .*$\n)+)", r"\1\n\n\2", text, flags=re.MULTILINE)

    # Ensure that section headings have two line breaks before and after, but only if the
    # following line starts with a capital letter (which should avoid Python code).
    text = re.sub(
        r"(.)\n{1,2}(#+ .*$\n{1,2})(?=[A-Z])\n{0,}(.)", r"\1\n\n\2\n\n\3", text, flags=re.MULTILINE
    )
    
    # Convert wikilinks to bolded text
    text = re.sub(r"\[\[(.*?)\]\]", r"**\1**", text, flags=re.MULTILINE)
    
    # Remove excess line breaks (two or more in a row, flags=re.MULTILINE)
    text = re.sub(r"\n{2,}", r"\n\n", text)
    
    # Automatically identify valid URLs (http/https) and convert them to
    # Markdown hyperlinks, with the URL as the link text.
    # text = re.sub(r"(https?://\S+)", r"[\1](\1)", text)
    

    # Write the file
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(text)

@dataclass
class TableMeta:
    """
    Process the complex `longtable` environments generated from Pandoc and convert
    them into significantly simpler tables, consistent with the FSIDI style.
    """
    
    label: str
    caption: str
    alignments: list[str]
    
    @classmethod
    def from_match(cls, match: re.Match):
        label = match[0].replace("\n", " ").strip()
        caption = match[1].replace("\n", " ").strip()
        alignments = [v.strip() for v in match[2].split(",")]
        return cls(label, caption, alignments)
    
    def process_table(self, table_text: str) -> str:
        """
        Convert a Pandoc-generated table into a nicer-looking table with the provided
        parameters.
        """
        
        # Extract headers
        column_names = re.findall(
            r"\\begin{minipage}.*?\\raggedright\n(.*?)\n\\end{minipage}",
            table_text,
            flags=re.DOTALL | re.MULTILINE,
        )
        
        # Create header row
        header_row = " & ".join([f"\\textbf{{{name.strip()}}}" for name in column_names])
        
        
        # Extract data
        data = re.search(
            r"\\endlastfoot\n(.*?)\\end{longtable}",
            table_text,
            flags=re.DOTALL | re.MULTILINE,
        ).group(1)
        
        alignments = " ".join([f"L{{{alignment}}}" for alignment in self.alignments])
        
        template = dedent(
            f"""
            \\begin{{table*}}[tb]
            \\footnotesize
            \\centering
            \\begin{{tabularx}}{{\\linewidth}}{{{alignments}}}
            \\toprule
            <substitute_header> \\\\
            \\midrule
            <substitute_content> \\\\
            \\bottomrule
            \\end{{tabularx}}
            \caption{{{self.caption}}}\label{{{self.label}}}
            \\end{{table*}}
            """
        )
        
        # Substitute the alignments and content
        template = template.replace("<substitute_header>", indent(header_row, "  "))
        template = template.replace("<substitute_content>", indent(data.strip("\n"), "  "))
        
        return template

def substitute_labels(tex_file: Path) -> dict:
    """
    Find all label tags in the tex files in the given directory,
    then substitute any tags currently inside `\textbf{}` with matching
    label text and convert it to its corresponding `\ref{}` tag, using
    the label.

    The result is a dictionary of the text being labeled to the label
    itself (for example, "\section{1.2.3 - Title}\label{title}" becomes
    {"1.2.3 - Title": "title}).
    """

    # Hardcoded labels that are not in the tex files
    label_table = {
    }

    text = tex_file.read_text()
    # Forbid the right brace from being part of anything - this is how we'll know
    # if we're not actually next to a label, if there's another brace
    # in between us and the next label tag
    labels = re.findall(
        r"^\\\w+?\{([^\{\}]*?)\}\\label\{(.*?)\}$",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )

    label_table.update(
        {k.replace("\n", " "): v.replace("\n", " ") for k, v in labels}
    )

    print(label_table)

    # With all labels collected, go through the tex files again.
    # Search for any `\textbf{label}`, and check if any of the keys in
    # label_table contain the label. If they do, replace the `\textbf{label}`
    # with a `\ref{}` tag containing the corresponding value in label_table.
    
    text = tex_file.read_text()
    # search for all textbfs. if there's a \# inside the textbf,
    # ignore everything before the \#
    textbfs = re.findall(r"\\textbf\{(.*?)\}", text, flags=re.DOTALL | re.MULTILINE)
    textbfs = [textbf.split("#")[-1] for textbf in textbfs]
    textbfs = [textbf.replace("\n", " ") for textbf in textbfs]
    print(tex_file, textbfs)

    # for each textbf, check if it's in the label table
    for textbf in textbfs:
        if textbf in label_table:
            textbf2 = textbf.replace(" ", "[ \\n]")
            print(
                rf"Replacing \\textbf\{{[^\{{\}}]*?{textbf2}\}} with \\autoref{{{label_table[textbf]}}}"
            )

            # if it is, replace it with a ref. note that every space in the textbf
            # might actually be a newline here, so we have to convert every space
            # into a regex charset that could be either a space or a newline

            text = re.sub(
                rf"\\textbf\{{[^\{{\}}]*?{textbf2}\}}",
                rf"\\autoref{{{label_table[textbf]}}}",
                text,
                flags=re.DOTALL | re.MULTILINE,
            )

    # The extra-special one because it's inside a bullet point and I can't
    # figure out how to get it out of the textbf
    text = re.sub(
        r"\\textbf{39.5 - Output and validation\\#5.3 - Human readable\n  reporting}",
        r"\\autoref{human-readable-reporting}",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )

    # Final pass - remove anything that looks like "1.2.3 -" inside any
    # tags, because it's already handled by the engine.
    text = re.sub(
        r"section\{(?:\d\.)+\d - ",
        r"section{",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )

    tex_file.write_text(text)

def process_tex_file(tex_file: Path):
    """
    Pre-process a tex file.
    """
    
    # Substitute all labels
    substitute_labels(tex_file)
    
    with open(tex_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Convert \autocite to \citep (cite with parentheses)
    text = re.sub(r"\\autocite", r"\\citep", text)
    
    # Tightlists aren't real
    # If they are, you have to do this:
    """
    \providecommand{\tightlist}{%
        \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
    """
    text = re.sub(r"\\tightlist\n", r"", text)
    
    # Special syntax: if an lstlisting's first line contains a line of the form
    # !lst:caption|label, convert it to a lstlisting with a caption and label
    text = re.sub(
        r"\\begin\{lstlisting\}(?:\[(.*?)\])?\n!(.*?)\|(.*?)\n",
        r"\\begin{lstlisting}[label={\2}, caption={\3}, \1]\n",
        text,
    )

    # Search for the special syntax \textbf{!(.*?)} and replace it with
    # \autoref{\1}
    text = re.sub(r"\\textbf\{!(.*?)\}", r"\\autoref{\1}", text)

    # Citations in code blocks sometimes just don't work, so manually extract
    # any [@citekey] and replace them with \cite{citkey}
    text = re.sub(r"\[@(.*?)\]", r"\\cite{\1}", text)

    # Convert \begin{figure} to \begin{figure}[h]
    text = re.sub(r"^\\begin\{figure\}$", r"\\begin{figure}[htbp]", text, flags=re.MULTILINE)
    
    # A \pandocbounded{\includegraphics[...]{...}} command should be substtituted
    # with \includegraphics[width=1\linewidth]{...}
    text = re.sub(
        r"\\pandocbounded\{\\includegraphics\[(.*?)\]\{(.*?)\}\}",
        r"\\includegraphics[width=1\\linewidth]{\2}",
        text,
    )
    
    # All figures are figure* environments    
    # text = re.sub(r"\\begin\{figure\}", r"\\begin{figure*}", text)
    # text = re.sub(r"\\end\{figure\}", r"\\end{figure*}", text)
    
    # Convert the first two figures to figure* environments (the rest are figure)
    text = re.sub(r"\\begin\{figure\}", r"\\begin{figure*}", text, count=2)
    text = re.sub(r"\\end\{figure\}", r"\\end{figure*}", text, count=2)
    
    # Special syntax for tables.
    # Start by finding all meta declarations for tables
    meta_matches = re.findall(
        r"\\emph\{!([^\\]+?)\\textbar\s*([^\\]+?)\\textbar\s*([^}]+?)\}",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    table_metas = [TableMeta.from_match(match) for match in meta_matches]
    
    # Also remove the meta declarations from the text
    text = re.sub(
        r"\\emph\{![^\\]+?\\textbar\s*[^\\]+?\\textbar\s*[^}]+?\}\n\n",
        "",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )

    table_matches = re.findall(
        r"(\\begin\{longtable\}.*?\\end\{longtable\})",
        text,
        flags=re.DOTALL | re.MULTILINE
    )

    if len(table_matches) == len(table_metas):    
        # Substitute table matches with the corresponding index in table_metas
        for i, match in enumerate(table_matches):
            table_meta = table_metas[i]
            table_text = table_meta.process_table(match)
            text = text.replace(match, table_text)
            
    else:
        print("Table count and meta count do not match, won't perform substitutions")
        print(f"Table count: {len(table_matches)}")
        print(f"Meta count: {len(table_metas)}")
        
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(text)

def substitute_into_base(base_file: Path, input_file: Path, output_file: Path):
    """
    Substitute the input file into the base file, and write the result to the output file.
    """
    
    # Read the base file
    with open(base_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Read the input file
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()
    
    # Extract the abstract from the input file, and discard everything else
    match = re.search(r".*\\label{abstract}(.*?)\\section", input_text, flags=re.DOTALL | re.MULTILINE)
    if match is None:
        raise ValueError("No abstract found in input file")
    abstract = match.group(1)
    input_text = re.sub(r".*\\label{abstract}.*?\\section", r"\\section", input_text, flags=re.DOTALL | re.MULTILINE)
    
    # Substitute the abstract into the base file
    text = text.replace("{{substitute_abstract}}", abstract.strip())
    
    # Substitute the remaining input file into the base file
    text = text.replace("{{substitute_content}}", input_text.strip())
    
    # Write the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    
    target_md = TARGET_MD_DIR / "_FSIDI submission.md"
    target_tex = TARGET_TEX_DIR / "_FSIDI submission.tex"
    
    # Copy assets
    shutil.copy(SOURCE_MD_DIR / "_FSIDI submission.md", target_md)
    # Also copy everything to the asset directory
    TARGET_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for asset_file in SOURCE_ASSET_DIR.glob("*"):
        shutil.copy(asset_file, TARGET_ASSET_DIR / asset_file.name)
    
    # Preprocess the markdown file
    process_md_file(target_md)
    
    # Initial pass
    subprocess.run([
        "pandoc",
        str(target_md),
        "-f",
        "markdown",
        "-o",
        str(target_tex),
        "-t",
        "latex",
        "--csl",
        "http://www.zotero.org/styles/ieee",
        "--bibliography=thesis_bib.bib",
        "--pdf-engine=pdflatex",
        "--filter",
        "pandoc-crossref",
        "--number-sections",
        "--citeproc",
        "--verbose",
        "--biblatex",
        "--listings",
        "--resource-path=.:./assets"
    ])
    
    process_tex_file(target_tex)
    
    substitute_into_base(
        Path("fsidi_base.tex"),
        target_tex,
        Path("fsidi.tex")
    )
    