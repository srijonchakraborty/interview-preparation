# AI

### tokens
- title: Models read tokens, not words
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

Why can a short word cost more than one token, and why does a context limit of 128k tokens not mean 128k words?

---

A tokenizer splits text into tokens before the model sees it. A token may be a word, a piece of a word, punctuation, or whitespace. English prose is often around four characters per token, but code, non-English text, and identifiers split into more tokens.

The context window is a token budget for the prompt plus the completion, not a word budget. Pricing and rate limits are also per token. In an interview, do not equate tokens with words, and do not forget that the answer consumes the same window as the prompt.

### temperature
- title: Temperature changes randomness, not knowledge
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/

What does a low temperature do to a chat completion, and why is temperature 0 not a proof that the answer is true?

---

Temperature scales the distribution the model samples from. Lower values make already-likely tokens more likely, so the output is more repetitive and deterministic. Higher values flatten the distribution and increase variety. `top_p` is a different control: it samples from the smallest set of tokens whose cumulative probability reaches `p`.

Neither parameter looks up facts. Temperature 0 still repeats whatever the model assigns the highest probability, including a confident wrong answer. Use a low temperature for extraction and formatting. Use a higher temperature only when variety is the goal. Grounding, tools, and evaluation are what address correctness.

### hallucination
- title: A fluent answer can still be false
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What is a hallucination, and which product controls reduce it without pretending it is gone?

---

A hallucination is generated content that is not supported by the source of truth you care about. The model can invent an API, a citation, or a date because it is predicting a plausible continuation, not retrieving a row from a database.

You reduce the rate. You do not get a switch that turns it off. Techniques that help: give the source in the prompt and require quotes, call tools for facts that must be current, constrain the output schema, and evaluate on a set of questions with known answers. Saying "do not hallucinate" in the prompt is not a control. In an interview, separate fluency from faithfulness.

### embeddings
- title: Embeddings put text in a space where distance means similarity
- version: Core
- level: intermediate
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

What does an embedding model return, and what does cosine similarity actually tell you?

---

An embedding model maps text to a vector of numbers. Texts with similar meaning land near each other, so you can rank documents by cosine similarity or dot product against a query vector. The vector is not a summary a human reads, and it is not a keyword index.

Similarity is not truth and not permission. Two passages can be near each other and both be wrong, or near each other for a reason the user did not intend. Embeddings also depend on the model: vectors from two different embedding models are not comparable. Use them for retrieval and clustering. Use a generative model, after retrieval, when you need an answer.

### context-window
- title: A long context is not the same as retrieval
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

A model accepts 1 million tokens. Why can stuffing the whole wiki into the prompt still lose to a smaller retrieved context?

---

The context window is only the maximum input the model will accept. Attention over a huge prompt costs latency and money, and models use the middle of a long context less reliably than the beginning and the end. Irrelevant paragraphs compete with the question.

Retrieval selects a small set of passages that the answer should depend on, which is easier to cite and cheaper to run. A long window is useful when the user really did supply one large document. It does not replace chunking, ranking, or evaluation. If the fact is not in the window, the model still has to guess.

### prompt-versus-finetune
- title: Prompt, retrieval, and fine-tuning solve different gaps
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

The model knows the language but not your refund policy, and it also uses the wrong JSON shape. Which fix belongs to prompting, which to retrieval, and which to fine-tuning?

---

Put stable instructions and the output schema in the prompt or in a structured-output setting. Put facts that change, or that are private to the company, in retrieval so the prompt cites today's policy instead of a baked-in paragraph.

Fine-tuning updates model weights from examples. It can teach a tone, a format, or a specialized task when prompting is not enough. It is the wrong place to store facts that change weekly, because every policy edit becomes a training job and the model can still answer without the new fact. Order the decision as: prompt and tools first, retrieval for knowledge, fine-tuning for behavior you cannot specify cheaply.

### evaluations
- title: An eval set is the only way to know a change helped
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

You changed the system prompt and three manual questions look better. Why is that not enough to ship, and what belongs in an evaluation set?

---

A handful of demos cannot show regressions. An evaluation set is a fixed list of inputs with a way to score the outputs: an exact match, a rubric, a retrieved-document check, or a human label. You run it before and after the change and compare the scores.

Include cases the feature must get right, cases it must refuse, and cases that broke in production. Score faithfulness to the provided source, not only fluency. If you change the set and the prompt in the same step, you no longer know which one moved the number. Offline evals do not replace production monitoring; they are how you stop a bad prompt before it ships.
