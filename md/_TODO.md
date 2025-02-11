See **_Chapters_v2**

# Things to address

Things to address

- Does the inclusion of the architectural diagram at the start of every chapter work, or should it just be included? Is it good/does it make sense/does it fit on the page? Do I need to describe it in greater detail, if I'm going to bother introducing it at all?
- Does the introduction of each chapter work? Or is it too sudden if it's just like "here's a diagram", blah blah blah?

Mechanical things to address:

- Still need to figure out a good way to do tables, maybe we just have to do them manually
- Also images, that's probably going to be kind of annoying
- All the sections called "overview" conflict with each other and have the same label defined twice, which is Bad
- ~~Code blocks also need to be done manually, which is a little annoying~~
	- no longer is this the case, but the spacing and sizing is kinda annoying
	- ==Do code blocks also have to adhere to the double spacing requirement? Do code blocks need a figure/listing number and a caption? Do they even belong in the thesis body?==

- Gotta standardize use of existing synthesizers - sometimes I wikilink them, sometimes I just italicize them, and that's inconsistent. Do I make a citation to the associated paper or repo every single time I mention it?
	- =="Script and italic typefaces are not acceptable except where absolutely necessary i.e. in Latin designations of species, etc."== - so no italicization for emphasis or to designate names of tools? what's the convention for that?

# Things to do

Things that can be done Right Now:

- 5.2 (core outputs)
- ~~8.2 (future work), things that are out of scope that we *definitely* know won't happen and therefore don't have to wait until we're done with implementation to figure out what didn't get done~~
- ~~9 (conclusion), it's just like one paragraph lmao~~
- ~~put a link to the AKF repos... somewhere lol~~
	- currently it's in **39.1 - Introduction#1.5 - Contribution**, surely there is a better place to do it...

- apparently i just Forgot that **TraceGen** exists, so that has to be included where relevant
- have all references used that are currently in the Forensic Image Synthesis library/bibliography
- apparently i need like a glossary. and acronyms. and stuff. gotta make those Soon:tm:

Actual things that still have to be done:

- Analysis and review of ForTrace's declarative system
	-  ... and implementation of a declarative-to-imperative system

- Integration of the CASE libraries EVERYWHERE (ideally)
- Physical artifact generation (can `pytsk` really solve the issue of parsing and reading disk images?)
- Finish up the VirtualBox concrete hypervisor API
- Freshen up the Windows VM, develop a dedicated process for setting up a Windows VM and installing the agent on it for use
- All the funny AI stuff

# How to do the things (for the paper)

Compilation notes:

- `\autoref` is used to stick the word "chapter" and "section" into the actual reference. Don't do hyperlinks like "refer to chapter **39.0 - Abstract**", just use "refer to **39.0 - Abstract**"
- I'm pretty sure figures will have to be done manually, look for anything in the form `!\textbf{...}`
	- This also includes the rendering of figures (e.g. excalidraw to png) and uploading them into Overleaf, as an example

Order of operations:

- Write the whole thing (code and paper), get the overall structure approved (so answer the questions above)
- Make sure that the bibliography file contains only used references, rewrite so that this is the case
- Do grammar checking by copying *from Obsidian* to Grammarly, and apply edits in Obsidian
- Use the thesis compiler to generate `thesis.tex`, copy it directly into Overleaf
- Add/fix figures, code blocks, and other things as needed (this is the most time-consuming step, and hopefully only needs to be done once - use `git diff` on the base output if needed)
- tada...

# Actual chapter to-dos

**39.0 - Abstract** (100%)
Done (may require some light editing if we don't fulfill all the promises made in the abstract)

**39.1 - Introduction** (100%)
Done

**39.2 - Literature review** (100%)
Done

- [x] #task 2.1 - Write this entire section, probably mostly from [@grajedaAvailabilityDatasetsDigital2017] 📅 2025-02-08 ✅ 2025-02-08

**39.3 - Architecture and design** (100%)
Done (unless the architecture diagram needs to be reworked, either to fit in better with the text or to actually move stuff around in the diagram itself)

- [x] #task 3 - Consider incorporating concepts explicitly from [@horsmanDatasetConstructionChallenges2021] 📅 2025-02-09 ✅ 2025-02-08
- [x] #task 3.2 - Update the architecture diagram to look nicer, and remove all "notes" that are supposed to just be for me 📅 2025-02-09 ✅ 2025-02-08
- [x] #task 3.2 - Consider making the connection between the "three distinct concepts" and the diagram to be more clear, most likely by editing or adding a simpler diagram that provides a closer 1-1 connection between those components 📅 2025-02-09 ✅ 2025-02-08
	- that is, you'd have one big scary diagram, and then a simplified version of the same diagram

**39.4 - Action automation** (~75%)

- [x] #task 4 - Consider adding an inset diagram from the complete architectural diagram, and then briefly explaining what parts of the diagram correspond to which sections below; also consider moving the content into 4.1 📅 2025-02-08 ✅ 2025-02-08
- 4.2 - after more agentless generation is implemented, it needs to be discussed in greater detail in the context of AKF
- 4.3 - add any new application-specific information to the table
	-  [ ] #task by extension: achieve feature party with what's discussed in ForTrace page 11, at least as close as possible 📅 2025-02-09 

- [ ] #task 4.4 - after physical generation is implemented, it needs to be discussed in greater detail in the context of AKF 📅 2025-02-10 

**39.5 - Output and validation** (~30%)

- 5.1 - Consider removing this section and just having it be at the top level
- [ ] #task 5.2 - Write the entire section (how do we generate relevant outputs from the framework? how do we optimize these outputs for distribution and storage?) 📅 2025-02-08 
- 5.3.3 - Show how the CASE bindings are actually used throughout AKF
- 5.4 - Write the entire section (human readable reporting) - also requires implementation

**39.6 - Building scenarios** (~20%)

- 6.2 - Demonstrate what simple usage of the AKF libraries look like
- 6.3 - Describe the design decisions and analysis of prior declarative languages, and also implement the declarative syntax + translator itself
- 6.4 - Describe using generative AI for artifacts
- 6.5 - Describing using generative AI for scenarios 

**39.7 - Evaluation and observations** (0%)

- The whole thing – can't be worked on *at all* unless we make enough progress 

**39.8 - Future work** (100%)
Done, except for some sentences that may be dependent on things getting done or not

**39.9 - Conclusion** (100%)
Done, except for some sentences that may be dependent on things getting done or not

---
Chapters, v1

!**Chapters**