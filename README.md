this basically does the following:
- copies a bunch of markdown files from a target folder over to `/md`
- removes a variety of Illegal stuff that doesn't play well with pandoc...
    - all blockquotes removed
    - all dataview code blocks removed
    - bulleted lists get double line breaks before a paragraph that uses them
    - numbered lists get double line breaks before a paragraph that uses them
    - section headings get double line breaks before and after any text
    - section headings are kicked down a level (anything with two hashes at the start of a line)
    - wikilinks are removed, and converted to bolded text to make sure you don't forget to fix them if necessary
- passes the resulting `/md` folder through pandoc with the specified bibliography, plus a bunch of flags, and spits it out to `/tex`
- re-parses the resulting `/tex` to re-convert references, labels, and other fun things from their markdown form (e.g. wikilinks)
- combines all of the `/tex` documents in a hardcoded order with hardcoded chapter names and labels
- sticks it in the middle, using `base.tex` as a template
- spits the result out as `thesis.tex`, which should be valid to copy-paste into overleaf

just run `python src/main.py`

known issues:
- tables are still kinda broken
- code blocks look ugly
- figures/images aren't accounted for at all, and certainly not excalidraw drawings