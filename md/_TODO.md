See **_Chapters_v2**

# The shortest term

Paper-related:

- Rework all architectural diagram-related stuff. Make appendix A, which has individual architectural diagrams.
	- At the start of each (sub)section, there should be a focus on just a specific part of the complex diagram, with non-related elements simplified. 
	- Each chapter will have the complete simple diagram at the top, with irrelevant components reduced in opacity.
	- Make a label-less version of the complex diagram (which will allow it to fit, rotated, on a single page). This can go into the appendix, and will help orient the user to where things are. It should be followed by a series of complex diagram insets, describing each part.

- Rework text containing code blocks to only describe why things matter. Make appendix B, which has longer code blocks describing why specific structural changes are better. The appendix should (ideally?) have sections that can be referenced by the main text body.
- As the below are finished, write their relevant sections.
- Review text so that "feature parity" actually means "feature parity with most synthesizers" or something that doesn't mean "full feature parity", just "good enough and it is possible to reimplement all existing features if there was more time"

---

Implementation:

- Implement the remaining hypervisor API stuff. More likely than not, we're going to fold on implementing direct disk writes.
	- There is still *one* option, and that's seeing if pytsk can tell us the exact offset (and size) of a block with slack space so that we can just write directly to that space.

- Implement declarative wrappers for the hypervisor API stuff, as well as simple Chrome-related actions (like "visit three websites, at some random interval, from this larger list of URLs")
- Add CASE integrations
- Single AI artifact generation
- AI full scenario generation
- Bonus for the agent: individual applications, pyautogui, mouse, keyboard
- GitHub action to automatically build AKF agent for multiple platforms on tagged commits; update the Vagrant file to point to the latest available Windows release (or a specific release is fine too)

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
		- currently they're condensed in size to make them easier to read
		- go to grad school and ask q
	- Guidance: **Limit inline code blocks, and make them as short as possible. Make your point with a code block *once* - it's not supposed to be technical documentation. For longer code blocks, or those that require additional explanation, these belong in the appendix.**

- Gotta standardize use of existing synthesizers - sometimes I wikilink them, sometimes I just italicize them, sometimes I do nothing, and that's inconsistent. ==Do I make a citation to the associated paper or repo every single time I mention it?== **Answer: yes** (it won't hurt)
	- =="Script and italic typefaces are not acceptable except where absolutely necessary i.e. in Latin designations of species, etc."== - so no italicization for emphasis or to designate names of tools? what's the convention for that? - ask the grad school
	- Should my tools also go in the Glossary?

- ==Citing code repositories - do I need to go find the name of the person who made it? Or is what Zotero spits out fine?== (but what if it's *a lot* of people?)
	- ==Also, do I even cite names of tools to begin with? If I mention that `pycdlib` is a thing, do I now need to cite it? Or do I just need to make a generic hyperlink to it?== **Answer: yes**; references aren't just to cover your ass, they may be actual references to interesting things as well. zotero's autocite is fine, and you can refer to the University of Arizona's guidelines for more detail.

- Glossary and acronym entries need to be ref-linked. Those use `\acrfull{}` tags based on the names in the glossary.
	- ==Do I need a glossary and acronym listing?== optional, but if it would be helpful you can
	- ==Should the names of synthesizers go into the glossary? What belongs in a glossary?== - sure, it wouldn't hurt

# Things to do

Things that can be done Right Now:

- ~~5.2 (core outputs)~~
- ~~8.2 (future work), things that are out of scope that we *definitely* know won't happen and therefore don't have to wait until we're done with implementation to figure out what didn't get done~~
- ~~9 (conclusion), it's just like one paragraph lmao~~
- ~~put a link to the AKF repos... somewhere lol~~
	- currently it's in **39.1 - Introduction#1.5 - Contribution**, surely there is a better place to do it...

- apparently i just Forgot that **TraceGen** exists, so that has to be included where relevant
- have all references used that are currently in the Forensic Image Synthesis library/bibliography, or delete them
- apparently i need like a glossary. and acronyms. and stuff. gotta make those soon, since i'll probably end up wikilinking them or smth...
- Fix the architectural diagrams as per Nancy's suggestions
- Double-check and clean up anything that has a code block near it; does it solve the purpose that it's supposed to be solving?
	- I think we should move most/all of the code blocks, along with any significant explanations, to a dedicated appendix section for code snippets. This would also allow us to introduce that section with the links to the relevant repositories.

- Roll back the "feature parity" language to something like "almost full feature parity", since physical generation seems Extra annoying
	- but we can say somewhere that this is reflective of over 15 years of development in this field!

Actual things that still have to be done:

- [x] Analysis and review of ForTrace's declarative system
- [x] ... and implementation of a declarative-to-imperative system, with the bare minimum working
- [ ] Integration of the CASE libraries EVERYWHERE (ideally)
	- Start with adding CASE bundle options to the agent and hypervisor APIs, and let's go from there
	- Also includes managing CASE bundles as part of the declarative translator; presumably, this means that the bundle would be part of global state, and also that the metadata for CASE bundles would also have to be included in scenario definitions

- [ ] Physical artifact generation (can `pytsk` really solve the issue of parsing and reading disk images? what else?)
	- implication: pytsk is not suitable for this task because it's largely read-only; you can *analyze* arbitrary filesystems through a very well-abstracted API, but it seems you can't write to anything. it'd probably have to be a manual implementation from one of the prior synthesizers but that seems like a lot of WORK (and may require some linux-specific tooling, which in turn requires docker)

- [ ] Logical agentless generation (finish up the VirtualBox concrete hypervisor API, includes all the dumps, human inputs, and flash drive "from a folder" logic)
- [ ] AI stuff: single artifacts
- [ ] AI stuff: a whole ass declarative scenario
- [x] Freshen up the Windows VM, develop a dedicated process for setting up a Windows VM and installing the agent on it for use
	- see **Setting up the VM**. seems to yield a stable VM

- [ ] Implement more application-specific stuff (this is the whole "feature parity" promise) - whatever is necessary to implement what's described below
- [ ] Re-implement individual modules in the declarative-to-imperative system to implement whatever's necessary below
	- this also includes implementing new modules that serve as a wrapper around multiple features, like "go visit a bunch of these websites at random"

The ultimate goal: Develop a scenario in which all of the following happens:

- A person copies a bunch of "important" documents to their device from a flash drive (which, ideally, is just a mountable folder converted to an ISO using something like [https://clalancette.github.io/pycdlib/,](https://clalancette.github.io/pycdlib/,) and then [https://serverfault.com/questions/171665/how-to-attach-a-virtual-hard-disk-using-vboxmanage](https://serverfault.com/questions/171665/how-to-attach-a-virtual-hard-disk-using-vboxmanage) to attach the iso)
	- These documents are generated using the single-artifact AI thing

- They interact with the internet, preferably doing a mix of web browsing and chatting with someone using the native email application (or something similar that leaves actual chat artifacts)
- That other person sends them some ransomware
- A bunch of those important documents disappear with the ransomware
- The person pays the ransom by going to some website... maybe? Or maybe by just going to some stores implying they purchased some gift cards, which they then visited a fictitious website to enter

The goal would be to have the student solve two things: 

- Who did they pay the ransom to, and to what wallet/website/etc did they pay the ransom to (whether giftcard or crypto)?
- Can you reverse engineer the ransomware to recover the documents? In particular, there's one document with some important details...

this might be hard to convince AI to do, but we can just give examples, I'm guessing; also, some routine parts, like "browse on the internet with a subset of the websites, then send some emails from the provided dataset" can be done using the scenario-wide AI

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

deadline by april 1st, after spring break, for committee to review

**39.0 - Abstract** (~100%)
Done (may require some light editing if we don't fulfill all the promises made in the abstract)

**39.1 - Introduction** (100%)
Done

**39.2 - Literature review** (100%)
Done

- [x] #task 2.1 - Write this entire section, probably mostly from [@grajedaAvailabilityDatasetsDigital2017] 📅 2025-02-08 ✅ 2025-02-08

**39.3 - Architecture and design** (~95%)
Done, except for reworking chapters 3-6 based on the whole architectural diagram stuff

- [x] #task 3 - Consider incorporating concepts explicitly from [@horsmanDatasetConstructionChallenges2021] 📅 2025-02-09 ✅ 2025-02-08
- [x] #task 3.2 - Update the architecture diagram to look nicer, and remove all "notes" that are supposed to just be for me 📅 2025-02-09 ✅ 2025-02-08
- [x] #task 3.2 - Consider making the connection between the "three distinct concepts" and the diagram to be more clear, most likely by editing or adding a simpler diagram that provides a closer 1-1 connection between those components 📅 2025-02-09 ✅ 2025-02-08
	- that is, you'd have one big scary diagram, and then a simplified version of the same diagram

**39.4 - Action automation** (~95%)
Done, except for the architectural diagram stuff and any additional table rows for new RPyC submodules

- [x] #task 4 - Consider adding an inset diagram from the complete architectural diagram, and then briefly explaining what parts of the diagram correspond to which sections below; also consider moving the content into 4.1 📅 2025-02-08 ✅ 2025-02-08
- [x] 4.2 - after more agentless generation is implemented, it needs to be discussed in greater detail in the context of AKF
	- basically done, it's just the same as VMPOP

- 4.3 - add any new application-specific information to the table
	- this can kinda just be written as we go, it's just individual table lines

- [x] #task 4.4 - after physical generation is implemented, it needs to be discussed in greater detail in the context of AKF 📅 2025-02-10 ✅ 2025-02-27

**39.5 - Output and validation** (~75%)
Also needs architectural diagram stuff

- 5.1 - Consider removing this section and just having it be at the top level
- [x] 5.2 - Write the entire section (how do we generate relevant outputs from the framework? how do we optimize these outputs for distribution and storage?)
- [x] 5.3.3 - Show how the CASE bindings are actually used throughout AKF
	- i don't really show how they're used but it's at a high-enough level detail that you'll get the point -- anyways, that can be deferred to sections 6.2 and 6.3

- 5.4 - Write the entire section (human readable reporting) - also requires some implementation
- [x] 5.5 - need to talk about making scenarios reproducibility

**39.6 - Building scenarios** (~60%)
Also needs architectural diagram stuff

- [ ] 6.2 - Demonstrate what simple usage of the AKF libraries look like
	- Still need example imperative script of AKF doing some basic browser stuff and dumping out core outputs, preferably also using CASE

- [ ] 6.3 - Describe the design decisions and analysis of prior declarative languages, and also implement the declarative syntax + translator itself
	- Still need example declarative script doing the same browser stuff, with brief explanation

- [ ] 6.4 - Describe using generative AI for artifacts
- [ ] 6.5 - Describing using generative AI for scenarios 

**39.7 - Evaluation and observations** (0%)

- The whole thing – can't be worked on *at all* unless we make enough progress 

**39.8 - Future work** (~100%)
Basically done, might need to change some language depending on what does/doesn't get done

**39.9 - Conclusion** (~100%)
Done, except for some sentences that may be dependent on things getting done or not

**39.A - Architectural diagrams** (0%)
Need to rework everything, break up the architectural diagrams and put them here (maybe)

**39.B - Code samples** (~100%)
Likely done unless more code blocks need to be moved in here

**39.C - Acronyms** (?)
Will take some work to integrate with rest of thesis

**39.D - Glossary** (?)
Will take some work to integrate with thesis; also need to identify actual glossary terms to include

---
Chapters, v1

!**Chapters**