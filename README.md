this basically does the following:
- copies a bunch of markdown files from a target folder over to `/md`
- removes a variety of Illegal stuff that doesn't play well with pandoc...
    - all blockquotes removed
    - all code blocks removed
    - bulleted lists get double line breaks before a paragraph that uses them
    - section headings get double line breaks before and after any text
    - section headings *remain the same* (so nothing happens)
    - wikilinks are removed, and converted to bolded text to make sure you don't forget to fix them if necessary
- passes the resulting `/md` folder through pandoc with the specified bibliography, and then spits them out to the `/tex` folder
- changes all `\autocite` tags with `\cite`

you'll still have to add `lstlisting` code blocks yourself