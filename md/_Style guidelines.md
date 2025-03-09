- Synthesizers are not to be italicized. Every mention of a synthesizer in a paragraph not focusing on that synthesizer should have a citation.

- Bulleted lists should have their key element **bolded** where applicable.
- Tools or libraries may be `monospace` to distinguish them from regular text. Use this sparingly; tools with "actual names" should have no formatting applied. (for example: `uv`, `dfvfs`, the Digital Forensics Virtual Filesystem, Pydantic, CASE, `caselib`)
- Italicization *for emphasis* is allowed. Bolding for emphasis is not.
- Italicization for "proper" terms, such as the names of modules, is allowed but should be limited in usage.

`\autoref` is used to stick the word "chapter" and "section" into the actual reference. Don't do hyperlinks like "refer to chapter **39.0 - Abstract**", just use "refer to **39.0 - Abstract**".

There's a special syntax for making code listings appear. Anything of the form `**!lst:(.*?)**` will turn into an `\autoref{lst:label}`. Also, if the first line of an `lstlisting` is of the form `!label|caption`, it'll make the listing accordingly. You can see the syntax towards the start of **39.6 - Building scenarios#6.1 - Scripting background**.

For now, figures are just going to be done manually. We don't really even have any yet, so I guess it's not an issue lol

