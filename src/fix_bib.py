import re

# Input and output files
input_file = "thesis_bib.bib"
output_file = "thesis_bib_fixed.bib"

# Read the content of the original BibTeX file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Generate year entries
modified_content = re.sub(
    r"^  (date = {(\d{4}).*},\n)",
    r"  \1  year = {\2},\n",
    content, flags=re.MULTILINE
)

# Fix the complex author name format
modified_content = re.sub(
    "family=Beek, given=Harm, prefix=van, useprefix=true",
    "van Beek, Harm",
    modified_content
)

# All software/online is misc
modified_content = modified_content.replace("@online", "@misc")
modified_content = modified_content.replace("@software", "@misc")

# Write the modified content to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"Modified BibTeX saved to {output_file}")