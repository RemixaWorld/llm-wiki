# DeepSeek V4 Flash Provider — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add DeepSeek V4 Flash as a provider in the LLM fallback chain (MiniMax → DeepSeek → Groq → Gemini → Ollama).

**Architecture:** Follow existing provider pattern — add config fields to `Settings`, add provider entry to `_get_providers()`, use `instructor.Mode.TOOLS` (DeepSeek V4 supports tool calls natively). One new env var: `WIKI_DEEPSEEK_API_KEY`.

**Tech Stack:** litellm (`deepseek/deepseek-v4-flash`), instructor (TOOLS mode), pydantic-settings.

---

### Task 1: Add DeepSeek config fields and provider

**Files:**
- Modify: `src/config.py:22-31` (add DeepSeek fields after MiniMax)
- Modify: `src/llm.py:33-80` (add DeepSeek provider after MiniMax)
- Modify: `.env.example:1-7` (add DeepSeek section)
- Modify: `tests/test_llm.py:18-65` (update provider order tests)

- [ ] **Step 1: Update provider order tests in `tests/test_llm.py`**

In `TestGetProviders`, update the test methods to account for DeepSeek in the fallback chain.

In `test_ollama_always_present`, add DeepSeek env reset:

```python
def test_ollama_always_present(self, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
    monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "")
    monkeypatch.setenv("WIKI_GROQ_API_KEY", "")
    monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

    # Reset singleton
    import src.config

    src.config._settings = None

    providers = _get_providers()
    assert len(providers) >= 1
    names = [p[1] for p in providers]
    assert "ollama" in names

    src.config._settings = None
```

In `test_groq_added_when_key_set`, add DeepSeek env reset and update assertion:

```python
def test_groq_added_when_key_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
    monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "")
    monkeypatch.setenv("WIKI_GROQ_API_KEY", "test-key-123")
    monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

    import src.config

    src.config._settings = None

    providers = _get_providers()
    names = [p[1] for p in providers]
    assert names[0] == "groq"

    src.config._settings = None
```

In `test_provider_order`, add DeepSeek key and update expected order:

```python
def test_provider_order(self, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
    monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "ds-key")
    monkeypatch.setenv("WIKI_GROQ_API_KEY", "groq-key")
    monkeypatch.setenv("WIKI_GEMINI_API_KEY", "gemini-key")

    import src.config

    src.config._settings = None

    providers = _get_providers()
    names = [p[1] for p in providers]
    assert names == ["deepseek", "groq", "gemini", "ollama"]

    src.config._settings = None
```

Add a new test for DeepSeek-specific ordering:

```python
def test_deepseek_after_minimax(self, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "mm-key")
    monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "ds-key")
    monkeypatch.setenv("WIKI_GROQ_API_KEY", "groq-key")
    monkeypatch.setenv("WIKI_GEMINI_API_KEY", "gemini-key")

    import src.config

    src.config._settings = None

    providers = _get_providers()
    names = [p[1] for p in providers]
    assert names == ["minimax", "deepseek", "groq", "gemini", "ollama"]

    src.config._settings = None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_llm.py::TestGetProviders -v`
Expected: FAIL — `WIKI_DEEPSEEK_API_KEY` env var and DeepSeek provider not yet implemented

- [ ] **Step 3: Add config fields in `src/config.py`**

After the MiniMax fields (line 26, after `minimax_api_base`), add:

```python
    # DeepSeek
    deepseek_api_key: SecretStr = SecretStr("")
    deepseek_model: str = "deepseek/deepseek-v4-flash"
```

- [ ] **Step 4: Add provider entry in `src/llm.py`**

In `_get_providers()`, after the MiniMax block (after line 49), add:

```python
    # DeepSeek V4 Flash
    if settings.deepseek_api_key.get_secret_value():
        providers.append(
            (
                settings.deepseek_model,
                "deepseek",
                {"api_key": settings.deepseek_api_key.get_secret_value()},
            )
        )
```

DeepSeek V4 supports tool calls natively, so it does NOT need to be added to the JSON mode set on line 103. The existing check `name in {"ollama", "minimax"}` already excludes `deepseek`, so it will correctly use `instructor.Mode.TOOLS`.

- [ ] **Step 5: Update `.env.example`**

After the MiniMax section (after line 6), add:

```
# DeepSeek V4 Flash (cheap, high quality, 1M context)
# WIKI_DEEPSEEK_API_KEY=sk-...
```

- [ ] **Step 6: Run all LLM tests to verify they pass**

Run: `uv run pytest tests/test_llm.py -v`
Expected: ALL PASS (4 provider order tests + 3 complete_structured tests + 1 semaphore test)

- [ ] **Step 7: Run full test suite**

Run: `uv run pytest -v`
Expected: ALL PASS

- [ ] **Step 8: Commit**

```bash
git add src/config.py src/llm.py .env.example tests/test_llm.py
git commit -m "feat: add DeepSeek V4 Flash as LLM provider in fallback chain"
```

---

### Self-Review

**1. Spec coverage:**
- Config fields (`deepseek_api_key`, `deepseek_model`) → Task 1 Step 3
- Provider in fallback chain → Task 1 Step 4
- `instructor.Mode.TOOLS` (not JSON) → Already correct, no change needed (only `ollama` and `minimax` use JSON mode)
- `.env.example` update → Task 1 Step 5
- Provider order tests → Task 1 Step 1

**2. Placeholder scan:** No TBD/TODO. All code blocks are complete.

**3. Type consistency:**
- `deepseek_api_key: SecretStr` — same pattern as `groq_api_key`, `gemini_api_key`. Called with `.get_secret_value()` in `_get_providers()`. Consistent.
- `deepseek_model: str = "deepseek/deepseek-v4-flash"` — litellm model string format, same pattern as `groq_model`, `gemini_model`. Consistent.
- Provider name `"deepseek"` — not in `{"ollama", "minimax"}` set on line 103, so `instructor.Mode.TOOLS` is used. Correct.
- No `api_base` needed — DeepSeek uses the default `https://api.deepseek.com` which litellm handles automatically via the `deepseek/` prefix. Consistent with how Groq and Gemini work.
