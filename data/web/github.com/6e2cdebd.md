---
domain: github.com
fetch_date: '2026-05-18T12:38:08.988742'
status: ok
url: https://github.com/generative-computing/mellea
---

Inside every AI-powered pipeline, the unreliable part is the same: the LLM call itself.
Silent failures, untestable outputs, no guarantees.
Mellea is a Python library for writing *generative programs* — replacing brittle prompts and flaky agents
with structured, testable AI workflows built around type-annotated outputs, verifiable requirements, and automatic retries.

`uv pip install mellea`

See installation docs for additional options, such as installing all extras via `uv pip install 'mellea[all]'`

.
For source installation directly from this repo, see CONTRIBUTING.md.

The `@generative`

decorator turns a typed Python function into a structured LLM call.
Docstrings become prompts, type hints become schemas — no templates, no parsers:

```
from pydantic import BaseModel
from mellea import generative, start_session
class UserProfile(BaseModel):
name: str
age: int
@generative
def extract_user(text: str) -> UserProfile:
"""Extract the user's name and age from the text."""
m = start_session()
user = extract_user(m, text="User log 42: Alice is 31 years old.")
print(user.name) # Alice
print(user.age) # 31 — always an int, guaranteed by the schema
```

`start_session()`

is the convenience entry point: it returns a `MelleaSession`

with sensible defaults you can override as needed.

**Structured output**—`@generative`

turns typed functions into LLM calls; Pydantic schemas are enforced at generation time**Requirements & repair**— attach natural-language requirements to any call; Mellea validates and retries automatically**Sampling strategies**— run a generation multiple times and pick the best result; swap between rejection sampling, majority voting, and more with one parameter change**Multiple backends**— Ollama, OpenAI, HuggingFace, WatsonX, LiteLLM, Bedrock**Legacy integration**— easily drop Mellea into existing codebases with`mify`

**MCP compatible**— expose any generative program as an MCP tool

| Resource | Description |
|---|---|
| docs.mellea.ai | Full docs — vision, tutorials, API reference, how-to guides |
| Colab notebooks | Interactive examples you can run immediately |
| Code examples | Runnable examples: RAG, agents, Instruct-Validate-Repair (IVR), MObjects, and more |

We welcome contributions of all kinds — bug fixes, new backends, standard library components, examples, and docs.

**Contributing Guide**— development setup, workflow, and coding standards**Building Extensions**— create reusable components in your own repo**mellea-contribs**— community library for shared components

Questions? See GitHub Discussions.

Mellea was started by IBM Research in Cambridge, MA.

Licensed under the Apache-2.0 License. Copyright © 2026 Mellea.
