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

### token-is-a-chunk
- title: A token is a chunk of characters
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/concepts

What is a token, and why does the first token of a word often include a leading space?

---

Text generation and embedding models process text in tokens, which are commonly occurring sequences of characters. The concepts guide gives " tokenization" as " token" plus "ization", while a short common word such as " the" is one token. In a sentence, the first token of each word typically starts with a space.

That is why a word count is a poor estimate of cost or of how much of the context window you used. Use the tokenizer on the exact string, including spaces and punctuation, before you assume a prompt will fit.

### token-budget-effects
- title: Tokens set cost, time, and whether the call fits
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

What three things does the total token count of an API call affect?

---

The advanced usage guide says the total number of tokens affects how much the call costs, because you pay per token, how long the call takes, because writing more tokens takes more time, and whether the call works at all, because the total must stay under the model's maximum.

Both the input and the output count toward those quantities. A short prompt can still fail or get expensive if the completion is long, and some models price input tokens differently from output tokens.

### usage-field
- title: The usage field is the token receipt
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

How do you see how many tokens an API call actually used?

---

Check the `usage` field on the API response, for example `response['usage']['total_tokens']`. That is the count the service billed and enforced, not a guess from a word counter.

Chat models make the count harder to predict ahead of time because messages add formatting beyond the visible text. The exact conversion can change from model to model, so a counter written for one snapshot can be only approximate for the next.

### message-token-overhead
- title: Message fields add tokens beyond the text
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

Why can a chat message cost more tokens than the characters in its content?

---

Each message consumes the tokens in its content, role, and other fields, plus a few extra tokens for behind-the-scenes formatting. The guide's example for `gpt-3.5-turbo-0613` adds tokens per message for the framing, adjusts the count when a `name` is present, and adds tokens that prime the assistant reply.

If you delete a message to make the conversation fit, the model loses all knowledge of that message. Shrinking history is not free: the model cannot recall what you removed.

### reply-cut-off
- title: A full prompt leaves almost no room to answer
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

Why do long conversations tend to get incomplete replies?

---

Input and output tokens share the model's maximum. The guide's example is a `gpt-3.5-turbo` conversation that is already 4090 tokens long: the reply is cut off after just 6 tokens because the limit in that example is 4097.

The same idea applies whenever the prompt consumes almost the whole window. Leave room for the answer, or the model stops because it ran out of tokens, not because it finished the thought.

### seed-mostly-deterministic
- title: A seed makes outputs mostly repeatable
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

How do you ask Chat Completions for more repeatable output, and why is it still not a guarantee?

---

Chat Completions are non-deterministic by default. To receive mostly deterministic outputs, set `seed` to the same integer on each request and keep every other parameter, including the prompt and temperature, exactly the same.

Determinism can still change when OpenAI changes model configuration. Compare `system_fingerprint` on the responses. If that value differs, you may see different outputs because of a change on their systems.

### frequency-versus-presence
- title: Frequency penalty and presence penalty
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

What is the difference between a frequency penalty and a presence penalty?

---

Both penalties reduce the chance of sampling repetitive tokens by subtracting from logits. The presence penalty is a one-off subtraction for any token that has already been sampled at least once. The frequency penalty grows with how often that token has already been sampled.

The guide says coefficients around 0.1 to 1 mildly reduce repetition, values up to 2 suppress it more strongly but can degrade quality, and negative values increase repetition. Neither penalty checks whether the repeated text is true.

### logprobs-are-not-truth
- title: Logprobs show confidence, not correctness
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

What does requesting `logprobs` tell you about a completion?

---

When `logprobs` is requested, the API returns the log probability of each output token and a limited number of the most likely alternatives at each position, with their log probabilities.

That is useful for judging how concentrated the model's distribution was, or for seeing another token it almost chose. It is not a lookup against a source of truth. A high log probability can still sit on a wrong token.

### embedding-input-limit
- title: Embedding models do not spend tokens on an answer
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/concepts

How does the context limit work for an embedding model compared with a text generation model?

---

For a text generation model, the prompt and the generated output together must stay within the model's maximum context length. Embedding models do not output tokens, so only the input must be shorter than that model's maximum context length.

The limits differ by model and are listed in the model index. A string that fits a chat model can still be too long for the embedding model you are calling.

### prompt-is-the-program
- title: The prompt is how you program the model
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/concepts

What does the platform mean when it says a prompt programs a model?

---

Text generation models take inputs called prompts and return text. Designing a prompt means providing instructions or examples of how to complete a task. The concepts page lists uses such as content or code generation, summarization, conversation, and creative writing.

The same page says the platform does not train its models on inputs and outputs through the API. Prompting changes the request. It does not, by itself, update the model's weights.

### accuracy-is-a-matrix
- title: Accuracy work is two levers, not one ladder
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

Why is "prompt, then RAG, then fine-tune" the wrong mental model?

---

The accuracy guide says those methods solve different problems. Context optimization is for knowledge the model lacks, knowledge that is out of date, or proprietary information. LLM optimization is for inconsistent formatting, wrong tone, or reasoning that is not followed consistently.

You start with a prompt, evaluate failures, and then pull the lever that matches the failure. The methods can stack later. Jumping to the most elaborate pipeline first is not what the guide recommends.

### prompt-first-for-some-tasks
- title: Some tasks stop at the prompt
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

When does the accuracy guide say prompt engineering is often enough?

---

Prompt engineering is typically the best place to start, and it is often the only method needed for use cases like summarization, translation, and code generation where a zero-shot approach can reach production accuracy and consistency.

It forces you to define what a good output is, because you have to judge the result. If the output is wrong, the reason it is wrong tells you whether the next step is more context or more consistent behavior.

### prompt-engineering-does-not-scale
- title: A static prompt stops scaling
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What is the main limit of prompt engineering once the task gets wide?

---

The guide says prompt engineering often does not scale. You either need dynamic context for a wider range of problems than you can paste into the prompt, or you need more consistent behavior than a few examples can lock in.

Long-context models extend how far a prompt can go, but the guide says you should still evaluate at different context sizes. A bigger window is not a substitute for measuring whether the model still finds the fact.

### baseline-eval-before-advanced
- title: Leave prompt work with an eval set
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What should you have in hand before you move past prompt engineering?

---

The guide says a good prompt plus an evaluation set of questions and ground-truth answers is the best output of the prompt stage. It specifically points at a set of 20 or more questions, with the failures inspected and a hypothesis for why they happen.

Automatic scores such as ROUGE or BERTScore can show that an iteration moved the text, but the guide says they do not correlate that closely with human reviewers. They are a quick check, not the definition of correct.

### learned-versus-in-context
- title: Learned memory versus the textbook
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

How should you tell a learned-memory failure from an in-context failure?

---

The guide compares two ways to pass an exam. Learned memory is practice: you show many prompt-and-response examples so the model learns the behavior. In-context memory is an open textbook: you put the relevant information in the window, either statically or with retrieval.

The two are additive, not exclusive. Diagnose the failed eval question first. Retrieval does not fix a model that already has the facts and still formats them wrong, and examples do not insert a policy that changes every week.

### rag-definition
- title: RAG retrieves, then the model answers
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What does retrieval-augmented generation actually add to a prompt?

---

RAG means retrieving content to augment the prompt before the model generates an answer, so the model gets domain-specific context. In the guide's picture, you embed the question, retrieve the most relevant pieces of a knowledge base, and present those pieces to the model.

The guide says many large OpenAI customer deployments used only prompt engineering and RAG. Retrieval is its own thing to evaluate: the model cannot answer from context you did not supply, and too much irrelevant context can drown the useful part and cause hallucinations.

### right-context-wrong-answer
- title: A correct passage can still be misused
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

If retrieval returned the right passage and the answer is still wrong, what failed?

---

The guide splits RAG failures into retrieval and the LLM. Wrong or noisy context means the model cannot possibly answer well, and the fix is retrieval. Right context used the wrong way is an LLM failure, fixed by instructions and, when examples raise accuracy, fine-tuning.

You still evaluate after the change. Adding retrieval when the task was already a behavior problem can add noise. In the guide's Icelandic correction example, retrieved extra examples lowered the fine-tuned model's score.

### fine-tune-two-reasons
- title: Fine-tuning is for behavior or for fewer tokens
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What two reasons does the accuracy guide give for fine-tuning?

---

Fine-tuning continues training on a smaller, domain-specific dataset. The guide gives two reasons: improve accuracy on a specific task by showing many correct examples, or reach the same accuracy with fewer tokens or a smaller model.

The examples must represent what the model will see in production. A common pitfall is training data whose formatting differs from production. If production uses retrieval, the training examples should include that retrieved context.

### prompt-baking
- title: Pilot logs can become training data
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What is prompt baking, and what must you hold out of training?

---

Prompt baking means logging prompt inputs and outputs during a pilot, then pruning those logs into a training set of realistic examples. After you have a clean set, you run a training job and keep a hold-out set for evaluation so you can detect overfitting.

The guide says to start from a prompt-engineering eval baseline, prefer quality over quantity, and start with 50 or more examples. If the remaining errors are missing context rather than inconsistent behavior, adding more training rows is the wrong lever.

### stack-prompt-rag-finetune
- title: Prompt, retrieval, and fine-tuning can stack
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

When would a production system use fine-tuning and retrieval together?

---

If early evals show both missing context and inconsistent behavior, the guide says you may end up with both. Fine-tuning can replace long instructions and few-shot examples, and it can teach complex behavior. RAG still injects context that is recent or specialized.

Each addition slows iteration. Retrieval has to be tuned as well as the model, and further fine-tuning means another training run plus training and validation sets. The guide says to squeeze accuracy from basic methods before you take on that complexity.

### accuracy-good-enough
- title: Good enough is a cost, not 100 percent
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

How does the accuracy guide say you decide an accuracy target?

---

The guide says off-the-shelf methods are unlikely to reach 99.999 percent accuracy, so you price success and failure. In its customer-service illustration, an AI-solved case saves money, a bad escalation costs money, and a churn event costs much more, and those weights produce a break-even accuracy.

Where failure is very expensive, such as a fraud case resolved incorrectly, the guide says the human drives and the AI assists. Technically, you then design escapes: ask for more information, send the case back, or hand off to a human.

### output-tokens-dominate-latency
- title: Output tokens dominate latency
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

Why does shortening the answer usually beat shortening the prompt for latency?

---

The latency guide says generating tokens is almost always the highest-latency step. Its heuristic is that cutting 50 percent of output tokens may cut about 50 percent of latency. For prose, ask for a shorter answer or teach brevity with examples or fine-tuning. For structured output, shorten names and drop extra syntax. `max_tokens` or `stop_tokens` can end generation early.

Cutting input helps less. The same guide says cutting 50 percent of the prompt may only cut about 1 to 5 percent of latency, unless the context is truly huge, such as documents or images.

### smaller-model-latency
- title: A smaller model can be the latency fix
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

What does the latency guide say is the main factor in inference speed?

---

Inference speed is the rate of token processing, often measured in tokens per minute or tokens per second. The main factor it names is model size: smaller models usually run faster and cheaper, and when used correctly can outperform larger models.

To keep quality, the guide suggests a longer, more detailed prompt, more few-shot examples, or fine-tuning and distillation. Predicted outputs are a separate optimization when you already know most of the completion, such as a code edit.

### fewer-requests
- title: Sequential prompts pay round trips
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

When should several model steps be one request?

---

Each request pays round-trip latency. If the steps are sequential, the guide says to put them in one prompt and ask for named fields in one JSON object, so you avoid extra round trips and can still parse each result.

If the steps are not strictly sequential, run them in parallel. The guide's image is that two shirts take as long to dry as one. Do not split a reasoning chain just to parallelize if tests show the split answers get worse.

### speculative-execution
- title: Speculative work hides a likely check
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

How can speculative execution remove latency from a sequential check?

---

When one outcome is much more likely, start the likely next step at the same time as the check. The guide's example starts input moderation and story generation together, then cancels generation if moderation does not come back as expected.

If the guess is right, the check added no latency. If it is wrong, you cancel and retry. This is a latency tactic for a predictable branch, not a way to skip the check.

### streaming-versus-spinners
- title: Streaming changes when the user can read
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

Which latency tricks actually finish the user's wait sooner?

---

The guide says streaming is the single most effective way to make users wait less, because they see tokens instead of a blank screen. If the output needs moderation or translation first, stream to your backend and send processed chunks onward.

Showing steps and loading states mostly change how the wait feels. Streaming and chunking change when the user finishes reading. The guide also says not to default to a model: hard-code confirmations and refusals, precompute constrained replies, or use ordinary UI and caching when the output is not really a generation problem.

### stable-prefix-for-latency
- title: Put changing text at the end of the prompt
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

Why does prompt order matter for latency on a long input?

---

For huge contexts, the guide says to maximize the shared prompt prefix by putting dynamic portions, such as retrieval results and history, later. That is more friendly to the key-value cache most providers use, so fewer input tokens are processed on each request.

Fine-tuning can also replace long instructions, and filtering the context, such as pruning retrieval results or cleaning HTML, removes input tokens. The guide still says to spend effort on output length first unless the input is massive.

### evals-because-variable
- title: Evals exist because the same input can differ
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

Why are ordinary software tests not enough for a model application?

---

Generative models sometimes produce different output from the same input, so traditional software tests are insufficient. Evals are structured tests that measure performance despite that variability.

The guide is about tests you design for your application, not an industry benchmark such as MMLU and not a generic score such as ROUGE used by itself. A score between 0 and 1 still needs human judgment so you know you asked the right question.

### eval-anti-patterns
- title: Vibes and generic metrics are not an eval
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

Which eval habits does the best-practices guide tell you to avoid?

---

It calls out overly generic metrics such as relying only on perplexity or BLEU, datasets that do not reproduce production traffic, vibe-based checks such as "it seems to work" or waiting until after you ship, and automated scores that were never calibrated against people.

The matching habits are to evaluate early, make tests match real traffic, log so you can mine new cases, automate scoring where you can, and keep human agreement with those automated scores.

### eval-workflow
- title: An eval has an objective, data, and a metric
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What are the steps of an eval workflow?

---

Define the success criterion, collect data, define how you will score that criterion, run and compare, then keep evaluating. Data can be synthetic, domain-specific, purchased, human-curated, from production, or historical.

Continuous evaluation means running evals on every change, watching production for new nondeterministic failures, and growing the set. The guide also says models are better at pairwise comparison, classification, and scoring against criteria than at open-ended generation, so prefer those shapes when a model is the judge.

### where-nondeterminism-enters
- title: Find the step that can vary
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

Where should you place evals as the architecture gets more complex?

---

A single turn varies in instruction following and in whether the output is functionally correct. A workflow does not add a new kind of nondeterminism, but each model call can be scored on its own. An agent adds tool selection and the precision of the arguments it extracts. Multiple agents add handoffs between specialists.

The guide says the decision to use multiple agents should come from evals. Starting there adds complexity that can slow the path to production.

### grader-types
- title: Metric, human, and model graders
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

How do metric graders, human graders, and model graders differ?

---

Metric graders return a number you can use for regression tests, such as exact match, ROUGE or BLEU, function-call accuracy, or an executable check. They can miss nuance. Human review is the highest quality and is slow and expensive, and experts disagree, so the guide suggests examples of score levels, a pass-fail line, and consensus across reviewers.

A model judge is cheaper to scale. The guide warns about position bias and verbosity bias, and it says to prefer pairwise or pass-fail judgments, control length, ask for reasoning before the score, and scale only after the judge consistently agrees with human labels.

### eval-edge-cases
- title: Happy-path evals miss real traffic
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What edge cases does the eval guide say real systems hit?

---

Cover input variability such as other languages, non-plain formats, and images. Cover messy context: several intents in one request, typos, a one-word request, long history, tool payloads with ambiguous names, several tool calls, and handoffs that loop.

Also define what you support and what you block: jailbreak attempts, format demands, and user text that conflicts with the system prompt. The guide says to include typical, edge, and adversarial cases, and to use human experts to label them.

### evals-platform-timeline
- title: The Evals platform has a shutdown date
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What does the evaluation guide say about the future of the Evals platform?

---

The page says OpenAI is deprecating the Evals platform. Existing evals content stays available during the transition. Evals become read-only for existing users on October 31, 2026, and the platform is scheduled to shut down on November 30, 2026.

That timeline is about the hosted Evals product named on the page. It does not mean you stop measuring your application. The same guide still tells you to keep a dataset, a metric, and a comparison before and after changes.

### embedding-uses
- title: What embeddings are for
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

Which product jobs does the embeddings guide assign to a vector?

---

OpenAI's text embeddings measure relatedness. The guide lists search ranked by relevance, clustering, recommendations, anomaly detection of outliers, diversity measurement, and classification by the nearest label.

An embedding is a list of floating-point numbers. Small distance means high relatedness and large distance means low relatedness. Requests are billed on the number of input tokens. The vector is a feature for those jobs, not a paragraph the user reads.

### embedding-dimensions
- title: Default embedding length and the dimensions knob
- version: Core
- level: intermediate
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

What vector lengths does the embeddings guide state, and how do you shorten one?

---

By default, `text-embedding-3-small` returns 1536 dimensions and `text-embedding-3-large` returns 3072. You can pass a `dimensions` parameter to shorten the vector without, the guide says, losing its concept-representing properties.

The same page lists a maximum input of 8192 tokens for `text-embedding-3-small`, `text-embedding-3-large`, and `text-embedding-ada-002`. Count tokens before you send a long document. The `dimensions` value changes the length of the vector that model returns. It does not raise the input token maximum.

### cosine-and-dot-product
- title: Cosine similarity on normalized embeddings
- version: Core
- level: intermediate
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

Which distance should you use to rank OpenAI embeddings?

---

The guide recommends cosine similarity and says the choice of distance function typically does not matter much. OpenAI embeddings are normalized to length 1, so cosine similarity can be computed as a dot product, and cosine similarity and Euclidean distance produce the same rankings.

For many vectors, it recommends a vector database. The FAQ says customers own their inputs and outputs, including embeddings, and that you are responsible for keeping inputs lawful. Ownership is permission to store the vector. It is not a claim about which distance function you should use. The page still recommends cosine similarity.

### embedding-knowledge-cutoff
- title: Embedding models can miss later events
- version: Core
- level: intermediate
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

Do third-generation OpenAI embedding models know about events after they were trained?

---

The FAQ says no. `text-embedding-3-large` and `text-embedding-3-small` lack knowledge of events that occurred after September 2021. The page says this is usually less limiting than it would be for a text generation model, but it can still hurt performance in edge cases.

To count tokens before you embed, the FAQ says to use tiktoken, and for those third-generation models to use the `cl100k_base` encoding. A string that looks short in words can still exceed the input limit once it is tokenized.

### tool-calling-is-your-code
- title: The model requests a tool, your app runs it
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What is a tool call, and who executes it?

---

Function calling lets the model interface with external systems and data outside its training data. You tell it which tools exist. If the prompt requires one, the model returns a tool call, which is a request, not the result. Your application executes the code and sends the tool output back.

The flow is: request with tools, receive a call, run your code, send the output, then receive a final answer or more calls. A function is a tool defined by JSON schema. Custom tools use free text. Built-in tools cover things like web search, code execution, and MCP.

### function-schema-fields
- title: A function definition is a schema
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Which fields define a function tool?

---

A function in the `tools` list has `type` set to `function`, a `name`, a `description` of when and how to use it, `parameters` as a JSON schema, and `strict` for whether strict mode is enforced. The schema can include types, enums, descriptions, nested objects, and recursive objects.

Namespaces group related tools, such as CRM tools versus support tools, which helps when similar actions belong to different systems. The description is what the model uses to choose and fill the call. A vague description is a product bug, not a model mystery.

### tool-search-defer
- title: Tool search defers a large tool list
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What is tool search for, and which models does the guide say support it?

---

If you have a large set of tools, `tool_search` lets the model search for relevant tools, load them into context, and then call them. The guide says only `gpt-5.4` and later models support it. Deferred tools should carry the detailed guidance in the function description, with a shorter namespace description so the model can decide what to load.

GPT-6 Astra and GPT-6.1 Sol require the Responses API for tool calling. The guide says the Chat Completions examples use a different model. Do not assume every model accepts tools on every endpoint.

### function-design-rules
- title: Design tools the way you would design an API
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What does the function-calling guide tell you to put in a tool definition?

---

Write clear names, parameter descriptions, and instructions. Say what each parameter's format is and what the output represents. Use the system prompt to say when not to call a function. Include examples and edge cases for recurring failures, with the note that examples may hurt reasoning models.

Prefer enums and object shapes that cannot represent invalid states. Do not ask the model to fill an argument your code already knows. Merge functions that you always call in sequence. The guide suggests keeping initially available functions under 20 at the start of a turn, and it calls that a soft suggestion, not a hard cap.

### functions-cost-tokens
- title: Tool definitions spend the context window
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Do function definitions count against the context limit?

---

Yes. Functions are injected into the system message in a syntax the model was trained on, so their definitions count against the context limit and are billed as input tokens. If you hit the limit, load fewer functions up front, shorten descriptions, or defer tools with tool search.

Fine-tuning can also reduce the tokens spent on a large tool list. A long schema is not free context. It competes with the user message and the retrieved facts.

### many-tool-calls
- title: One turn can contain several tool calls
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

How should application code handle the model's tool calls?

---

A response can include zero, one, or multiple calls, so assume there may be several. Each `function_call` has a `call_id`, a `name`, and JSON-encoded `arguments`. You run the function and return a `function_call_output` that references that `call_id`.

The output is typically a string, and you choose the format, such as JSON, an error code, or plain text. If the function returns nothing, still send a string such as success or failure. Images or files can be returned as an array of objects instead of a string.

### tool-choice
- title: tool_choice constrains which tools run
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What are the tool_choice modes?

---

By default the model decides whether to call tools and how many. `auto` allows zero, one, or many. `required` requires one or more. A forced function calls exactly that function. `none` behaves like passing no functions. `allowed_tools` restricts calls to a subset without changing the tool list you send, which the guide says helps prompt-cache savings.

When tool search is in use, `tool_choice` applies to the tools that are currently callable. Forcing a tool does not execute it. You still receive a call and must run it yourself.

### parallel-tool-calls
- title: Parallel tool calls are optional
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

How do you stop the model from calling several tools in one turn?

---

The model may call multiple functions in a single turn. Set `parallel_tool_calls` to false to allow exactly zero or one tool. On supported models beginning with GPT-5, functions can be called in parallel when built-in tools are also available, but built-in tools cannot be part of a parallel function-call batch.

If a fine-tuned model calls multiple functions in one turn, the guide says strict mode is disabled for those calls. It also says the `gpt-4.1-nano-2025-04-14` snapshot can emit multiple calls for the same tool when parallel calls are enabled, and it recommends turning that feature off for that snapshot.

### strict-function-calls
- title: Strict mode is schema adherence
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What does strict mode change about a function call?

---

`strict: true` makes the call adhere to the function schema instead of a best effort. The guide recommends enabling it. It requires `additionalProperties` false on each object in `parameters`, and every field in `properties` must be required. Emulate an optional field with a union that includes `null`.

If you omit `strict`, Responses tries to normalize the schema into strict mode and falls back to best effort when it cannot, showing `strict: false` on the tool. Chat Completions stays non-strict unless you opt in. A schema that claims strict mode but misses those constraints is rejected.

### strict-mode-limits
- title: Strict schemas are cached and not fully free
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What extra costs and limits come with strict function schemas?

---

Strict mode uses Structured Outputs, so some JSON Schema features are unsupported. For fine-tuned models, the first request does extra schema processing that is then cached, so schemas that change every request can add latency. Those cached schemas are not eligible for zero data retention.

Schemas generated in the Playground have strict mode enabled. If you need best-effort calls on the Responses API, set `strict` to false. Omitting the field is not the same default as Chat Completions, which stays non-strict until you opt in.

### structured-outputs-guarantee
- title: Structured Outputs follow the schema
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

What does Structured Outputs guarantee that a careful prompt does not?

---

Structured Outputs makes the model generate responses that adhere to the JSON Schema you supply, so it does not omit a required key or invent an invalid enum value. The guide lists reliable type safety without retrying bad shapes, safety refusals you can detect in code, and less need to beg for a format in the prompt.

Python and JavaScript libraries can define that schema with Pydantic or Zod. The feature is about shape. A value can match the schema and still be the wrong fact.

### function-call-versus-response-schema
- title: Schema for a tool versus schema for the user
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

When should the schema be a function, and when should it be the response format?

---

Use function calling when the model should reach tools, data, or other functionality in your system. Use a structured response format when the model is replying to the user and your app needs to render parts of that reply.

The guide says Structured Outputs is available in those two forms. It is available in recent large language models starting with GPT-4o. Older models such as `gpt-4-turbo` and earlier may use JSON mode instead. For new projects the page says to start with `gpt-6-astra`.

### json-mode-versus-schema
- title: JSON mode is valid JSON, not your schema
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

How is JSON mode different from Structured Outputs?

---

Both can produce valid JSON. Only Structured Outputs adheres to your schema, within the supported subset. The guide says both are available on the Responses, Chat Completions, Assistants, Fine-tuning, and Batch APIs, and it recommends Structured Outputs whenever you can use them.

JSON mode is `text.format` of type `json_object`. Schema mode is `json_schema` with `strict` true. The page says schema response format is supported on `gpt-4o-mini`, `gpt-4o-mini-2024-07-18`, `gpt-4o-2024-08-06`, and later snapshots. JSON mode's compatible set on that table starts earlier, including `gpt-3.5-turbo` and `gpt-4` models.

### json-mode-must-say-json
- title: JSON mode requires the word JSON
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

What happens in JSON mode if the conversation never asks for JSON?

---

You must instruct the model to produce JSON somewhere in the conversation. If you do not, the model may generate an unending stream of whitespace until it hits the token limit. The API returns an error if the string JSON does not appear in the context.

JSON mode does not match a schema. Validate and retry, or use Structured Outputs. If you are using function calling, the guide says JSON mode is always on for that path. You still have to handle incomplete output.

### incomplete-or-refused-json
- title: A schema request can refuse or stop early
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

When does a Structured Outputs response fail to match the schema?

---

The model might refuse for safety reasons, or the response can be incomplete if it hits the max tokens limit. Check for `status` incomplete with reason `max_output_tokens`. A message content item of type `refusal` carries the refusal text instead of `output_text`.

JSON mode adds another incomplete reason: `content_filter`, when generation stops because of restricted content and the JSON may be partial. Treat those branches as errors in your parser. Do not `JSON.parse` a refusal or a truncated object and hope.

### schema-required-and-closed
- title: Every field is required and extra keys are forbidden
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Which two schema rules does Structured Outputs always require?

---

All fields must be listed in `required`, and every object must set `additionalProperties` to false, because the feature only generates keys you specified. You can imitate an optional value with a type that includes `null`, and that key stays required.

The root schema must be an object. It must not be `anyOf`. A discriminated union that compiles to a top-level `anyOf` is invalid for this feature. Outputs are produced in the same order as the keys in the schema.

### schema-size-limits
- title: Schema size limits
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

What size limits does Structured Outputs put on a schema?

---

A schema may have up to 5000 object properties total and up to 10 levels of nesting. The total string length of property names, definition names, enum values, and const values cannot exceed 120,000 characters. Across the schema, enum values cannot exceed 1000. For one string enum with more than 250 values, those values cannot exceed 15,000 characters together.

Supported types are string, number, boolean, integer, object, array, enum, and `anyOf`. Composition keywords such as `allOf`, `not`, `if`, `then`, and `else` are not supported. `strict: true` with an unsupported schema returns an error rather than a best-effort object.

### schema-constraints-and-first-request
- title: String and number constraints are not universal
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Which extra JSON Schema constraints does the guide say work, and where do they not?

---

For strings it lists `pattern` and formats such as date-time, email, uuid, and IP addresses. For numbers it lists `multipleOf` and minimum and maximum bounds. For arrays it lists `minItems` and `maxItems`. The page says these constraints are not yet supported for fine-tuned models, and fine-tuned models also lack string length, pattern, format, numeric bounds, `patternProperties`, and array item counts.

The first request with a given schema has additional latency while the API processes it. Later requests with the same schema do not pay that extra latency. Clear key names and descriptions still matter, and the guide says to use evals to pick the structure.

### sft-what-it-is
- title: Supervised fine-tuning copies demonstrated answers
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What does supervised fine-tuning change?

---

Supervised fine-tuning trains an OpenAI model on examples for your use case so it more reliably produces the style and content you demonstrated. You provide prompts and correct responses, often human-written ground truth. The guide says it is a fit for classification, nuanced translation, a specific content format, and correcting instruction-following failures.

The training file updates the model's weights. It is not a longer system prompt. You still evaluate the fine-tuned model against the base model before you trust it.

### sft-availability
- title: Fine-tuning access is being wound down
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

Who can still create an OpenAI supervised fine-tuning job?

---

The guide says the fine-tuning platform is no longer accessible to new users. Eligible existing customers can create training jobs until January 6, 2027, unless the base model shuts down earlier. A fine-tuned model remains available for inference until its base model shuts down.

The page names shutdown dates for specific `gpt-4.1` snapshots and their fine-tunes. Do not describe fine-tuning as a generally available next step for every new API project. Check the availability timeline on that guide before you plan a training job.

### sft-example-counts
- title: How many fine-tuning examples to start with
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

How many demonstrations does the supervised fine-tuning guide recommend?

---

The minimum is 10 examples, and the file must have at least 10 JSONL lines. The guide says it sees improvements from 50 to 100 examples, the right number varies, and you should start with 50 well-crafted demonstrations and evaluate.

If 50 good examples help, add more. If 50 have no impact, rethink the task or the prompt before you add data. Examples should be realistic prompts and outputs, specific and clear, from historical, expert, or logged data.

### sft-jsonl-and-tools
- title: Training rows are chat-shaped JSONL
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What format is a supervised fine-tuning file, and can it teach tool calls?

---

Use JSONL, one complete JSON object per line, in the chat completions message format. Upload the file with purpose `fine-tune` and pass that file id as the training file. The job also needs a base model id, which can be an OpenAI model or a previously fine-tuned model.

You can train text completions, structured JSON, and function calls. The weights are updated to produce outputs like the rows you uploaded. A row that never shows the tool schema you will send in production teaches a different task from the one you will run.

### distill-to-a-smaller-model
- title: Distill a large model's good answers
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

How does the guide describe distillation into a smaller model?

---

Tune a prompt on a larger model until it meets your evals, capture the responses that pass, and train a smaller model on that dataset. The guide says the Responses API stores model responses for 30 days by default, which is one way to collect those outputs.

The point is a small model that performs similarly on that specific task to a larger, more costly model. Distillation copies the large model's successes and its mistakes. Filter to the rows that meet the eval before you train.

### sft-holdout-and-checkpoints
- title: Hold out data and keep epoch checkpoints
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

How do you tell fine-tuning helped, and what is a checkpoint for?

---

Before the job, carve holdout data from the same collection as the training set, with a similar mix of inputs and responses, and use it as the control when you compare the fine-tuned model to the base model. After training, call the new model id the same way you call a base model.

A full checkpoint is written at the end of each epoch. Use an earlier one if the model improves and then memorizes the set, which the guide calls overfitting. Only the checkpoints for the last three epochs are saved.

### sft-safety-block
- title: A fine-tuned model can be blocked for safety
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What happens after a supervised fine-tuning job finishes, besides getting a model id?

---

OpenAI assesses the model across 13 safety categories, including advice, harassment, hate, illicit acts, self-harm, sexual content, violence, and sensitive data. Each category has a pass threshold. If too many evaluated examples fail, the fine-tuned model is blocked from deployment, and the job message says which categories missed.

You can read `moderation_checks` events for detail and add training data aimed at those categories. The guide still says to run your own evals. Passing the platform check does not prove the model is fit for your use case.

### moderation-endpoint
- title: Moderation classifies text and images
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

What does the Moderation API classify, and what does it refuse to be used for?

---

`omni-moderation-latest` accepts text and images and does not classify audio. The moderation endpoint is free to use. Image files can be up to 20 MB. You can classify a standalone input, or request scores alongside a generated response.

Do not send known or suspected child sexual abuse material to the Moderation API. The guide says the API is not designed for CSAM detection or handling and is not a substitute for dedicated child-safety safeguards.

### moderation-does-not-block
- title: A moderation flag is a signal
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

Does a moderation result automatically hide the model's answer?

---

If you pass a moderation model on a generation request, the model still generates normally and the API returns input and output scores. Review those results before you show the output or take another action. Start with `flagged`, then use `categories` and `category_scores` for logging, routing, or human review.

Treat scores as policy signals, not as an automatic block. A refusal can still be flagged if it discusses harmful content. If a moderation step fails, that side of the result can be an error object instead of scores.

### moderation-tool-coverage
- title: Moderation skips tool schemas
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

What does inline moderation cover on a tool-calling request?

---

It covers tool-call arguments and tool outputs when they appear in conversation content. It does not cover tool names, tool descriptions, tool schemas, or response-format schemas.

If you stream, moderation scores arrive after the full output is available. They are not included with partial deltas. A streaming UI that reveals tokens immediately has not yet seen the output flag.

### moderation-scores
- title: Category scores sit between 0 and 1
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

How should you read a moderation category score?

---

`flagged` is true when the model classifies the content as potentially harmful. `categories` holds a boolean per category. `category_scores` holds a confidence from 0 to 1, higher meaning more confidence. `category_applied_input_types` says whether that score applied to text, image, or both.

The endpoint's underlying model is upgraded over time, so a custom policy that thresholds `category_scores` may need recalibration. Text-only categories, including harassment, hate, illicit content, and sexual content involving minors, return a score of 0 when you send only an image. Hate aimed at a non-protected group is categorized as harassment.

### safety-layers
- title: Safety is several product controls
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

Which safety practices does the OpenAI safety guide list for an application?

---

Use the free Moderation API or your own filter. Red-team with ordinary inputs and with inputs meant to break the product, including prompt injection. Keep a human in the loop for high-stakes domains and for code, and give that person the source they need to check the output. Constrain topic and tone with the prompt and with a few examples of desired behavior.

Also register users where that fits, limit how much text a user can inject and how many tokens you emit, let users report problems, and tell them the system can hallucinate, offend, or show bias. Narrow inputs such as a dropdown, or answers chosen from a validated article, reduce misuse compared with open-ended generation.

### safety-identifier
- title: A safety identifier traces abuse to one user
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

What is `safety_identifier` for, and what should you put in it?

---

It helps OpenAI detect abuse and helps you trace activity to one end user so one person's misuse is less likely to disrupt the whole organization. It is recommended when individuals use the model, and it is not required. Send a unique string per user. Hash a username or email so you do not send the raw identifier. For a logged-out preview, a session id is the guide's alternative.

Identifiers do not carry between APIs or sessions. Images requests take the same stable value, at most 128 characters, on each generation or edit. Realtime uses the `OpenAI-Safety-Identifier` header. If an API key is exposed, revoke it and replace it.

### claude-context-rot
- title: More context is not automatically better
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What is a context window, and what is context rot?

---

Anthropic defines the context window as all the text the model can reference while generating, including the response itself. It is working memory, not the training corpus. A larger window handles longer prompts, but more context is not automatically better. As the token count grows, accuracy and recall degrade. The page calls that context rot.

Curating what is in the window matters as much as the size. Everything in the request counts: the system prompt, every message including tool results, images, and documents, the tool definitions, and the output, including extended thinking.

### claude-context-sizes
- title: Claude context size is per model
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What context and output limits does the Claude context-window page state?

---

It says Claude Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5.5, Sonnet 5, Sonnet 4.6, Haiku 5.5, and Mythos Preview have a 1 million token window, and one request can generate up to 128k output tokens. Other Claude models, including deprecated Sonnet 4.5, have a 200k window.

For those 1 million token models, 1 million is the default without a beta header. Long-context requests are billed at standard pricing except on Claude Haiku 5.5, where prompts over 100,000 tokens cost more. A request can include up to 600 images or PDF pages, or 100 on a 200k model, and you can hit a request-size limit before the token limit.

### claude-thinking-tokens
- title: Thinking tokens occupy the window
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

How do Claude thinking tokens affect the context window and the bill?

---

Thinking tokens are part of `max_tokens`, are billed as output tokens, and count toward rate limits. With adaptive thinking, the amount varies by request. On models that keep previous thinking blocks, those blocks later count as input and are billed as input. On models that strip them, passing the old blocks back does not keep them in the window. The API strips them.

When you return tool results, you must send the entire unmodified thinking block that accompanied that tool request, including its signature. If you modify it, the API returns an error because it checks a cryptographic signature. Cached prefixes still occupy the window. Caching changes the price, not whether the tokens count.

### claude-overflow
- title: A too-long Claude prompt is a 400
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What does the Claude API do when the prompt does not fit?

---

If the input alone exceeds the context window, every model returns a 400 `invalid_request_error` that the prompt is too long. On Claude 4.5 models and newer, a request whose input plus `max_tokens` exceeds the window is still accepted. If generation then hits the window, it stops with `stop_reason` `model_context_window_exceeded`. Earlier models return a validation error instead, unless you opt into that stop reason with the beta header named on the page.

Use the token counting API before you send a long conversation. Compaction, in beta for Claude 4.6 and later and for Mythos Preview, summarizes earlier context on the server so the conversation can continue. Context editing can also clear old tool results or thinking blocks.

### claude-context-awareness
- title: Some Claude models are told their remaining budget
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What is context awareness on Claude?

---

The page says Claude Sonnet 5, Sonnet 4.6, deprecated Sonnet 4.5, and Haiku 4.5 track remaining context. The API injects the total budget into the system prompt and, after tool calls, a remaining-token warning. You do not send those tags yourself. Image tokens are included.

Later models listed on the page, including Opus 4.7 and later, Sonnet 5.5, Fable, Mythos, and Haiku 5.5, do not receive those injected tags. For those, the page points at task budgets, which it marks as beta. Do not assume every Claude model can see a running token budget.

### claude-hallucination-controls
- title: Claude can still state a false fact
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

What does Anthropic say a hallucination is, and what does not remove it?

---

The guide says even an advanced model such as Claude can generate text that is factually incorrect or inconsistent with the given context. That is a hallucination, and it can undermine reliability. The techniques on the page reduce hallucinations. They do not eliminate them. Validate critical information, especially for high-stakes decisions.

Basic tactics on the page: explicitly allow "I don't know", ask for word-for-word quotes before analysis on long documents, and require a citation or a retraction when no supporting quote exists. You can also restrict the model to the provided documents rather than its general knowledge.

### claude-hallucination-checks
- title: Check Claude by repeating and by thinking
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

Which checks does the Claude hallucination guide add beyond the prompt wording?

---

Chain-of-thought verification means using thinking with summarized display and reading the thinking blocks when an answer looks wrong, to see faulty logic. Best-of-N means running the same prompt several times and treating inconsistencies as a warning. Iterative refinement feeds an answer back and asks the model to verify or expand it.

Those checks are still model behavior. Disagreement is evidence of instability, not a proof of which run was right. The page's quote-first example is aimed at documents longer than 20k tokens, where it says extracting exact quotes before the task grounds the answer in the text.

### anthropic-has-no-embedding-model
- title: Claude does not serve embeddings
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/embeddings

Does Anthropic offer an embedding model?

---

The embeddings page says Anthropic does not offer its own embedding model. It points at Voyage AI by MongoDB as one provider and says you should assess vendors for your use case.

When you choose a provider, the page says to weigh dataset size and domain fit, lookup speed and end-to-end latency, and whether you can keep training on private data or specialize for a vocabulary. An embedding is a separate system from the chat model that will read the retrieved text.

### voyage-input-type
- title: Query and document embeddings are not the same call
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/embeddings

Why does the Voyage guidance on Anthropic's docs insist on `input_type`?

---

For retrieval, set `input_type` to query or document. Do not omit it or set it to none. The page says specifying the type produces better dense vectors for retrieval. The API prepends a prompt: a query is prefixed as a query to retrieve supporting documents, and a document is prefixed as a document for retrieval.

Voyage embeddings are normalized to length 1, so cosine similarity matches the dot product and matches Euclidean rankings. Embed the documents and the query with the matching types before you compare them. Mixing those prefixes is a retrieval bug.

### voyage-quantization-and-truncation
- title: Shorter embedding storage has a defined procedure
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/embeddings

How does the Voyage page say you shrink an embedding vector?

---

`output_dtype` can return float, which is the default and the highest precision, 8-bit integers, or packed binary values. The page says int8 and binary cut storage, memory, and cost by 4 times and 32 times respectively. Binary packing uses a sign rule and then packs eight bits into one integer.

Models with multiple output dimensions, such as `voyage-code-4`, use Matryoshka embeddings. Pass `output_dimension` to get a shorter vector from the API. If you already stored a long vector, keep the leading dimensions and normalize again. A reranker is a different call: it takes a query and documents and returns them ranked by relevance.

### azure-embedding-shape
- title: Azure OpenAI embeddings are semantic vectors
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings

What does an Azure OpenAI embedding represent, and which name do you send as the model?

---

An embedding is a vector of floating-point numbers that represents the semantic meaning of text. Similar text produces vectors that are close together. The page says that supports vector search, recommendations, classification, and clustering.

In the request, `model` is your Azure deployment name, not necessarily the base model id. The examples use a deployment named `text-embedding-3-small` and say to replace it if your deployment name differs. A 404 means you should check that the endpoint includes `/openai/v1/` and that `model` is a real deployment name.

### azure-embedding-limits
- title: Azure embedding requests have three limits
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings

What input limits does the Azure OpenAI embeddings article state?

---

Each input for the current embedding models can be at most 8,192 tokens. An array of inputs can contain at most 2,048 items. A single embeddings request also fails with HTTP 400 when the sum of input tokens exceeds 300,000, even if every item is under the per-input limit. Split large batches.

Keep total tokens per minute under the deployment quota. The page also says embedding models can be unreliable or pose social risks and can cause harm without mitigations, and it points you at the Responsible AI content rather than treating similarity as a safety decision.

### azure-embedding-auth
- title: Azure embedding errors are often identity or shape
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings

How does the Azure embeddings article tell you to authenticate, and what do 401 and 403 mean?

---

The v1 embeddings API accepts Microsoft Entra ID and API keys. The article recommends Entra ID so you do not store long-lived credentials. The examples use `DefaultAzureCredential` and the scope `https://ai.azure.com/.default`. Locally you sign in with the Azure CLI first.

A 401 means sign in again and check the token audience. A 403 means the identity needs the Cognitive Services OpenAI User role on the Azure OpenAI resource. A 400 means check the body, each input's tokens, the number of inputs, and the aggregate token count.

### azure-content-filter-runs-alongside
- title: Azure filters prompts and completions
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What does Azure OpenAI content filtering run on?

---

The filter runs alongside the core models, including DALL-E, by passing both the prompt and the completion through classification models that detect harmful content and can prevent that output. It is not applied to prompts and completions processed by the Whisper model.

Hate, sexual, violence, and self-harm are scored at safe, low, medium, and high. Safe is labeled and is not filtered, and that level is not configurable. The filter models for those four categories were trained and tested on English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. Other languages may work at lower quality, so you test your own application.

### azure-filter-defaults
- title: Azure's default filter starts at medium
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What does the default Azure OpenAI content filter block?

---

For the GPT model series, the default filters hate, violence, sexual content, and self-harm at medium severity, on prompts and on completions. Medium and high are filtered. Low is not. For DALL-E, the default threshold is low for text prompts and for image completions, so low, medium, and high are filtered.

You can configure prompts and completions separately, in preview. Filtering only high severity, or turning filters off, requires approval for modified content filters. Customers remain responsible for the Code of Conduct even when a filter is relaxed.

### azure-filter-api-behavior
- title: A filtered Azure call is a 400 or content_filter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

How does a blocked Azure OpenAI request show up in the API?

---

A prompt classified at a filtered category and severity returns HTTP 400. If the completion is filtered, `finish_reason` is `content_filter`, and the content may be incomplete. Non-streaming calls usually return no content in that case. In rare longer responses a partial result can be returned and `finish_reason` is updated.

Streaming keeps sending segments until a stop, a length limit, or filtered content. If the filter system is down or too slow, the request can still complete without filtering. Look for an error in `content_filter_result` rather than assuming the text was checked.

### azure-prompt-shields
- title: Jailbreaks and indirect attacks are different shields
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What does Azure OpenAI call a jailbreak, and what is an indirect attack?

---

A jailbreak is a user prompt designed to provoke behavior the model was trained to avoid or to break the rules in the system message, from role-play to a subtle subversion. An indirect attack, also called cross-domain prompt injection, is malicious instructions placed in a document the model will read. Detecting it requires document embedding and formatting.

Optional classifiers also cover protected material: known text such as lyrics or articles, and source code that matches public repositories. The page says the protected-material code model may be required for Customer Copyright Commitment coverage. Those classifiers are not the same as the four harm categories.

### azure-document-tags
- title: Tag retrieved documents for indirect-attack detection
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

How should retrieved documents be marked so Azure can scan them?

---

The safety system uses the chat message structure to tell system input, user input, and assistant output apart. For documents such as a retrieved page or an email, wrap them in a `documents` element. Indirect-attack detection on that tagged content is optional.

When you tag unvetted documents, JSON-escape the document content so the safety system can parse it. Untagged retrieved text is not identified to the filter as a document. The page says detection improves when the prompt structure distinguishes those parts.

### azure-lora-fine-tune
- title: Azure fine-tuning adapts a smaller set of weights
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning

What does Azure OpenAI say fine-tuning gives you that few-shot prompting does not?

---

The article lists higher-quality results than prompt engineering alone, training on more examples than fit in the request, shorter prompts that save tokens, and lower latency, particularly with smaller models. Unlike few-shot learning, it trains on more examples than fit in the prompt, so the weights adapt and you send fewer examples or instructions.

Azure uses low-rank adaptation. It approximates a high-rank matrix with a lower-rank one and trains a smaller subset of parameters, which the article says makes training faster and more affordable without, in its words, significantly affecting performance. Fine-tuning still does not remove the need to evaluate the deployed model.

### azure-finetune-data
- title: Azure fine-tuning files are JSONL with a BOM
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning

What file rules does Azure OpenAI fine-tuning enforce?

---

Training and validation data are JSONL in the Chat Completions conversational format, encoded as UTF-8 with a byte-order mark, and each file must be under 512 MB. Jobs will not proceed with fewer than 10 training examples, and the article says that few examples will not noticeably change responses.

It recommends starting with 50 well-crafted examples and, as a best practice, hundreds or thousands. Doubling the dataset can raise quality roughly linearly, but low-quality rows can make the model worse. Prune to the best examples before you train on a large internal dump.

### prompt-engineering-definition
- title: Prompt engineering is written instructions
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What is prompt engineering on the OpenAI platform?

---

It is writing instructions so the model consistently generates content that meets your requirements. Because generation is non-deterministic, the guide calls it a mix of art and science, and it says you can still apply techniques that work repeatedly.

Some techniques, such as message roles, apply to every model. Reasoning models and GPT models, and even snapshots in one family, can need different prompting. The guide says to pin production to a specific snapshot, such as the `gpt-4.1` snapshot it names, and to build evals so you notice when a prompt or a model upgrade changes behavior.

### instructions-outrank-input
- title: Instructions outrank the input prompt
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

How do you give a model higher-priority instructions in the Responses API?

---

The `instructions` parameter carries high-level behavior such as tone, goals, and examples of correct responses. The guide says any instructions provided that way take priority over a prompt in the `input` parameter.

Use `instructions` for the stable tone, goals, and examples. The user text still arrives in `input`. The same guide says generation is non-deterministic and that snapshots in one family can differ, so pin the snapshot and test the prompt rather than assuming priority alone makes every request identical.

### few-shot-versus-weights
- title: Few-shot learning does not update weights
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What is few-shot learning, as the prompt engineering guide defines it?

---

Few-shot learning steers the model by including a handful of input and output examples in the prompt, rather than fine-tuning. The model picks up the pattern and applies it to the new prompt. Show a diverse range of inputs with the desired outputs. The guide typically puts those examples in a developer message.

This changes one request. It does not train a new model. When the pattern is stable and the prompt full of examples is too expensive, that is the point where the fine-tuning guides say to consider weight updates instead.

### rag-in-the-prompt
- title: Retrieved text is just more prompt
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

Why does the prompt engineering guide tell you to paste extra context into the prompt?

---

Extra context gives the model proprietary data or anything outside its training set, and it can constrain the answer to a set of resources you trust. The guide says this technique is sometimes called retrieval-augmented generation. You might query a vector database and insert the text, or use the built-in file search tool.

The context window is the memory limit for that request, measured in tokens, including images. The page says sizes differ by model, from the low 100k range up to one million tokens for newer GPT-4.1 models. Look up the specific model rather than assuming one window.

### reasoning-versus-gpt-prompts
- title: Reasoning models want a goal, GPT models want steps
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

How should prompting change between a reasoning model and a GPT model?

---

The guide says reasoning models generate an internal chain of thought, do well at complex tasks and multi-step planning, and are generally slower and more expensive than GPT models. They tend to do better with high-level guidance. GPT models are fast and cost-efficient and benefit from explicit instructions. The analogy on the page is a senior coworker versus a junior coworker who needs the output specified.

When you are unsure which model to start with, the same page says `gpt-6-astra` is a strong default for general-purpose text generation and prompt iteration. Large models understand prompts across domains more effectively. Mini or nano models are generally faster and cheaper.

### model-choice-tradeoff
- title: Model choice is speed, cost, and instruction burden
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What trade-off does the prompt guide state between large and small models?

---

Large models are more effective at understanding prompts and solving problems across domains. Small models, described as mini or nano, are generally faster and cheaper. GPT models in general benefit from more explicit instructions about how to accomplish the task.

Pin the snapshot you evaluated. The guide warns that different snapshots in the same family can produce different results. Changing the model string without rerunning evals is an unmeasured behavior change.

### cache-reuses-prefix
- title: Prompt caching reuses a prefix, not a response
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What does prompt caching save?

---

It reuses work when requests share the same prompt prefix. The guide lists less recomputation, cheaper input tokens discounted up to 95 percent, and less time spent processing input before the response starts. Pricing still varies by model, and a cache write is not an extra fee added on top of a full input charge. Each input token uses the uncached, cached, or cache-write rate.

The cache stores key-value tensors, not the tokens themselves. The model still processes any new suffix to generate a new response. Caching does not make the answer deterministic or correct.

### cache-prefix-must-match
- title: The whole rendered prefix has to match
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What has to be identical for a prompt-cache hit?

---

OpenAI caches the full rendered context, including its own instructions, developer messages, tool definitions, and history that can contain text, images, documents, and supported audio. Reuse requires the entire rendered prefix to match. A change before a breakpoint means the suffix after that change cannot match the old entry.

Settings that affect the prefix include `model`, `tools`, `parallel_tool_calls`, `text.format`, `reasoning.effort`, `text.verbosity`, and compaction via `context_management`. A session does not guarantee a cache hit. Agents API calls follow the same caching behavior as the Responses API.

### cache-minimum-and-modes
- title: Short prompts are not cached
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

When is a prefix long enough to cache, and what does explicit mode do?

---

A prefix must meet the model's minimum cacheable length. Tokens in OpenAI's hidden system content do not count toward that minimum. For GPT-5.6 and later, the minimum is 1,024 tokens. Earlier models vary with request settings, so the page tells you not to assume one number.

Caching is on by default for supported models. For GPT-5.6 and later, explicit mode uses only breakpoints you set. If you set explicit mode and place no breakpoint, the request does not cache and does not create a cache write. Each request can create up to four cache writes. Content after the last breakpoint is billed as ordinary uncached input, which is how you avoid writing a suffix that changes every time.

### cache-lifetime-rates
- title: Cache lifetime changes the write price
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What cache lifetimes and rates does the guide state for GPT-5.6 and later?

---

In the Responses API, `prompt_cache_options.ttl` of `30m` is the default, with a write rate of 1.25 times the uncached input rate. `12h` is a minimum lifetime of 12 hours at 2.5 times. Those are total write rates, not surcharges. Reads are 0.1 times ordinary input on most of these models and 0.05 times on GPT-6.1 Sol and GPT-6.1 Terra, for either lifetime.

The minimum lifetime does not guarantee that a later request reuses the stored tensors or is faster. OpenAI may keep an entry longer than the minimum. `12h` is not a deletion deadline. Unsupported ttl values return a 400.

### earlier-cache-retention
- title: Older models use retention, not a ttl
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

How does prompt cache retention work before GPT-5.6?

---

Those models use `prompt_cache_retention`. `in_memory` typically stays active for about 5 to 10 minutes of inactivity, up to one hour. `24h` typically stays available for about 30 minutes and can be retained up to 24 hours. For models that support both, organizations without Zero Data Retention default to `24h`, and organizations with Zero Data Retention default to `in_memory`.

Earlier models only have implicit breakpoints. Reported `cached_tokens` excludes hidden system tokens and rounds down to a multiple of 128. GPT-5.6 and later can report the exact eligible boundary instead.

### cache-routing
- title: A cache lives on one machine
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Why can two identical prompts miss the cache?

---

Cached state lives on individual machines. Traffic above 15 requests per minute can overflow onto other machines. A request reuses a prefix only if it reaches a machine that still holds an unexpired match. Caches are not shared across organizations or across regional processing boundaries.

On models before GPT-5.6, a stable `prompt_cache_key` helps route requests that share a prefix. The key does not pin a machine and does not guarantee a hit. The guide suggests keeping each key near about 15 requests per minute and splitting hotter traffic across keys. On GPT-5.6 and later, routing is automatic, and separate keys are for separate cache accounting, including reducing the chance that one user probes whether another user's content was cached.

### cache-write-order
- title: Stable instructions go first
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

How should you order a prompt if you want cache reuse?

---

Put stable developer instructions and shared reference material first. Put timestamps, user-specific text, and other dynamic content at the end or in later messages. Append new turns instead of rewriting earlier ones. Summarization, compaction, or truncation changes the prefix and resets reuse.

On GPT-6 models, the guide says you can change reasoning effort with a `configuration_update` input item while leaving request-level `reasoning.effort` unchanged, so the original prefix can still match. Top-level `instructions` cannot hold an explicit breakpoint. Put reusable developer text in an `input_text` block inside a developer message if you need to mark one.

### coding-tool-done-is-not-success
- title: A tool that says done can still have failed
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What does the prompt guide warn about when a coding agent applies a patch?

---

For coding with `gpt-6-astra`, it says to define the agent's role, show structured tool use, require tests, and set Markdown conventions. It specifically says to validate patches carefully because tools such as `apply_patch` may return "Done" even on failure.

The guide also says to avoid interactive execution unless you need it, and to include concrete examples of how to invoke the functions. A tool result string is not a test suite. Ask for a command or a unit test that checks the change.

### agent-prompt-persistence
- title: Agentic prompts have to demand a finished task
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What three prompt practices does the guide give for long agent runs?

---

For agentic rollouts with `gpt-6-astra`, plan until the query is fully resolved, give a short preamble before notable tool calls, and track work with a TODO tool or a rubric. The sample instruction tells the model not to stop after only part of the request and to reflect after each function call.

That is prompting for persistence, not a platform setting that forces the loop to finish. You still cap turns, evaluate tool choice, and check that the final answer matches the tools' results.

### moderation-categories-split
- title: Harm categories are not all available on images
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

Which moderation categories apply to images as well as text?

---

The guide marks harassment, threatening harassment, hate, threatening hate, illicit, violent illicit, and sexual content involving minors as text only. Self-harm, self-harm intent, self-harm instructions, sexual content, violence, and graphic violence apply to text and images.

Illicit content is advice or instruction on committing illicit acts. The page's example phrase is "how to shoplift". Violent illicit content is that plus violence or procuring a weapon. Sexual content excludes sex education and wellness. Use the category list for policy routing. Do not treat a single `flagged` bit as a full explanation.

### azure-optional-classifiers
- title: Some Azure classifiers are optional
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

Which Azure OpenAI classifiers are optional add-ons?

---

Besides the four harm categories, the article describes optional binary classifiers for jailbreak risk and for known text or code. Protected material for text covers known items such as song lyrics, articles, recipes, and selected web content. Protected material for code covers source that matches public repositories and can be emitted without citing those repositories.

The use of those models is optional, but the article says the protected-material code model may be required for Customer Copyright Commitment coverage. They do not replace the hate, sexual, violence, and self-harm filters, and they do not run on Whisper.

### functions-intern-test
- title: A tool should pass the intern test
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

How does the function-calling guide say you should test a tool definition?

---

Apply an intern test: could a person use the function correctly with nothing except what you gave the model? If they would ask a question, add the answer to the prompt. Keep functions predictable. The guide's invalid example is a light toggle with separate on and off booleans, which allows impossible calls.

Offload work the model should not do. If you already know the order id, do not make the model pass it. Define a function with no such parameter and inject the id in your code. Generate and iterate on schemas in the Playground, and consider fine-tuning when you have many functions or a hard calling task.

### streaming-function-arguments
- title: Streamed tool arguments arrive in pieces
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What does streaming add to function calling?

---

Set `stream` to true and you receive events as the model fills the function call. The guide says you can show which function is being called and display the arguments as they arrive, the same way you stream ordinary text.

The stream is how you show progress while the model fills the call. The tool-calling flow on the same page still has your application execute the function and return `function_call_output` with that call's `call_id`. Displaying arguments as they arrive does not run the tool.

### schema-key-quality
- title: Schema names are part of the prompt
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

How does the Structured Outputs guide say you should name schema fields?

---

Name keys clearly, and add titles and descriptions for important fields. Use evals to decide which structure works. Structured Outputs removes the need to plead for braces, and it does not remove the need to say what each field means.

Chain-of-thought can be a schema: an array of steps with an explanation and an output, plus a final answer. That structures the reply. It does not prove the arithmetic. You still check the values.

### json-mode-edge-cases
- title: JSON mode has three incomplete outcomes
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Which edge cases does the JSON mode guide tell you to handle in code?

---

If status is incomplete because of `max_output_tokens`, the JSON can be cut off because the conversation was too long for the window. If a message content item has type `refusal`, the safety system refused and you should read the refusal text instead of parsing JSON. If status is incomplete because of `content_filter`, generation stopped and the JSON may be partial.

When status is completed and you did not set stop tokens, the guide says the content should be the serialized JSON object. If you did set stop tokens, check whether the text ends with one of them. Network errors are a separate failure from all of these.

### fine-tune-hyperparameters-shown
- title: A finished fine-tuning job reports how it trained
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What does a succeeded fine-tuning job object tell you?

---

Polling the job id returns status, the base `model`, the `fine_tuned_model` id, the training file, and hyperparameters. The guide's succeeded example includes `n_epochs`, `batch_size`, and `learning_rate_multiplier`, plus `trained_tokens`. The method type in that example is supervised.

The model id begins with `ft:` and is what you pass to Responses or Chat Completions. Checkpoints expose `step_number` and metrics such as validation loss and token accuracy so you can pick an earlier epoch. The example metrics are measurements of that checkpoint, not a promise about your data.

### eval-objective-examples
- title: Write the success test before the metric
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What does a concrete eval objective look like in the guide's examples?

---

For transcript summaries, the objective is to compete with reference summaries on relevance and accuracy, using production feedback and expert-written references, with a stated ROUGE-L bar and a coherence score from G-Eval. For questions over documents, the objective is a precise answer that uses the needed context and satisfies the user, with context recall, context precision, and a rate of positively rated answers.

Those numbers are examples of how to define a metric, not universal pass marks. Copy the shape: a held-out set, a score you can recompute, and a comparison when the prompt changes. Do not treat a metric you have not calibrated against people as the product requirement.

### single-turn-versus-agent-eval
- title: Tool evals check the call, not only the prose
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What extra questions appear when you evaluate an agent?

---

Tools are developer-defined code the model can execute, from a helper to an API call. The guide says to evaluate tool selection, such as whether an order-status question invokes the order lookup tool, and data precision, such as whether the order id extracted from the conversation is the argument that was sent.

Workflows can be scored step by step: extract an id, look it up, then phrase the reply. Multi-agent systems add handoff accuracy, including whether a topic change returns control to the triage agent. A fluent final sentence can hide a wrong tool or a wrong argument.

### safety-limit-output
- title: Limit input length and output tokens
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

Why does the safety guide tell you to cap user input and output length?

---

Limiting how much text a user can put in the prompt helps avoid prompt injection. Limiting output tokens reduces the chance of misuse. Narrowing inputs or outputs, especially to trusted sources, reduces how far misuse can go.

A dropdown of known values is safer than open text. Returning a vetted support article is safer than answering from scratch. Users should also have a monitored way to report bad behavior. None of these replace evals on the inputs your real customers send.

### know-the-limits
- title: Say what the model is bad at
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

What does the safety guide say you should tell users about limitations?

---

Models may hallucinate, produce offensive output, or show bias, and they may be unfit for a use case without significant changes. Evaluate the API on a wide range of inputs, including the inputs your customers will actually send, and calibrate their expectations.

Human reviewers need the source material. If the product summarizes notes, the reviewer should be able to open the notes. High-stakes decisions and generated code are called out as places where that review matters most.

### concepts-rough-token-rule
- title: The English token rule of thumb
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/concepts

What rough conversion does OpenAI give for English text and tokens?

---

As a rough rule of thumb, 1 token is about 4 characters or 0.75 words for English text. The advanced usage guide uses the same approximation and shows that "ChatGPT is great!" encodes as six tokens, including pieces of the word ChatGPT and the exclamation mark.

Code, other languages, and identifiers split more finely. The concepts page says tokens in some languages can be shorter than one character or longer than one word. Use the approximation for a back-of-the-envelope check, then measure with the tokenizer or the `usage` field.

### tiktoken-without-a-call
- title: Count tokens without an API call
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

How can you estimate tokens before you send a request?

---

The advanced usage guide says to use the tiktoken Python library to see how many tokens are in a string without making an API call, and it points at the cookbook for examples. There is also a tokenizer tool for specific strings.

For chat messages, a string count is not the whole bill. Formatting around role and name adds tokens, and future models may not match a counter written for an older snapshot. Confirm with `usage` on a real response when the estimate is close to the limit.

### optimization-loop
- title: Optimize by hypothesis, then re-evaluate
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What loop does the accuracy guide say you should repeat?

---

Evaluate, hypothesize which lever to pull, apply it, evaluate again, and reassess. The guide's sample path is a prompt, then static few-shot examples for consistency, then retrieval so examples arrive dynamically, then a fine-tune on 50 or more examples, then retrieval tuning and a fact-check for hallucinations, then another fine-tune that includes the retrieval inputs.

That path is an example of matching the lever to the failure, not a required sequence. If evals say the model already has the knowledge, more context is the wrong next step.

### retrieval-noise
- title: Extra passages can cause hallucinations
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

How can retrieval itself make answers worse?

---

The guide says you can supply the wrong context, so the model cannot answer, or supply too much irrelevant context, which drowns the real information and causes hallucinations. Fixes it lists include returning the right results, less noise, and more useful information inside each result.

RAG only solves in-context gaps. If the failure is that the model will not perform the task consistently, the guide says to turn to fine-tuning. Adding a vector search step does not grade faithfulness by itself.

### representative-training-rows
- title: Fine-tuning rows must look like production
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What is the most common fine-tuning data pitfall the accuracy guide names?

---

Non-representative training data, where formatting or form differs subtly from what the model sees in production. If the live system uses RAG, fine-tune on examples that already contain that retrieved context so the model is not learning how to use the context zero-shot.

Quality matters more than quantity on top of a foundation model. Start with 50 or more examples, evaluate, and add rows only while the remaining errors are consistency or behavior. Keep the prompt-engineering eval as the baseline so you know the training helped.

### latency-do-not-default-to-llm
- title: Some answers should not be generated
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

When does the latency guide say to skip the model?

---

If the output is highly constrained, hard-code it. Confirmations, refusals, and requests for standard input are the examples, and you can store a few variations. If the input is constrained, such as a category, precompute responses and avoid showing the same one twice.

Summaries of metrics, reports, or search results are sometimes clearer as ordinary UI. Binary search, caching, hash maps, and ordinary complexity still apply. A model call is a latency choice, not the default for every string on the screen.

### latency-tradeoff-test
- title: Fewer calls can lose to a faster model
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

How do you choose between one large call and two smaller ones?

---

The guide's support-bot example faces a conflict: one GPT-4 request avoids a round trip, while splitting classification onto a smaller model processes most tokens faster and adds a request. The right side depends on how many tokens sit in the final answer, how much faster the small model is, and how much the extra request costs.

Decide with production examples, not with the principle alone. In that example they also shortened JSON field names and moved explanations into the prompt, which cut output tokens. Very short names can hurt quality, so test that too.

### parallel-with-retrieval
- title: Independent retrieval and classification can overlap
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

When can a reasoning step run at the same time as retrieval?

---

In the guide's example, once the reasoning prompt no longer needs the retrieved context, it can be fired in parallel with the retrieval prompts. Steps that do depend on each other stay sequential, or they get merged into one prompt.

The guide also combines a query rewrite and a "do we need retrieval" check into one smaller model call because both are well defined. Open-ended assistant replies are the part it leaves on the larger model. Measure the split. A parallel schedule that drops the needed context is slower in product terms because the answer gets worse.

### eval-log-and-agree
- title: Mine logs and calibrate the judge
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

Why does the eval guide tell you to log while you develop?

---

Logs are where later eval cases come from. The guide says to log as you develop so you can mine failures, then grow the set over time as production shows new nondeterministic cases.

Automated scores need a human agreement check. The guide's recommendations for human rubrics include several rounds of review, examples of what a low, middle, and high score look like, a pass-fail threshold beside the number, and consensus across reviewers. A judge that disagrees with those labels is not ready to gate releases.

### multi-agent-from-evals
- title: Add agents when evals say the single agent fails
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

When does the eval guide say a multi-agent design is justified?

---

As you add tools and tasks, one agent may struggle to follow instructions or pick the right tool. Several specialists plus a handoff can address that, and the handoff is a new place for nondeterminism. The guide says to make that split because evals show the need.

Starting with multiple agents adds complexity that can slow time to production. Score handoff accuracy: the right specialist for the request, and a return to triage when the topic changes. A circular handoff is one of the edge cases it tells you to test.

### embedding-billing
- title: Embeddings are billed on input tokens
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

What do you pay for when you create an embedding?

---

The embeddings guide says requests are billed based on the number of tokens in the input, and usage is priced per input token. The sample response includes a `usage` object with `prompt_tokens` and `total_tokens`. There is no completion string to bill.

The page also shows a pricing comparison table with pages per dollar and an MTEB score, and it says the page counts assume about 800 tokens per page. Use the pricing page for current rates. Do not treat a table in a guide as a quote you can hard-code into a contract without checking that page.

### embedding-v3-models
- title: Third-generation embedding model ids
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

Which embedding models does the guide tell you to call?

---

It says OpenAI offers two third-generation models, marked by `-3` in the id: `text-embedding-3-small` and `text-embedding-3-large`. The comparison table also lists `text-embedding-ada-002`. You send the model name to the embeddings endpoint with the input string.

The response contains the vector and metadata, including the model id and token usage. You can store the vector in a vector database. The guide's use cases on that page include search, recommendations, classification, regression on the vectors, clustering, and visualization. The vector is an input to those algorithms, not the user-visible answer.

### owners-of-embeddings
- title: You own the embeddings you create
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

Can you store or publish vectors from the OpenAI embeddings API?

---

The FAQ says yes. Customers own their input and output, including embeddings. You are responsible for making sure the content you send does not violate the law or the Terms of Use.

Ownership is not a quality claim. The same FAQ says the v3 embedding models lack knowledge of events after September 2021, which can reduce performance in edge cases. A vector you own can still rank a stale or wrong passage near the query.

### tool-output-string
- title: Tool results go back as strings you design
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What should you put in a function call result?

---

The `function_call_output` should typically be a string. The format is up to you: JSON, an error code, or plain text. The model interprets that string. If there is no return value, still return a string that says whether the action succeeded or failed.

For images or files, you can pass an array of image or file objects instead. Include the `call_id` so the result is tied to the specific call. Then send the tool definition, the original prompt, the call, and the output back to get a text answer or another call.

### allowed-tools-for-cache
- title: Restrict tools without rewriting the tool list
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Why does the guide suggest `allowed_tools` instead of deleting tools from the request?

---

`tool_choice` of type `allowed_tools` limits which of the provided tools the model may call, while you keep passing the same tool list. The guide says that lets you maximize savings from prompt caching, because changing tool names, descriptions, schemas, or ordering changes the cached prefix.

You can set the mode inside that object, such as auto, and list the function names that remain callable. This does not defer loading. Tool search is the feature for keeping unused tools out of context. `allowed_tools` only constrains calls among tools that are already on the request.

### structured-outputs-libraries
- title: SDKs can turn a class into a schema
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

How do the official libraries express a response schema?

---

The REST API accepts JSON Schema. The Python library can take a Pydantic model, and the JavaScript library can take a Zod object. The Ruby SDK can use a Sorbet struct and return typed parsed results. The guide shows `responses.parse` returning `output_parsed` for that path.

The schema still has to be in the supported subset. A Pydantic or Zod type that compiles to an unsupported shape, such as a top-level `anyOf`, will not become a valid Structured Outputs schema just because it type-checks in your language.

### anyof-nested-only
- title: anyOf is allowed below the root
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Where can you use `anyOf` in a Structured Outputs schema?

---

`anyOf` is a supported type, and the nested schemas must each be valid under the same subset, including closed objects and required fields. The root of the schema cannot be `anyOf`. It has to be an object.

Definitions and recursive schemas are supported. The page shows a linked-list style recursion as a valid pattern. Recursion still has to respect the 10-level nesting limit and the property-count limit. A recursive schema that blows those limits is rejected.

### sft-four-steps
- title: Fine-tuning is data, upload, job, eval
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What are the four parts of a supervised fine-tuning job?

---

Build a dataset that defines the good output, upload the JSONL file of prompts and desired outputs, create a job that trains a base model on that file, and evaluate the fine-tuned model. The guide says to set up evals first so you can tell whether the new model beats the base model.

You can watch status in the dashboard or by polling the job id. The dashboard shows status, checkpoints, the message, and metrics. Iterate on the prompt, the data, and the job. The guide says the best way to fine-tune is to keep iterating, not to treat the first job as final.

### sft-safety-categories-not-enough
- title: Platform safety checks are not your eval
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

Does passing OpenAI's fine-tuning safety check mean the model is safe for your product?

---

The check covers 13 categories with predefined thresholds and can block deployment. The guide says those evaluations cover a broad range and that you should still evaluate the fine-tuned model for your use case.

If a category fails, the job explains which thresholds missed, and the events endpoint can return `moderation_checks` with category results. Use that to target more training data. A pass means those platform thresholds were met. It does not score your task accuracy.

### claude-tool-thinking-signature
- title: Do not edit a thinking block you send back
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What must you preserve when you return a Claude tool result during thinking?

---

You must return the entire unmodified thinking block that accompanies that tool request, including its signature. The API verifies authenticity with a cryptographic signature and returns an error if you modify the block. This is the case where you have to send thinking blocks back.

On models that strip previous thinking, that block is required for the tool cycle and is then dropped on a later user turn. On models that keep it, it stays unless you clear it. Interleaved thinking, which lets the model think between tool calls, is automatic on adaptive-thinking models. The page says some earlier Claude 4 models need a beta header, and Haiku 4.5 does not support it.

### claude-compaction-beta
- title: Compaction summarizes instead of dropping the chat
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What is server-side compaction on Claude?

---

The context-window page says server-side compaction is the primary strategy for long-running conversations and agent workflows. It summarizes earlier parts of the conversation on the server so the chat can continue past the window. It is in beta for Claude 4.6 and later models and for Claude Mythos Preview.

Context editing is the more specialized option: clear old tool results, or clear thinking blocks. Neither feature makes a long, noisy prompt as reliable as a short, relevant one. The page still describes context rot as tokens grow.

### prompt-cache-dashboard
- title: Cache hits are something you measure
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

How do you tell whether prompt caching is working?

---

The guide says caching is enabled by default on supported models and points you at the Prompt Caching Dashboard for cache-read hit rate and at Prompt Cache Diagnostics for misses. A reused session prefix can preserve a shared prefix, and it does not guarantee a hit.

Look at cached input tokens on the response, and remember that on models before GPT-5.6 the reported cached-token count rounds down to a multiple of 128 after hidden system tokens are removed. A low number can mean a real miss or that rounding. Diagnostics are how you tell them apart.

### cache-not-shared
- title: Caches do not cross organizations or regions
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Can one organization reuse another organization's prompt cache?

---

No. The guide says caches are not shared across organizations and cannot be reused across regional processing boundaries. Even inside one organization and region, the request has to land on a machine that holds a matching unexpired entry.

Prompt caching may store encrypted key-value tensors in GPU-local storage as application state. That is why retention and routing show up as product settings. It is also why a cache hit is not a data-sharing feature between customers.

### azure-filter-languages
- title: Azure harm filters were tested on eight languages
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

Which languages were the Azure harm classifiers trained and tested on?

---

The article says the hate, sexual, violence, and self-harm models were specifically trained and tested on English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. The service can run on many other languages, and quality might vary.

In all cases you should test your application. A filter score in an unlisted language is not the same evidence as a score in a listed one. The article also says API configuration and application design can change completions and therefore change filtering behavior.

### azure-severity-annotations
- title: Safe severity is visible and not blocked
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What do Azure's four severity levels mean for filtering?

---

Hate, sexual, violence, and self-harm are each scored safe, low, medium, or high. Content at safe severity is labeled in annotations, is not filtered, and that level cannot be configured away. At the GPT default, low is also not filtered, while medium and high are.

Annotations can show severity even when nothing was blocked. A response that completed does not mean every category was safe. Read `content_filter_results` if you need the severity, and do not infer safety only from HTTP 200.

### hallucination-quote-then-answer
- title: Quote the source before you analyze it
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

What grounding steps does the Claude guide recommend for long documents?

---

For documents longer than 20k tokens, ask for word-for-word quotes first, and say what to do if no relevant quote exists. Then analyze only from those quotes. A second pattern drafts from the documents, then requires a supporting quote for each claim and removes the claim if none exists.

You can also tell the model to use only the provided documents and not its general knowledge, and to say it does not know. The guide says these steps reduce false statements and do not remove them. High-stakes facts still need a check outside the model.

### best-of-n-is-not-a-vote
- title: Repeated answers can reveal instability
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

What is best-of-N verification in the Claude hallucination guide?

---

Run the same prompt multiple times and compare outputs. Inconsistencies can indicate hallucinations. Iterative refinement uses one output as the input to a follow-up that verifies or expands it, which can catch contradictions.

Agreement is not labeled as proof. The page says the techniques do not eliminate hallucinations and that you should validate critical information. Use disagreement as a reason to check the source, not as a majority vote that replaces the source.

### embedding-provider-choice
- title: Pick an embedding model for the domain
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/embeddings

What should you compare before you choose an embedding provider?

---

The Anthropic page lists dataset size and how relevant the training data is to your domain, inference speed and end-to-end latency, and customization such as continued training on private data or specialization for a vocabulary. Larger or more domain-specific data generally produces better in-domain embeddings.

It then documents Voyage models, including general-purpose, code, finance, and legal variants, plus rerankers. The page says to assess a variety of vendors. A model name on that list is not a claim that it is the right index for every corpus.

### voyage-context-and-rerank
- title: Chunk embeddings and rerankers are different tools
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/embeddings

What do contextualized embeddings and rerankers add, according to that page?

---

Contextualized chunk models produce chunk-level vectors that capture full-document context without manual metadata. The page says to call them with `contextualized_embed` rather than `embed`. `voyage-context-4` is listed with a 120,000-token context when auto-chunking is on. Otherwise the total tokens across inputs cannot exceed 32,000.

A reranker takes a query and a list of documents and returns them ranked by relevance, via `rerank`. The page recommends `rerank-3` for accuracy and a lite variant for latency and cost. Reranking does not replace the embedding step. It reorders candidates you already retrieved.

### azure-finetune-versus-few-shot
- title: Azure fine-tuning shortens the live prompt
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning

Why can a fine-tuned Azure model be cheaper per call than a few-shot prompt?

---

Few-shot learning puts examples in the prompt. Fine-tuning trains on more examples than fit there and adapts weights, so you include fewer examples or instructions on later calls. The article says that means less text and fewer tokens each call, which can lower cost and latency, especially with smaller models.

You still pay for the training run, and you still have to deploy and evaluate. The article's quality warning is that a large set of unpruned internal data can make the model worse than you expect. Token savings do not repair bad labels.

### openai-data-not-used-for-training
- title: API data is not training data by default
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/concepts

Does OpenAI train on what you send to the API?

---

The concepts page says protecting user data is fundamental and that OpenAI does not train its models on inputs and outputs through the API. It points to the API data privacy page for the details.

That statement is about training. It is not a statement that prompts are free of retention, moderation, or abuse monitoring. Safety identifiers, moderation requests, and fine-tuning uploads are separate flows described in their own guides. Read the privacy page before you make a retention promise to a customer.

### programming-a-gpt
- title: GPT here means a text generation model
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/concepts

What does the concepts guide mean by a GPT model?

---

It says OpenAI's text generation models are often called generative pre-trained transformers, or GPT models. Examples it names include `gpt-6-astra` and `gpt-5.6-terra`. They were trained to understand natural and formal language and they return text for a prompt.

An embedding model is a different endpoint. It takes a string and returns a vector meant to preserve content or meaning, and similar chunks land closer together. Do not send generation parameters to an embeddings call and expect a paragraph back.

### presence-penalty-formula
- title: Penalties edit logits before sampling
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

How are frequency and presence penalties applied?

---

They modify logits, the un-normalized log probabilities, with an additive term. For token j, the guide subtracts the count of prior samples of that token times the frequency coefficient, and subtracts the presence coefficient if that count is greater than zero.

So presence fires once a token has appeared, and frequency scales with repetitions. The guide says you can use negative coefficients to encourage repetition. This is a sampling control. It does not retrieve a fact or enforce a schema.

### long-conversation-formatting
- title: Chat token counts are model-specific
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

Why is it hard to predict tokens for a chat transcript?

---

Chat models use tokens the same way completion models do, but message-based formatting makes the count harder. The guide gives a counter for `gpt-3.5-turbo-0613` and warns that future models may deviate, so the function may be only approximate. If the model is unknown to tiktoken, that sample falls back to the `cl100k_base` encoding.

The practical rule on the page: if the conversation exceeds the model's maximum, truncate, omit, or shrink text until it fits. The example maximums it names are 4097 tokens for `gpt-3.5-turbo` and more than 128k tokens for `gpt-4o`. Those are examples of limits, not a limit you should assume for every current model.

### accuracy-prompt-strategies
- title: Prompt tactics map to context or behavior
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

Which prompt strategies does the accuracy guide sort into context versus behavior?

---

Its table marks clear instructions and giving the model time to think as LLM optimization. Providing reference text and using external tools are context optimization. Splitting complex tasks and testing changes systematically are marked as both.

That sorting is how you choose the next experiment. A formatting failure is not fixed by pasting a longer policy. A missing policy is not fixed by asking the model to think step by step. Test one change against the eval set so you know which strategy moved the score.

### production-accuracy-ux
- title: Higher accuracy can cost latency or handoffs
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

How does the accuracy guide say you should absorb the errors you still have?

---

Once the business has priced failure, the technical job is to fail in a way that does not wreck the experience. The guide's examples are asking the customer for more information when the model is unsure, letting a later step send the case back to intent detection, and handing off to a human when intent is unclear.

Those choices can make the first attempt less accurate and the second attempt better, or they spend the operational savings to avoid churn. The UX gets slower or more human. Feed that cost back into the same business model that set the accuracy target.

### moderation-inline-fields
- title: Inline moderation returns input and output
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

Where do generation-time moderation scores appear?

---

Pass a top-level moderation object, including the model, on the generation request. The Responses API returns `response.moderation.input` and `response.moderation.output`. Those use the same category fields as a standalone moderation result.

Check the result type before you read scores. Either side can be an error if that step does not complete. Standalone classification uses the moderations endpoint and does not generate a model answer. Use that when you only need a label.

### safety-red-team
- title: Red-team the feature, including injection
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

What does adversarial testing mean in the safety guide?

---

Red-team the application over a wide range of inputs and user behaviors, both a representative set and attempts to break it. The page asks whether the product wanders off topic and whether someone can redirect it with a prompt injection such as telling it to ignore the previous instructions.

Prompt engineering that fixes topic and tone, plus a few high-quality examples, reduces undesired content even when a user tries to produce it. It is not a proof that injection is impossible. Pair the tests with a way for users to report problems and with a human who answers those reports.

### claude-image-budget
- title: Images can exhaust the request before tokens do
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What non-token limit does the Claude context page put on images and PDFs?

---

A single request can include up to 600 images or PDF pages, and 100 for models with a 200k-token window. If you send many images or large documents, you might hit request size limits before the token limit.

Image tokens are included in the context-awareness budgets on the models that receive them. Tool definitions also count. To shrink that part of the request, the page points at managing tool context or deferring definitions with the tool search tool. A 1 million token window does not mean 1 million tokens of images will be accepted as one request.

### claude-stop-reason
- title: Running out of window is a stop reason
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

How is a Claude context overflow different from a validation error?

---

Input that is already too long is a 400 on every model. On Claude 4.5 and newer, input plus `max_tokens` may exceed the window and the API still accepts the call. Generation then stops with `model_context_window_exceeded` if it actually hits the limit. Earlier models reject that request unless you send the beta header the page names.

`max_tokens` includes the thinking produced on the current turn and is a hard cap. Plan the output budget with the token counting API, especially for multi-turn sessions that include thinking and tool results. A stop reason is a completed HTTP call with a truncated generation. A 400 is a request you must shrink before it will run.

### cache-explicit-slots
- title: Implicit mode spends one of four write slots
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

How do implicit and explicit breakpoints interact on GPT-5.6 and later?

---

Implicit mode places a breakpoint at the end of the latest eligible message. Eligible messages are a user message, the last tool response in a consecutive group, and the last developer message in the initial consecutive developer group. You can add explicit breakpoints without turning implicit mode off. The implicit breakpoint uses one of the four write slots, leaving three for explicit breakpoints.

Explicit breakpoints can keep prefixes that change at different rates, such as a 12-hour instruction prefix and a 30-minute session prefix. A breakpoint covers the whole prefix before it. Within one request, each token is billed once at the longest lifetime of the writes that cover it. Upgrading 30-minute coverage to 12 hours charges a new 12-hour write without credit for the earlier write.

### cache-read-refresh
- title: A cache read can refresh the lifetime
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What does a cache read do to the entry's lifetime?

---

A 30-minute read refreshes coverage to at least 30 minutes after that read. If the entry already has valid 12-hour coverage, the read keeps the later of the existing expiry and 30 minutes after the read. It does not restart a 12-hour clock and it does not charge another write.

Lookups walk from the longest prefix to the shortest, only at lookup boundaries. In explicit-only mode those boundaries are the first two and the latest 50 explicit breakpoints. A breakpoint you placed but that falls outside those lookup rules is not a hit you can count on. The page documents the boundary list so you can see why a long conversation stopped matching.

### function-call-flow-five
- title: Tool calling is a five-step loop
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What are the five steps of a tool-calling conversation?

---

Make a request that includes tools the model could call. Receive a tool call. Execute your code with the arguments. Make a second request that includes the tool output. Receive a final response, or more tool calls.

With the Responses API you can continue that loop for as many calls as the task needs. The model does not run your database or your refund function. If you stop after the first response, you have a request for an action, not the action's result.

### namespaces-reduce-confusion
- title: Namespaces separate similar tools
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Why does the function-calling guide suggest namespaces?

---

A namespace groups related tools by domain, such as CRM, billing, or shipping. That matters when the model must choose between tools that serve different systems, for example one search tool for the CRM and another for the support desk.

A namespace has a name, a description, and a list of tools. A tool inside it can set `defer_loading` so it is not loaded up front. The guide says the namespace description should stay concise because it helps the model decide what to load, while the function description helps it call the loaded tool correctly.

### structured-output-on-batch
- title: Schema adherence is an API feature, not a prompt trick
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Where can you turn on Structured Outputs?

---

The comparison table says Structured Outputs and JSON mode are supported in the Responses API, Chat Completions API, Assistants API, Fine-tuning API, and Batch API. You enable schema adherence with a `json_schema` text format and `strict` true, or with strict function calling.

JSON mode only promises JSON that parses, aside from the edge cases the guide tells you to handle. If the model snapshot is older than the ones the table lists for schema mode, use JSON mode and validate. Do not describe a prompt that says "return JSON" as Structured Outputs.

### azure-streaming-filter
- title: Azure streaming can stop mid-answer
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What should a streaming client do when Azure filters a completion?

---

Segments are returned as they complete. Streaming continues until a stop token, a length limit, or content classified at a filtered category and severity. The last chunk includes `finish_reason`, and that value is `content_filter` when the generation was filtered.

The article says the returned content might be incomplete, and how you react is application-specific. Do not treat a partial stream as a full answer when the finish reason says the filter stopped it. A prompt that is itself filtered never starts that stream. It returns HTTP 400.

### azure-enqueued-filter-error
- title: A missing filter is reported on the result
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What if Azure's content filter does not run?

---

If the content filtering system is down or cannot finish in time, the article says the request can still complete without filtering. You detect that by an error message in the `content_filter_result` object, with a code the sample identifies as a content filter error.

A successful HTTP status is not proof the filter ran. Check that object before you tell a user the text was screened. The same article says you should design for filtered, incomplete completions as a normal branch.

### eval-deprecate-does-not-end-measurement
- title: Measure the app even if a product is deprecated
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

Does the Evals platform timeline remove the need for a test set?

---

The guide separates the hosted platform, which it says will become read-only and then shut down on the dates it lists, from the practice of evaluation. The practice is a dataset, a metric, a comparison, and continuous runs when something changes.

It also says evals are one of the only ways to improve an LLM application's performance, through fine-tuning. The page's anti-pattern is deciding from "it seems to work" or waiting until after you ship. Keep a scored set and hold the inputs fixed while you change the prompt.

### fine-tune-efficiency
- title: Fine-tuning can buy a smaller prompt
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

How can fine-tuning reduce tokens without being a knowledge store?

---

One of the two reasons in the accuracy guide is efficiency: the same accuracy with fewer tokens or a smaller model. Later it says you can use fine-tuning to replace instructions and few-shot examples with many training examples so the behavior is in the weights.

The other reason is accuracy on a learned-memory task, by showing many correct examples. The same guide assigns recent or specialized context to retrieval, not to the weight update. Fine-tuning replaces instructions and examples. It does not, in that split, insert a document that changes after training.

### tools-are-not-knowledge
- title: A tool is how you leave the training data
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Why give a model a tool instead of asking it to recall the fact?

---

The guide says tool calling reaches data and actions outside the training data. The examples are today's weather, an account for a user id, and a refund for a lost order. The model may decide it needs that capability to follow the prompt.

You still write the description that teaches when to call it. A weather tool does not run until your code runs it and you pass the output back. The model's message that names `get_weather` is a request. It is not today's weather.

### schema-order-is-output-order
- title: Key order in the schema is key order in the JSON
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Does Structured Outputs preserve the order of keys?

---

Yes. The guide says outputs are produced in the same order as the keys in the schema. Put the field you want to stream or display first at the start of the schema if order matters to the client.

Order is not accuracy. A required string will be present and still be wrong. Pair the schema with an eval on the values. The first call with a new schema also pays extra latency while the schema is processed, so a client that generates a unique schema per request pays that cost every time.

### moderation-free-and-separate
- title: You can moderate without generating
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

When would you call the moderations endpoint by itself?

---

Use it to classify text or images when you do not want a generated answer. The guide shows `omni-moderation-latest` with a string or with a list of text and image parts. Image URLs can be a normal URL or a base64 data URL.

Use inline moderation when you need the generation and the scores together. Either way, decide your own threshold and action: filter, review, or intervene on the account. The endpoint does not apply your product policy for you.

### safety-kyc
- title: Knowing the user reduces abuse risk
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

What does the safety guide say about accounts?

---

Users should generally register and log in. Linking an existing account such as Gmail, LinkedIn, or Facebook may help, and may not fit every product. Requiring a credit card or an ID reduces risk further.

A safety identifier then gives you a stable, hashed handle for that user in API requests. The guide says this is how you trace misuse to one user instead of having one user take down access for the organization. It is recommended, not required, for products where individuals talk to a model.

### latency-predicted-outputs
- title: Predicted outputs skip text you already know
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

What are predicted outputs for?

---

The latency guide says predicted outputs significantly reduce generation latency when you know most of the output ahead of time, such as code editing. You give the model a prediction so it can focus on the actual changes instead of the text that stays the same.

It is an inference optimization beside model size, not a correctness feature. The rest of that section notes that available compute and other inference optimizations also affect speed, and that most people cannot change the hardware. Predicted outputs are the lever it offers inside the API for this case.

### chunk-before-the-user-sees-it
- title: Moderate in chunks if you stream
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

How do you stream and still moderate or translate?

---

Stream to your backend, process chunks there, and send the processed chunks to the front end. The guide contrasts that with waiting for the entire completion before any processing. Showing the steps of a tool-using flow also lets the user see real progress.

Spinners help the perception of waiting. Streaming and chunking are the techniques it says genuinely reduce latency of the combined app and user, because the user finishes reading sooner. If you wait for the full completion before moderation or translation, you give up that gain on that hop.

### embedding-search-is-not-answering
- title: Nearest vectors are a ranking
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

What does a nearest-neighbor search over embeddings return?

---

Search is one of the listed uses: rank results by relevance to a query string. You embed the query and compare it with stored vectors. Small distance means high relatedness. The guide says to use a vector database when you need the K nearest vectors quickly.

The ranking is relatedness in that model's space. The FAQ says v3 models lack events after September 2021, so a semantically close passage can still be stale. Classification by nearest label has the same limit. It assigns the closest label you embedded. It does not check that the label is the right policy today.

### zero-shot-embedding-labels
- title: Labels can be embedded too
- version: Core
- level: intermediate
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

How does the embeddings guide describe zero-shot classification?

---

The use-case section includes classification by the most similar label, and a later section on zero-shot classification using embedding features. You embed the text and the label descriptions and pick the nearest label. The same page also shows embeddings as input features for ordinary regression and classification models.

The label set is yours. If two labels are worded similarly, their vectors will be close and the boundary will be unstable. Relatedness is not a calibrated probability. Use a held-out set if you need to know how often the nearest label is the right one.

### developer-message-examples
- title: Put few-shot examples in the developer message
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

Where does the prompt guide put few-shot examples?

---

Typically in a developer message, with an identity, instructions, and examples that pair an input with the exact output you want. Its sentiment example tells the model to emit only one of three words and then shows three reviews with those labels.

Diverse inputs matter more than repeating one happy sentence. The guide also says to keep content you will reuse at the beginning of the prompt and among the first JSON fields, so prompt caching can reuse that prefix. Examples that change every request belong after the stable instructions.

### pin-the-snapshot
- title: Pin a model snapshot before you trust a prompt
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

Why does the prompt guide tell you to pin a snapshot?

---

Different model types need different prompting, and different snapshots in the same family can produce different results. Pin production applications to a specific snapshot so behavior stays consistent, and build tests that measure the prompt when you iterate or upgrade.

The page's example snapshot is `gpt-4.1-2025-04-14`. A floating alias can move. When it moves, your eval suite is how you notice. Prompt changes and model changes should not be judged from one chat transcript.

### cache-write-not-additive
- title: A cache write replaces the input rate
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Is a cache write an extra charge on top of normal input tokens?

---

No. The guide says cache-write pricing is not an additive fee. Input tokens use the uncached-input rate, the cached-input rate, or the cache-write rate. For GPT-5.6 and later, a 30-minute write is 1.25 times the uncached rate and a 12-hour write is 2.5 times, and those figures are the total write rates.

It also walks the break-even. At the 0.1 times read rate with 30-minute writes, one write and one full reuse cost 1.35 times the ordinary input, versus 2 times if you processed the prefix twice with no cache. Ten requests with one write and nine reads cost 2.15 times, versus 10 times without caching. Those comparisons are on the page for that rate. Other models have their own cached-input rates.

### hidden-tokens-and-minimum
- title: Hidden instructions do not fill the cache minimum
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Do OpenAI's hidden system tokens help you reach the cache minimum?

---

No. The guide says tokens in the hidden system content do not count toward the minimum cacheable prompt length. For GPT-5.6 and later you still need 1,024 visible input tokens before a prefix can be cached. Earlier models vary with tools, images, output schemas, reasoning effort, and verbosity.

On earlier models, implicit breakpoints are counted from the beginning of the hidden system message, and only breakpoints at or beyond the minimum, counted from the end of the hidden context, are eligible. A short instruction plus a short user question will not cache, no matter how stable it is.

### tool-definitions-break-cache
- title: Editing a tool schema busts the cache
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What tool edits invalidate a cached prefix?

---

The settings table says `tools` changes the prefix when you change tool names, descriptions, schemas, ordering, or tool-specific instructions. `parallel_tool_calls` can change instructions about calling multiple tools. `text.format` adds output-format instructions and the schema.

So a deploy that reorders functions or tweaks a description is a cache miss even if the user message is identical. The function-calling guide's `allowed_tools` option exists so you can narrow calls without editing that list. Keep the rendered tool block byte-stable if you care about the hit rate.

### compaction-resets-cache
- title: Compaction saves the window and spends the cache
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What does compaction do to prompt caching?

---

`context_management` compaction replaces earlier conversation content with a compacted context. The caching guide says that can prevent reuse from the first changed token onward. The prompt-engineering and caching pages both tell you to append history rather than rewrite it if you want the prefix to match.

Compaction is still the tool for a conversation that will not fit. The trade is explicit: you buy room in the window by changing the prefix, so the next turn processes that new summary as a cache miss. Put the stable instructions before the part you expect to compact.

### azure-harm-categories
- title: Azure's four harm categories
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What kinds of harm do Azure OpenAI's main filters cover?

---

Hate and fairness covers attacks or pejorative language tied to identity attributes the article lists, such as race, gender, religion, and disability, plus disparate treatment of those groups. Sexual content covers sexual language and abuse, with the article's own scope. Violence covers physical harm and weapons. Self-harm covers harm directed at one's own body.

Those four are the multi-class models with severity levels. Jailbreak, indirect document attacks, and protected material are separate, and the article marks them as optional aside from the copyright-commitment note on code. Whisper is outside this system.

### sft-good-example
- title: A fine-tuning example is a realistic pair
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What makes a good supervised fine-tuning example?

---

Use the prompts and outputs you expect in the application, as realistic as possible, with specific, clear questions and answers. Sources the guide names are historical data, expert data, logged data, or other collected data.

The file is JSONL in chat format. One line is one example, including the assistant's correct message, which may be a tool call. Ten lines is the minimum that will run. The guide's advice is that fifty careful rows teach more than a large file of vague ones, and that you should evaluate before you scale the file up.

### responses-retention-for-distill
- title: Distillation can use stored responses
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

How long does the fine-tuning guide say Responses keeps outputs for distillation?

---

It says you can capture results from the large model by whatever technique is convenient, and notes that the Responses API stores model responses for 30 days by default. You then keep the captures that meet your eval criteria and train the smaller model on those.

That default is a collection window, not a quality filter. The guide's order is: meet the eval on the large model, filter to rows that fit the criteria, then train. Training on every stored response also trains on the failures.

### gpt-models-need-explicit-steps
- title: A fast model still needs the task spelled out
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What does the prompt guide say GPT models need that reasoning models often do not?

---

GPT models are described as fast, cost-efficient, and highly intelligent, and they benefit from explicit instructions about how to accomplish the task. Reasoning models do better with high-level goals and work out the details, at the cost of being generally slower and more expensive.

The latest-model notes on that page say `gpt-6-astra` benefits from precise instructions that put the logic and the data in the prompt. Giving a GPT model only a goal, because that worked on a reasoning model, is a prompt mismatch. Rerun the eval when you switch families.

### file-search-is-rag
- title: File search is one way to add context
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

What does the prompt guide call the built-in file search tool?

---

It describes adding relevant context as retrieval-augmented generation, whether you query a vector database yourself or use OpenAI's built-in file search tool to generate from uploaded documents. The reasons it gives are proprietary or out-of-training data, and constraining the answer to resources you chose.

File search still has to fit the context window, which the page defines as the token memory of one generation request, from text through images. Model windows differ, from the low 100k range up to one million tokens for newer GPT-4.1 models. Look up the model instead of assuming the upload fits.

### eval-for-tool-arguments
- title: Score the argument, not only the tool name
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What is data precision in an agent eval?

---

Tool selection asks whether the right tool was chosen. Data precision asks whether the arguments are correct. The guide notes those arguments are usually extracted from the conversation, so the eval checks that extraction. Its example is passing the user-provided order id to the lookup tool.

A test that only checks that some tool ran will pass a call with a swapped id. Include cases with several tool calls, because the guide lists those as a source of incorrect arguments, and cases where a tool result uses an ambiguous field name.

### human-before-code-ships
- title: Generated code needs a reviewer with the source
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

Where does the safety guide say a human review is especially important?

---

Wherever you can, review outputs before they are used, especially in high-stakes domains and for code generation. Reviewers should know the system's limits and have the information needed to verify the output. The summary example is access to the original notes.

That review sits beside moderation and adversarial testing. The guide's point is that the reviewer can check the output, which means they can see the source. A summary reviewer without the notes, or a code reviewer without what the code was supposed to do, is not the check it describes.

### temperature-still-samples
- title: Penalties and seeds do not add knowledge
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

Can sampling parameters make a completion more truthful?

---

Temperature, penalties, and `seed` change which tokens are sampled or how repeatable the sample is. The advanced usage guide describes penalties as edits to logits and `seed` as a way to get mostly deterministic output when every other parameter matches. `logprobs` reports how likely those tokens were.

The page describes them as sampling controls. `logprobs` is the probability the model assigned to a token, not a check against a document. A seed can make that same token come back on the next call when the other parameters match. Repeatability is not a source of truth.

### context-window-is-not-memory
- title: The window is not the training set
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

Why can a model "forget" a fact that was in an earlier chat?

---

Anthropic's definition says the context window is working memory for the request, including the response, and it is different from the corpus the model was trained on. Previous turns stay only if you send them again. The page says each user message and assistant response accumulates and previous turns are preserved completely when they are still in the request.

If you drop a turn, compact it, or exceed the window, that text is no longer available to attend to. Chat products may manage a window with first-in, first-out. The API, the page says, does not do that for you unless you use a feature such as compaction. If the fact is not in the request, the model is not looking it up from the old conversation.

### documents-count-as-tokens
- title: Tool results and files count as context
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What besides the user message counts toward Claude's context window?

---

The system prompt, every message including tool results, images, and documents, the tool definitions, and the output, including extended thinking. Prompt-cache accounting splits input across uncached, cache-read, and cache-creation tokens, and all three count toward the window.

A long tool result can crowd out the question. The page points at tool-result clearing and at deferring tool definitions when that happens. Estimate with the token counting API before you send the turn, especially once images are involved, because you can hit size limits before the token limit.

### azure-deployment-name
- title: The Azure model field is the deployment
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings

Why does an Azure embeddings call fail when the base model name is correct?

---

The article says the `model` value is your Azure model deployment name. The samples use `text-embedding-3-small` only as that deployment's name and tell you to replace it if you named the deployment something else. A 404 is the signal to check the `/openai/v1/` endpoint and the deployment name.

Authentication is separate. Entra ID is recommended. A 401 is an audience or sign-in problem. A 403 is a missing Cognitive Services OpenAI User role. A correct model string does not fix either of those.

### filter-medium-means-low-passes
- title: Low severity still comes back
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

If Azure's default filter is on, can low-severity hate or violence reach the user?

---

Yes for the GPT default. Medium and high are filtered. Low is not. Safe is annotated and never filtered. DALL-E is different: its default threshold is low, so low, medium, and high are filtered for text prompts and image completions.

If you need to filter only high, or to disable filters, the article says that requires approval for modified content filters. Until that approval, you cannot assume the default is the strictest setting. The strictest row in the table filters low, medium, and high, and it is configurable for prompts and completions separately.

### indirect-attack-needs-markup
- title: Retrieved pages are an injection path
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

How can a retrieved document attack an Azure OpenAI prompt?

---

The article defines an indirect attack as malicious instructions a third party places in a document the model will process, also called cross-domain prompt injection. Detection requires the document to be embedded and formatted. You mark it with the `documents` delimiter so Prompt Shields can look for indirect attacks. That detection is optional.

JSON-escape the document text when you tag it. The safety system also uses chat roles to separate system, user, and assistant content. A blob of retrieved HTML stuffed into a user message is not the same signal as a tagged document.

### structured-outputs-refusals-detectable
- title: Refusals are a typed result
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

How do you detect a safety refusal when Structured Outputs is on?

---

One benefit the guide lists is that safety-based refusals are programmatically detectable. In the edge-case handling, a message content item with type `refusal` means the model refused, and the refusal field holds the explanation if one was generated. That is different from `output_text`, which is the schema-shaped payload.

Do not treat a refusal as a JSON object that failed validation and retry it blindly. Also handle `max_output_tokens`, which yields incomplete JSON rather than a refusal. The first request for a new schema is slower. That latency is not a refusal.

### strict-null-optional
- title: Optional arguments are required nullable fields
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

How do you express an optional argument in strict mode?

---

Every property must be required, and `additionalProperties` must be false. To make a value optional, set its type to an array that includes `null`, and keep the key in `required`. The guide's weather example does this for units.

If the schema does not meet those rules and you send `strict: true`, the request is rejected with the missing constraints. Omitting `strict` is not the same on every API. Responses may upgrade you into strict mode or fall back and show `strict: false`. Chat Completions stays non-strict until you set true. Set the flag explicitly so the behavior is the one you tested.

### parallel-batch-excludes-builtin
- title: Built-in tools do not batch with functions
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Can a parallel tool-call batch include web search or code execution?

---

On supported models beginning with GPT-5, the guide says functions can be called in parallel when built-in tools are also available, and built-in tools cannot be included in a parallel function-call batch. Your functions can run together. A built-in tool does not join that batch.

`parallel_tool_calls` set to false limits the turn to zero or one tool. Fine-tuned models that emit multiple function calls in one turn have strict mode disabled for those calls. Plan for a best-effort argument object in that case, and validate it before you execute.

### eval-continuous
- title: Run the eval on every change
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What does continuous evaluation mean?

---

Set it up to run evals on every change, monitor the app for new cases of nondeterminism, and grow the set over time. The workflow before that is an objective, a dataset, a metric, and a comparison.

The guide says evaluation is a journey, not a destination. Logging during development is how new cases get into the set. A one-time spreadsheet that nobody reruns is the vibe-based anti-pattern it tells you to avoid, even if the first scores looked fine.

### rouge-is-a-rough-check
- title: ROUGE is a rough change detector
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

When is ROUGE or BERTScore useful, according to the accuracy guide?

---

They can give a quick measure of how much an iteration changed the outputs. The guide says they do not correlate that closely with human reviewers. It also mentions using a model as an evaluator with a scorecard, as in the G-Eval approach it cites, when you want a more targeted automatic judgment.

The eval best-practices guide puts the same scores in a warning: do not rely only on academic metrics such as perplexity or BLEU. Use them as a fast diff, then calibrate against people before a number gates a release.

### start-with-fifty
- title: Fifty examples, then measure
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What does OpenAI say to do if the first fifty fine-tuning examples do nothing?

---

Start with 50 well-crafted demonstrations. If performance improves, add examples. If those 50 have no impact, rethink the task or the prompt before you add training data. The minimum that will start a job is 10, and the guide says the useful range it sees is often 50 to 100, with wide variation.

The guide's sequence is evaluate those 50 rows first. Adding data is the next step only when the first 50 already moved the result. A flat result means the task or the prompt is the thing to change.

### holdout-same-mix
- title: The holdout set must look like the training set
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

How should you build the holdout set for a fine-tune?

---

Carve it out of the same dataset you collected, before the job, and use it as the control group in evals. The training rows and the holdout rows should have roughly the same diversity of user inputs and model responses.

That mix is what makes the holdout a control. A holdout that is narrower than the training distribution is not the comparison the guide describes. Run the base model and the fine-tuned model on that same holdout before you decide the job helped.

### overfit-checkpoint
- title: An earlier epoch can be the better model
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What failure mode are fine-tuning checkpoints meant to catch?

---

The guide says a model can improve early and then memorize the dataset instead of learning something generalizable. It calls that overfitting. A full checkpoint is created at the end of each epoch, and only the last three epochs are kept. Each checkpoint has a step number and metrics such as validation loss and mean token accuracy.

You can call a checkpoint model id the same way you call the final fine-tune. Pick it by those metrics and by your holdout eval, not by the fact that it is the last epoch.

### latency-principles
- title: Seven latency principles
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

What are the latency guide's seven principles?

---

Process tokens faster, generate fewer tokens, use fewer input tokens, make fewer requests, parallelize, make users wait less, and do not default to a language model. The guide says these came from production applications and apply from a small workflow to a full chat product.

Generating tokens is the one it says is almost always the slowest step. Input cuts are usually a small latency win. The last principle exists so you do not send a constrained string through a model when a constant, a cache, or a UI control would do.

### max-tokens-ends-early
- title: max_tokens can cut the answer on purpose
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

How can `max_tokens` or stop tokens reduce latency?

---

The guide says they are an uncommon way to end generation early, after you have already tried asking for a shorter answer or shrinking structured output. Because output tokens dominate latency, an earlier stop saves time.

The guide calls this uncommon next to asking for a shorter answer or shrinking the structured syntax. Use it when an early stop is an acceptable answer. Cutting the generation off is a latency win only if the product can use the shorter text.

### images-are-tokens-too
- title: Images spend the same window as text
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-engineering

Does the context window count only text?

---

The prompt guide defines the context window as the memory limit of a generation request, in tokens, and it says those chunks of data run from text to images. Models differ, from the low 100k range up to one million tokens for newer GPT-4.1 models. Check the model docs for the number.

Images are part of that token budget, not a side channel. A request that is mostly images can fill the window before the instructions and the answer have room. Check the model page for the actual limit instead of reusing a number from a different model.

### safety-identifier-per-api
- title: Safety identifiers are per API
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

If you send `safety_identifier` on Responses, does Images or Realtime inherit it?

---

No. The guide says safety identifiers do not carry between APIs or sessions. Pass the same stable value separately on each Images generation or edit, and on the server-side call that creates a Realtime client secret, using the `OpenAI-Safety-Identifier` header for Realtime connections.

For Images, keep it to 128 characters or fewer. The `user` field is deprecated. A nonempty `safety_identifier` takes precedence if both are set. If the safety identifier is omitted, null, or empty, the API uses `user` when it is present. Hash the value so you are not sending a raw email or username.

### moderation-image-text-only-zero
- title: Image-only moderation zeros text categories
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

What score do text-only moderation categories return for an image with no text?

---

The guide says categories marked text only do not support image inputs. If you send only images to `omni-moderation-latest`, those categories return a score of 0. Image files are limited to 20 MB.

A zero on harassment or hate in that situation means the category was not applied to the image, not that the image was judged safe for every harm. Read `category_applied_input_types` to see which inputs the score refers to. Violence and self-harm, which support images, are the categories that can actually flag a picture.

### claude-budget-tags
- title: You do not send Claude's budget tags
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

Who inserts Claude's token-budget tags?

---

On the models with context awareness, the API injects the total budget into the system prompt and a remaining-token warning after tool calls. The page says there is nothing to enable and that you never send those tags yourself. The budget matches the window for that request, and the examples show 200k or 1 million depending on the model. Image tokens are included.

The page lists later models that do not get those tags, including Opus 4.7 and later, Sonnet 5.5, the Fable and Mythos models it names, and Haiku 5.5. For those, it points at beta task budgets. Copying the tag XML into your own prompt is not how the feature works.

### voyage-normalize-after-truncate
- title: Truncated embeddings must be normalized again
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/embeddings

How do you shorten a Voyage vector you already stored?

---

Matryoshka embeddings put a coarse-to-fine representation in one vector. To shorten at request time, pass `output_dimension`. To shorten a stored vector, keep the leading dimensions and normalize the rows again. The page's sample raises an error if a row has norm zero so you do not divide by zero.

Because the vectors are normalized to length 1, cosine similarity and the dot product rank the same. If you truncate and forget to renormalize, that equivalence no longer holds for the shortened vectors. Quantizing to int8 or binary is a different storage trade, with the page's stated 4 times and 32 times reductions, and float remains the highest precision.

### azure-jsonl-bom
- title: A UTF-8 JSONL file can still be rejected
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning

What encoding checks does Azure run on a fine-tuning file?

---

The file must be JSONL in the Chat Completions conversational format, UTF-8 with a byte-order mark, and smaller than 512 MB. The article says validation checks confirm those three things after you upload.

A JSONL file that is valid UTF-8 without a BOM fails that check. So does a file at or above 512 MB, or a file that is not conversational chat format. Separately, fewer than 10 training examples will not start the job, and 10 is still too few to expect a visible change.

### lora-is-not-full-retrain
- title: LoRA trains a smaller set of parameters
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning

What does Azure say LoRA changes about fine-tuning?

---

Low-rank adaptation approximates the original high-rank matrix with a lower-rank one and fine-tunes a smaller subset of important parameters during supervised training. The article says this keeps performance from being significantly affected, makes the model more manageable, and makes training faster and more affordable than other techniques.

That is a training method, not a data policy. You still need representative conversational examples, a validation file in the same format, and an evaluation after you deploy. LoRA does not let the model see more context at inference time than the deployment's window allows. The article's separate claim is that you can train on more examples than fit in one request.

### prompt-cache-key-accounting
- title: Cache keys can separate customers
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

What is `prompt_cache_key` for on current models?

---

Before GPT-5.6 it helps route requests that share a prefix onto the same cache, without pinning a machine or guaranteeing a hit. On GPT-5.6 and later, routing is automatic and the key is optional. You can still use separate keys so customers or users have separate cache accounting.

The guide gives a concrete risk: without separation, someone can submit candidate prompts and watch cache hits to learn whether matching content was cached before. Separate keys make that probing harder and make cached-token bills easier to explain per customer. They do not encrypt the prompt against your own organization. Caches already stay inside the organization and the processing region.

### eval-synthetic-and-production
- title: Mix production logs with expert cases
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What kinds of data does the eval guide say you can collect?

---

Synthetic data, domain-specific data, purchased data, human-curated data, production data, and historical data. The transcript example mixes user feedback on real summaries with summaries written by domain experts. The question-answering example mixes satisfaction data, expert-written answers, and historical logs.

The anti-pattern is a set that does not reproduce production traffic. Synthetic cases are allowed. They are not a substitute for the distribution you actually serve. The page also says `gpt-6-astra` is useful for collecting examples and edge cases, and that human experts should label them.

### instruction-following-conflict
- title: Test the system prompt against the user
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

What instruction-following conflict should an eval include?

---

The guide asks whether the model follows the instructions and whether it prioritizes the system prompt over a conflicting user prompt. In the retail example, the model should return only the intent label and not get pulled into answering the user's question instead of triaging it.

The same guide's edge cases include jailbreak attempts, formatting demands, and user prompts that conflict with the system prompt. A set of only polite, on-policy questions never asks the priority question. Put the conflict in the set and score whether the system instruction won.

### embedding-anomaly-and-diversity
- title: Embeddings can flag outliers
- version: Core
- level: intermediate
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

How does the embeddings guide describe anomaly detection?

---

Anomaly detection is identifying outliers with little relatedness to the other strings. Diversity measurement is analyzing the distribution of similarities. Both use the same distance idea: small distance, high relatedness, large distance, low relatedness.

An outlier is not automatically an error or a policy violation. It is far from the other vectors in that model's space. Cluster first if you need a group, and keep a human or a task-specific eval if the outlier has to trigger an action. The guide also says the v3 models miss events after September 2021, so a new kind of text can look like an outlier because it is outside the model's experience.

### recommendations-from-related-text
- title: Recommendations follow related text, not purchases
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

What does the embeddings guide mean by a recommendation?

---

Items with related text strings are recommended to each other. The vector captures relatedness of the text you embedded, such as a review or a description. The page later shows obtaining user and product embeddings for a cold-start recommendation as one recipe.

There is no purchase graph in that definition. If the text is a poor description, the neighbor is a poor recommendation. Embed the same fields at index time and query time. The Azure article states the same geometric idea: similar text produces vectors that are close together, which is what makes search, recommendations, classification, and clustering possible.

### openai-moderation-not-audio
- title: Audio is outside omni moderation
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

Can you send audio to the OpenAI moderation model described in the guide?

---

`omni-moderation-latest` accepts text and image inputs. The guide says it does not classify audio. Images can be up to 20 MB. Text and images can be sent together as a list of typed parts.

If the input is audio, this model will not classify it. Send text, an image, or both. A transcript is text and can be classified. The waveform itself is outside what this page says the model accepts.

### function-strict-first-request
- title: The first strict schema call is slower
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

Why might the first strict tool call be slower than the next ones?

---

For fine-tuned models, the guide says schemas get extra processing on the first request and are then cached. If the schema changes every request, that processing repeats and latency stays high.

Those cached schemas are not eligible for zero data retention. A unique schema per user repeats the slow first request and opts that schema out of zero data retention. Keep the schema stable if you want the cache the page describes.

### json-whitespace-trap
- title: Forgetting the word JSON can stream spaces
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

What failure mode does JSON mode have if the prompt never mentions JSON?

---

The model may generate an unending stream of whitespace, and the request can run until it hits the token limit. The API returns an error if the string JSON is absent from the context, which is there so you do not forget the instruction.

That trap is specific to JSON mode. Structured Outputs is constrained to the schema instead, and the guide says you should prefer it when the model supports it. If you stay on JSON mode, include the instruction, handle truncated JSON, and validate the shape yourself.

### accuracy-tools-are-context
- title: External tools are a context lever
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

Where do tools sit in the accuracy guide's strategy table?

---

"Use external tools" is marked as context optimization, next to "provide reference text". Clear instructions and time to think are behavior optimization. Splitting a task and testing systematically are both.

A tool call can supply a fact the model does not have. It does not, by itself, make the model's format consistent. If evals show the format is the failure, the table points you at instructions, examples, or fine-tuning. If evals show a missing or stale fact, the table points you at reference text or a tool.

### few-shot-then-retrieve
- title: Static examples and retrieved examples do different jobs
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

Why does the accuracy guide add few-shot examples before retrieval?

---

Its sample optimization flow starts with a prompt, adds static few-shot examples to improve consistency, and then adds retrieval so the examples are chosen dynamically for each input. The static examples teach behavior. The retrieved ones try to put relevant context on the request.

The Icelandic example later in the guide shows the risk of the second step. Once a fine-tune had learned the task, extra retrieved examples lowered the score because they added noise. Retrieve when the failure is missing context. Do not retrieve by habit after the eval says the behavior is already learned.

### deployment-blocked
- title: Safety thresholds can block a fine-tuned deployment
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What does a failed fine-tuning safety check look like?

---

After the job completes, each of 13 categories is compared with a pass threshold. If too many evaluated examples in a category fail, OpenAI blocks that fine-tuned model from deployment. The job message says which categories missed, and you can read them in the moderation checks section or in `moderation_checks` events.

The categories named on the page include harassment and threatening harassment, hate and threatening hate, illicit content, self-harm intent and instructions, sexual content and sexual content involving minors, violence, advice, propaganda, and sensitive or highly sensitive data. Fixing the miss means more training data aimed at that category, then your own eval on top.

### cost-of-a-wrong-refund
- title: Price the error before you chase accuracy
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

Why does the accuracy guide talk about dollars before metrics?

---

It says there is a difference between bad copy a person can fix and refunding 1000 dollars instead of 100. You should know what a failure costs and what a success saves before you discuss accuracy. Its help-desk table assigns a value to an AI-solved case, a bad escalation, and a churn event, then derives a break-even accuracy.

An accuracy of 85 percent can be acceptable in that story if the misses are early escalations and the operation still saves money. Where the miss is fraud resolved incorrectly, the human drives. The metric follows the cost. It is not a universal percentage.

### cache-fifteen-per-minute
- title: High traffic overflows the cache machine
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Why does the caching guide mention 15 requests per minute?

---

Cached state is on individual machines, and traffic above 15 requests per minute can lead to overflow routing. A hit requires the request to reach a machine that still holds the entry. For models before GPT-5.6, the guide says to aim for about 15 requests per minute in total across all prefixes that share one `prompt_cache_key`, and to partition higher volume across keys with a stable mapping.

On GPT-5.6 and later, OpenAI routes automatically and the key is not required for routing. The 15-request figure is still the overflow note for machine-local caches. A hit rate that collapses under load can be routing, not a changed prompt.

### claude-progressive-context
- title: Claude keeps prior turns only if you resend them
- version: Core
- level: beginner
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

How does a multi-turn Claude API conversation fill the window?

---

Each turn's input is all previous history plus the current user message. The output, including thinking, becomes part of the next turn's input if you send it back. The page says previous turns are preserved completely as the conversation advances. The window holds that history plus the new output. Capacity depends on the model, up to 1 million tokens for the models it lists.

The usage field reports what the request consumed. If you use prompt caching, uncached input, cache reads, and cache writes all count toward the window. Dropping history on the client is how you forget a turn. The API does not keep a server-side transcript for you unless a feature such as compaction is doing it.

### protected-material
- title: Protected material is a copyright filter, not a harm filter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What is Azure OpenAI protected-material detection?

---

Protected material for text is known content such as song lyrics, articles, recipes, and selected web content that a model might output. Protected material for code is source that matches public repositories and might be output without citing those repositories. Both are described as optional binary classifiers, separate from hate, sexual, violence, and self-harm.

The article says use of the code model may be required for Customer Copyright Commitment coverage. Owners of text can file a request to submit material for protection. This classifier does not judge whether an answer is true. It judges whether the output matches protected material the system knows about.

### schema-string-formats
- title: Some string formats are enforced
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Which string formats can a Structured Outputs schema require?

---

The guide lists `pattern` plus the formats date-time, time, date, duration, email, hostname, ipv4, ipv6, and uuid. Numbers can use multipleOf and inclusive or exclusive minimum and maximum. Arrays can use minItems and maxItems.

Those constraints are not supported on fine-tuned models. The page also says fine-tuned models lack string length, pattern, format, numeric bounds, patternProperties, and array length constraints. A schema that validates in your test against a base model can be rejected after you switch the same request to a fine-tuned model.

### eval-pairwise
- title: Ask a judge to compare, not to write
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

Why does the eval guide prefer pairwise grading?

---

It says models are better at discriminating between options than at open-ended generation, so evaluations should lean on pairwise comparison, classification, or scoring against criteria. For a model judge, pairwise comparison or pass-fail is more reliable than an unconstrained score. Position bias and verbosity bias remain. Control length, because judges tend to prefer longer answers.

Use the most capable judge you can, validate it against human labels, and only then optimize the judge for cost or latency. The page says to start with `gpt-6-astra` when you need a strong judge. A judge that has not been checked against people is another model, not a ground truth.

### red-team-and-eval-together
- title: Red-team ordinary use and break attempts
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/safety-best-practices

What does the safety guide want you to try when you red-team?

---

Test a representative set of inputs and a set that tries to break the product. The page's injection example is a user who says to ignore the previous instructions and do something else. Also ask whether the product wanders off topic.

Prompt examples and a constrained topic reduce undesired output. They are not a substitute for the test. Keep a human in the loop for high-stakes domains and for code, and give that person the source they need to check the model. Users should have a monitored way to report what the red team, and later real users, still get through.

### token-both-sides
- title: A 10-token prompt and a 20-token answer cost 30
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

How does the advanced usage guide add up a billable token count?

---

If the message input used 10 tokens and the output used 20, you are billed for 30 tokens. Input and output both count toward cost, latency, and the model's maximum. Some models charge a different price per token for input than for output. The pricing page is where those rates live. This guide does not fix a number for that difference.

The `usage` object is the authoritative split. A word-based estimate that ignores the answer will undercount both the bill and the chance of a cut-off reply.

### context-rot-curate
- title: Curate the window as it grows
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What should you do about context rot besides buying a larger window?

---

The page says accuracy and recall degrade as token count grows, so curating the context matters as much as the available space. Compaction summarizes older turns. Context editing can drop old tool results or thinking blocks. Tool search can keep unused tool definitions out of the request.

A 1 million token default on the models it lists does not cancel that degradation. Long-context requests on those models are standard-priced except Haiku 5.5 over 100,000 tokens. The cost exception is not a quality exception. You still decide what deserves to stay in working memory.

### azure-batch-token-sum
- title: A legal embedding batch can still be too big
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings

Why does Azure return 400 for embeddings when every string is under 8192 tokens?

---

The article says each current embedding input can be at most 8,192 tokens and a request array can hold at most 2,048 inputs. It also says the sum of input tokens in one request cannot exceed 300,000, even if each input is under the per-input limit. Over that sum, the request fails with HTTP 400. Split the batch.

Stay under the deployment's tokens-per-minute quota as well. A 400 after you have checked the JSON is often this aggregate, the per-item length, or the array length. A 401 or 403 is authentication or the Cognitive Services OpenAI User role, not the token sum.

### fine-tune-base-or-prior
- title: You can fine-tune a fine-tune
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

What can you pass as the base model of a fine-tuning job?

---

The guide says the `model` field can be an OpenAI model id or the id of a previously fine-tuned model. You also pass the `training_file` id from the upload whose purpose was `fine-tune`. Which models support fine-tuning is in the model docs, and the availability section says new users cannot start jobs.

The resulting id is what you call for inference, until that base model shuts down. Stacking another job on a fine-tune does not skip the holdout eval or the safety check. Each job is assessed again.

### custom-tools-free-text
- title: Not every tool is a JSON schema
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/function-calling

What is a custom tool, as opposed to a function tool?

---

A function is a tool defined by a JSON schema, so the model passes structured data to your code. The guide says custom tools work with free-form text inputs and outputs. Built-in tools are a third group: web search, code execution, MCP, and others the platform provides.

Choose the function form when you need arguments you can validate, especially with strict mode. Choose free text when the interface really is text. Built-in tools are not something you implement, and they cannot be mixed into a parallel function-call batch on the models where the guide describes that limit.

### show-steps-are-psychological
- title: A progress spinner is not faster inference
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/latency-optimization

Which user-facing latency tricks actually shorten the wait?

---

The guide says showing steps and loading states mostly change how the wait feels. Streaming, and chunking work that would otherwise wait for the full output, reduce latency of the system made of the app plus the user, because reading can start sooner.

Streaming does not reduce the time to the last token by itself. It reduces time to the first useful token. If you also need fewer tokens, ask for a shorter answer or stop early. If you need the whole answer before you can show anything, because you moderate the full text, you will not get the streaming benefit on that hop.

### system-fingerprint
- title: A new fingerprint can explain a changed answer
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/advanced-usage

What should you compare when a seeded request starts returning different text?

---

Keep `seed` and every other parameter identical, including the prompt and temperature. If outputs still diverge, compare `system_fingerprint`. The guide says a different fingerprint means OpenAI changed model configuration, and you may see different outputs because of that.

A fingerprint match does not mean the answer is true. It means the backend configuration you are comparing did not change in the way that field tracks. Pair the seed with an eval if you need to know whether the text is acceptable, not only whether it repeats.

### hate-versus-harassment
- title: Hate and harassment are different moderation labels
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

How does the moderation guide separate hate from harassment?

---

Hate is content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste. The guide says hateful content aimed at a non-protected group, and its example is chess players, is harassment. Harassment is harassing language toward any target. Threatening variants add violence or serious harm.

Both hate categories are text only. An image-only request will not produce a meaningful hate score. Use the category booleans for routing and the scores, between 0 and 1, as confidence that may need recalibration when the moderation model changes.

### docs-delimiter-escape
- title: Escape document text inside the Azure delimiter
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What does Azure tell you to do when you tag a document for indirect-attack detection?

---

Wrap the document in the `documents` delimiter so the safety system can run optional indirect-attack detection on it. The article says that when you tag unvetted documents, the document content should be JSON-escaped so parsing succeeds.

The chat roles still matter. The safety system uses the structured message list to tell system, user, and assistant content apart, and it detects jailbreak, self-harm, violence, sexual content, and hate on the latest user content. The document tag is how retrieved text gets the indirect-attack check rather than being treated as the user's own words.

### reference-text-is-context
- title: Reference text is the context lever
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What does "provide reference text" optimize?

---

In the accuracy guide's strategy table, providing reference text is context optimization, not a behavior tweak. You use it when the model lacks the knowledge, the knowledge is stale, or the knowledge is proprietary. External tools sit in the same column.

Clear instructions do not insert a missing document. If the eval failure is "the fact was not available", add the source and require the answer to depend on it. If the failure is "the fact was available and the format was wrong", the table points at instructions, time to think, or eventually fine-tuning.

### split-complex-tasks
- title: Split a task when both context and behavior break
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

Which prompt strategy does the accuracy guide say helps both context and behavior?

---

Splitting complex tasks into simpler subtasks is marked in both columns. Testing changes systematically is marked in both as well. Clear instructions and time to think are behavior only. Reference text and tools are context only.

The table is how you pick the next experiment. A missing fact points at reference text or a tool. A wrong format points at clearer instructions or time to think. Testing changes systematically is in both columns because you still measure which one moved the result.

### give-time-to-think
- title: Time to think is a behavior control
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

What does the accuracy guide mean by giving the model time to think?

---

Its strategy table lists "Give GPTs time to think" under LLM optimization, beside clear instructions. That column is for inconsistent formatting, tone, or reasoning. It is not the column for missing or proprietary facts.

That column is inconsistent formatting, tone, or reasoning. Missing, stale, or proprietary facts are the other column, which the table assigns to reference text and external tools. Asking the model to think does not insert a document it never received.

### cache-default-on
- title: Prompt caching is on unless you turn the mode off
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Do you have to enable prompt caching?

---

The guide says prompt caching is enabled by default for supported models. You monitor it. You do not turn on a separate product switch for the basic behavior. Explicit mode is the exception: if you set the mode to explicit and add no breakpoint, that request does not use caching and does not create a cache write.

Default-on does not mean every call hits. The prefix must be long enough, identical, and routed to a machine that still holds it. Use the dashboard hit rate before you assume the discount is showing up on the bill.

### twenty-question-baseline
- title: Twenty questions is the prompt-stage exit
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy

How big a set does the accuracy guide want before advanced optimization?

---

It says that if you have 20 or more questions and answers, and you have looked at the failures and have a hypothesis, you have the right baseline to take on more advanced methods. Automate that set so iteration is faster, with the caveat that ROUGE and BERTScore are only rough.

Twenty, with the failures inspected, is the point at which the guide says you may move on to retrieval or fine-tuning. It is not a sample of all production traffic. ROUGE or BERTScore can show that an iteration changed the wording and still disagree with a human reviewer.

### self-harm-categories
- title: Self-harm is three moderation labels
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

How does the moderation guide split self-harm?

---

`self-harm` is content that promotes, encourages, or depicts acts such as suicide, cutting, and eating disorders. `self-harm/intent` is the speaker saying they are engaging in or intend those acts. `self-harm/instructions` encourages the acts or gives advice on how to commit them. All three apply to text and images.

They are separate from violence, which is death, violence, or physical injury generally, and from graphic violence. A product policy can treat intent differently from instructions. The `flagged` bit alone does not tell you which of these fired. Read `categories`.

### sexual-minors-text-only
- title: Sexual content involving minors is text-only in moderation
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/moderation

How is sexual content involving minors categorized?

---

The guide defines `sexual/minors` as sexual content that includes an individual under 18, and it marks that category text only. General sexual content, excluding sex education and wellness, applies to text and images.

The same page says not to send known or suspected CSAM to the Moderation API at all, because the API is not a CSAM detection system. A text-only category score is not a child-safety program. Follow the CSAM guidance the page links for prevention, detection, response, and reporting.

### dall-e-filter-stricter
- title: DALL-E's default filter is stricter than GPT's
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

How does Azure's default content filter differ between GPT and DALL-E?

---

GPT defaults to filtering medium and high for hate, violence, sexual content, and self-harm, on both prompts and completions, so low severity is not filtered. DALL-E defaults to a low threshold for text prompts and image completions, so low, medium, and high are filtered.

Configurability is in preview and can differ between prompts and completions. The models listed for that configurability include DALL-E 2 and 3, GPT-4o, GPT-4 Turbo Vision GA, and the GPT model series. Turning filters off requires modified-content-filter approval. Do not copy a GPT filter setting onto an image deployment and assume the defaults match.

### finish-reason-length-versus-filter
- title: Stop, length, and content_filter are different endings
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter

What finish reasons does the Azure content-filter article contrast?

---

When every generation passes the configured filters, the article says no moderation details are added and `finish_reason` is stop or length. When a generation is filtered, `finish_reason` is `content_filter`. A filtered prompt does not finish. It returns HTTP 400.

Stop means the model ended normally. Length means it hit a length limit. `content_filter` means the filter stopped or removed content, and the text may be incomplete. Handle the three differently. Retrying a filtered prompt without changing it will hit the same 400.

### vector-database-for-k
- title: Use a vector database for large searches
- version: Core
- level: beginner
- status: verified
- source: https://platform.openai.com/docs/guides/embeddings

How does the embeddings FAQ say you should find the nearest vectors?

---

For searching many vectors quickly, use a vector database. The FAQ points at cookbook examples for working with vector databases and the API. The distance it recommends is cosine similarity, which matches a dot product because the vectors are normalized to length 1.

A linear scan is not what the page recommends once the set is large. The database does not fix a mismatch between embedding models or between a query embedded as a document and a document embedded as a query. Those are properties of the vectors you insert.

### claude-haiku-long-context-price
- title: Haiku long context is priced differently
- version: Core
- level: experienced
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

Which Claude model does the context page single out for long-context pricing?

---

For every model it lists with a 1 million token window, 1 million is the default and you do not send a beta header. Long-context requests are billed at standard pricing except on Claude Haiku 5.5, where prompts over 100,000 tokens cost more.

The page does not state the multiplier. Do not invent one. The exception is a reason to measure prompt length on that model before you assume a long retrieval is the same price as a short one. Other 1 million token models on the list stay at standard pricing for long context, according to that sentence.

### tool-result-clearing
- title: Old tool results can be cleared on purpose
- version: Core
- level: intermediate
- status: verified
- source: https://platform.claude.com/docs/en/build-with-claude/context-windows

What context-editing options does the Claude page list besides compaction?

---

Tool-result clearing for agent workflows, and thinking-block clearing for extended thinking. Compaction remains the primary strategy it names for conversations that regularly approach the limit, and it is in beta for Claude 4.6 and later and Mythos Preview.

Clearing a tool result frees tokens and removes that observation from working memory. The next decision cannot depend on text you deleted. Cached prefixes still count toward the window after you have paid the cache rate. Clearing is a context decision, not a billing switch.

### openai-owns-the-routing
- title: You do not place the cache yourself
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/prompt-caching

Who decides which machine serves a cached prompt?

---

OpenAI handles routing automatically. Inside an organization and processing region, routing for a model depends on machine load and capacity, a hash of the initial tokens after the hidden content, including tool definitions, and, on models before GPT-5.6, a `prompt_cache_key` you supply.

The hash length varies by model. You influence routing by keeping the prefix stable and, on older models, by reusing the key. You do not choose the machine. A miss under uneven load is consistent with that design, which is why the diagnostics tool exists.

### batch-and-schema
- title: Batch requests can require a schema too
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/structured-outputs

Does Structured Outputs apply outside interactive chat?

---

The guide's comparison table includes the Batch API and the Fine-tuning API alongside Responses, Chat Completions, and Assistants. Schema adherence is the `json_schema` format with strict mode. JSON mode on those APIs still only promises valid JSON.

A batch job that asks for JSON in the prompt can still return a shape you cannot parse, or it can hit the whitespace failure if the context never contains the word JSON. Put the schema on the request if the model supports it, and still handle incomplete and refused items when you read the batch output.

### representative-azure-rows
- title: Azure wants the prompt that already worked
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning

What prompt should you put in every Azure fine-tuning example?

---

The article says to put the instructions and prompts that already worked best into every training example. That matters most when you have fewer than a hundred examples.

The file still has to be conversational JSONL, UTF-8 with a byte-order mark, and under 512 MB. Reusing a prompt that failed in the playground teaches that failure. Reusing the prompt that passed, on realistic inputs, is the recommendation on the page.
