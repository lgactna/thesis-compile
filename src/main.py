from pathlib import Path
import concurrent.futures
import re
import subprocess

# absolute path to the markdown files to copy here
SOURCE_MD_DIR = Path("C:/Users/Kisun/Desktop/Obsidian/Academic research/30 - Research topics/39 - By chapter")
# absolute path to the bibliography
BIBLIOGRAPHY_PATH = Path("./Forensic Image Synthesis.bib")

# absolute path to the directory where the markdown files will be copied
TARGET_MD_DIR = Path("./md")
# absolute path to the directory where the generated tex files should go
TARGET_TEX_DIR = Path("./tex")

PANDOC_EXE = Path("C:/Program Files/Pandoc/pandoc.exe")

def process_markdown_text(text: str) -> str:
    # Remove all blockquotes
    text = re.sub(r">.*", "", text)
    
    # Remove everything inside dataview blocks entirely
    text = re.sub(r"```dataview.*?```", "\n\n", text, flags=re.DOTALL) 
    
    # Remove everything inside code blocks, or triple backticks
    # text = re.sub(r"```.*?```", "\n\nREPLACE CODEBLOCK HERE\n\n", text, flags=re.DOTALL) 
    
    # Ensure that bulleted lists have two line breaks before
    text = re.sub(r"(.)\n{1,2}((- .*$\n)+)", r"\1\n\n\2", text, flags=re.MULTILINE)
    
    # Ensure that numbered lists have two line breaks before
    text = re.sub(r"(.)\n{1,2}((\d\. .*$\n)+)", r"\1\n\n\2", text, flags=re.MULTILINE)
    
    # Ensure that section headings have two line breaks before and after
    text = re.sub(r"(.)\n{1,2}(#+ .*$\n)\n{0,}(.)", r"\1\n\n\2\n\n\3", text, flags=re.MULTILINE)
    
    # Reduce section headings by one level. Require that the heading contains at
    # least two hashes (which avoids Python comments).
    text = re.sub(r"^\#\#", r"#", text, flags=re.MULTILINE)
    
    # Convert wikilinks to bolded text
    text = re.sub(r"\[\[(.*?)\]\]", r"**\1**", text, flags=re.MULTILINE)
    
    # Remove excess line breaks (two or more in a row, flags=re.MULTILINE)
    text = re.sub(r"\n{2,}", r"\n\n", text)
    
    return text

def process_latex_text(text: str) -> str:
    # Convert \autocite to \cite
    text = re.sub(r"\\autocite", r"\\cite", text)
    
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
    }
    
        
    for tex_file in tex_dir.glob("*.tex"):
        text = tex_file.read_text()
        # Forbid the right brace from being part of anything - this is how we'll know
        # if we're not actually next to a label, if there's another brace
        # in between us and the next label tag
        labels = re.findall(r"^\\\w+?\{([^\{\}]*?)\}\\label\{(.*?)\}$", text, flags=re.DOTALL | re.MULTILINE)
        
        label_table.update({k.replace("\n", " "): v.replace("\n", " ") for k, v in labels})
    
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
                print(rf"Replacing \\textbf\{{[^\{{\}}]*?{textbf2}\}} with \\autoref{{{label_table[textbf]}}}")
                
                # if it is, replace it with a ref. note that every space in the textbf
                # might actually be a newline here, so we have to convert every space
                # into a regex charset that could be either a space or a newline
                
                text = re.sub(rf"\\textbf\{{[^\{{\}}]*?{textbf2}\}}", rf"\\autoref{{{label_table[textbf]}}}", text , flags=re.DOTALL | re.MULTILINE)
        
        # Final pass - remove anything that looks like "1.2.3 -" inside any
        # tags, because it's already handled by the engine.
        text = re.sub(r"section\{(?:\d\.)+\d - ", r"section{", text, flags=re.DOTALL | re.MULTILINE)
        
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
        "39.7 - Evaluation and observations": ("Evaluation and observations", "chapter-seven"),
        "39.8 - Future work": ("Future work", "chapter-eight"),
        "39.9 - Conclusion": ("Conclusion", "chapter-nine"),
    }
    
    output = "% == Begin thesis content\n"
    
    for tex_file in tex_dir.glob("*.tex"):
        if tex_file.stem in chapter_labels:
            chapter_name, label = chapter_labels[tex_file.stem]
            output += f"\\chapter{{{chapter_name}}}\\label{{{label}}}\n\n"
            output += tex_file.read_text() + "\n"
    
    output += "% == End thesis content\n"
    
    text = base_file.read_text()
    text = text.replace("{{thesis_sub_here}}", output)
    
    with output_file.open("w") as f:
        f.write(text)

if __name__ == "__main__":
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
        
    # Invoke pandoc on each markdown file to generate a tex file
    TARGET_TEX_DIR.mkdir(parents=True, exist_ok=True)
    
    # this mangles stdout pretty bad, just set the worker count to 1
    # if needed
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for md_file in TARGET_MD_DIR.glob("*.md"):
            tex_file = TARGET_TEX_DIR / (md_file.stem + ".tex")
            futures.append(executor.submit(convert_with_pandoc, md_file, tex_file))

        for future in futures:
            future.result()
    
    # now substitute labels
    substitute_labels(TARGET_TEX_DIR)
    
    join_tex_files(TARGET_TEX_DIR, Path("./thesis.tex"), Path("./base.tex"))
        
