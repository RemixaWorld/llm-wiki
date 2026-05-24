---
domain: help.openai.com
fetch_date: '2026-05-18T12:57:20.376419'
status: ok
url: https://help.openai.com/en/articles/5072263-how-do-i-use-stop-sequences-in-the-openai-api
---

Stop sequences are used to make the model stop generating tokens at a desired point, such as the end of a sentence or a list. Using the Chat Completions API, you can specify the `stop`

parameter and pass in the sequence. The model response will not contain the stop sequence and you can pass up to four stop sequences.

**Simple example:**

In this simple chat example, one stop sequence is used, the word "world". The system message and the user message are designed to try to get the model to output "Hello world"; when the generated text reaches the exact stop sequence "world", the response stops before including that stop sequence, so the returned output is "Hello".

You can explore additional stop sequence examples using the OpenAI chat playground.
