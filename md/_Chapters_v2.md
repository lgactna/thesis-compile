The chapter list, 2e.

REPLACE CODEBLOCK HERE

Left to do:
**39.2 - Literature review**

- 

---

This outline assumes that *every* stretch goal is achieved, including those that I have doubts about being able to implement.

**39.0 - Abstract**

- (Dedication)
- (Acknowledgments)
- (Abstract)

**39.1 - Introduction**

- **(1.1) History of digital forensics**: How did we get to the present state of the field? What are forensic images in the broader context of digital forensics as a whole?
- **(1.2) Purpose of forensic images**: How are forensic images used in "the real world" – that, is what do forensic analysts do when presented with a new scenario? How does this differ from how they are used in the education of new forensic analysts, and how does this differ from how they are used in research (often for tool validation and development)?
- **(1.3) Real and synthetic datasets**: Where do researchers and instructors actually get these datasets from? What is the difference between "real" and "synthetic" datasets, and what are the issues of developing or using each type?
- **(1.4) Research objectives**: What are the final goals of this thesis?
	- Goals are same as described in the abstract: describe and implement a modern architecture for building new forensic datasets, provide a mechanism for reporting on and searching through the contents of forensic images, and greatly streamline the overall process of constructing a scenario around which a forensic dataset can be built. 
	- "by the conclusion of this thesis, readers will understand the value of synthetic images in forensic research and education, as supported by an evaluation of AKF in an actual classroom setting"
	- blurry line with 1.5, might just write 1.4/1.5 as one section

- **(1.5) Contribution**: Who benefits from this? What are the specific contributions to the field that AKF makes?
	- Will be pretty similar to the abstract - in short, it gives a modernized framework that is designed to enable a larger ecosystem in which AKF-generated images. This thesis contributes a framework that can be used to not only vastly reduce the time spent developing new datasets for research and education, but also improve the discoverability of existing datasets and promote the long-term development of the framework based on new advances in technology. In turn, educators and researchers alike will have a greater variety in the scenarios available to them...

**39.2 - Literature review**

- **(2.1?) Existing datasets**: What datasets (or collections of datasets) for digital forensics currently exist? Where do they come from, and what are their drawbacks?
	- what's in here that isn't already part of 1.3? is this really necessary? should 2.2 just be the entire chapter, and have it further broken down?

- **(2.2) Prior synthesizers**: At a high level, what are the major synthesizers that have been developed in the past, and how did they work? Why are synthesizers used at all, and what challenges do/did they solve?  What were their specific contributions?  
	- do NOT go into low-level technical/implementation details here, that's for the future chapters
	- should contain similar content to the **CS 650 paper**
		- however, the content of that paper's literature review will need to be distributed across a bunch of sections - this is because we're now sprinkling low-level technical details of older synthesizers within future sections

**39.3 - Architecture and design**

- **(3.1) Motivation:** Why reinvent the wheel (again)? (The answer is that none of the existing synthesizers make use of modern Python features or best practices, and lack the interfaces necessary to support a community-driven approach to maintaining the synthesizer. on top of that, they don't use CASE and use non-standardized output formats...)
	- in other words, what qualities did we observe from existing synthesizers that made it difficult to simply adapt or modify them, and completely build a new one from scratch instead? why did these qualities make it difficult to achieve the goals outlined in 1.4/1.5?
	- can be merged with the literature review if necessary...
	- this is NOT "what does this contribute", it's the "why bother reinventing the wheel?"
	- this is also NOT  "what does AKF do better?" - we're just introducing the deficiencies in existing synthesizers and explaining why they're a problem. the solutions to those problems, which are enabled by AKF, will be described in the following sections

- **(3.2) Overview** : At a high level, what modules (or group of modules) do we need to implement for a synthesizer to do what it is designed to do? What technologies, such as hypervisors, do we depend on? What is each of these modules' roles, and how do they feed into other roles?
	- in other words, explain the role of `akflib`, the output and validation modules, etc

All following sections, except for **39.8 - Future work** and **39.9 - Conclusion**, are grouped by major "modules" (or groups of libraries) that are a part of AKF. They roughly correspond to one of the big colored boxes in the **Architecture** diagram.

**39.4 - Action automation** (more generally, `akflib`, hypervisors, and the agent system)

- **(4.1) Overview**: What options exist for generating artifacts as part of a scenario dataset? How do each of them work, at a high-level? What techniques have each of the synthesizers in **39.2 - Literature review** taken?
- **(4.2) Agentless artifact generation**: What's the role of a hypervisor in AKF, and what features can it provide to help facilitate artifact generation when we don't want to use an agent?
	- important to note here that the current implementation will only use VirtualBox, even if Qemu has been used elsewhere before
	- **Do hypervisors belong elsewhere?** seems like an odd place to introduce them, since we almost certainly will need to explain them a little bit in 3.2

- **(4.3) Agent-based artifact generation**: How do we use agents and existing automation frameworks to simplify application-specific actions? Why is the RPyC-based system so much better than other options, such as **ForTrace**? How does this enable us to do runtime introspection, so we know that particular artifacts are actually on the disk?
- **(4.4) Physical artifact generation**: How do we deterministically stick things in the slack space of a file in a filesystem? More broadly, how do we "poof" data onto a disk?

**39.5 - Output and validation**

- **(5.1) Overview:** Great, so we've figured out how to generate artifacts. What are the actual file outputs that need to be generated by the framework (both core outputs and metadata)? Why are these important, and what are their actual uses in industry?
	- for metadata, the usefulness is in developing a comprehensive ecosystem and making AKF-generated images machine searchable, so researchers know what things of interest are in their disk -- even if the original creator didn't think that stuff was significant, and therefore didn't include it in any human-generated data 
		- this statement probably belongs in 5.3. this is briefly alluded to in the **60 - Classes/61 - Old/CS 704/Final Project/Final paper|CS 704 Final paper**
	- in incident response, you're not getting the whole picture if you're just looking at disk images or just network captures! so you shouldn't be training on *just* disk images, either!

- **(5.2) Core outputs**: How do we generate disk/network/volatile captures? Can we optimize these outputs for making distribution and storage more efficient, and how have synthesizers (particularly **EviPlant**) tackled this issue before?
- **(5.3) Metadata and ground truth:** What is ground truth used for, and why is it significant? How do we achieve logging, metadata, and ground truth generation through CASE? How can this information be used to build a comprehensive ecosystem?
- **(5.4?) Human-readable reporting**: idk if this will be its own section, or it might just end up being a mention in 5.3 or **39.8 - Future work**; what about human-readable answer keys, similar to the ones in CFReDS? should the work regarding **60 - Classes/61 - Old/CS 704/Final Project/Final paper|fastlabel** be here?

**39.6 - Building scenarios** (ok, so now you have all of these systems to manipulate a virtual machine into automating a bunch of user actions in a deterministic manner with comprehensive logging. but how do you actually invoke these systems? and how do you generate the artifacts themselves, to be placed onto the device?)

- **(6.1) Overview/imperative usage**: What does basic (imperative) usage of AKF look like? How do you set up the Python library, hypervisor, and possibly the "base" image used to generate the scenario? Should the "base" image be publicly distributable (if so, how do we deal with copyright concerns)?
- **(6.2) Declarative inputs**: How do we define a **Declarative to imperative translation|declarative** format that acts as a simpler interface to the imperative format, so that instructors (who might just want *an image* with some files in it) don't have to learn how to program?
- **(6.3) Using LLMs to build high-level scenarios**: How can recent advancements in LLMs be used to write AKF scenarios using the simpler declarative syntax, which can then be converted into the full imperative syntax?
- **(6.4) Using generative AI for individual artifacts:** Even if we can automate everything, this still doesn't solve the issue of things like images, email conversations, and other things that may be easy to automate, but difficult to make by hand (but we still want these in the image). How can generative AI help solve this issue?
	- for example: the Data Leakage case has *very* brief email conversations, and not a lot of noise to go along with it. there should be more noise, possibly involving conversations with other people.

**39.7 - Evaluation and observations** (if we end up with datasets that end up being usable in CS 252, we'll probably need another section to describe observations. should follow [@mochEvaluatingForensicImage2012] somewhat closely)

- **(7.1) Scenario**: What class was this used in, and elements of the class are worth mentioning? What was the scenario we gave students? What was the context provided to students about the dataset (for example, were they told this was a synthetic dataset? if so, what were they told about it being synthetic?)?
- **(7.2) Student analysis:** How well were students able to analyze the scenario? If there were specific items that we expected students to find, how many of these items were identified in the reports that students created?
	- *Extreme* stretch goal - this only covers the student side of things. What about the instructor side of things? Do they think AKF covers their use cases, and is it as easy to use as I claim it is?
	- Wouldn't it be great to have a full ransomware incident response scenario, where all of network, memory, and disk images are relevant, and there's more than one machine involved, and there's a bunch of "typical" user files that get encrypted? wouldn't that be great ???

- **(7.3) Findings/observations**: Were there other things of note, like the students noticing traces (**Synthesis pollution**) of AKF being left behind? Did students like the alternative scenario compared to an existing, human-crafted scenario? What did students like or dislike?

**39.8 - Future work** (structure depends a lot on what i simply don't get done)

- **(8.1) Integration of recent advancements**: stuff like Operator that has significant, material value and does something I don't, but still has some drawbacks (particularly, the non-determinism of LLMs?) that don't make it applicable in every use case; not to mention it's not like it's *incompatible* with AKF
- **(8.2) Framework limitations**: the "smaller" things described below

- OpenAI's Operator is a thing now 

- The smaller things that don't deserve extensive focus
	- Mobile device support (though [@demmelDataSynthesisGoing2024] does some work towards this)
	- Handling other operating systems (simply because there's no time, not because it's not possible with the current architecture and strategies)
	- Describing volatile memory captures and network captures? We can generate CASE entries as we're acting on the machine, but the contents of volatile memory captures and network captures may require after-the-fact analysis, and they might not fit well into CASE. What kind of labels do researchers working on memory/network datasets need?
	- Limitations (whatever they end up being)

- Any discussions with the folks over at CFReDS/Josh Brunty/Coach Morgan
- The "creator" side of things - does AKF suck to use? (see 7.2)

**39.9 - Conclusion**

- I conclude that this took a lot of time, and it is valuable, and i hope it will be useful to the greater forensic community because x, y, and z

