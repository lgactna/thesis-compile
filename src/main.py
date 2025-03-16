import concurrent.futures
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

# Check if platform is windows
CODESPACE = False
if os.name != "nt":
    CODESPACE = True

# absolute path to the markdown files to copy here
SOURCE_MD_DIR = Path(
    "C:/Users/Kisun/Desktop/Obsidian/Academic research/30 - Research topics/39 - By chapter"
)
SOURCE_ASSET_DIR = SOURCE_MD_DIR / "Assets"

# absolute path to the bibliography
BIBLIOGRAPHY_PATH = Path("./thesis_bib.bib")

# absolute path to the directory where the markdown files will be copied
TARGET_MD_DIR = Path("./md")
# absolute path to the directory where the generated tex files should go
TARGET_TEX_DIR = Path("./tex")
# absolute path to the directory where stuff to include like images should go
TARGET_ASSET_DIR = Path("./assets")

if CODESPACE:
    # absolute path to the pandoc executable
    PANDOC_EXE = Path("/usr/bin/pandoc")
    ENGINE = "/usr/bin/pdflatex"
    BIB_ENGINE = "/usr/bin/biber"
else:
    # absolute path to the pandoc executable
    PANDOC_EXE = Path("C:/Program Files/Pandoc/pandoc.exe")
    ENGINE = "pdflatex"
    BIB_ENGINE = "biber"


# Number of workers for ProcessPoolExecutor
WORKERS = None


def process_markdown_text(text: str) -> str:
    # Remove all blockquotes
    text = re.sub(r"^>.*", "", text, flags=re.MULTILINE)

    # Remove everything inside dataview blocks entirely
    text = re.sub(r"```dataview.*?```", "\n\n", text, flags=re.DOTALL)

    # Remove everything inside code blocks, or triple backticks
    # text = re.sub(r"```.*?```", "\n\nREPLACE CODEBLOCK HERE\n\n", text, flags=re.DOTALL)

    # Ensure that bulleted lists have two line breaks before
    text = re.sub(r"(.)\n{1,2}((- .*$\n)+)", r"\1\n\n\2", text, flags=re.MULTILINE)

    # Ensure that numbered lists have two line breaks before
    text = re.sub(r"(.)\n{1,2}((\d\. .*$\n)+)", r"\1\n\n\2", text, flags=re.MULTILINE)

    # Ensure that section headings have two line breaks before and after
    text = re.sub(
        r"(.)\n{1,2}(#+ .*$\n)\n{0,}(.)", r"\1\n\n\2\n\n\3", text, flags=re.MULTILINE
    )

    # Reduce section headings by one level. Require that the heading contains at
    # least two hashes (which avoids Python comments).
    text = re.sub(r"^\#\#", r"#", text, flags=re.MULTILINE)

    # Convert wikilinks to bolded text
    text = re.sub(r"\[\[(.*?)\]\]", r"**\1**", text, flags=re.MULTILINE)

    # Remove excess line breaks (two or more in a row, flags=re.MULTILINE)
    text = re.sub(r"\n{2,}", r"\n\n", text)

    # Automatically identify valid URLs (http/https) and convert them to
    # Markdown hyperlinks, with the URL as the link text.
    text = re.sub(r"(https?://\S+)", r"[\1](\1)", text)

    return text


@dataclass
class TableMeta:
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
        
        # Extract Pandoc's auto-calculated tabcolsep value
        match = re.search(r"(\d+)\\tabcolsep", table_text)
        if match is None:
            raise ValueError("Table does not contain tabcolsep")
        
        tabcolsep = match.group(1)
        
        # Generate alignment lines for each column
        alignments = ""
        for alignment in self.alignments:
            alignments += f"  >{{\\raggedright\\arraybackslash}}p{{(\\linewidth - {tabcolsep}\\tabcolsep) * \\real{{{alignment}}}}}\n"
        
        # Extract the rest of the table, everything between \toprule\noalign{} and \end{longtable}
        match = re.search(r"\\toprule\\noalign\{\}(.*?)\\end\{longtable\}", table_text, flags=re.DOTALL | re.MULTILINE)
        if match is None:
            print(table_text)
            raise ValueError("Table does not contain top rule or noalign")
        table_text = match.group(1)
        
        template = dedent(
            f"""
            {{
            \\small % 10pt font
            \\setstretch{{1}} % Single spacing
            \\begin{{longtable}}[]{{@{{}}
            <substitute_alignments>
            @{{}}}}
            \\caption{{{self.caption}}}\\label{{{self.label}}} \\\\
            \\toprule\\noalign{{}}
            <substitute_content>
            \\end{{longtable}}
            }}
            """
        )
        
        # Substitute the alignments and content
        template = template.replace("<substitute_alignments>", alignments.strip("\n"))
        template = template.replace("<substitute_content>", table_text.strip("\n"))
        
        return template


def process_latex_text(text: str) -> str:
    # Convert \autocite to \cite
    text = re.sub(r"\\autocite", r"\\cite", text)

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
    text = re.sub(r"^\\begin\{figure\}$", r"\\begin{figure}[h]", text, flags=re.MULTILINE)
    
    # A \pandocbounded{\includegraphics[...]{...}} command should be substtituted
    # with \includegraphics[width=1\linewidth]{...}
    text = re.sub(
        r"\\pandocbounded\{\\includegraphics\[(.*?)\]\{(.*?)\}\}",
        r"\\includegraphics[width=1\\linewidth]{\2}",
        text,
    )

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

    return text


def convert_with_pandoc(md_file, tex_file):
    subprocess.run(
        [
            str(PANDOC_EXE),
            str(md_file),
            "-f",
            "markdown",
            "-o",
            str(tex_file),
            "-t",
            "latex",
            "--csl",
            "http://www.zotero.org/styles/ieee",
            f"--bibliography={str(BIBLIOGRAPHY_PATH)}",
            "--pdf-engine=pdflatex",
            "--filter",
            "pandoc-crossref",
            "--number-sections",
            "--citeproc",
            "--verbose",
            "--biblatex",
            "--listings",
            "--resource-path=.:./assets",
        ]
    )
    text = tex_file.read_text()
    text = process_latex_text(text)
    tex_file.write_text(text)


def substitute_labels(tex_dir: Path) -> dict:
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
        "39.1 - Introduction": "chapter-one",
        "39.2 - Literature review": "chapter-two",
        "39.3 - Architecture and design": "chapter-three",
        "39.4 - Action automation": "chapter-four",
        "39.5 - Output and validation": "chapter-five",
        "39.6 - Building scenarios": "chapter-six",
        "39.7 - Evaluation and observations": "chapter-seven",
        "39.8 - Future work": "chapter-eight",
        "39.9 - Conclusion": "chapter-nine",
        "39.A - Architectural diagrams": "appendix-a",
        "39.B - Code samples": "appendix-b",
    }

    for tex_file in tex_dir.glob("*.tex"):
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
    for tex_file in tex_dir.glob("*.tex"):
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

        # Final pass - remove anything that looks like "1.2.3 -" inside any
        # tags, because it's already handled by the engine.
        text = re.sub(
            r"section\{(?:\d\.)+\d - ",
            r"section{",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )

        tex_file.write_text(text)


def join_tex_files(tex_dir: Path, output_file: Path, base_file: Path) -> None:
    """
    Join all the tex files in the given directory into a single file.
    """
    chapter_labels = {
        "39.1 - Introduction": ("Introduction", "chapter-one"),
        "39.2 - Literature review": ("Literature review", "chapter-two"),
        "39.3 - Architecture and design": ("Architecture and design", "chapter-three"),
        "39.4 - Action automation": ("Action automation", "chapter-four"),
        "39.5 - Output and validation": ("Output and validation", "chapter-five"),
        "39.6 - Building scenarios": ("Building scenarios", "chapter-six"),
        "39.7 - Evaluation and observations": (
            "Evaluation and observations",
            "chapter-seven",
        ),
        "39.8 - Future work": ("Future work", "chapter-eight"),
        "39.9 - Conclusion": ("Conclusion", "chapter-nine"),
    }

    appendix_labels = {
        "39.A - Architectural diagrams": ("Architectural diagrams", "appendix-a"),
        "39.B - Code samples": ("Code samples", "appendix-b"),
    }

    output = "% == Begin thesis content\n"
    appendix = ""

    for tex_file in tex_dir.glob("*.tex"):
        if tex_file.stem in chapter_labels:
            chapter_name, label = chapter_labels[tex_file.stem]
            output += f"\\chapter{{{chapter_name}}}\\label{{{label}}}\n\n"
            output += tex_file.read_text() + "\n"
        elif tex_file.stem in appendix_labels:
            appendix_name, label = appendix_labels[tex_file.stem]
            appendix += f"\\chapter{{{appendix_name}}}\\label{{{label}}}\n\n"
            appendix += tex_file.read_text() + "\n"

    output += "% == End thesis content\n"

    text = base_file.read_text()
    text = text.replace("{{thesis_sub_here}}", output)

    text = text.replace("{{thesis_appendix_here}}", appendix)

    with output_file.open("w") as f:
        f.write(text)

def compile_pdf(tex_file: Path) -> None:
    """
    Compile a tex file into a PDF.
    """
    subprocess.run(
        [
            ENGINE,
            str(tex_file),
        ]
    )
    subprocess.run(
        [
            BIB_ENGINE,
            str(tex_file.with_suffix("")),
        ]
    )
    subprocess.run(
        [
            ENGINE,
            str(tex_file),
        ]
    )
    subprocess.run(
        [
            ENGINE,
            str(tex_file),
        ]
    )
    
    print("Cleaning up...")
    # Clean up everything that isn't *.pdf or *.tex
    for file in tex_file.parent.glob("*"):
        if file.stem == tex_file.stem and file.suffix not in [".pdf", ".tex"]:
            file.unlink()


if __name__ == "__main__":    
    # If on my actual machine, copy stuff over from Obsidian
    
    if not CODESPACE:
        # Start by copying everything in SOURCE_MD_DIR to TARGET_MD_DIR
        # Create the target directory if it doesn't exist
        TARGET_MD_DIR.mkdir(parents=True, exist_ok=True)

        # Copy all the markdown files from the source directory to the target directory
        for md_file in SOURCE_MD_DIR.glob("*.md"):
            # Process the markdown file
            text = md_file.read_text()
            text = process_markdown_text(text)

            # Write the processed markdown file to the target directory
            target_md_file = TARGET_MD_DIR / md_file.name
            target_md_file.write_text(text)
            
        # Also copy everything to the asset directory
        TARGET_ASSET_DIR.mkdir(parents=True, exist_ok=True)
        for asset_file in SOURCE_ASSET_DIR.glob("*"):
            shutil.copy(asset_file, TARGET_ASSET_DIR / asset_file.name)

    # Invoke pandoc on each markdown file to generate a tex file
    # Start by creating the target directory for the tex files
    TARGET_TEX_DIR.mkdir(parents=True, exist_ok=True)

    # Run pandoc on each markdown file in parallel
    # this mangles stdout pretty bad, just set the worker count to 1
    # if needed
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = []
        for md_file in TARGET_MD_DIR.glob("*.md"):
            tex_file = TARGET_TEX_DIR / (md_file.stem + ".tex")
            futures.append(executor.submit(convert_with_pandoc, md_file, tex_file))

        for future in futures:
            future.result()

    # now substitute labels
    substitute_labels(TARGET_TEX_DIR)

    join_tex_files(TARGET_TEX_DIR, Path("./thesis.tex"), Path("./base.tex"))
    
    compile_pdf(Path("./thesis.tex"))
