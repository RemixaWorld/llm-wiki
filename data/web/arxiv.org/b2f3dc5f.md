---
domain: arxiv.org
fetch_date: '2026-05-18T12:37:16.701891'
status: ok
url: https://arxiv.org/abs/2503.00808
---

# Computer Science > Computation and Language

[Submitted on 2 Mar 2025 (v1), last revised 2 Aug 2025 (this version, v4)]

# Title:Predictive Data Selection: The Data That Predicts Is the Data That Teaches

View PDF HTML (experimental)Abstract:Language model pretraining involves training on extensive corpora, where data quality plays a pivotal role. In this work, we aim to directly estimate the contribution of data during pretraining and select pretraining data in an efficient manner. Specifically, we draw inspiration from recent findings showing that compression efficiency (i.e., the normalized loss) of diverse models on certain text correlates strongly with their downstream performance, when the text domain aligns with the downstream benchmarks(Huang et al., 2024). Building on this observation, we hypothesize that data on which model losses are predictive of downstream abilities also contribute effectively to learning, which shares similar intuition with Thrush et al.(2024). To leverage this insight, we introduce predictive data selection (PreSelect), a lightweight and efficient data selection method that requires training and deploying only a fastText-based scorer. Through comprehensive experiments with 1B and 3B parameter models, we demonstrate that models trained on 30B tokens selected with PreSelect surpass the performance of the vanilla baseline trained on 300B tokens, achieving a 10x reduction in compute requirements. Furthermore, PreSelect significantly outperforms other competitive data selection baselines, such as DCLM and FineWeb-Edu on a scale of 3B models trained on 100B tokens. We open-source our trained data selection scorer along with the curated datasets at this https URL.

## Submission history

From: KaShun Shum [view email]**[v1]**Sun, 2 Mar 2025 09:21:28 UTC (1,313 KB)

**[v2]**Tue, 4 Mar 2025 06:15:27 UTC (2,113 KB)

**[v3]**Fri, 4 Apr 2025 10:59:54 UTC (2,277 KB)

**[v4]**Sat, 2 Aug 2025 08:34:03 UTC (1,258 KB)

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer

*(What is the Explorer?)*
Connected Papers

*(What is Connected Papers?)*
Litmaps

*(What is Litmaps?)*
scite Smart Citations

*(What are Smart Citations?)*# Code, Data and Media Associated with this Article

alphaXiv

*(What is alphaXiv?)*
CatalyzeX Code Finder for Papers

*(What is CatalyzeX?)*
DagsHub

*(What is DagsHub?)*
Gotit.pub

*(What is GotitPub?)*
Hugging Face

*(What is Huggingface?)*
ScienceCast

*(What is ScienceCast?)*# Demos

# Recommenders and Search Tools

Influence Flower

*(What are Influence Flowers?)*
CORE Recommender

*(What is CORE?)*# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? **Learn more about arXivLabs**.
