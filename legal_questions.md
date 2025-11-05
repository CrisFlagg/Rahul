# AI-Generated Music: Legal Implications and the Big Outstanding Questions (2025 Snapshot)

This report maps the current legal landscape around AI-generated music and highlights the key unresolved questions. It is informational and not legal advice. Laws evolve quickly; check the cited sources and monitor updates.

## Executive summary

- Copyright protection in the US requires human authorship. Purely AI-generated music generally is not protectable; human contributions may be, if sufficiently creative.
- Training on copyrighted music is legally unsettled in the US (fair use vs. licensing). The EU allows text-and-data mining (TDM) with a rightsholder opt-out; Japan’s exception is broader.
- Output risks include:
  - direct copying/sampling (sound recordings and compositions),
  - “substantial similarity” to protected works,
  - sound-alike voice cloning triggering rights of publicity and unfair competition claims.
- Platforms face liability questions (DMCA §512 safe harbor applicability, §1201 anti-circumvention). Transparency and deepfake labeling obligations rise in the EU AI Act.
- Royalty and ownership frameworks are adapting: PROs accept AI-assisted works with human authorship; UK law recognizes “computer-generated works” differently than the US.
- Active litigation (e.g., Suno/Udio) and state/federal initiatives (e.g., Tennessee’s ELVIS Act; proposed NO FAKES Act) suggest movement toward consent-and-licensing models for voice and training data.

## 1) Copyright and authorship of AI-generated music

- United States
  - Human authorship is required; purely AI-generated works are not copyrightable. Applicants must disclose AI-generated material and claim only human-authored portions. See the 2023 guidance and subsequent reporting by the US Copyright Office. [USCO 2023 Guidance (Fed. Reg. 88 Fed. Reg. 16190)](https://www.regulations.gov/document/COLC-2023-0006-0001); [USCO AI page](https://www.copyright.gov/ai/).
  - Courts reaffirm the human authorship requirement (e.g., Thaler v. Perlmutter). Humans using AI as tools can claim protection for their original contributions. [Summary](https://www.dwt.com/blogs/artificial-intelligence-law-advisor/2023/08/ai-artwork-copyright-district-court).
- United Kingdom
  - Section 9(3) CDPA 1988 assigns authorship of “computer-generated works” to the person making the arrangements necessary for creation; protection lasts 50 years from creation. This differs from US law. [Overview](https://www.iptechblog.com/2023/07/copyright-protection-for-ai-works-uk-vs-us/).
- European Union
  - Author’s rights require human creativity; however, neighbouring rights (e.g., phonogram producer rights) attach to sound recordings regardless of human performance. AI-generated tracks may be “phonograms” with producer rights even if no human performer is involved. See WPPT and EU neighbouring rights frameworks. [Primer](https://labelgrid.com/blog/royalties/a-guide-to-neighbouring-rights-for-musicians/).

Practical implication: If you want exclusivity in the US, you must add meaningful human creative input (selection, arrangement, editing, composition), disclose the AI’s role on registration, and expect protection to cover only human-authored portions.

## 2) Training data: fair use vs. licensing

- United States (unsettled)
  - Key question: Is training on copyrighted music “fair use”? Courts have not squarely resolved this for audio. Digitization cases (e.g., Authors Guild v. Google) recognized transformative indexing as fair use, but recent decisions (e.g., Warhol v. Goldsmith) narrowed the “transformative” analysis and emphasize market substitution and specific context. [Authors Guild v. Google](https://law.justia.com/cases/federal/appellate-courts/ca2/13-4829/13-4829-2015-10-16.html); [Warhol v. Goldsmith summary](https://www.copyright.gov/fair-use/summaries/Andy-Warhol-Found-for-the-Visual-Arts-Inc-v-Goldsmith-143-S-Ct-1258-2023.pdf).
  - Major labels sued Suno and Udio, alleging unauthorized training on copyrighted recordings and stream-ripping from platforms like YouTube; litigation continues, with some settlement activity and licensing negotiations reported. [RIAA Suno complaint (PDF)](https://www.riaa.com/wp-content/uploads/2024/06/Suno-complaint-file-stamped20.pdf); [RIAA press](https://www.riaa.com/record-companies-bring-landmark-cases-for-responsible-ai-againstsuno-and-udio-in-boston-and-new-york-federal-courts-respectively/); industry reporting on Udio settlement/licensing ([MBW](https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/)).
- European Union
  - The DSM Directive (2019/790) provides TDM exceptions with an opt-out for rightsholders; lawful access is required, and opt-outs should be machine-readable (e.g., robots.txt, metadata). [Overview](https://legalblogs.wolterskluwer.com/copyright-blog/the-new-copyright-directive-text-and-data-mining-articles-3-and-4/).
  - The EU AI Act (Regulation 2024/1689) adds transparency obligations for providers of general-purpose/generative models, including summaries of copyrighted training data and deepfake labeling. [EU AI Act explainer](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence); [Hunton summary](https://www.hunton.com/privacy-and-information-security-law/ai-act-published-in-the-official-journal-of-the-eu).
- Japan
  - 2018 copyright amendments permit broad TDM for non-enjoyment purposes (Article 30-4), enabling AI training on copyrighted works without permission, subject to the three-step test and other limits. [Analysis](https://hughstephensblog.net/2024/03/10/japans-text-and-data-mining-tdm-copyright-exception-for-ai-training-a-needed-and-welcome-clarification-from-the-responsible-agency/).

Practical implication: In the EU, respect machine-readable opt-outs and prepare dataset documentation. In the US, treat training datasets as a high-risk area—document sources, avoid DRM circumvention, and consider licensing.

## 3) Output infringement risks

- Direct copying and sampling
  - Sound recordings: In the Sixth Circuit, any unlicensed digital sampling of a sound recording can be infringement (“get a license or do not sample”). [Bridgeport Music v. Dimension Films](https://en.wikipedia.org/wiki/Bridgeport_Music,_Inc._v._Dimension_Films).
  - Compositions: Very short, simple excerpts might be de minimis (e.g., Newton v. Diamond), but this is fact- and circuit-specific. [Newton v. Diamond](https://blogs.law.gwu.edu/mcir/case/newton-v-diamond/).
- “Substantial similarity”
  - If an AI output reproduces protectable musical expression (melody, harmony, lyrics) of a specific work, infringement may be found even without direct sampling.
- “Style-of” outputs
  - Copyright does not protect style per se. However, if outputs emulate protectable expression or use distinctive identifiers (e.g., lyrics, riffs) they can still infringe.

Practical implication: Use filters and fingerprinting to detect memorization/regurgitation, avoid “sound-alike” matching of protectable passages, and keep audit trails of prompts/edits.

## 4) Voice cloning and rights of publicity/personality

- US case law (California)
  - Courts have recognized unauthorized commercial voice imitation as a tort: Midler v. Ford Motor Co.; Waits v. Frito-Lay (voice sound-alike in ads). [Midler case](https://law.justia.com/cases/federal/appellate-courts/F2/849/460/37485/); [Waits overview](http://law2.umkc.edu/faculty/projects/ftrials/communications/waits.html).
- State-level developments
  - Tennessee’s ELVIS Act (effective July 2024) expressly protects voice against AI impersonation. [ELVIS Act explainer](https://www.saul.com/insights/article/elvis-act-tennessee-law-addresses-ais-impact-music-industry).
  - Illinois BIPA regulates voiceprints (biometric identifiers) with strict consent and retention rules; damages landscape adjusted post-White Castle decision. [BIPA overview](https://frostbrowntodd.com/state-privacy-laws-poised-to-fight-unauthorized-voice-cloning/).
- Federal proposals
  - The proposed NO FAKES Act would create a federal right of publicity and DMCA-like takedown/staydown for unauthorized digital replicas; still pending. [Bill overview](https://dean.house.gov/2024/9/dean-salazar-introduce-bill-to-protect-americans-from-ai-deepfakes).
- Labor/contract protections
  - SAG-AFTRA agreements require explicit consent and compensation before creating/using digital voice replicas. [Summary](https://san.com/cc/video-game-actors-end-11-month-strike-with-new-ai-protections/).

Practical implication: Obtain written consent for voice training and cloning; prohibit impersonation in user terms; provide rapid takedown pathways; consider geographic tailoring for state laws.

## 5) Data protection and privacy (EU focus)

- GDPR
  - Voice data is personal data; processed voiceprints for identification are biometric data and require explicit consent or other lawful bases. [GDPR biometric definition](https://www.gdprregister.eu/gdpr/biometric-data-gdpr/).
- EU AI Act
  - Adds risk-based obligations for biometric systems; deepfake labeling duties for AI-generated or modified audio/video. [EU AI Act explainer](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence).

Practical implication: If training on human voices in the EU, implement GDPR notices/consents, retention limits, DSAR workflows, and security controls; label synthetic audio when required.

## 6) Platform liability: DMCA safe harbor and anti-circumvention

- DMCA §512 safe harbor
  - Traditional UGC platforms may qualify, but applicability to generative AI providers is uncertain because outputs are dynamically generated and providers may be active creators rather than passive hosts. [Statute](https://www.law.cornell.edu/uscode/text/17/512).
- DMCA §1201 anti-circumvention
  - Unlawful to bypass “access controls”; litigation argues that stream-ripping/scraping to obtain training data can violate §1201 if protective measures are circumvented. [Register’s Recommendation 2024](https://www.copyright.gov/1201/2024/2024_Section_1201_Registers_Recommendation.pdf); [Reddit v. Perplexity coverage](https://natlawreview.com/article/anti-circumvention-reddits-case-against-perplexity).

Practical implication: Avoid scraping behind paywalls or technical access controls; use licensed sources; honor robots.txt and TOS; maintain notice-and-takedown workflows and content fingerprinting.

## 7) Royalty and collective management

- PROs (BMI, ASCAP, SOCAN) accept registrations of partially AI-generated musical works where human authorship is substantial; fully AI-generated works are not eligible. [BMI/ASCAP alignment](https://www.musicbusinessworldwide.com/ascap-bmi-and-socan-will-now-accept-registrations-of-partially-ai-generated-musical-works/).
- PRS (UK) aligns with human authorship eligibility under UK law. [PRS policy coverage](https://www.musicbusinessworldwide.com/ascap-bmi-and-socan-will-now-accept-registrations-of-partially-ai-generated-musical-works/).
- Neighbouring rights: Producers of phonograms have rights in sound recordings; AI-generated tracks may trigger producer rights even if no human performer is present. Collecting societies’ operational policies may vary by jurisdiction.

Practical implication: For AI-assisted works, document human authorship to qualify for PRO registration. For recordings, analyze neighbouring rights and local collection practices.

## 8) Consumer protection and transparency

- EU AI Act requires labeling of AI-generated or AI-modified content (deepfakes).
- Industry is moving toward watermarking/provenance systems (e.g., C2PA; platform fingerprinting akin to YouTube Content ID).

Practical implication: Label AI-generated music and disclose tool usage where required; deploy watermarks/fingerprints to trace provenance and manage takedowns.

## 9) Contract and licensing

- Dataset licensing: Increasing shift toward licensing catalogs for training; platform terms often prohibit scraping and derivative model training.
- Artist contracts: Labels/publishers may restrict training and synthetic uses; negotiate carve-outs and consent frameworks.

Practical implication: Maintain a rights registry; upstream licenses and consents should explicitly cover training, model improvement, and synthetic outputs.

## Big outstanding legal questions

1) US fair use for training on copyrighted music  
Will courts deem audio model training transformative fair use, or require licenses (especially where outputs can substitute for originals)?

2) Scope of US copyrightability of AI-assisted music  
How much human involvement is enough? How should registration disclosures be assessed for musical works that intermix AI outputs and human edits?

3) “Style-of” legality and boundaries  
When does emulating an artist’s style cross into protectable expression or false endorsement/unfair competition?

4) Voice rights: national uniformity  
Will Congress enact a federal right of publicity (e.g., NO FAKES Act) to harmonize protections for voice and likeness, including post-mortem rights and takedown/staydown regimes?

5) Platform liability frameworks  
Do generative AI platforms qualify for DMCA §512 safe harbor? How will §1201 apply to scraping methods (access vs. copy controls)?

6) EU operationalization of AI Act transparency  
What will “summaries of copyrighted training data” look like in practice; how will TDM opt-outs be enforced at scale?

7) Neighbouring rights for AI recordings  
How will EU/UK collecting societies treat AI-only phonograms; who gets remunerated; will reforms extend personality/identity protections to synthetic performances?

8) Global divergence and cross-border licensing  
With EU opt-outs, Japan’s permissive TDM, UK’s computer-generated works, and US human-authorship rules—how will global licensing and enforcement align?

9) Provenance and watermarking  
Will standard, robust content provenance and watermark systems become mandatory, and can they withstand adversarial removal?

10) Competition and market effects  
Will licensing deals between labels and AI platforms create “walled gardens” and raise antitrust concerns if access to training corpora concentrates?

## Practical risk controls (for creators, platforms, and enterprises)

- Governance
  - Establish AI content policies: no unauthorized voice impersonation; disclose AI use where required.
  - Keep detailed data lineage: sources, licenses, opt-out compliance; maintain model cards and training logs.
- Data acquisition
  - Prefer licensed catalogs or opt-out-respecting sources; avoid DRM circumvention and terms-of-service violations.
- Outputs
  - Implement filters to reduce memorization; fingerprint outputs against known catalogs; prohibit “in the style of [X]” if risk is high.
  - Deepfake labeling in EU; watermarking/provenance (C2PA or equivalent).
- Legal/contract
  - Consent for voice: written agreements; SAG-AFTRA terms if applicable; state law compliance (e.g., ELVIS Act, BIPA).
  - Registration: document human authorship for PROs and copyright filings; disclose AI portions per USCO guidance.
  - Takedown: fast DMCA/notice handling; repeat infringer policies; staydown for exact matches where feasible.

## Notable references and further reading

- US Copyright Office: human authorship and AI registration
  - [Federal Register 88 Fed. Reg. 16190 (Mar. 16, 2023)](https://www.regulations.gov/document/COLC-2023-0006-0001)
  - [USCO AI initiative](https://www.copyright.gov/ai/)
- Case law and fair use context
  - [Authors Guild v. Google (2015)](https://law.justia.com/cases/federal/appellate-courts/ca2/13-4829/13-4829-2015-10-16.html)
  - [Warhol v. Goldsmith (2023) summary](https://www.copyright.gov/fair-use/summaries/Andy-Warhol-Found-for-the-Visual-Arts-Inc-v-Goldsmith-143-S-Ct-1258-2023.pdf)
- Voice cloning and publicity
  - [Midler v. Ford Motor Co.](https://law.justia.com/cases/federal/appellate-courts/F2/849/460/37485/)
  - [Waits v. Frito-Lay](http://law2.umkc.edu/faculty/projects/ftrials/communications/waits.html)
  - [ELVIS Act](https://www.saul.com/insights/article/elvis-act-tennessee-law-addresses-ais-impact-music-industry)
  - [NO FAKES Act (proposal)](https://dean.house.gov/2024/9/dean-salazar-introduce-bill-to-protect-americans-from-ai-deepfakes)
- EU frameworks
  - [EU AI Act explainer](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence)
  - [DSM TDM exceptions overview](https://legalblogs.wolterskluwer.com/copyright-blog/the-new-copyright-directive-text-and-data-mining-articles-3-and-4/)
- Litigation: training on music catalogs
  - [RIAA Suno complaint (PDF)](https://www.riaa.com/wp-content/uploads/2024/06/Suno-complaint-file-stamped20.pdf)
  - [RIAA press](https://www.riaa.com/record-companies-bring-landmark-cases-for-responsible-ai-againstsuno-and-udio-in-boston-and-new-york-federal-courts-respectively/)
  - [MBW report on Udio settlement/licensing](https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/)
- Sampling and composition
  - [Bridgeport Music v. Dimension Films](https://en.wikipedia.org/wiki/Bridgeport_Music,_Inc._v._Dimension_Films)
  - [Newton v. Diamond](https://blogs.law.gwu.edu/mcir/case/newton-v-diamond/)
- Data protection
  - [GDPR biometric data overview](https://www.gdprregister.eu/gdpr/biometric-data-gdpr/)
- Platform liability
  - [DMCA §512 statute](https://www.law.cornell.edu/uscode/text/17/512)
  - [§1201 anti-circumvention (Register’s Recommendation 2024)](https://www.copyright.gov/1201/2024/2024_Section_1201_Registers_Recommendation.pdf)

— Prepared November 2025.