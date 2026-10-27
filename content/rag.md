# RAG

### pipeline
- title: Retrieval-augmented generation has two systems
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What are the two steps in RAG, and which step is allowed to invent a sentence?

---

RAG first **retrieves** passages from a corpus you control, then **generates** an answer conditioned on those passages. The retriever is a search system: keyword, vector, or hybrid. The generator is a language model. Only the generator writes prose, and the prompt should tell it to use the retrieved text.

If retrieval misses the fact, generation cannot honestly add it. Debugging starts by splitting the two steps: inspect the passages, then inspect the answer. A beautiful answer with the wrong documents is a retrieval bug. The right documents and a contradictory answer is a generation bug.

### chunking
- title: Chunk size is a retrieval decision
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Why do you split documents before embedding them, and what goes wrong when a chunk is a whole chapter or a single sentence?

---

Embedding and ranking operate on the unit you store. A whole chapter mixes several topics, so the vector is an average and a query about one detail ranks poorly. A single sentence often lacks the definition or the exception that makes the fact true.

Split on structure you already have: headings, paragraphs, or a sliding window with overlap so a sentence on a boundary still appears with its neighbors. Store the title and section path on the chunk. There is no universal token count. Choose the size by evaluating retrieval on real questions, then keep that configuration fixed while you compare models.

### vector-search
- title: Vector search ranks by embedding distance
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

A user searches for "cancel a subscription" and the document says "terminate the plan". Why can vector search find it when keyword search does not?

---

Vector search embeds the query and compares it with stored embeddings. "Cancel a subscription" and "terminate the plan" can be near each other even though they share no tokens. The index returns the nearest chunks, usually approximately, using an algorithm such as HNSW rather than scanning every vector.

That same behavior causes false friends: a chunk about purchasing a subscription can outrank the cancellation policy because the vectors are close. Vector search does not understand entitlement, recency, or which tenant the user belongs to unless you filter on those fields. Always apply the security filter before you treat a neighbor as context.

### hybrid-search
- title: Hybrid search runs keyword and vector, then fuses them
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Why does an exact error code search fail on vectors alone, and what does hybrid search return?

---

Keyword search (BM25) is strong when the query has rare tokens: error codes, SKUs, function names, quotes. Vector search is strong when the wording differs. Hybrid search runs both queries and merges the rankings. Azure AI Search fuses them with Reciprocal Rank Fusion so a document that ranks well in either list can surface, without requiring the two scores to share a scale.

Hybrid is the default you should defend in an interview for documentation and support content. Pure vector search drops exact identifiers. Pure keyword search misses paraphrases. The fusion step does not rerank by meaning; it combines ranks. A cross-encoder reranker is a later, optional pass.

### reranking
- title: A reranker rescores a short list
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

The hybrid index returns 50 chunks in a millisecond. Why would you pay for a semantic reranker on the top 50 instead of asking it to score the whole corpus?

---

A semantic reranker, often a cross-encoder, reads the query and the passage together and assigns a relevance score. That is more accurate than comparing two precomputed vectors, and it is too expensive to run on every document in the corpus.

The pattern is retrieve a candidate set cheaply, then rerank the top 50 or so. Azure AI Search semantic ranker does this on the results of a keyword, vector, or hybrid query. Reranking cannot recover a passage the first stage never returned, so a bad candidate set stays bad. Evaluate the retriever and the reranker separately.

### grounding
- title: Grounding means the answer has to follow the passages
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What instruction and response shape make a RAG answer grounded? What is an ungrounded answer that still sounds helpful?

---

Grounding means the claims in the answer are supported by the retrieved text. The prompt should include the passages, tell the model to answer only from them, and tell it to say when they are insufficient. A practical response shape is the answer plus the passage ids it used.

An ungrounded answer uses the passages as decoration and fills gaps from the model's prior. "I don't have that in the documents" is a successful grounded outcome when the corpus is silent. Refusing less often is not an improvement if the extra answers are unsupported. Measure groundedness against the passages, not against how confident the prose sounds.

### failure-modes
- title: Most RAG bugs are retrieval bugs
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

A RAG bot answers with last year's refund window. Name the failure points you check, in order, before you blame the model.

---

Check them in the order the data flows.

- The source document is stale, duplicated, or missing the updated policy.
- The chunk split the rule away from its exception, or the title never made it into the chunk.
- The security filter dropped the passage, or a missing filter exposed another tenant's passage.
- The embedding or keyword query ranked a related but wrong chunk above the policy.
- The prompt's passage limit cut the right chunk off.
- The model had the right passage and contradicted it.

Only the last item is a generation failure. Logging the retrieved ids next to the answer is what makes this list debuggable. Changing the system prompt first, with no trace, hides the actual break.

### rag-grounds-responses
- title: RAG grounds the model in your content
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What does retrieval-augmented generation add to a language model?

---

Retrieval-augmented generation is a pattern that extends a language model by grounding the response in proprietary content you control.

The model still writes the prose. Grounding quality depends on the passages the retrieval system actually returns. A fluent answer is not evidence that those passages contained the fact.

### rag-query-understanding
- title: Keyword search misses intent
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Why does a keyword index fail a question like the remote-worker PTO example?

---

Azure AI Search describes the query-understanding problem this way: people ask conversational questions with assumed context, while the documents use different words, such as time off, telecommute, and recent hires.

A retriever that only matches the user's tokens misses the policy. Classic RAG answers that gap with hybrid search, semantic ranking, and vector similarity. Agentic retrieval can also split the question into subqueries.

### rag-token-budget
- title: Retrieval must stay inside the token budget
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Why can't you paste the whole corpus into the model for every question?

---

Language models accept a limited token input. The RAG overview uses GPT-4's about 128,000-token window against 10,000 pages as the example: sending everything wastes tokens and degrades quality.

The retrieval system has to return a short, relevant set. Classic RAG uses semantic ranking on the top 50, result limits, scoring profiles, and a select list. Agentic retrieval returns a structured set of chunks, with optional answer synthesis.

### rag-latency-expectation
- title: Users expect an answer in seconds
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What response-time problem does the RAG overview call out?

---

The overview says users expect an AI answer in seconds, and it gives 3 to 5 seconds as the expectation, while a pipeline that queries many sources can take much longer.

Agentic retrieval runs subqueries in parallel and exposes a reasoning-effort setting of minimal, low, or medium. Classic RAG keeps a single query and leaves timeout and retry logic to the application.

### rag-two-approaches
- title: Agentic retrieval and classic RAG
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What two RAG approaches does Azure AI Search document?

---

Azure AI Search documents agentic retrieval and the classic RAG pattern. Agentic retrieval is a pipeline with LLM query planning in preview, multi-source access, and structured responses. Classic RAG uses hybrid search and semantic ranking and is the path when you need generally available features.

New implementations are told to start with agentic retrieval. Keep classic RAG when you need GA-only features, a simpler and faster pipeline, existing orchestration, or fine-grained control of the query.

### classic-rag-handoff
- title: Classic RAG is one query plus your orchestration
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Who calls the language model in classic RAG on Azure AI Search?

---

In classic RAG the application sends one query to Azure AI Search and orchestrates the handoff to a deployed language model separately. That model formulates the answer from the flattened result set.

Query planning does not add another model call, so the architecture has fewer moving parts. The cost is that one query has to carry the whole question.

### agentic-query-planning
- title: Query planning splits a complex question
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What does LLM query planning do in agentic retrieval?

---

At low and medium retrieval reasoning effort, the knowledge base sends the query and the conversation history to a language model, which generates focused subqueries. Query planning is a preview capability.

At minimal effort that planning step is skipped and the queries go straight to the knowledge sources. The default reasoning effort is low, and you set it on the knowledge base.

### agentic-parallel-subqueries
- title: Subqueries run together
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

After agentic retrieval plans subqueries, do they run one after another?

---

The knowledge base sends the subqueries to the knowledge sources and runs them at the same time. Each subquery can be keyword, vector, or hybrid search, and each one is semantically reranked.

Parallel execution is how the pipeline covers a multi-part question without stacking the latency of sequential searches. References from those subqueries are kept for citations.

### agentic-response-shape
- title: Grounding data comes back with the retrieve call
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What does an agentic retrieve call always return, and what is optional?

---

Result synthesis always returns the merged content. Source references and the execution activity log are optional.

You can show the grounding data directly or pass it to a language model. If you skip the activity log, you lose the record of which queries hit which sources.

### agentic-when-to-use
- title: Agentic retrieval is for harder questions
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

When does Azure AI Search say agentic retrieval is worth its extra latency?

---

Agentic retrieval adds latency compared with a single-query pipeline. It is meant for questions a single query handles poorly: several asks in one sentence, dependence on earlier chat turns, synonym or paraphrase expansion, and spelling mistakes.

A beach-hotel question that also asks for airport transport and vegetarian restaurants is the documented example of a multi-ask query. A single hybrid string has to carry all of those constraints at once.

### agentic-components
- title: Knowledge base, source, and retrieve
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Which objects do you create for agentic retrieval?

---

You need a knowledge base and at least one knowledge source. The application calls the knowledge base with a retrieve action that supplies the query and the conversation history.

An indexed knowledge source points at a search index and needs a semantic configuration. A remote knowledge source reads an external platform at query time. The semantic ranker is what the pipeline uses for L2 reranking.

### agentic-ga-versus-preview
- title: Which agentic features are generally available
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Which REST API version does the agentic retrieval overview assign to production versus preview?

---

The overview says to use the 2026-04-01 REST API for production workloads that use generally available knowledge source types with minimal, extractive retrieval. It says to use 2026-08-01-preview for preview knowledge sources, LLM query planning, answer synthesis, non-minimal reasoning effort, and multi-turn messages.

The Azure portal and the Microsoft Foundry portal expose the preview experience. Objects created there can use preview schemas and may need migration when you move to the generally available API.

### agentic-billing-unit
- title: Agentic retrieval is billed in tokens
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

How does agentic retrieval billing differ from classic semantic ranker billing?

---

Classic semantic ranking is billed per query, with a monthly free query allowance. Agentic retrieval is billed per retrieval token on Azure AI Search, with a monthly free token allowance, and the cost varies with reasoning effort.

Query planning and answer synthesis are preview stages billed as Azure OpenAI input and output tokens, always pay-as-you-go, on the model assigned to the knowledge base. Those charges show up on the Azure OpenAI bill.

### agentic-subquery-rerank-window
- title: Each subquery reranks a bounded set
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

How large a set does the agentic retrieval cost example say each subquery reranks?

---

The overview's cost walkthrough says each subquery reranks up to 50 chunks, and it uses three subqueries per plan as the average planning assumption.

That window is the same shape as semantic ranking's top-50 input. Extra knowledge sources multiply the fan-out. The page's cost-control tips are to reduce the number of sources, lower the reasoning effort, and read the activity log.

### agentic-activity-log-limit
- title: The activity log is not a perfect replay
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Can you rebuild an agentic query exactly from the activity log?

---

The activity log reports which queries were issued, which sources they hit, and which parameters were used. You can reissue those queries and compare a public tokenizer with the API-reported usage.

The overview says precise reconstruction of a query or response is not guaranteed. Public web data and a remote SharePoint source that depends on user identity are the examples it gives.

### foundry-iq-endpoint
- title: Foundry IQ is the managed knowledge layer
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What is Foundry IQ in the Azure AI Search RAG overview?

---

Foundry IQ is the managed knowledge layer that turns enterprise content into reusable, permission-aware knowledge bases for agents in the Microsoft Foundry portal. The overview says Foundry IQ uses agentic retrieval and can be an agent's single endpoint for grounding data.

You can also build agentic retrieval yourself with the Azure portal, the Search REST API, or a supported SDK. The managed path and the custom path share the knowledge-base pipeline.

### classic-versus-agentic-choice
- title: When the overview says to stay on classic RAG
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

When does the RAG overview tell you to use classic RAG instead of agentic retrieval?

---

Use classic RAG when you need generally available features only, when simplicity and speed matter more than the advanced relevance path, when you already have orchestration you want to keep, or when you need fine-grained control of the query pipeline.

Use agentic retrieval for an agent or chatbot, for the highest relevance the service describes, for complex or conversational queries, for structured responses with citations and query details, and for new implementations.

### rag-skip-autocomplete
- title: Some search features are for humans, not RAG
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Which Azure AI Search features does the RAG overview say you can skip?

---

The overview says autocomplete and suggestions are meant for human interaction and are not useful in a RAG pattern. Facets and orderby might be useful, and it calls them uncommon in RAG.

A RAG request wants passages for a model. Typeahead UI features do not fill that role. Sorting is a separate trap: an explicit orderby replaces relevance order.

### rag-content-prep
- title: Index preparation is part of RAG quality
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What content problems does the RAG overview say Azure AI Search can prepare for?

---

The overview lists automatic chunking for large documents, more than 50 language analyzers plus multilingual vectors, OCR and image skills for images and PDFs, integrated vectorization for similarity search, and synonym maps plus semantic ranking for terminology mismatches.

Agentic knowledge sources can generate the chunking and vectorization pipeline for you. Classic RAG uses indexers and skillsets, or you push preprocessed documents through the push API.

### rag-hybrid-same-input
- title: Send the text and its vector together
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does the RAG overview describe a hybrid query that doubles down on one input?

---

It says to run hybrid queries that combine keyword and vector search. If you use the same input twice, the text string and its vector equivalent run in parallel and the unified result set keeps the strongest matches from each.

Semantic ranking is built into agentic retrieval and optional for classic RAG. Scoring profiles and vector-query weights and thresholds are the other knobs the overview names.

### rag-security-filter
- title: The chatbot still has to enforce access
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does the RAG overview say private finance content stays off an executive's chatbot?

---

Opening private content to a model requires granular access control. Agentic retrieval can use knowledge-source access control, inherited SharePoint permissions on remote SharePoint queries, and Microsoft Entra ID permission metadata for indexed Azure Storage content.

Both agentic and classic paths also document filter-based security at query time for other sources, and network isolation with private endpoints. Classic RAG adds document-level security trimming.

### rag-incremental-index
- title: Freshness is an indexing job
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does classic RAG on Azure AI Search keep indexed content current?

---

The classic path uses indexers against more than 10 Azure data sources, a skills pipeline, and incremental indexing so the corpus stays fresh. You choose what is indexed and how.

A stale answer often starts here. If the updated policy never landed in the index, no query rewrite will invent the new rule.

### rag-multisource-without-copies
- title: Do not copy every system into one folder first
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does agentic retrieval approach content that lives in SharePoint, a database, and web pages?

---

The overview's problem statement is that copying those systems into one corpus disrupts governance. Agentic retrieval uses a knowledge base over multiple knowledge sources, and it can query remote SharePoint and Bing directly to supplement indexed content.

Retrieval instructions tell the planner which source to use. Blob, OneLake, ingested SharePoint, and other ingested external content can get an automatic indexing pipeline.

### rag-select-fields
- title: Return the fields the model should read
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Why does the classic RAG section mention the select statement?

---

The classic path lists a select statement as a way to control which fields come back, next to top-k, top-n, minimum thresholds, and scoring profiles.

Extra fields spend the token budget on text the model does not need. Missing the field that holds the rule means the model never sees it, even if the document matched.

### chunk-token-limit
- title: Chunk so the embedding call is not truncated
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Why does the chunking article say a whole document can be unsafe to embed?

---

The Azure OpenAI text-embedding-3-small model accepts a maximum of 8,191 tokens. The article treats a token as about four characters for common OpenAI models, which it equates to about 6,000 words.

Input past that limit is truncated, so the embedding silently drops the tail of the document. Chat models have their own input limits, so the same split protects the later RAG prompt.

### chunk-even-when-small
- title: A short page can still be a bad single vector
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Is chunking only for documents that exceed the model limit?

---

The article says chunking is required when the source is too large for the model, and it is also useful when one vector would mix many subtopics. A wiki page can be under the token limit and still retrieve better if you split it finer.

One vector for a multi-topic page averages those topics together. A query about one section then ranks the whole page poorly.

### chunk-fixed-size-example
- title: Fixed-size chunks are a starting pattern
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What fixed-size chunk example does the Azure AI Search chunking article give?

---

It describes a fixed size large enough for a meaningful paragraph, for example 200 words or 600 characters, plus some overlap, for example 10 to 15 percent of the content. The built-in tool it names is the Text Split skill splitting by pages, where a page is a character length.

Those figures are examples of the pattern, not a universal constant. The same article later recommends a different starting point of 512 tokens when you are choosing an overlap.

### chunk-start-512
- title: Start at 512 tokens and 25 percent overlap
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What chunk size and overlap does Azure AI Search say to start with for fixed-size chunks?

---

For fixed-size chunking it recommends starting at 512 tokens, about 2,000 characters, with an initial overlap of 25 percent, which is 128 tokens.

It says the best overlap depends on the content. Highly structured data may need less overlap. Conversational or narrative text may need more. Overlap keeps a boundary sentence with its neighbors, at the cost of duplicated text.

### chunk-variable-structure
- title: Split on sentences or headings when the format is there
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What variable-size chunking signals does the chunking article name?

---

Variable-size chunking partitions on end-of-sentence punctuation, end-of-line markers, NLP structure, or heading syntax in HTML or Markdown. The built-ins it names are the Azure Content Understanding skill and the Text Split skill in sentence mode.

Semantic chunking, also through Content Understanding with markdown output, breaks text into units that keep relationships across sentences and paragraphs and can cross page boundaries.

### chunk-append-title
- title: Put the title back on middle chunks
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What custom chunking trick does the article give for context loss in the middle of a long document?

---

It says you can combine fixed and variable chunks, and the example is variable-size chunks that also append the document title onto chunks from the middle of the document.

A middle chunk that loses its title no longer says which policy or product it belongs to. The retriever and the model then see an orphaned paragraph.

### chunk-parsing-is-not-chunking
- title: One-to-many indexing is a cousin of chunking
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Is splitting a Markdown or JSON blob into search documents the same as chunking?

---

The article says indexers can parse a large source document into smaller search documents. It says this is not chunking in the strict sense, and it can sometimes achieve the same goal. The built-ins it names are Markdown blob indexing, one-to-many indexing, and JSON blob indexing.

Use that path when the file already has records or sections the indexer understands. Use a text-split skill when you need a length or sentence rule the parser does not apply.

### text-split-modes
- title: Pages mode versus sentences mode
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What do the Text Split skill modes pages and sentences mean?

---

pages is the default. Those chunks are made of multiple sentences. sentences makes each chunk one sentence, and what counts as a sentence depends on defaultLanguageCode. In English the skill uses punctuation such as a period or an exclamation mark.

Sentence mode can explode the chunk count. In the Earth at Night sample, sentences mode produced 13,361 chunks, while pages mode at 2,000 characters with no overlap produced 85.

### text-split-page-params
- title: Page length, overlap, and how many pages to take
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What do maximumPageLength, pageOverlapLength, and maximumPagesToTake control?

---

maximumPageLength is the maximum characters, or tokens in the preview tokenizer path, in a chunk. The splitter tries not to break a sentence, so the real length depends on the text. pageOverlapLength is how many characters from the end of the previous page are repeated. maximumPagesToTake defaults to 0, which means take every chunk.

If you set overlap, it must be less than half the maximum page length. Character length is not token length, so a character budget can still overflow an embedding model's token limit.

### text-split-recommended-chars
- title: A character-based default to try first
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What character settings does the Text Split section recommend starting with?

---

For character-based splitting it recommends textSplitMode pages, maximumPageLength 2000, and pageOverlapLength 500.

The Earth at Night walkthrough then says that sample's pages were short enough that a smaller split was reasonable, and that an overlap set too large can result in no overlap appearing at all. Measure the document before you freeze the setting.

### chunk-overlap-raises-count
- title: Overlap increases how many chunks you store
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What happened to chunk count when the Earth at Night sample added overlap?

---

The article's table shows pages mode at 1,000 characters going from 172 chunks with no overlap to 216 chunks with 200 characters of overlap. At 2,000 characters the count went from 85 to 113 when overlap was 500.

That table is one PDF, not a law for every corpus. It does show the cost of overlap: more chunks, more embeddings, and duplicated sentences that can compete with each other in the ranking.

### chunk-factors
- title: Match the chunk to the query and the model
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Which factors does the chunking article tell you to weigh?

---

It names the shape and density of the documents, the queries users actually ask, and the chunk-size guidance of every model in the path. If you both summarize and embed, it says to pick a size that works for both models.

Larger chunks and overlap preserve context for queries that target a specific fact. If you need an intact passage, it prefers larger variable chunks that keep sentence boundaries.

### chunk-for-agentic-sources
- title: Some knowledge sources build the chunking pipeline
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Which knowledge sources does the chunking article say can generate the indexer pipeline for you?

---

For agentic retrieval, knowledge sources over Azure Blob Storage, Azure Data Lake Storage Gen2, and OneLake can generate the indexer, data source, skillset, and index, including chunking and optional vectorization.

That generated pipeline is defined by the knowledge source. If you cannot use integrated vectorization, the article points you at external splitters such as LangChain text splitters or Semantic Kernel's TextChunker.

### text-split-ga
- title: Built-in text splitting is generally available
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Is the Text Split skill a preview-only way to chunk?

---

The chunking article says integrated data chunking through the Text Split skill is generally available. Token-based chunking, including a tokenizer and unsplittable tokens, is called out as available in the latest preview skillset API.

If you need a stable pipeline, character or sentence splitting on the GA skill is the documented path. Token-aware splitting is the preview path, and preview behavior can change.

### embedding-is-a-vector
- title: An embedding is a list of floats
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What is a text embedding, in the OpenAI embeddings guide?

---

An embedding is a vector, a list of floating-point numbers. The distance between two vectors measures relatedness. Small distances mean high relatedness and large distances mean low relatedness.

The guide lists search, clustering, recommendations, anomaly detection, diversity measurement, and classification as uses. Search ranks results by relevance to a query string. You pay by the number of input tokens.

### embedding-default-dimensions
- title: Default vector lengths for the v3 models
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

How long is a text-embedding-3 vector if you do not pass dimensions?

---

By default the vector length is 1,536 for text-embedding-3-small and 3,072 for text-embedding-3-large.

You can pass a dimensions parameter to shorten the vector while keeping its concept-representing properties. A shorter vector that was produced with a different dimensions value is not interchangeable with a full-length vector from the same text.

### embedding-max-input
- title: Embedding models cap the input at 8,192 tokens
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What maximum input does the embeddings guide list for the third-generation models and ada-002?

---

The model table lists a max input of 8,192 tokens for text-embedding-3-small, text-embedding-3-large, and text-embedding-ada-002.

The same table lists MTEB scores of 62.3 percent, 64.6 percent, and 61.0 percent for those three models. A higher eval score does not remove the token cap. Text past the cap cannot be embedded as one string.

### embedding-count-tokens
- title: Count tokens with cl100k_base before you embed
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Which tokenizer does the embeddings FAQ tell you to use for text-embedding-3-small?

---

It says to use tiktoken, and for third-generation models such as text-embedding-3-small it says to use the cl100k_base encoding.

Guessing from character count will disagree with the model's token count. The FAQ's point is to count before you send a string that might exceed the input limit.

### embedding-cosine
- title: OpenAI tells you to use cosine similarity
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Which distance function does the OpenAI embeddings FAQ recommend?

---

It recommends cosine similarity, and it says the choice of distance function typically does not matter much. OpenAI embeddings are normalized to length 1.

Because they are unit length, cosine similarity can be computed with a dot product, and cosine similarity and Euclidean distance produce the same ranking. A database metric that assumes unnormalized vectors will not match that ranking story.

### embedding-knowledge-cutoff
- title: Embedding models are not a news feed
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Do the v3 embedding models know about events after they were trained?

---

The FAQ says text-embedding-3-large and text-embedding-3-small lack knowledge of events after September 2021. It calls this less of a limitation than it is for generation models, and it says some edge cases still lose quality.

Retrieval over your documents is how new facts enter the system. The embedding model places text by its training, so a brand-new product name can sit in a weak neighborhood until the surrounding words carry it.

### embedding-you-own-them
- title: You own the embedding vectors
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Can you store or publish OpenAI embeddings?

---

The FAQ says customers own their input and output, including embeddings. You are responsible for making sure the content you send does not violate the law or the terms of use.

Ownership of the vector does not make the source text shareable. The vector is a transform of that text, so the same retention rules you apply to the document still matter.

### embedding-same-model
- title: Query and documents must share an embedding space
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

Why does Azure AI Search say the query should go through the same embedding model as the index?

---

Vector queries run in an embedding space built from one embedding model. The ranking article says the query input is generally fed into the same model that embedded the index, so the query lands in that space.

Similar vectors cluster together only inside one model's space. A query embedded with a different model is a point in a different geometry, and nearest-neighbor search will return neighbors that are not meaningful.

### vector-matches-concepts
- title: Vector search matches concepts, languages, and modalities
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What kinds of matches does Azure AI Search vector search claim, beyond shared words?

---

Vector search matches numeric representations. The overview's examples are conceptual likeness such as dog and canine, multilingual likeness such as dog and hund, and cross-modal likeness such as the word dog and an image of a dog.

The match is similarity in the embedding space. It does not apply an entitlement check or a recency rule unless you add a filter on some other field.

### vector-knn-k
- title: The query asks for k nearest neighbors
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What does Azure AI Search return from a vector query?

---

After the query text is encoded, Azure AI Search returns the documents for the requested k nearest neighbors.

k is the size of the candidate set, not a guarantee that the true answer is inside it. Hybrid search, which runs vector and keyword search in parallel, is described as often better than either alone.

### vector-where-embeddings-come-from
- title: Embed inside the indexer or push vectors yourself
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What two ways does the vector overview give for getting embeddings into the index?

---

Integrated vectorization chunks and embeds inside an indexer pipeline. You supply the model endpoint and connection, and the service makes the calls. External processing means you embed outside Azure AI Search and push the vectors into vector fields.

The query can use the same split. Integrated vectorization can encode the query text, or your application can send a vector it already computed.

### vector-not-filterable
- title: You filter a neighbor query through another field
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Can you put an OData filter directly on a vector field?

---

The overview says a vector query can include a filter, and filters apply to text and numeric fields. A vector field is not filterable. You create a filterable text or numeric field for metadata such as tenant or category.

The engine can apply that filter before or after the vector query. Which one you pick changes recall, and the filter-mode article is where that choice is defined.

### vector-multimodal-models
- title: Text and images can share one embedding space
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Which multimodal embedding examples does the vector overview name?

---

It names OpenAI CLIP and GPT-4 Turbo with Vision in Azure OpenAI as examples of models that encode text and images into one space you can query.

Both content types have to be embedded with a model that was built for that shared space. A text-only embedding of a caption is a different feature from a multimodal embedding of the image.

### vector-availability
- title: Vector search does not add a search surcharge
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Is vector search an extra-charge feature of Azure AI Search?

---

The overview says vector search is available in all regions and on all tiers at no extra charge. Generating embeddings or using AI enrichment can still be billed by the model provider.

Older search services created before 1 January 2019 can fail when you add a vector field. The fix the page gives is a new search service. Services created after 3 April 2024 have higher vector-index quotas, and some older services can be upgraded.

### vector-as-memory
- title: The index can be the RAG memory
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What does the vector overview say a pure vector index is for?

---

It says you can use Azure AI Search as a vector database for long-term memory, a knowledge base, grounding data for RAG, or any app that queries vectors.

Even a pure vector store still needs a document key. Integrated vectorization notes that the document id is the string field a vector-only index still requires.

### recommend-azure-openai-embeddings
- title: Azure OpenAI is the recommended text embedder
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Which embedding provider does the vector overview recommend for text?

---

It says Azure OpenAI provides embedding models and chat models, that samples target text-embedding-ada-002, and that it recommends Azure OpenAI for text embeddings. For images it recommends the Foundry Tools Image Retrieval vectorize API.

The recommendation is about where you generate vectors. The search service stores them and runs nearest-neighbor search. It does not replace the embedding model.

### hnsw-versus-exhaustive
- title: Approximate graph search versus a full scan
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

What is the difference between HNSW and exhaustive KNN in Azure AI Search?

---

Exhaustive KNN scans the vector space and returns the exact k nearest neighbors. HNSW is an approximate nearest-neighbor algorithm. Azure AI Search uses HNSW for its ANN search.

Exhaustive KNN does not use vector index size quota, because it does not build the in-memory graph. HNSW keeps every point in memory for fast random access, and that graph does consume vector quota.

### exhaustive-when
- title: Use a full scan when you need the true neighbors
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

When does the ranking article tell you to use exhaustive KNN?

---

It says exhaustive KNN is expensive, so use it for small or medium datasets, or when precision matters more than latency. It is also how you build a ground-truth neighbor set when you want to measure ANN recall.

A field indexed for HNSW can still run exhaustive search with exhaustive set to true on the query. A field indexed only for exhaustive KNN cannot run HNSW, because the graph was never built.

### hnsw-parameters
- title: m, efConstruction, and efSearch
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

What do m, efConstruction, and efSearch change on an HNSW index?

---

While indexing, each node connects to up to m neighbors. efConstruction is how many candidate connections are considered. The article says the default efConstruction is 400 and the range is 100 to 1,000. Higher values consider more nodes and often make denser neighborhoods.

At query time, efSearch is the length of the candidate priority queue as the search walks from the top of the graph downward. k is how many neighbors you asked to get back. Raising recall usually raises latency and memory.

### similarity-metrics
- title: Cosine, dot product, and Euclidean
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

Which similarity metrics can a vector field use, and which one matches Azure OpenAI embeddings?

---

The metrics are cosine, dotProduct, and euclidean, also called l2. Cosine measures the angle and ignores length differences. The article says Azure OpenAI embeddings use cosine, so you specify cosine for those vectors.

For normalized vectors, dot product matches cosine and is slightly faster. Euclidean distance measures the length of the difference. If two queries run together, or a query is hybrid, Reciprocal Rank Fusion scores the final list.

### cosine-score-transform
- title: The search score is not raw cosine
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

Why is a cosine vector hit's @search.score not the cosine similarity?

---

For cosine, @search.score falls between 0.333 and 1.00. Azure AI Search transforms the value so the score always drops as similarity gets worse. The article defines that score as 1 divided by 1 plus the cosine distance, and cosine distance as 1 minus cosine similarity.

If you need the original cosine, convert it back. The page gives cosine distance as (1 minus score) divided by score, then similarity as 1 minus that distance. A threshold written against raw cosine will not match this score.

### vector-no-term-boost
- title: You cannot term-boost a vector field
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

Can you attach a scoring profile or a term boost to a pure vector query?

---

The ranking article says vector queries do not have scoring-profile or field or term boosting. The tuning steps it lists are chunk size and overlap, efConstruction, a larger k when a chat model will read the results, and hybrid search with semantic ranking.

It says benchmark testing consistently found hybrid queries plus semantic ranking the most relevant combination. Raising k only helps if the right passage is near the query. It cannot repair a chunk that mixed unrelated topics.

### only-searchable-vectors
- title: Only searchable vector fields are scored
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

Which vector fields participate in similarity scoring?

---

Only vector fields marked searchable on the index, or named in the query's search fields, are used for searching and scoring.

A vector you stored for later and left non-searchable will not produce neighbors. The query also has to name the field when you are not searching every searchable vector field.

### hybrid-one-request
- title: Hybrid search is one request with two parameters
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

What makes a query a hybrid query in Azure AI Search?

---

Hybrid search is one request that includes both the search parameter and vectorQueries. Full-text search and vector search run in parallel. Reciprocal Rank Fusion merges them into one result set.

The index needs plain-text content and embeddings. Keyword search is the precise path for product codes, specialized jargon, dates, and people's names. Vector search is the path for conceptual matches with no shared keyword.

### hybrid-rankers
- title: BM25 and HNSW do not share a score scale
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Which ranking functions does a hybrid query run before fusion?

---

Full-text search uses a ranker such as BM25. Vector search uses HNSW or exhaustive KNN. RRF merges those ranked lists. The response contains one result set ordered by the fused score.

The overview says benchmark tests found hybrid retrieval plus the semantic ranker significantly more relevant. RRF combines ranks. It does not put BM25 points and cosine points on one scale.

### hybrid-k-50
- title: Give the semantic ranker fifty vector neighbors
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

What k does the hybrid overview tell you to use when semantic ranking is on?

---

It says vectorQueries can target several vector fields, and if you are using the semantic ranker you should set k to 50 so the ranker gets the largest input it will accept.

select should return human-readable text for a person or a language model. Autocomplete and suggestions are the text interactions the overview says you cannot use with a vector query.

### hybrid-omit-orderby
- title: Sorting cancels relevance order
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Why does the hybrid overview leave orderby out of the sample query?

---

An explicit sort overrides relevance-ranked results. If you want similarity and BM25 relevance, omit sorting.

Filters, facets, and scoring profiles still apply, because they target fields outside the inverted index and the vector index. The sample filter is a geo distance, and the sample sets vectorFilterMode to postFilter.

### hybrid-semantic-optional
- title: Semantic ranking is a switch on the hybrid request
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

How do you turn semantic ranking on for a hybrid query?

---

Set queryType to semantic and provide the semantic configuration and query language. The overview says semantic ranking is optional. If you are not using it, drop those parameters.

When it is on, the sample response includes both @search.score and @search.rerankerScore. The fused score and the semantic score answer different questions, so a cutoff on one is not a cutoff on the other.

### hybrid-patterns
- title: Start with a balanced hybrid query
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

What three hybrid patterns does the hybrid query article describe?

---

Balanced hybrid is the starting point: k in the 30 to 50 range, top in the 10 to 20 range, and semantic ranking only when it improves measured relevance. Recall-first raises maxTextRecallSize gradually and keeps vector settings moderate. Precision-first keeps k and top modest, uses selective filters, and skips semantic features that do not help.

The article says not to begin with maximum vector recall, a large text recall, and semantic reranking in the same request. That combination raises merge cost and CPU and memory pressure.

### max-text-recall-size
- title: How many BM25 hits reach fusion
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

What is maxTextRecallSize on a hybrid query?

---

It is a preview parameter on hybridSearch. It sets how many BM25-ranked documents are passed to Reciprocal Rank Fusion. The default is 1,000 and the maximum is 10,000.

Lower it when vector search is already beating the text side. Raise it on a large index when 1,000 text hits are not enough. Raising it does not raise the vector side past k.

### count-and-facet-mode
- title: Facet counts can include documents that were not fused
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

What does countAndFacetMode change on a hybrid query?

---

The default, countAllResults, counts and facets every text match, including documents outside the maxTextRecallSize window that never entered RRF. countRetrievableResults limits count and facets to the documents that were retrieved for ranking: the BM25 window plus the k vector hits.

Vector fields are not facetable. In a vector-only query, facets count the k documents. In a text-only query, they count the text matches. A hybrid facet is both, scoped by this mode.

### semantic-recall-floor
- title: Keep at least fifty candidates for the semantic ranker
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

What candidate total does the hybrid query article recommend when semantic ranking is on?

---

For semantic ranker on API version 2024-05-01-preview or later, it says to set k and maxTextRecallSize so they sum to at least 50, then use top to limit what the caller sees.

The ranker only rescores what the first stage returns. A tiny k plus a tiny text window can starve it even if the index holds the right passage.

### vector-weighting
- title: You can weight the vector side of a hybrid query
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

What does the hybrid query article say vector weighting is for?

---

It describes vector weighting as another way to tune a hybrid query, by increasing the importance of the vector queries in the request.

If vector hits dominate and the text query is underperforming, the troubleshooting table says to raise maxTextRecallSize or adjust vector weighting. Weighting changes the mix. It does not create a keyword match that BM25 never found.

### filter-modes-three
- title: Prefilter, postfilter, and strict postfilter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

Where can a filter run relative to a vector query?

---

vectorFilterMode has three settings. preFilter applies the filter during HNSW traversal. postFilter runs the traversal and then filters inside each shard. strictPostFilter, which is preview, finds the unfiltered global top k and then applies the filter.

Filters still target filterable string or numeric fields. The vector field itself is not filterable. HNSW graphs are stored across shards, and each shard holds part of the index.

### prefilter-recall
- title: Prefilter is the recall-first default
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

Why is preFilter the recommended vector filter mode?

---

preFilter is the default on indexes created after approximately 15 October 2023 because it favors recall and quality over latency. It guarantees that k filtered results come back when that many matches exist.

Selective filters make the traversal walk more of the graph, so CPU and latency go up. For a highly selective filter the article says to consider exhaustive set to true. Indexes created earlier default to postFilter, and using preFilter means recreating the index.

### postfilter-false-negatives
- title: Postfilter can miss matches that exist
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

Why can postFilter drop a document that satisfies the filter?

---

Each shard finds an unfiltered local top k, then applies the filter, then the shards merge. A matching document that is less similar than that unfiltered top k never appears.

The article says this risk is worse for highly selective filters and for small k. Raise k and top to reduce false negatives. Latency is more predictable than preFilter because the walk does not grow with selectivity.

### strict-postfilter-zero
- title: Strict postfilter can return nothing
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

When is strictPostFilter the wrong filter mode?

---

strictPostFilter returns only the filtered subset of the unfiltered global top k. If the matches are outside that global top k, the result is empty even though matches exist. The article says this mode has the highest false-negative risk.

It is aimed at faceted navigation, where applying a stricter filter must not increase the count. The page says not to use it when a missed result is serious, and it names healthcare and patent search as examples. Do not pair it with a small k.

### prefilter-slower
- title: Prefilter buys recall with latency
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

What did Azure's filter-mode benchmarks say about speed?

---

Prefiltering was almost always slower than postfiltering, except on small indexes where they were about equal. On larger data the gap was large. The write-up says preFilter is still the default because it returns k matches when they exist.

One documented point: on 1 million vectors at 1,536 dimensions, filtering less than 2 percent of the set made prefiltering about seven times slower. Use postFilter when you want speed, the filter is not very selective, and the index is large enough that preFilter is too slow.

### score-one-means-unranked
- title: A score of 1.0 can mean no ranking happened
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Which queries skip relevance ranking in Azure AI Search?

---

Ranking runs for agentic retrieval and for classic keyword, vector, and hybrid queries. It does not run for strict pattern matching: a filter-only query, autocomplete, suggestions, geospatial search, fuzzy search, or a regular expression.

A uniform @search.score of 1.0 means no ranking algorithm ran. If you treat that 1.0 as a perfect relevance score, you will promote an unranked hit.

### ranking-levels
- title: L1, fusion, L2, and L3
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What are the ranking levels in Azure AI Search?

---

L1 is @search.score: BM25 for tokenized text, and HNSW or exhaustive KNN for vectors. Fused L1 is Reciprocal Rank Fusion when a hybrid query or several vector queries run together. L2 is semantic ranking in @search.rerankerScore.

L2 is optional for text and for vector queries that contain text, and it is required for agentic retrieval. L3 is preview iterative search, and it applies only to agentic retrieval at medium reasoning effort, when the engine and the model agree a second pass is needed.

### score-ranges
- title: Do not compare every @search.score on one scale
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What ranges does the relevance overview give for the different scores?

---

BM25 @search.score runs from 0 with no fixed upper limit. Vector @search.score for HNSW or exhaustive KNN runs from 0.333 to 1.00. RRF @search.score runs from 0 up to a limit set by how many queries were fused. Semantic @search.rerankerScore runs from 0.00 to 4.00.

@search.rerankerBoostedScore, after a scoring profile on an L2 result, runs from 0 with no fixed upper limit and can sit well above 4. A threshold copied from one of these ranges is meaningless on another.

### scoring-profiles
- title: Scoring profiles boost nonvector fields
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What can a scoring profile boost, and what does it cost?

---

A scoring profile is optional and has no extra charge. It boosts weighted fields, or it boosts by freshness, proximity, magnitude, or range. You define it on the index and name it on the query. The logic applies to text and numeric nonvector content.

On a pure vector query, the profile can still touch nonvector fields on the k matching documents. The vector fields themselves are outside that tuning. On a text query, the profile identifies the top 1,000 BM25 matches, and the top 50 come back.

### hybrid-scoring-order
- title: Fusion first, then the profile and the semantic ranker
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

In a hybrid query, when does a scoring profile run relative to RRF and semantic ranking?

---

For the text side, the profile finds the top 1,000 BM25 matches, then those hits are put back in original BM25 order so they can be fused with the vector hits. The profile is applied again on the merged results, along with vector weighting, and semantic ranking is the last step.

On a preview API, a scoring profile can also run over an L2 set and produce @search.rerankerBoostedScore. rankingOrder chooses whether the final order follows the semantic score or the boosted score.

### l2-too-expensive-for-l1
- title: Semantic ranking is a second pass on purpose
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Why does Azure AI Search refuse to use semantic ranking as the first-stage ranker?

---

The relevance overview says L2 reranks L1 results because using semantic ranking as the L1 system would be too expensive in time and money. It is a premium feature billed for use of the ranking models.

Agentic retrieval sends many queries, and the ranking algorithm for that pipeline is still the semantic ranker. The first stage still has to put the right documents into the set the ranker will see.

### semantic-three-jobs
- title: Rerank, captions, and query rewrite
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

What three things does semantic ranking add to a query?

---

It always adds a second ranking over a BM25 or RRF result, using multilingual deep-learning models adapted from Bing. It can return captions and optional answers. If you enable query rewrite, which is preview, it expands the query into as many as 10 variants.

Secondary ranking and answers are part of the response. Query rewrite is part of the request. The rewritten queries are scored with BM25 or RRF and then rescored by the semantic ranker.

### semantic-top-50
- title: Only the first fifty hits are reranked
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

How many results does the semantic ranker actually read?

---

It starts from a BM25 list or an RRF list. Even if the first stage returned more than 50 hits, only the top 50 go to semantic ranking. The rerank uses text, typically informational and descriptive fields.

The ranker cannot search the rest of the corpus for a better passage. If the first stage missed the document, the semantic score cannot bring it back.

### semantic-token-budget
- title: Title, keywords, and content have token budgets
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

How does the semantic ranker trim a long document?

---

For each document, the summarization model accepts up to 2,000 tokens, and this article treats a token as about 10 characters. Title is allotted 128 tokens, keywords 128 tokens, and content receives the remaining tokens. Anything past the limit is ignored.

Field order in the semantic configuration is the priority order, because trimming keeps the earlier fields. As of November 2024, the summary string passed to the ranker is at most 2,048 tokens. Before that, the maximum was 256 tokens.

### reranker-score-meaning
- title: What 4, 3, 2, 1, and 0 mean
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

How should you read @search.rerankerScore?

---

The score runs from 4 down to 0. The article's scale is: 4 fully answers the question, 3 is relevant but incomplete, 2 is partial, 1 answers a small part, and 0 is irrelevant.

The distribution can shift with infrastructure conditions and with model updates. The page says that if you set a minimum threshold, you should not make the cutoff too fine-grained.

### captions-are-verbatim
- title: Captions and answers are extracts, not generations
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

Does the semantic ranker write a new summary sentence?

---

Captions and answers are verbatim text from the index. The article says there is no generative model in this workflow that composes new content. A caption is often under 200 words and comes in plain text and highlighted form.

An answer is returned only if you asked for answers, the query looks like a question, and a passage looks like an answer. If the text has no answer-shaped sentence, you get no answer. That empty result is the ranker refusing to invent one.

### semantic-best-on-prose
- title: Prose benefits more than sparse fields
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

What content does the semantic ranker help most?

---

It promotes matches that are semantically closer to the query intent, and it can extract caption and answer strings. The language models work best on information-rich prose, such as a knowledge base, online documentation, or descriptive documents.

It does not help every corpus. Short codes and sparse fields are the keyword path. The ranker also will not create a string that is not already in the document.

### semantic-synonyms
- title: Synonym maps apply during reranking
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

When does the semantic ranker apply a synonym map?

---

If synonym-map support is enabled on a field and that field is in the semantic configuration, the ranker applies the configured synonyms while it reranks.

The map does not run on a field you left out of the semantic configuration. Query rewrite is a separate preview feature that can also rephrase the query with generated synonyms.

### semantic-billing-empty-query
- title: An empty search string is not a semantic query
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

When does a semantic query get billed?

---

Semantic ranker has a free plan with a monthly request allowance and a standard plan after that. You are charged when the request sets queryType to semantic and the search string is not empty.

search=* is not charged, even with queryType semantic. It also does not produce a semantic ranking, because there is no query text to compare.

### semantic-needs-text
- title: Vector hits need text for the ranker to read
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

Can you semantically rank a vector query that has no text in the document?

---

The how-to says you can apply semantic ranking to text queries, hybrid queries, and vector queries when the documents contain string fields and the vector query has a text representation in the document.

Captions and answers are extracted from that text. Definitions and explanations work best. If you want a generated chat answer, the page points you to agentic retrieval or RAG, not to the semantic ranker.

### semantic-rejects-orderby
- title: orderby plus semantic ranking is a 400
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

What happens if you sort a semantic query with orderby?

---

Sorting on a field overrides the search score and the semantic score. The how-to says adding orderby when semantic ranking is applied returns HTTP 400.

A filter-only query or search=* also skips semantic ranking, because there is nothing to score and the search scores are zero. The query has to contain terms or phrases.

### semantic-query-parameter
- title: semanticQuery keeps Lucene on the search string
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

Why would you set semanticQuery instead of queryType semantic?

---

queryType semantic uses the simple parser's default behavior and does not take explicit simple or full syntax. semanticQuery accepts a plain-text string for the ranker while search can still use simple syntax, full Lucene syntax, a vector query, or a hybrid query.

The semanticQuery string itself must be non-empty plain text, without operators. Search Explorer in the portal cannot set semanticQuery. You set queryType to semantic there instead.

### semantic-answers-count
- title: Extractive answers are recognized, not written
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

How many semantic answers can you ask for, and when will you get one?

---

answers accepts extractive or none. The default is one answer, and you can request up to 10 with a count, for example extractive|count-3. The query has to look like a question, and the field has to contain verbatim text that looks like an answer.

The language models are trained to recognize answers, not to generate them. captions defaults to none. extractive captions highlight by default, and extractive|highlight-false turns the highlight off. The fields in the semantic configuration share a budget of about 2,000 tokens, or about 20,000 characters.

### query-rewrite-exception
- title: Query rewrite is the step that may rephrase
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

Which semantic feature is allowed to compose new wording?

---

The how-to says the semantic subsystem does not compose new sentences or phrases, except for query rewrite in preview. Captions and answers stay verbatim extracts.

Query rewrite can correct spelling or expand the query. It does not fill in a fact the index does not contain. If you need a written answer, that is a later generation step over the retrieved text.

### integrated-vectorization-two-places
- title: Vectorize at index time and at query time
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

What does integrated vectorization add to Azure AI Search?

---

It encodes vectors during indexer indexing and during queries. A vectorizer on the index schema converts the query text with the same embedding model that encoded the content.

The conversion is one way, from text to a vector. There is no vector-to-text step, so the index keeps the human-readable fields beside the vectors. Chunking is not strictly required, and it is required in practice unless the raw documents are already small enough for the embedding model.

### vectorizer-must-match
- title: The query vectorizer and the index model must match
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

What fails if the query vectorizer is a different model from the indexing skill?

---

The vectorizer assigned to the vector field is used automatically at query time, and it must match the embedding model that encoded the content. The article pairs AzureOpenAIEmbedding with the Azure OpenAI vectorizer, a custom skill with a custom Web API vectorizer, and the preview vision and model-catalog skills with their vectorizers.

A mismatched vectorizer puts the query in a different space from the stored vectors. Nearest neighbors from that query are not neighbors in the index's space.

### text-split-is-free
- title: The Text Split skill does not bill as a model call
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Does the Text Split skill have a model charge?

---

The integrated vectorization article says data chunking with the Text Split skill is free and available on all Foundry Tools in all regions. Integrated vectorization itself is available in all regions and tiers. Skills that call a model can still have regional requirements and model charges.

Search services created before 1 January 2019 can lack vector support. The page's remedy is a new search service.

### secondary-index-parent
- title: A chunk index can point back at the parent
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Why does integrated vectorization talk about a secondary index for RAG?

---

A secondary index can hold the chunks while the primary index holds the parent document. They are populated in the same indexer run. The secondary index is aimed at question-answering and chat, because the smaller unit matches more specifically.

When a chunk matches, the query returns the parent document from the primary index. The parent often has the title, date, author, and description that a lone chunk lacks. The page's example is a large PDF.

### indexer-retry-schedule
- title: Throttled embedding calls need another pass
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

What does Azure AI Search do when the embedding endpoint throttles the indexer?

---

Batching and retry logic are built in and are not configurable. If the Azure OpenAI token quota is exhausted, those retries fail. The article recommends a schedule, and it gives every 5 minutes as the example, so a later run can pick up documents the quota blocked.

Token-per-minute limits are per model, per subscription. If one deployment serves both indexing and queries, they compete. The page says to use a separate embedding deployment per workload and, if you can, different subscriptions.

### private-link-azure-only
- title: A private link does not reach public OpenAI
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

When can integrated vectorization call the embedding model over a private link?

---

A shared private link works for Azure-to-Azure connections. openai_account is the group for an Azure OpenAI embedding resource. sites is the group for an App Service or Azure Function that hosts some other embedding model.

A connection to OpenAI or another external model stays on the public internet. A private-network design that assumes the public API is reachable only through that private link will fail for those endpoints.

### oyd-retired
- title: On Your Data has a retirement date
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What does the Azure OpenAI On Your Data reference say about support?

---

The reference says Azure OpenAI On Your Data retired on 14 October 2026 and is no longer supported. Migration is not automatic. It points Azure AI Search applications at a Foundry IQ migration sample.

Before retirement it lists GPT-4o versions 2024-05-13, 2024-08-06, and 2024-11-20, and GPT-4o-mini version 2024-07-18. The page's GA alternatives are minimal extractive knowledge-base retrieval on API 2026-04-01, or classic RAG where the application generates the answer.

### oyd-one-data-source
- title: On Your Data takes exactly one data source
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What happens if you omit data_sources on a chat completion?

---

data_sources is required for On Your Data, and the array must contain exactly one element. If you omit it, the service calls the chat model directly and does not use On Your Data.

When data_sources is set, logprobs and top_logprobs cannot be used. The supported sources on that page are Azure AI Search, Azure Cosmos DB for MongoDB vCore, and, in preview, Elasticsearch and Pinecone.

### oyd-breaking-changes
- title: The API path and the property names changed
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What breaking changes landed in On Your Data at API version 2024-02-15-preview?

---

The path changed from /extensions/chat/completions to /chat/completions. Property names and enum values moved from camel case to snake case. The data source type AzureCognitiveSearch became azure_search. Citations and intent moved to the assistant message context root.

The reference lists 2024-02-15-preview, 2024-02-01, and 2024-05-01-preview as supported versions, and it calls 2024-05-01-preview the latest in that article. Clients written against the old extension path do not hit this schema.

### oyd-citations-shape
- title: Citations are the passages behind the answer
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What does the On Your Data context.citations array contain?

---

citations is the retrieval result used to generate the assistant message. Each citation has required content, plus optional title, url, filepath, and chunk_id. Clients render references from that array.

intent is the detected intent from chat history. The schema says passing the previous intent back is no longer needed and that you should ignore the property. all_retrieved_documents is the wider set, including documents that may have been filtered out.

### oyd-filter-reason
- title: A dropped passage says why it was dropped
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What does filter_reason mean on an On Your Data retrieved document?

---

If the document was not filtered, filter_reason is unset. The value score means the document lost to the original search-score threshold from strictness. The value rerank means it survived that threshold and then lost to the rerank score and top_n_documents.

Each retrieved document also includes the search_queries that found it, the data_source_index, original_search_score, and an optional rerank_score. That is the trace you read before you blame the chat model.

### oyd-doc-markers
- title: The sample maps doc markers onto citations
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

How does the On Your Data sample attach a citation to a sentence?

---

The Python sample walks context citations and replaces markers of the form [doc1], [doc2], and so on in the assistant text with a link built from the citation url, title, filepath, content, and chunk_id.

The marker is only as good as the citation object. If you ask for a response shape the model did not use, the replace step finds nothing and the user sees an answer with no source.

### azure-search-in-scope
- title: in_scope defaults to indexed data only
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What does in_scope do on an Azure AI Search data source for On Your Data?

---

in_scope controls whether queries are restricted to the indexed data. The default is true.

The playground quickstart describes the same switch as limit responses to your data, also defaulting to true, where the model attempts to rely on your documents. Turning the restriction off lets the answer leave the index.

### azure-search-query-types
- title: Five query types for On Your Data
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

Which query_type values does the Azure AI Search data source define?

---

The enums are simple, the default simple query parser; semantic; vector; vector_simple_hybrid; and vector_semantic_hybrid. The default query_type is simple.

embedding_dependency is required for vector, vector_simple_hybrid, and vector_semantic_hybrid. semantic_configuration is required for semantic and vector_semantic_hybrid. A vector query without an embedding deployment has nothing to search with.

### azure-search-strictness
- title: Strictness trades recall for precision
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What does strictness do, and what is the default?

---

strictness sets how aggressive relevance filtering is. Higher strictness raises precision and lowers recall. The default is 3.

The playground quickstart says strictness 5 filters aggressively with a very high similarity threshold, and that lower strictness produces longer answers that can include information that is not in the index. top_n_documents defaults to 5.

### azure-search-top-n
- title: How many chunks reach the model
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What is top_n_documents on the Azure AI Search data source?

---

It is the number of documents featured for the query. The default is 5.

The playground quickstart says the retrieved-documents control accepts 3, 5, 10, or 20 and defaults to 5. That integer is how many chunks the language model sees. A fact that ranks sixth is absent from a five-document prompt.

### azure-search-partial-results
- title: One failed rewrite can fail the request
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What does allow_partial_result change?

---

If it is true, partial search results are allowed and the request fails only when every query fails. If it is omitted or false, the request fails when any search query fails.

max_search_queries caps how many rewritten queries are sent for one user message. If you omit it, the service chooses the count. A fan-out of rewrites is why a single user question can produce several search failures.

### azure-search-include-contexts
- title: Ask for every retrieved document when you are debugging
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What does include_contexts return by default?

---

If you omit it, the default is citations and intent. The allowed values are citations, intent, and all_retrieved_documents.

citations are the passages used for the assistant message. all_retrieved_documents is how you see the wider set, including filter_reason. Without that flag, a filtered-out chunk is invisible in the response.

### azure-search-fields-mapping
- title: Tell the data source which index fields are content
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What can fields_mapping rename for On Your Data?

---

You can name content_fields, vector_fields, filepath_field, title_field, and url_field. content_fields_separator defaults to a newline.

If the content field name in your index does not match what the data source expects, retrieval reads the wrong text. dimensions on a vectorization source is supported only for text-embedding-3 and later models.

### azure-search-vectorizer-same-resource
- title: A deployment-name vectorizer stays inside the resource
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

Why does the Azure Search data source offer a deployment_name vectorization source?

---

deployment_name points at an embeddings deployment in the same Azure OpenAI resource. The reference says this lets you run vector search without an Azure OpenAI API key and without public network access to Azure OpenAI.

The endpoint vectorization source instead calls an embeddings URL and needs API-key authentication. That URL must not include an api-version query parameter. Its dimensions property is supported in API version 2024-10-21.

### azure-search-roles
- title: The managed identity needs search permissions
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

Which roles does the On Your Data sample assign for a system-assigned managed identity?

---

The sample's prerequisites say the Azure OpenAI system-assigned identity needs Search Index Data Reader and Search Service Contributor on the search service. The caller needs Cognitive Services OpenAI User on the Azure OpenAI resource.

Those are data-plane and control-plane roles on search, plus the OpenAI user role. A chat deployment that can call the model and cannot read the index will fail in retrieval, not in generation.

### oyd-playground-history
- title: History helps the next answer and spends tokens
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

What does the On Your Data playground say about conversation history?

---

You choose how many past messages to include. History gives the model context for a related answer, and it consumes tokens. The input token indicator tracks the question you submit.

The advanced settings are the retrieval knobs: strictness, how many documents come back, and whether responses are limited to your data. The quickstart says chat models do best on questions such as what plans are available, not on analysis over the whole corpus.

### oyd-cannot-count-the-corpus
- title: Search does not answer questions about the whole set
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

Why does the On Your Data quickstart say how many documents have I uploaded will fail?

---

It says analysis questions such as which plan is most popular, and questions about the entire dataset, are likely to fail. Search looks for chunks with the same or similar terms. The model can understand the question while the chunks still do not contain the answer.

The playground returns 3 to 20 chunks. A question about all of the titles needs a scan of the store, and a handful of nearest chunks is not that scan.

### oyd-strictness-five
- title: Strictness 5 throws away weak neighbors
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

What does the playground say strictness 5 does to the retrieved documents?

---

Strictness is how aggressively documents are filtered by similarity score. Strictness 5 applies a very high threshold and filters aggressively. The default is 3.

The quickstart says semantic search helps in that setting because the ranking models infer intent. Lower strictness is more verbose and can include text that is not in your index. A high threshold is a cause of empty answers when the right chunk is only moderately similar.

### openai-semantic-no-keywords
- title: Semantic search can rank a sentence with no shared words
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What does the OpenAI retrieval guide mean by semantic search?

---

Semantic search uses vector embeddings to surface similar text, including results that share few or no keywords. The guide's example query is when did we go to the moon. The lunar-landing sentence shares no query words and is listed at 65 percent semantic similarity, above the moon-cake sentence at 28 percent.

The guide says keyword similarity in that table is intersection over union, and semantic similarity is cosine similarity with text-embedding-3-small. A keyword index would have preferred the moon-cake sentence because it shares more tokens.

### vector-store-auto-index
- title: A vector store chunks and embeds for you
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What happens when you add a file to an OpenAI vector store?

---

Vector stores back the Retrieval API and the file search tool. Adding a file automatically chunks it, embeds it, and indexes it. A vector_store.file is the file after that processing, and it carries an attributes map for filtering.

The file object from the Files API is the uploaded bytes and is also used for other purposes. The vector store is the searchable container. You do not embed those chunks yourself on this path.

### vector-store-search-limit
- title: Search returns ten chunks unless you raise the cap
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How many results does vector store search return?

---

A search response contains at most 10 results by default. max_num_results can raise that cap to 50. Each result includes the chunks, a similarity score, attributes, and the file it came from.

Fifty is the documented maximum on that parameter. Asking for more results spends more context later. It does not search a second index.

### rewrite-query
- title: The retrieval API can rewrite the query
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What does rewrite_query do on vector store search?

---

Setting rewrite_query to true rewrites the natural-language query for better retrieval. The rewritten text comes back in search_query.

The guide's examples turn a polite question into a shorter noun phrase, such as primary office building height. The rewrite can drop words you needed as a filter. If the constraint matters, put it in an attribute filter rather than hoping the rewrite keeps it.

### attribute-filter-ops
- title: Filter attributes before the semantic search
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

Which comparison operators can an OpenAI vector store filter use?

---

Attribute filters narrow files before semantic search. Comparison types are eq, ne, gt, gte, lt, lte, in, and nin. Compound filters combine them with and or or.

A filename filter matches a custom filename attribute you set on the vector store file. It does not automatically match the uploaded file's name. Dates in the guide's example are Unix timestamps.

### attribute-limits
- title: Sixteen attribute keys, 256 characters each
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How large can vector store file attributes be?

---

The retrieval guide says each vector_store.file attributes dictionary can have at most 16 keys, with a limit of 256 characters each.

Attributes are the filter surface. A tenant id or a region that you forget to set cannot be filtered later, and a 17th key does not fit the documented limit.

### ranking-threshold
- title: A score threshold drops weak chunks
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What do ranker and score_threshold do in OpenAI ranking options?

---

ranking_options can set a ranker, and the guide names auto and default-2024-08-21, plus a score_threshold from 0.0 to 1.0. A higher threshold keeps chunks that score as more relevant and can drop useful ones.

If you pass hybrid_search weights, embedding_weight emphasizes semantic similarity and text_weight emphasizes token overlap. At least one of those weights must be greater than zero. They tune reciprocal rank fusion. They do not replace the threshold.

### vector-store-expiration
- title: An expired store deletes its files
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What does an expires_after policy do to a vector store?

---

You can set expires_after with an anchor such as last_active_at and a number of days. The guide's example is 7 days. When the store expires, its vector_store.file objects are deleted and you stop being charged for them.

Expiration is a retention control, not a query filter. A store that expires between sessions loses the index, and the next search has nothing to retrieve until you upload again.

### vector-store-file-limits
- title: Half a gigabyte and five million tokens
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What per-file limits does the retrieval guide state?

---

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens, counted automatically when you attach the file.

Text MIME types must be utf-8, utf-16, or ascii. A file inside those limits can still retrieve badly if the default chunking splits the fact away from its heading.

### openai-default-chunking
- title: The default chunk is 800 tokens with 400 overlap
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What chunk size does an OpenAI vector store use if you do not set one?

---

The default max_chunk_size_tokens is 800 and chunk_overlap_tokens is 400. Every file is split into 800-token chunks with 400 tokens of overlap.

If you set chunking_strategy, max_chunk_size_tokens must be from 100 to 4,096 inclusive. chunk_overlap_tokens cannot be negative and cannot exceed half of the max chunk size. Those are the documented bounds, not a quality guarantee.

### vector-store-batch
- title: Batch up to 500 files in one request
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How does the retrieval guide say you should ingest many files into one vector store?

---

It recommends file batches for higher throughput. A batch can include up to 500 files. You pass either file_ids, with optional shared attributes and chunking strategy, or a files array with per-file overrides. The two options are mutually exclusive.

Many single-file creates contend with each other. A batch that mixes the two payload shapes is rejected by that mutual exclusion, so pick one shape per request.

### vector-store-storage-price
- title: The first gigabyte of vector storage is free
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How does OpenAI bill vector store storage?

---

Storage is the size of the parsed chunks and their embeddings across all of your vector stores. Up to 1 GB is free. Beyond that, the guide lists 0.10 US dollars per GB per day.

Expiration policies are the documented way to stop paying for stores you no longer search. The charge follows the chunks and embeddings, not the original file size alone.

### synthesize-from-sources
- title: Generation is a second call over the search results
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How does the retrieval guide say you should turn search hits into an answer?

---

After search, you pass the results and the original query to a model. The guide's developer message tells the model to produce a concise answer based on the provided sources.

The search call does not write the answer. If you skip the sources in the second call, the model answers from its prior. If the sources do not contain the fact, the instruction to use them is what makes an abstention possible.

### file-search-hosted-tool
- title: File search is a hosted tool the model calls
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

Who executes OpenAI file search?

---

File search is a tool in the Responses API. It retrieves from files in vector stores using semantic and keyword search. OpenAI hosts it, so you do not implement the tool execution. When the model decides to call it, the platform retrieves the text and returns the output.

The model can also decline to call the tool. A vector store that was never attached cannot be searched, no matter how good the prompt is.

### file-search-two-outputs
- title: You get a tool call and a message with citations
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

What output items does a file search response contain?

---

The guide says you receive a file_search_call item, with the call id, and a message item whose text can include file_citation annotations. Those annotations carry the file id and the filename.

The sample file_search_call includes the queries that were run. search_results on that object stays empty unless you ask for them. Annotations show which file was cited. They do not, by themselves, show the chunk text.

### file-search-include-results
- title: Search hits are omitted unless you include them
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

How do you see the chunks file search actually retrieved?

---

Annotations in the output text reference files, and the file search call does not return search results by default. Set include to file_search_call.results to put the results on the response.

Without that include, you can see the answer and the file citations and still be unable to audit the passages. Debugging a wrong answer starts by reading those results.

### file-search-max-results
- title: Fewer file-search results save tokens and can hurt the answer
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

What does max_num_results change on the file search tool?

---

On the Responses API file search tool, max_num_results sets how many results are retrieved from the vector stores. The guide says this can reduce token usage and latency, and it may reduce answer quality.

The sample uses 2. A lower cap is a recall cut. If the supporting chunk is result number three, the model never sees it and the citation cannot point at it.

### file-search-metadata-filter
- title: File search can filter on file attributes
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

Can the file search tool restrict which files it reads?

---

The file search guide says you can filter on file metadata. Its sample uses an in filter on a category attribute with the values blog and announcement. It points to the retrieval guide for how attributes and filters are defined.

The filter runs against attributes you stored on the vector store file. A category that was never written onto the file will not match, and the tool will search the wrong set or an empty set.

### file-search-upload-purpose
- title: Files are uploaded before they join a vector store
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

What does the file search guide do before it attaches a file to a vector store?

---

It uploads the file through the Files API with purpose assistants, then creates a vector store and adds that file. The tool then searches the vector store.

Uploading the bytes does not make them searchable. The vector store step is what chunks, embeds, and indexes them. Text files must use utf-8, utf-16, or ascii. The supported-types table includes PDF, Word, PowerPoint, Markdown, HTML, JSON, and common source files.

### file-search-availability
- title: File search rate limits differ by usage tier
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

Which APIs and rate limits does the file search usage table list?

---

The usage notes list Responses, Chat Completions, and Assistants. The rate-limit row lists 500 requests per minute for the Build tier and 1,000 requests per minute for Launch and Grow.

Those are platform limits on the tool, separate from how many chunks you put in the prompt. Hitting the limit fails the call before retrieval quality matters.

### citation-five-parts
- title: A citation system has five parts the model sees
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

What five elements does the OpenAI citation-formatting guide say the model experiences?

---

They are the citable unit, how the material is represented, the citation format, the prompt instructions, and citation parsing after the model responds.

A citation the user cannot resolve is a broken system even if the prose is true. Parsing is what turns the model's marker into a link or a highlight.

### citable-unit-size
- title: Block citations are the default unit
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

Which citable unit does the citation guide recommend for most systems?

---

Document citations only identify the file and are imprecise. Line ranges are exact and harder for the model. Block or chunk citations are the guide's default, because they are easier than lines and more useful than a whole document.

A good unit keeps a stable id across runs, is readable with its surrounding context, and is large enough to make sense while staying precise. An id that changes every request makes the same passage look like a new source.

### source-id-versus-locator
- title: The model emits the id, your app renders the locator
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

What is the difference between a source id and a locator?

---

A source id is a stable identifier such as block1. A locator is the UI highlight, such as lines L8-L13 or a paragraph number. The guide says the model should emit the source id, and your system should resolve the locator.

Mixing the locator into the model's job early increases formatting errors. The material also needs readable text and, optionally, metadata such as a URL, a timestamp, or a title. The model cannot cite text you never presented.

### citation-marker-shape
- title: Use the marker shape the models were trained on
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

What citation marker shape does the OpenAI guide recommend?

---

It recommends a start marker, the family cite, a delimiter, a source id such as turn0file1, an optional locator, and a stop marker. The recommended start, delimiter, and stop characters are the private-use characters U+E200, U+E202, and U+E201.

For tool calls, the turn number increments once per tool invocation, not once per result. Inside one invocation the sources are file0, file1, and so on. A second tool call in the same response produces turn1 ids. Custom marker styles raise errors when reasoning effort is low or the task is complex.

### citation-placement-rules
- title: Where the guide says to put a citation
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

Where should citations sit in the answer, according to the recommended instructions?

---

The recommended instructions say to place citations at the end of the paragraph, or inline if the paragraph is long, after punctuation. They must not sit inside bold, italics, or code fences. They must not all be grouped at the end, and they must not occupy a paragraph by themselves.

A reference id written as plain text, outside the citation markers, violates the instruction. Multiple sources share one marker with repeated delimiters. Items that have no citation marker must not be cited.

### citation-grounding-rules
- title: Cite only text that supports the sentence
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

What extra grounding rules does the citation guide suggest?

---

Its optional block says each citation must support the sentence it is attached to, must reflect the source accurately, and must not be a selective reading. Irrelevant sources are described as permanently damaging trust.

The same block says that when reliable sources disagree you should cite a high-quality source for each major view, and that you should not drop a relevant source only because the domain is low quality. Those rules are prompt instructions. They do not check the citation for you.

### parse-before-display
- title: Strip markers before the user sees them
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

Why does the citation guide include a parser?

---

After the model emits citations, you extract them so you can resolve source ids, render links, or remove the raw markers before display. The sample parser handles one source, several sources, and an optional line range, and it keeps character offsets.

Showing the raw marker to the user is a formatting failure. Trusting the marker without resolving it to a stored chunk is a grounding failure. Both checks happen after generation.

### first-stage-miss
- title: The reranker cannot see what retrieval missed
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

The right paragraph exists in the index and the semantic ranker still does not return it. What limit explains that?

---

Semantic ranking rescores the top 50 results from BM25 or RRF. It does not run a new query over the corpus, and it does not create text.

Fix the first-stage query, the chunking, or the filter that kept the paragraph out of those 50. Changing only the ranker leaves the miss in place.

### empty-semantic-answer
- title: No answer-shaped sentence means no semantic answer
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

You asked for semantic answers and the response has captions but no answer. What does the ranker require?

---

An answer requires the answers parameter, a question-shaped query, and verbatim text in the summarized fields that looks like an answer. The score meanings top out at a document that answers completely, and they include 0 for irrelevant.

Captions can still appear, because a caption summarizes a result. An answer is a separate extract. If the index only has a table of codes, the ranker has no answer sentence to lift.

### truncation-on-embed
- title: Over-long input is truncated before it is embedded
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

A policy's exception is at the end of a long page and never retrieves. What embedding limit is the first check?

---

The chunking article says text-embedding-3-small accepts at most 8,191 tokens. Past that limit, the input is truncated and the tail of the document is lost before an embedding is stored.

Split so each piece fits. Overlap is how a sentence on a boundary stays with its neighbors. A vector built from the truncated head cannot retrieve a sentence that was cut off.

### selective-filter-miss
- title: A selective security filter plus postfilter drops the passage
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

A tenant filter is very selective and vector search returns nothing, even though the tenant's document is indexed. Which filter mode does that?

---

postFilter and strictPostFilter can return false negatives when the filter is highly selective or k is small. strictPostFilter can return zero results even though matches exist, because it only keeps matches inside the unfiltered global top k.

preFilter walks the graph until it finds k matches that satisfy the filter, when they exist. For a very selective filter the article also says to consider an exhaustive vector search. A missing filter is the opposite bug: another tenant's passage can be retrieved.

### hybrid-identifier-miss
- title: Product codes want the keyword side
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

A vector query misses an exact product code that is in the index. What does the hybrid overview say to add?

---

Keyword search is the precise path for product codes, specialized jargon, dates, and names, because it can require the exact token. Vector search is for conceptual similarity when the words differ.

Hybrid runs both and fuses them with RRF. If the text side is still weak, the hybrid query article says to raise maxTextRecallSize from its default of 1,000, up to a maximum of 10,000, or to adjust vector weighting.

### stale-index
- title: Incremental indexing is what makes the new policy searchable
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

The PDF in blob storage was updated and the chatbot still quotes the old rule. Where does the RAG overview put freshness?

---

Classic RAG relies on incremental indexing to keep indexed content fresh, after indexers pull from the data source and skills chunk and vectorize it.

Agentic remote SharePoint and Bing are the documented cases that can be queried without a copy in the index. An indexed knowledge source still serves the last indexed chunks. Query planning cannot retrieve a sentence that was never indexed.

### wrong-model-space
- title: Neighbors from a different embedding model are meaningless
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

You re-embedded the query with a new model and left the index on the old one. What does the ranking article imply?

---

Nearest-neighbor search assumes the query vector and the stored vectors were produced in the same embedding space, generally by the same model. Integrated vectorization states the same rule: the query vectorizer must match the model that encoded the content.

Cosine, dot product, and Euclidean distance do not repair a change of model. Re-embed the corpus with the new model, or keep the query on the old one, before you compare scores.

### oyd-score-versus-rerank-drop
- title: Strictness and top_n drop different documents
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

On Your Data returned an answer without the passage you expected. Which response field tells you whether strictness or the reranker dropped it?

---

On a retrieved document, filter_reason score means the original search score lost to the strictness threshold. filter_reason rerank means it passed that threshold and was then removed by the rerank score together with top_n_documents.

You only see that field when the document is present in all_retrieved_documents. The default include_contexts list is citations and intent, so ask for all_retrieved_documents when you are tracing a drop.

### citation-without-support
- title: A citation has to match the sentence
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

The answer cites a file and the sentence is still unsupported. What does the citation guide require?

---

Its grounding notes say to include only results that support the cited sentence, and that each citation must accurately reflect the source. Selective reading is called out as disallowed.

File search annotations identify a file id and a filename. They do not prove the sentence follows the chunk. Include file_search_call.results when you need to compare the prose with the retrieved text.

### agentic-minimal-skips-planning
- title: Minimal effort does not decompose the question
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

A multi-part question does poorly on agentic retrieval and the activity log shows a single query. What setting does that match?

---

At minimal retrieval reasoning effort, LLM query planning is skipped and the queries are issued directly to the knowledge sources. Low and medium effort send the query and the chat history to a model that writes subqueries. The default is low.

Minimal effort is the lower-latency, lower-cost setting, and it is the generally available extractive path the overview pairs with API 2026-04-01. A question with several asks needs the planning step the minimal setting turns off.

### semantic-field-priority
- title: Later semantic fields are the ones that get cut
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

The semantic caption quotes the title and ignores the body. What trimming rule explains that?

---

The ranker builds its input from title, keywords, and content in the semantic configuration. Title and keywords are allotted 128 tokens each, and content gets what remains of the 2,000-token summarization budget. Excess text is dropped.

Put the fields in priority order. A long body that sits after other long fields is the text the summarizer drops first, so the caption can quote the title and never reach the answer sentence.

### hnsw-recall-gap
- title: HNSW can miss a neighbor that exhaustive search would return
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

The exact nearest chunk shows up with exhaustive KNN and not with HNSW. Is that a broken index?

---

HNSW is approximate. It trades some accuracy for a faster search over a graph. Exhaustive KNN computes distances to the points it scans and returns the exact k nearest neighbors.

Use exhaustive search to build the ground-truth set when you measure that gap. On an HNSW field you can set exhaustive to true for a single query. Raising efSearch or efConstruction is how you spend latency and memory to close the approximation.

### openai-overlap-cap
- title: Overlap cannot be half the chunk or more
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

You set an OpenAI chunk overlap equal to the chunk size and ingestion fails. What limit did you hit?

---

chunk_overlap_tokens must be non-negative and must not exceed half of max_chunk_size_tokens. max_chunk_size_tokens itself must sit between 100 and 4,096.

The default overlap is 400 on an 800-token chunk, which is exactly half and therefore on the boundary the guide allows. A larger overlap is rejected. It is not silently reduced.

### filter-only-score
- title: A filter without a query does not rank
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

You sent only a filter and every hit came back with score 1.0. What does that score mean?

---

Filter-only queries are in the set that skips relevance ranking, along with autocomplete, suggestions, geospatial search, fuzzy search, and regular expressions. A uniform score of 1.0 means no ranking algorithm ran.

Add a keyword, vector, or hybrid query if you need an order. Semantic ranking also refuses an empty search string, and orderby together with semantic ranking returns HTTP 400.

### parent-versus-chunk
- title: The chunk matches and the parent answers
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Why would a RAG index keep both a chunk index and a parent index?

---

Integrated vectorization says a secondary index holds granular chunks for specific matches, and the primary index holds the fuller parent document. A match in the secondary index returns the parent.

The chunk is what similarity can find. The parent is what often contains the title and the surrounding facts. Returning only the chunk repeats the context-loss problem the chunking article addresses by appending the document title.

### rewritten-query-drops-constraint
- title: A rewritten query can lose a constraint
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

The user's question includes a region, and the rewritten search_query drops it. What should carry that constraint?

---

rewrite_query rewrites the natural-language string for retrieval, and the new text is returned in search_query. The guide's examples shorten a question into a noun phrase.

Attribute filters are applied from file attributes before semantic search. A region, a date range, or a project code belongs in a filter using eq, in, or a compound and. The rewrite is not the security boundary.

### billing-semantic-versus-empty
- title: Semantic billing follows a non-empty query
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

You set queryType to semantic with search=* and you were not charged. Why?

---

Charges apply when queryType is semantic and the search string is not empty. An empty search string such as search=* is not charged, and semantic ranking is not applied.

Agentic retrieval is a different meter: retrieval tokens on Azure AI Search, plus Azure OpenAI tokens when preview query planning or answer synthesis runs. A classic semantic query and an agentic retrieve call do not show up as the same line item.

### language-analyzers-versus-vectors
- title: Analyzers and vectors solve different language problems
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

How does the vector overview separate multilingual vectors from language analyzers?

---

Vector search can match across languages when the embedding model was trained for that, and the overview's example is dog and hund. For more control of translation on the nonvector side of a hybrid query, it points at Azure AI Search language analyzers.

The RAG overview says there are more than 50 language analyzers for text, plus multilingual vectors. An analyzer changes tokenization for BM25. It does not translate a vector built by a monolingual embedding model.

### image-verbalization
- title: Images enter RAG through skills, not through hope
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does the RAG overview say images and PDFs become searchable text?

---

It lists OCR, image analysis, image verbalization, and document extraction skills for images and PDFs. Integrated vectorization is the path it names for similarity search, including Azure OpenAI, Azure Vision, and custom embeddings.

A PDF page that is only a scan has no tokens for BM25 until a skill extracts text. A multimodal embedding is a different path, and the vector overview names CLIP and GPT-4 Turbo with Vision for a shared image and text space.

### scoring-profile-not-on-vectors
- title: Freshness boosts a field, not the vector
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Can a scoring profile make a newer vector rank higher by itself?

---

Scoring profiles boost text and numeric nonvector content, using field weights or functions for freshness, proximity, magnitude, or range. The relevance overview says the vector fields themselves do not take part in that tuning.

You can still put a freshness value on a filterable, sortable date field and boost that field. On a hybrid query the profile meets the fused list, and semantic ranking remains the last step described in that article.

### dot-product-normalized
- title: Dot product matches cosine only when vectors are normalized
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

When is dot product the same ranking as cosine in Azure AI Search?

---

The ranking article says that for normalized vectors, dot product is identical to cosine similarity and slightly faster. Cosine itself ignores differences in vector length.

OpenAI's embeddings FAQ says its embeddings are normalized to length 1, which is why a dot product computes cosine and why Euclidean distance ranks them the same way. A metric set to Euclidean on unnormalized vectors will not follow that shortcut.

### knowledge-base-instructions
- title: Retrieval instructions steer the planner
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does agentic retrieval choose among several knowledge sources?

---

The overview says retrieval instructions guide the language model to the appropriate data source, and a knowledge base presents one query interface and one query plan across those sources.

The planner can still miss a source you did not describe. Reducing the number of sources is also the cost tip in the agentic overview, because each extra source increases fan-out and token use.

### classic-milliseconds
- title: Classic RAG keeps the query path short
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Why does the RAG overview call classic RAG the faster architecture?

---

Classic RAG uses a single query, and the overview describes millisecond query times. There is no language model in query planning, so there are fewer components and fewer places to fail. You own timeout and retry behavior.

Agentic retrieval spends latency on planning and on parallel subqueries in exchange for questions that one string handles poorly. The overview tells you to pick classic RAG when speed and simplicity outrank that gain.

### answers-preview-synthesis
- title: Answer synthesis is optional and preview
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Does agentic retrieval always call a model to write the final answer?

---

Merged grounding content is always returned. Answer synthesis, which uses a language model to formulate an answer in the query response, is an optional preview stage. The same preview flag covers LLM query planning.

You can take the grounding data and call your own model, which is also how classic RAG works. Synthesis tokens are billed on Azure OpenAI. Skipping synthesis does not skip semantic reranking of the subqueries.

### entra-storage-permissions
- title: Indexed blob content can carry Entra permissions
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does the RAG overview say Azure Storage permissions show up at query time?

---

Both the agentic and classic sections say indexed content from Azure Storage can inherit Microsoft Entra ID permission metadata. Remote SharePoint queries inherit SharePoint permissions. Other sources use a filter at query time.

Inheritance applies to the path the overview names. A source outside that list does not pick up Entra trimming unless you add the filter yourself. Private endpoints are the network control, separate from the document filter.

### facet-vector-k
- title: A vector query's facets describe k hits, not the corpus
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

Why do facet counts on a vector query look smaller than the index?

---

The hybrid query article says that in a vector-only query, facets count the k documents the vector query returned. In a text-only query they count text matches. In a hybrid query they account for both, subject to countAndFacetMode.

Vector fields cannot be facetable. Put the facet on a filterable nonvector field. countAllResults can count text matches that never entered the RRF window, so the facet can describe documents the ranker did not see.

### efconstruction-default
- title: The HNSW build default is 400
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

What efConstruction does Azure AI Search use if you do not set one?

---

The ranking article says the default efConstruction is 400 and the allowed range is 100 to 1,000. Higher values consider more candidate neighbors while the graph is built and often produce denser neighborhoods.

That cost is paid at indexing time and in memory. efSearch is the query-time queue. Tuning only k changes how many hits you take home. It does not rebuild the graph.

### services-before-2019
- title: Very old search services cannot add vector fields
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

You add a vector field and the service returns an error. What age cutoff does the vector overview mention?

---

Some search services created before 1 January 2019 do not support vector workloads. The overview says the remedy is a new search service. Services created after 3 April 2024 offer higher vector-index quotas.

The integrated vectorization article repeats the same 2019 cutoff. The failure happens at schema update time, before any query runs. Embedding quality is not the variable.

### push-versus-indexer
- title: You can push prechunked documents
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Do you have to use an indexer to load a classic RAG index?

---

The RAG overview says classic RAG can use indexers and skillsets, or you can push preprocessed content through the push API.

If you push, you own chunking, embedding, and the refresh schedule. Incremental indexing is the indexer feature the overview credits with keeping content fresh. A push pipeline that never updates leaves the old policy in place.

### query-language-semantic
- title: Semantic ranking is aimed at natural-language queries
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

What kind of query text is semantic ranking built for?

---

The how-to says setting queryType to semantic reranks the top 50 matches with a model trained on the Bing corpus, for queries written as natural language rather than as keywords.

You still have to supply a non-empty plain-text query and a semantic configuration. Keyword operators belong on a search string paired with semanticQuery, not inside the semantic string itself.

### multi-vector-queries
- title: Several vector fields can be queried together
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Can one hybrid request search more than one vector field?

---

The hybrid overview says vectorQueries can contain multiple vector queries aimed at multiple vector fields. A multilingual embedding space can match without a language analyzer or a translation step.

Those queries are fused with RRF, the same fusion the relevance overview describes for any parallel vector queries. Each field still needs vectors from a compatible model. k on each query is that query's neighbor count.

### free-text-split
- title: Chunking cost and embedding cost are different bills
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Which part of integrated vectorization is free?

---

Text Split skill chunking is free on all Foundry Tools in all regions. Calls to an embedding model are not. The vector overview says vector search itself has no extra search charge, and embedding generation can still be billed by the model provider.

A quota error from Azure OpenAI stops vectorization even though the splitter succeeded. The indexer retry policy cannot proceed once the quota is exhausted, which is why the article suggests a later scheduled run.

### role-information
- title: role_information is the behavior prompt beside retrieval
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What is role_information on the Azure AI Search data source?

---

It is where you give the model instructions about how to behave and which context to use when it generates the response. The reference says you can describe the assistant's personality and how to format responses.

That string is not the search query. in_scope, strictness, and top_n_documents decide which passages exist. role_information tells the model what to do with them. A format instruction cannot cite a chunk the search dropped.

### content-separator
- title: Content fields are joined with a newline by default
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

How are multiple content fields combined for On Your Data?

---

fields_mapping.content_fields names the index fields treated as content. content_fields_separator is the joiner, and it defaults to a newline.

Title, URL, and filepath have their own mapping fields and become citation metadata. If you leave the title field unmapped, the citation's title stays empty even when the index has the title.

### simple-parser-default
- title: The default On Your Data query is the simple parser
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

If you do not set query_type, what retrieval do you get?

---

The Azure AI Search data source defaults query_type to simple, which the reference describes as the default simple query parser.

semantic, vector, and the two hybrid enums are opt-in. Vector forms need an embedding dependency. Semantic forms need a semantic configuration. A default setup is keyword simple search, with in_scope true and strictness 3.

### cosmos-and-preview-sources
- title: On Your Data listed more than Azure AI Search
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Which data sources does the On Your Data reference list?

---

It lists Azure AI Search, Azure Cosmos DB for MongoDB vCore, and, as preview, Elasticsearch and Pinecone.

The page also says On Your Data retired on 14 October 2026. The preview label on Elasticsearch and Pinecone meant those connectors were already outside the production recommendation before retirement. The migration note sends Azure AI Search apps toward Foundry IQ.

### chat-history-passed-explicitly
- title: On Your Data uses the messages you send
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

How does the On Your Data sample pass earlier turns?

---

The sample puts the prior user and assistant messages in the messages array, then the new user question. The data source is still a single azure_search entry.

intent in the response is not something you must send back. The schema says to ignore it. History still costs tokens, which the playground quickstart calls out separately.

### highlight-tags
- title: Caption highlights use tags you can replace
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

How do you control semantic caption highlighting?

---

When captions is extractive, highlighting defaults to on. You append highlight-true or highlight-false. highlightPreTag and highlightPostTag override the default highlight markup.

The highlight is a display aid on verbatim text. It is not a new sentence. answers is independent: extractive or none, one answer by default, up to ten.

### semantic-config-required
- title: Semantic ranking needs a configuration on the index
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request

What index object must exist before a semantic query works?

---

The how-to says that if you set queryType to semantic you must also set semanticConfiguration to a configuration stored on the index. That configuration names the title, keyword, and content fields the ranker reads.

Agentic retrieval's indexed knowledge source also depends on a semantic configuration, because the pipeline reranks with the semantic ranker. A vector index with no semantic configuration cannot take that L2 step.

### balanced-k-range
- title: The documented starting range for k is 30 to 50
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query

What k and top does the hybrid query article suggest you start with?

---

For a balanced hybrid query it says to start with k from 30 to 50 and top from 10 to 20, and to enable semantic ranking only when measured relevance improves.

Recall-first and precision-first are the other two patterns. Starting at the maximum of every knob at once is the pattern the article says raises merge cost.

### geofilter-with-hybrid
- title: A hybrid query can still take a geo filter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Can a hybrid request filter by distance?

---

The hybrid overview's sample includes a geo.distance filter, a vectorFilterMode, and facets, together with search and vectorQueries.

The filter uses a filterable location field, not the vector field. The overview also says that if you use the semantic ranker you will probably want post-filtering as the last step, and that you should test which mode is better for your queries.

### indexer-data-sources
- title: Indexers cover more than one store
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Which Azure data platforms does the vector overview say indexers can pull into a vector index?

---

It names Azure Blob Storage, Azure Cosmos DB for NoSQL, Azure SQL, Azure Data Lake Storage Gen2, Azure Table Storage, and Microsoft OneLake, with integrated vectorization to generate embeddings.

The RAG overview's broader claim is more than 10 Azure data sources for classic indexers. Remote SharePoint in the agentic path is the case that can skip indexing. These indexer sources still land in a search index.

### custom-skill-chunking
- title: A custom skill can replace the built-in splitter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What if the Text Split skill's page and sentence modes are not the split you want?

---

The chunking article says a custom skill can apply your own chunking strategy, and it points at a semantic-chunking sample. External libraries it names are LangChain text splitters and Semantic Kernel's TextChunker.

Those libraries implement fixed size, variable size, or a combination, and they can repeat a small overlap. You still have to keep each chunk inside the embedding model's input limit, or the call truncates.

### sentence-language
- title: Sentence boundaries follow the language code
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What decides where sentence mode splits?

---

The Text Split skill's sentence mode is language dependent, controlled by defaultLanguageCode. The article says English uses standard sentence-ending punctuation such as a period or an exclamation mark.

A wrong language code splits in the wrong places, so the chunk is a fragment or a run-on. Pages mode is less sensitive to that, because it groups sentences up to maximumPageLength and tries not to break a sentence.

### mteb-is-not-your-corpus
- title: An MTEB score is not your retrieval score
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

The embeddings table shows text-embedding-3-large at 64.6 percent MTEB. Does that number tell you your recall?

---

The guide lists that figure, along with 62.3 percent for text-embedding-3-small and 61.0 percent for text-embedding-ada-002, as performance on the MTEB eval. It also lists approximate pages per dollar, assuming about 800 tokens per page.

MTEB is the benchmark in the table, not a measurement of your index. The retrieval guide's moon example is there to show that cosine similarity can rank a paraphrase above a keyword overlap. You still evaluate on your questions.

### file-search-keyword-and-semantic
- title: File search uses both keyword and semantic retrieval
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

Is OpenAI file search vector-only?

---

The file search guide says the tool retrieves through semantic and keyword search over a vector store of previously uploaded files.

Keyword search uses the words in the file. Semantic search can match when the wording differs. Treating the tool as vectors only drops the keyword half the guide lists.

### citation-consistent-id
- title: The same passage needs the same id next time
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

Why does the citation guide insist on a stable source id?

---

It says a citable unit should be consistent, so the same source keeps the same id across runs, and easy to inspect, so a person can read the surrounding context.

Block ids are the recommended default. If your chunker renumbers chunks on every indexing run, yesterday's citation no longer points at the same text. The model emits the id. Your system maps it to the locator.

### do-not-cite-unmarked
- title: Unmarked text is not a citable source
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/citation-formatting

The prompt includes a tool result with no citation marker. Should the model cite it?

---

The guide says not to cite items that do not have a citation marker, because they are not meant to be cited. If you want line ranges, the prompt has to require the locator form and the item has to carry the marker.

Inventing a marker for unmarked text produces a citation your parser cannot resolve. The five-part system starts by deciding what may be cited, then showing that material with a stable id.

### rag-quality-combination
- title: Grounding data needs content, queries, and chunk choice
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What combination does the RAG overview say produces the best grounding data?

---

It says you need appropriate content, smart queries, and query logic that can identify the best chunks. At indexing time, chunk so large documents can match in parts, and vectorize those chunks.

At query time it tells you to use hybrid search, semantic ranking, scoring profiles, and vector-query weights and thresholds. Any one of those with a stale or unsplittable document still grounds the model on the wrong text.

### medium-effort-second-pass
- title: Medium effort can run a second search
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What is L3 ranking?

---

The relevance overview says L3 applies to agentic retrieval at medium retrieval reasoning effort, which is preview. It is an iterative second query pass, used when the agentic retrieval engine and the language model agree that another pass is needed.

Low effort plans subqueries once. Minimal effort skips planning. Medium effort is the setting that can decide the first results are not enough. That extra pass is also extra token cost, which is why the agentic overview lists lower reasoning effort as a cost control.

### select-for-the-model
- title: The model only sees fields you return
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Which fields should a hybrid RAG query return?

---

The hybrid overview says select should name human-readable text fields when a person will read them or when they will be sent to a language model.

A vector field is a list of numbers. Sending it to the model spends the token budget and does not give the model a sentence to cite. Keep the vector for retrieval and return the chunk text, title, and source metadata.

### parallel-not-sequential
- title: Agentic subqueries are simultaneous
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Why does the agentic overview contrast its latency with a sequential multi-source search?

---

It says subqueries run in parallel, and the RAG overview uses the same point: parallel execution rather than sequential execution, with adjustable reasoning effort, and with semantic ranking already in the pipeline.

Parallelism shortens the wait. It does not shrink the token bill, because each subquery can still rerank up to 50 chunks. Fewer knowledge sources is the control the billing section gives you for that fan-out.

### verbatim-caption-limit
- title: A caption is a short extract
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

How long is a semantic caption?

---

The semantic overview says each caption is often fewer than 200 words, in a plain version and a highlighted version, taken from the summary string.

The caption is for scanning a result. It is not the full chunk you would put in a prompt. If the answer sentence sits outside that extract, use the underlying field text, not only the caption, as the model's source.

### threshold-granularity
- title: Reranker scores move around slightly
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

Why does the semantic overview warn against a very fine score threshold?

---

It says @search.rerankerScore distributions can vary slightly with infrastructure conditions and with ranking-model updates. If you set a minimum threshold in code, or the threshold property on vector and hybrid queries, do not make the limit too granular.

The published meanings are still the 4-to-0 scale. A cutoff that distinguishes 2.01 from 1.99 is finer than that scale's stability. The same warning is why a single unlucky score should not be your only groundedness test.

### kb-requires-semantic-config
- title: An indexed knowledge source needs semantic configuration
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What must a search index have before it can back an agentic knowledge source?

---

The agentic overview says the search index stores text and vectors with a semantic configuration, and that this determines which query types run. The semantic ranker is an internal part of the pipeline.

A remote knowledge source does not use that index. It retrieves from the external platform at query time. Mixing the two without a semantic configuration on the indexed one leaves L2 reranking without the fields it expects.

### portal-preview-schemas
- title: Portal-created agentic objects may be preview
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

You created a knowledge base in the portal. Which API contract is it on?

---

The overview says the Azure portal and the Microsoft Foundry portal provide preview-only access to agentic retrieval. Objects created there might use preview schemas and can require migration to the generally available REST API.

The GA API it names for production is 2026-04-01, for GA knowledge source types with minimal, extractive retrieval. Preview planning, answer synthesis, non-minimal effort, and multi-turn messages stay on 2026-08-01-preview.

### openai-batch-mutual-exclusion
- title: One batch payload shape at a time
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

Can one vector-store file batch set a shared chunking strategy and also override it per file?

---

The retrieval guide says you either pass file_ids with optional shared attributes and chunking_strategy, or you pass a files array of per-file objects. The two options are mutually exclusive.

Use the shared form when every file should chunk the same way. Use the files array when one file needs a different overlap or different attributes. Sending both does not merge. It violates the contract the guide states.

### search-query-field
- title: The response tells you which query was searched
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How do you see the query a vector store search actually ran?

---

The search result includes search_query. When rewrite_query is true, that field contains the rewritten query. The guide's sample response shows the original question there when rewrite is not the point of the example.

Compare search_query with the user's words before you judge the hits. A rewritten query that dropped a qualifier explains a surprising top chunk better than a claim that cosine is broken.

### five-million-token-file
- title: A file can be under 512 MB and still too long
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

Which two per-file ceilings does OpenAI retrieval enforce?

---

The maximum file size is 512 MB, and each file should contain no more than 5,000,000 tokens. The token count is computed when you attach the file.

Chunking then splits what was accepted. The default split is 800 tokens with 400 overlap, inside a configurable range of 100 to 4,096 tokens. A legal file can still produce a huge number of chunks and a large storage bill past the free 1 GB.

### grounding-instruction
- title: Tell the model the sources are the whole world
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What instruction does the retrieval guide put on the synthesis call?

---

The developer message in the guide says to produce a concise answer to the query based on the provided sources. The user message carries the formatted sources and the query.

That is the grounding instruction. It does not retrieve anything. If the search step returned the wrong chunks, the model will follow those chunks. Inspect the search payload first.

### file-citation-is-not-the-chunk
- title: A filename citation is coarser than a chunk citation
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

What does a file_citation annotation identify?

---

In the file search guide, a file_citation annotation includes a file id and a filename on the assistant message. The file_search_call beside it records the call id and the queries.

The citation-formatting guide treats a whole document as the least precise citable unit. If you need the paragraph, include the search results and cite the chunk or block id, not only the filename.

### utf-encodings
- title: Text uploads have an encoding allowlist
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

Which encodings does the retrieval guide allow for text MIME types?

---

For text MIME types, the encoding must be utf-8, utf-16, or ascii. The supported-format table includes PDF, Office documents, Markdown, HTML, JSON, and a set of source-code extensions.

A file in another encoding can fail ingestion even when the extension looks supported. The file search guide repeats the same encoding rule and the same format table.

### k-exists-guarantee
- title: Only prefilter promises k filtered hits
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

Which vector filter mode promises k results when they exist?

---

preFilter does. It applies the predicate while it walks HNSW on each shard, then merges to a global top k. The comparison table rates its recall very high and its false-negative risk as none.

postFilter is rated medium to high recall, with a moderate chance of missing matches on a shard. strictPostFilter is rated lowest and can return an empty set. The table says preFilter's cost rises with how selective and complex the filter is.

### small-index-filter-tie
- title: On a small index, filter modes can tie on speed
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-filters

When were prefilter and postfilter about the same speed in the published test?

---

The article says they were about equal on small indexes, and it describes the small set as 100,000 documents, a 2.5 GB index, and 1,536 dimensions. On that set, filtering more than 30 percent of the data kept the two modes comparable, while filtering less than 0.1 percent made prefilter about 50 percent slower.

The large set in the same section is 1 billion documents at 96 dimensions. There, filtering less than 10 percent made prefilter about seven times slower. The default stays preFilter because the page prefers recall over that speed.

### semantic-free-allowance
- title: Semantic ranker has a free monthly allowance
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

Is semantic ranking always a paid call?

---

The overview says you can use it for free subject to the free tier's service limits, and that the free plan is the default, with a monthly free request allowance. The standard plan is pay-as-you-go after that allowance.

It is still a premium feature, billed by usage once you pass the allowance, and only when the query is a real semantic query. Availability is limited to select regions. Agentic retrieval bills its own token meter even though it uses the same ranker internally.

### chunk-both-models
- title: One chunk size has to serve every model in the path
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

You embed chunks and also ask a chat model to summarize them. How should you pick the size?

---

The chunking article says language models have performance guidelines for chunk size, and that if you use models for summarization and embeddings you should choose a size that works for both.

An embedding can accept a chunk the chat model handles poorly, or the reverse. The article's factors are document shape, the queries you expect, and those model guidelines together. The 512-token starting point is a start, and the Earth at Night sample then went smaller because its pages were short.

### overlap-half-page
- title: Text Split overlap must be under half the page
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What overlap constraint does the Text Split skill document?

---

pageOverlapLength is the number of characters from the previous page repeated at the start of the next. If you set it, it must be less than half of maximumPageLength.

The recommended character start is 2,000 with an overlap of 500, which satisfies that rule. The fixed-size narrative earlier in the article also suggests trying about 10 to 15 percent overlap, and the 512-token recommendation is 25 percent. They are different documented starting points for different units.

### document-layout-semantic-chunks
- title: Semantic chunks try to keep a coherent unit
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

What does the chunking article mean by semantic chunks?

---

Semantic chunks break content into units that preserve context and relationships across sentences and paragraphs, and they can span page boundaries. The built-in it names is the Azure Content Understanding skill with markdown output.

Fixed-size chunks ignore that structure and can cut a definition in half, which overlap only partly repairs. Semantic chunks are still separate documents at query time. A relationship that crosses the chunk boundary is still gone unless the chunk kept it.

### rag-structured-response
- title: Agentic retrieval returns structure a model can consume
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What does the RAG overview say agentic retrieval returns to the application?

---

It returns structured responses aimed at chat completion models, with grounding data, citations, and execution metadata. Optional answer synthesis can put a model-written answer in that response and reduce how many tokens you forward.

Classic RAG returns a flattened result set, and your application builds the prompt. If you need the query plan and the citation list from the service, that is the agentic response shape, not the classic one.

### spelling-and-rewrite
- title: Query rewrite can fix a misspelling
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

How can a misspelled query still match on Azure AI Search?

---

Semantic query rewrite, in preview, creates up to 10 variants of a text query or of the text portion of a vector query. The overview says those variants may correct typos or spelling, or rephrase the query with generated synonyms.

The rewritten queries run on the search engine, get BM25 or RRF scores, and are then rescored by the semantic ranker. Agentic retrieval lists spelling mistakes as one reason to accept its extra latency. Neither feature invents a document that was never indexed.

### network-isolation
- title: Private endpoints are the network boundary
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What network control does the RAG overview list for both agentic and classic retrieval?

---

Both sections list network isolation through private endpoints, next to the permission model for the content itself.

A private endpoint does not replace a document filter. The overview treats permissions and the network as separate controls. Integrated vectorization adds a further limit: a shared private link reaches Azure embedding endpoints, and a public OpenAI endpoint stays on the public internet.

### top-k-thresholds
- title: Classic RAG can cut on a minimum score
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What result limits does the classic RAG section name?

---

It names configurable result limits, top-k for vectors and top-n for text, and minimum thresholds, plus scoring profiles and the select list.

A minimum threshold drops weak neighbors before they reach the model. Set it loosely enough that a paraphrased passage still passes. The semantic overview warns that reranker distributions move, so a very tight cutoff is brittle.

### conversation-history-planning
- title: The planner sees the chat, not only the last sentence
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

How does agentic retrieval use earlier turns?

---

The retrieve action takes the query and the conversation history. At low and medium effort, both are sent to the planning model so it can generate subqueries that understand the context.

A follow-up such as what about contractors is ambiguous without the prior turn. Minimal effort skips that planning call and issues queries directly, so the history is not turned into subqueries on that setting.

### indexed-versus-remote
- title: Some sources are copied, some are queried live
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What is the difference between an indexed knowledge source and a remote one?

---

An indexed knowledge source is backed by a search index on your service. A remote knowledge source retrieves from an external platform at query time. The RAG overview's examples of remote query without indexing are SharePoint and Bing.

Remote SharePoint inherits SharePoint permissions. Indexed Azure Storage content can inherit Entra ID permission metadata. A remote source that depends on the user identity is also one the activity-log section says you may not be able to reproduce exactly later.

### bm25-unlimited
- title: BM25 scores have no fixed ceiling
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Can you treat a BM25 @search.score of 10 as highly relevant on every index?

---

The relevance overview gives BM25 @search.score a range from 0 through unlimited. Vector cosine scores sit between 0.333 and 1.00. RRF scores depend on how many queries were fused. Semantic scores sit between 0 and 4.

A cutoff of 10 means one thing on a BM25 index and an impossible value on a cosine vector score. Read the property you threshold. Hybrid responses can contain both @search.score and @search.rerankerScore at once.

### scoring-profile-on-semantic
- title: A profile can boost an already reranked list
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Can a scoring profile change the order after semantic ranking?

---

On a preview REST API or preview SDK, the relevance overview says a scoring profile can be applied over an L2 result set and produce @search.rerankerBoostedScore, which can be much higher than 4. rankingOrder selects whether you order by the semantic score or the boosted score.

The profile still boosts nonvector criteria such as freshness or a weighted field. It does not rescore the vector geometry. If you display the boosted score as if it were the 0-to-4 semantic meaning, the labels 4, 3, 2, 1, and 0 no longer apply.

### exhaustive-ground-truth
- title: Measure ANN recall against exhaustive neighbors
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

How does the ranking article say you should judge HNSW recall?

---

Exhaustive KNN can build the ground-truth set of nearest neighbors, because it returns the exact k. You compare the HNSW result with that set.

HNSW is the algorithm Azure AI Search uses for approximate search, and it is the one it recommends for larger datasets. The gap you measure is the accuracy you traded for latency. efConstruction and efSearch are the knobs that trade it back.

### multimodal-vector-field
- title: An image vector is still just a vector query
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

How does image search get a relevance score?

---

The relevance overview says image search and multimodal search are vector queries, scored with the L1 vector algorithms, HNSW or exhaustive KNN.

The vector overview's multimodal examples are CLIP and GPT-4 Turbo with Vision, so text and images share a space. Filters, semantic ranking, and hybrid keyword search still need text or numeric fields beside that vector. The image vector is not filterable.

### import-wizard
- title: You can try integrated vectorization without writing the pipeline
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

What does the integrated vectorization article suggest before you write indexer code?

---

It says to try the Import data wizard in the Azure portal to explore integrated vectorization. The programmed path is a data source, a skillset with Text Split and an embedding skill, an index with a vectorizer, and an indexer on a schedule.

The wizard is an exploration tool. Production limits remain: embedding quotas, the one-way conversion to vectors, and the need for the query vectorizer to match the indexing model.

### secondary-index-same-run
- title: Parent and chunks are indexed together
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

When are the primary and secondary indexes updated relative to each other?

---

The article says content from each source document flows to both indexes during the same indexing run. The secondary index is a normal index schema populated alongside the primary.

A match on a chunk then returns the parent. If a run fails partway, retry behavior is the indexer's built-in policy, and a schedule is how you pick up documents that throttling skipped. You do not get a configurable retry count.

### oyd-logprobs-disabled
- title: On Your Data turns off log probabilities
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Can you request token log probabilities while using data_sources?

---

The reference says that when data_sources is set, you cannot use logprobs or top_logprobs. The array must contain exactly one data source.

Log probabilities are a generation diagnostic. They are not available on this retrieval path. Use citations, and all_retrieved_documents with filter_reason, to see what the search step did.

### playground-limit-responses
- title: Limiting responses to your data is the default
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

What does the playground do when limit responses to your data is on?

---

The quickstart says the model then attempts to rely only on your documents. That setting defaults to true. It matches the API's in_scope default of true, which restricts queries to indexed data.

Lower strictness can still let in text that is not in the index. The quickstart says lower strictness is more verbose and might include information outside the index. The limit switch and the strictness slider are different controls.

### health-plan-question-shape
- title: Ask a question the chunks can answer
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

What question shape does the On Your Data quickstart say works?

---

It says the chat models perform best on question-and-answer prompts, and its examples are what health plans are available and what the health plus option is.

It says which plan is most popular, how many documents were uploaded, and list all titles are the shapes that fail, because search returns similar chunks rather than a scan or an aggregate. The model understanding the question does not create the missing aggregate.

### max-search-queries-unspecified
- title: Unspecified rewrite fan-out is chosen for you
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What happens if you omit max_search_queries?

---

The Azure AI Search data source says this parameter is the maximum number of rewritten queries sent for one user message. If you do not set it, the system decides how many queries to send.

Each of those queries can fail. Unless allow_partial_result is true, any failed query fails the request. Setting the cap is how you bound that fan-out. The system-chosen count is not a number the reference publishes.

### dimensions-v3-only
- title: You can shorten only v3 embeddings
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

Which embedding models accept a dimensions value on the On Your Data vectorization source?

---

Both the deployment-name source and the endpoint source say dimensions is the number of dimensions the embeddings should have, and that it is supported only on text-embedding-3 and later models.

The OpenAI embeddings guide says the same idea: pass dimensions to shorten a v3 vector without losing its concept-representing properties, from defaults of 1,536 or 3,072. The index field's dimensions must match what you stored. A query shortened to a different length will not line up.

### authentication-four-ways
- title: Four ways to authenticate On Your Data to search
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

Which authentication types does the Azure AI Search data source allow?

---

The reference lists an API key, a system-assigned managed identity, a user-assigned managed identity with a resource id, and an access token.

The endpoint vectorization source is narrower: it uses API-key authentication to call the embeddings URL. The deployment-name source is the one that avoids an API key and public network access, because the deployment is in the same Azure OpenAI resource.

### citation-content-required
- title: A citation must include its text
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Which citation properties are required?

---

content is required. title, url, filepath, and chunk_id are optional. citations as a whole is the retrieval result used to generate the assistant message.

A client that renders only the title will show an empty reference when the title was not mapped. Map title_field, url_field, and filepath_field if you need those on the citation. The content is the passage you can check the sentence against.

### agent-to-agent
- title: Agentic retrieval is also for agent-to-agent calls
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Who is the caller in the agentic retrieval overview?

---

It describes a multi-query pipeline for complex questions from users or from agents, in chat and copilot apps, for RAG and for agent-to-agent workflows.

The application, or the agent, calls the knowledge base and handles the response. The pipeline returns grounding data. Foundry Agent Service is one integration the vector overview mentions: a knowledge base connected so agents receive vector search results.

### hnsw-graph-levels
- title: HNSW searches from coarse to fine
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

How does an HNSW query walk the graph?

---

The ranking article says the search starts at the top level of the hierarchy, moves downward, and keeps candidates that are closer to the query under the configured metric. A priority queue, sized by efSearch, prunes the space. Lower levels refine the candidates. The walk stops when k neighbors are found or another stop condition hits.

Long-range links between levels are built at index time so the walk has shortcuts. If the right neighbor was never connected into that graph well, raising k at query time cannot fully compensate. That is an indexing-parameter problem, efConstruction and m, as well as a query-parameter problem.

### cosine-monotone
- title: Worse similarity always means a lower vector score
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

Why did Azure AI Search transform cosine into @search.score?

---

It wanted a score that always decreases as similarity gets worse, so the value can rank results. The formula it gives is 1 divided by 1 plus the cosine distance.

The raw cosine can be used if you invert that formula. Custom thresholds should use one convention and stick to it. Mixing a raw cosine cutoff with @search.score will drop or keep the wrong hits.

### hybrid-benchmark-claim
- title: The documented best classic stack is hybrid plus semantic rank
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What does Azure AI Search present as the strongest classic relevance strategy?

---

The relevance overview says two strategies stand out: hybrid search with the semantic ranker, and agentic retrieval with LLM query planning and answer synthesis, the latter two in preview. Hybrid combines keyword precision with vector similarity, then the semantic ranker promotes the best matches.

The vector ranking article says the same hybrid-plus-semantic combination produced the most relevant results in its benchmark testing. It does not publish a universal numeric lift. You still measure your own questions.

### filter-before-or-after
- title: The overview lets the engine filter before or after vectors
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Does the vector overview fix the filter to run before the vector search?

---

It says the engine can process the filter before or after the vector query. Filters are for metadata and for including or excluding results, and they apply to text and numeric fields.

The filter-mode article is the one that names preFilter as the recall default and postFilter as the faster option with false negatives. Choosing neither explicitly leaves you on the index's default, which depends on when the index was created.

### skills-pipeline-images
- title: A skills pipeline can verbalize an image
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What does the classic RAG skills pipeline include besides chunking?

---

The overview lists a skills pipeline for chunking, vectorization, image verbalization, and analysis. That is how non-text content becomes something a text query or a text embedding can use.

Verbalization writes a text stand-in for the image. It is not the same as a multimodal embedding of the pixels. Pick the one your query path actually searches.

### query-plan-citations
- title: Citations in agentic retrieval are collected per subquery
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Where do agentic citations come from?

---

During query execution, each subquery is semantically reranked and references are extracted and kept for citation. The unified response can include those source references.

If you do not request the references, you still get the merged content and you lose the provenance. The RAG overview calls this built-in citation tracking and pairs it with the activity log of what was searched.

### gpt4-token-example
- title: The 128,000-token window is still too small for the corpus
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

The RAG overview mentions GPT-4 and 10,000 pages. What point is it making?

---

It says GPT-4 accepts about 128,000 tokens, and that sending 10,000 pages wastes tokens and lowers quality. Retrieval has to return the relevant concise set instead.

A larger context window does not remove chunking, ranking, or filters. It raises how many of the retrieved chunks you can afford to paste. The first-stage miss is still a miss.

### owner-of-embeddings
- title: Embedding output belongs to the customer
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Who owns an OpenAI embedding vector?

---

The FAQ says customers own their input and output from the models, including embeddings. You must keep the submitted content within the law and the terms of use.

You can store the vector in Azure AI Search or another store. The September 2021 knowledge limit on the v3 embedding models still applies to how new phrases are placed. Ownership does not update the model's training.

### anomaly-and-search
- title: Embeddings are not only a search feature
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Besides search, what does the embeddings guide say embeddings are used for?

---

It lists clustering, recommendations, anomaly detection, diversity measurement, and classification, along with search that ranks by relevance to a query string.

RAG uses the search use case: relatedness between the query and a chunk. A vector that is an outlier in clustering is a different product question. Do not treat a low search score as an anomaly-detection label unless that is the system you built.

### price-per-input-token
- title: Embedding calls bill the input tokens
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What does an embeddings request cost, according to the guide?

---

Requests are billed based on the number of tokens in the input. The response includes usage with prompt_tokens and total_tokens. The guide points at the pricing page for rates and shows a table of approximate pages per dollar.

The sample usage block reports prompt_tokens and total_tokens for that input. The pages-per-dollar column is an illustration that assumes about 800 tokens per page, so it is not a substitute for counting the tokens you actually send.

### default-2024-ranker
- title: You can pin or relax the OpenAI ranker
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What ranker names does the retrieval guide mention?

---

It says you can specify a ranker such as auto or default-2024-08-21, and a score_threshold between 0.0 and 1.0.

auto leaves the choice to the service. A named ranker is a pin. Raising the threshold shrinks the set. The guide warns that a higher threshold can exclude useful chunks, so a grounded answer can disappear because the supporting chunk fell under the cutoff.

### and-or-filters
- title: Filters can combine with and and or
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How do you express a region plus a date range in OpenAI retrieval?

---

A compound filter has type and or or, and a list of filters. Comparison filters take a key, a type, and a value. The guide's date example uses gte and lte on a numeric timestamp inside an and.

or of two project codes, then and with a confidentiality flag, is the shape of the guide's more complex example. The filter selects files. It does not rescore the chunks inside the file. A file that passes the filter can still rank poorly.

### attributes-sixteen
- title: The seventeenth metadata key does not fit
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

You want to filter on many labels. What attribute limit will you hit?

---

The retrieval guide allows at most 16 keys on a vector store file's attributes, and 256 characters per key.

Put the access-control and scope fields in those keys first. A nice-to-have label that crowds out the tenant key removes your ability to isolate tenants at query time. The file search tool's filters use these same attributes.

### last-active-anchor
- title: Expiration is measured from last activity
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What anchor does the retrieval guide use in its expiration example?

---

The example sets expires_after.anchor to last_active_at and days to 7. When the store expires, the associated vector store files are deleted and billing for them stops.

A store that is searched stays active under that anchor. A store you created for a one-off upload and never queried again will expire and the next session will find it empty. That looks like a retrieval failure and it is a retention event.

### hosted-so-you-audit
- title: Hosted retrieval still needs an audit trail
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

If OpenAI runs file search for you, what can you still inspect?

---

You can read the file_search_call, including its queries, and the file_citation annotations on the message. Search result chunks appear when include contains file_search_call.results.

You cannot step through the hosted tool's internal code. The inspectable artifacts are the call, the queries, the optional results, and the citations. A wrong answer with the right chunks is a generation problem. A wrong answer with the wrong chunks is a retrieval problem.

### responses-tool-decision
- title: The model chooses whether to call file search
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

Does attaching a vector store guarantee a retrieval on every turn?

---

The file search guide says that when the model decides to use the tool, it calls the tool, retrieves from your files, and returns output. The tool is hosted, and you do not execute it yourself.

A turn with no file_search_call did not retrieve. The answer then comes from the model alone. If your product requires grounding, treat a missing tool call as a failed retrieval, not as a successful answer.

### caption-versus-answer
- title: A caption summarizes, an answer responds
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

What is the difference between a semantic caption and a semantic answer?

---

A caption is verbatim sentences and phrases that summarize the document, with optional highlights, often under 200 words. An answer is an optional extra structure that tries to answer a question-shaped query from answer-shaped text.

You can get captions without answers. answers defaults to none until you set extractive. Both are extracts. Query rewrite is the preview feature that may generate alternate query strings, and it does not write the caption.

### bing-models
- title: The semantic models come from Bing
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

What technology does Azure AI Search say powers semantic ranking?

---

The overview says the second ranking uses multilingual deep-learning models adapted from Microsoft Bing, and that the underlying technology is from Bing and Microsoft Research, integrated as an add-on.

That heritage is why the ranker is strong on natural-language prose and why it is billed as a premium feature in select regions. It does not make the ranker a generator, and it does not make it safe to run on every document in the index.

### l2-text-only
- title: The semantic ranker reads text, even on a vector hit
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

A hybrid hit has a vector and a long PDF. What does the semantic ranker actually score?

---

The overview says the reranking exercise uses only text. The input is assembled from the title, keywords, and content fields in the semantic configuration, then summarized.

The vector got the document into the top 50. The reranker then judges the text. A document whose text fields are empty or unconfigured cannot be promoted for its vector similarity at L2.

### query-rewrite-ten
- title: At most ten rewritten queries
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

How many query variants can semantic query rewrite produce?

---

The overview says the ranker creates up to 10 variants of a text query, or of the text portion of a vector query. They may fix typos or rephrase with generated synonyms. Those variants run as searches, then the results are rescored.

Ten variants multiply work on the same index. They can correct spelling or substitute a generated synonym, and they still cannot return a document that was never indexed. The results are scored with BM25 or RRF and then rescored by the semantic ranker.

### classic-single-shot
- title: Classic RAG is one round trip to search
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How many search requests does the classic pattern use for one user question?

---

The overview describes classic RAG as a single-shot query. The application sends one request and then calls the language model with the flattened results.

Agentic retrieval may issue several subqueries, three in the cost example's average plan, each semantically reranked. That is the coverage and the token cost you take on when one shot is not enough.

### more-than-ten-sources
- title: Classic indexers reach many Azure stores
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How many Azure data sources does the RAG overview say indexers can pull from?

---

It says indexers pull from more than 10 Azure data sources. The skills pipeline then chunks, vectorizes, verbalizes images, and analyzes.

The exact connector list lives in the indexer documentation. The RAG point is that classic RAG builds one index from those sources, while agentic retrieval can also query some remote systems without making a copy.

### fifty-analyzers
- title: Text search has a large analyzer list
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does the RAG overview handle multiple languages on the text side?

---

It says Azure AI Search has more than 50 language analyzers for text, and multilingual vectors for similarity search.

Analyzers affect keyword matching. Vectors affect similarity. A hybrid query can use both. A synonym map is the third tool the overview lists for terminology mismatches, and the semantic ranker applies synonyms only for fields in its configuration.

### push-api-refresh
- title: A pushed index does not refresh itself
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

You loaded chunks with the push API. What will not happen automatically?

---

The overview assigns incremental indexing to the indexer path. The push API is how you send content you already prepared.

If the source PDF changes, a push pipeline updates only when your code pushes again. Until then the index serves the old chunk, and the model will quote it. That is a freshness failure, ahead of any generation bug.

### vector-quota-date
- title: Newer services have higher vector quotas
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Why might two search services in the same tier allow different vector index sizes?

---

The vector overview says services created after 3 April 2024 offer higher quotas for vector indexes, and that an older service might be upgradeable. Services from before 1 January 2019 may not support vectors at all.

HNSW consumes that quota because the graph must reside in memory. Exhaustive KNN does not consume vector index quota. If you are out of quota, exhaustive search on a smaller set is the documented algorithm that avoids the graph, at a CPU cost.

### foundry-agent-connection
- title: Agents can consume a knowledge base
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

How does the vector overview connect Azure AI Search to Foundry Agent Service?

---

It says you can create an indexed knowledge source on an index that has vector fields and a vectorizer, parent that source to a knowledge base, and connect the knowledge base to Foundry Agent Service so agents get vector search results.

The knowledge base is the queryable object. The agent does not query the index schema directly in that description. Permissions on the knowledge source still apply, or the agent retrieves content the user should not see.

### oversampling-mentioned
- title: The hybrid sample sets exhaustive and k explicitly
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

What vector query knobs appear in the hybrid overview's sample?

---

Each sample vector query sets kind, the vector, k of 50, the fields, exhaustive true or false, and an oversampling value. The text beside the sample says to set k to 50 when you use the semantic ranker.

exhaustive true forces a full scan of that vector field for the query, which the ranking article says an HNSW field supports. The sample uses it on one language field and not the other. k is still how many neighbors you keep.

### facets-on-hybrid
- title: Facets can run on a hybrid response
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

Can you facet a hybrid query?

---

The hybrid overview says facets can compute buckets over the results of a hybrid query, and its sample facets a state field. Filters and facets use structures other than the inverted index and the vector index.

The facet field has to be facetable. A vector field is not. The count you show in the UI may include text matches outside the fusion window if countAndFacetMode is left at countAllResults.

### postfilter-sample-default-note
- title: The hybrid sample uses postFilter and tells you to test
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

The hybrid overview sample sets vectorFilterMode to postFilter. Is that the recommended default?

---

The sample uses postFilter. The prose says you can apply the filter at the beginning or the end, and that with the semantic ranker you probably want post-filtering as the last step, and you should test.

The sample is one request, not a rule that postFilter is always best. The same section tells you to test, because the filter can run at the start or the end and the better end depends on the query. A selective filter can change which neighbors survive that choice.

### score-fusion-small
- title: RRF scores are not probabilities
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

A hybrid hit has @search.score of about 0.03 and @search.rerankerScore of about 2.5. Which one is the semantic judgment?

---

The relevance overview assigns @search.rerankerScore to semantic ranking, on a 0 to 4 scale. @search.score on a hybrid query is the RRF score, whose upper bound depends on how many queries were fused. The hybrid overview's sample response shows both properties together.

The small RRF number is not a probability and not a cosine. Compare reranker scores with the 4-to-0 meanings. Compare RRF scores only with other RRF scores from a similar query shape.

### minimum-thresholds-brittle
- title: A granular vector threshold fights the score transform
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-ranking

You want to drop weak vector hits. What score are you thresholding?

---

For cosine, @search.score is the transformed value 1 over 1 plus cosine distance, in the range 0.333 to 1.00, not the raw cosine. The semantic overview adds that thresholds on vector and hybrid queries should not be too granular because reranker distributions move.

Convert to cosine if your cutoff was chosen in cosine units. Then evaluate on real questions. A cutoff copied from a blog will not match this transform, and the docs do not publish a universal cutoff.

### chunk-title-in-middle
- title: Middle chunks need the document title
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

A retrieved chunk is true and the model still applies it to the wrong product. What chunking fix does the article name?

---

The custom-combination example appends the document title to chunks taken from the middle of a large document, so those chunks do not lose their context.

Overlap keeps neighboring sentences. It does not add the title unless you add the title. Store the section path the same way if the index schema has a field for it. The model cannot see metadata you did not put in the text or the selected fields.

### pages-avoid-sentence-breaks
- title: Page mode tries to keep sentences whole
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Does maximumPageLength cut the text at an exact character?

---

The Text Split skill in pages mode avoids breaking sentences, so the actual character count depends on the content. Most chunks land near maximumPageLength. Token length still varies with the words inside the chunk.

A character budget can exceed the embedding token limit because characters and tokens are different units. The article says so explicitly. Count tokens if the embedding model is the constraint.

### langchain-overlap-too-big
- title: An overlap that is too large can vanish
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

The chunking article's LangChain example warns about a large overlap. What happens?

---

After measuring the Earth at Night pages, it says an overlap value that is too large can result in no overlap appearing at all. The sample pages averaged 189 tokens, with a maximum of 1,583.

That warning is about that sample's token counts, where the recommended 2,000-character overlap of 500 was larger than the content needed. Size the overlap from the document, using the article's starting points as starts.

### knowledge-source-blob-onelake
- title: Blob and OneLake can generate the whole pipeline
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Which stores does the chunking article say can generate an indexer, skillset, and index from a knowledge source?

---

Azure Blob Storage, Azure Data Lake Storage Gen2, and OneLake. The generated pipeline chunks and can vectorize, based on the knowledge source definition.

Other sources still need a pipeline you build, or a push. The generated pipeline is a convenience. The chunk size it applies is still a retrieval decision you should evaluate on real questions.

### semantic-chunk-page-span
- title: A semantic chunk may cross a page break
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Why would a page-based split hurt a paragraph that starts at the bottom of a page?

---

Fixed page splits follow length. The article's semantic chunking keeps relationships across sentences and paragraphs and can span page boundaries, via Content Understanding with markdown output.

A page break is not a topic break. If your splitter is the PDF page, the question at the bottom and the answer at the top of the next page land in different vectors. Semantic chunking is the documented way to keep them together.

### custom-web-api-vectorizer
- title: A custom embedder needs a custom vectorizer
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

You embed with a model that is not Azure OpenAI. How does integrated vectorization call it?

---

The article pairs a custom skill with a Custom Web API vectorizer, and an AML skill aimed at the Foundry model catalog with the model-catalog vectorizer, which it marks preview. The Azure OpenAI embedding skill pairs with the Azure OpenAI vectorizer.

Indexing and querying must use the matching pair. A custom skill that embeds at index time and an Azure OpenAI vectorizer at query time mixes two spaces. Shared private link for a non-Azure-OpenAI model uses the sites group, for App Service or Functions.

### quota-per-subscription
- title: Indexing and queries share a token quota
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Why does the integrated vectorization article tell you to split embedding deployments?

---

Azure OpenAI token-per-minute limits are per model, per subscription. One deployment used for both indexing and queries makes those workloads compete. The suggestion is one deployment per workload, in different subscriptions if you can.

When the quota is exhausted, the indexer's retries fail. The search query then cannot vectorize either, so both ingestion and retrieval stall together. Separate deployments isolate those failures.

### wizard-then-code
- title: Schedule the indexer after the wizard
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

What operational step does the article add after the pipeline exists?

---

It says to run the indexer on a schedule so it picks up changed documents and documents missed because of throttling. The example interval is 5 minutes.

A wizard run is a point in time. Without a schedule or a push on change, the index drifts from the source. RAG then answers from the last successful run.

### one-way-vectors
- title: You cannot decode a vector back into the sentence
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Why must the index store the original text as well as the vector?

---

Integrated vectorization says conversions are one way. There is no vector-to-text conversion for queries or results. That is why indexes contain both vector fields and nonvector fields.

The model and the user need the text. The vector is only for similarity. Dropping the text field after embedding leaves you with neighbors you cannot read, cite, or semantically rank.

### all-regions-vectorization
- title: Integrated vectorization is not region-locked by itself
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Is integrated vectorization limited to a short region list?

---

The article says it is available in all regions and tiers. Skills and vectorizers that call AI enrichment can still have regional requirements, and it points you at attaching a Foundry resource.

Semantic ranker is the feature the semantic overview limits to select regions. Do not confuse the two. You can vectorize in a region where semantic ranking is unavailable, and then you lose the L2 rerank, not the vector query.

### oyd-preview-synthesis-migration
- title: The migration sample's auto path is preview
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What does the On Your Data retirement note say to use in production?

---

It says the sample's auto retrieval and answer synthesis use API 2026-08-01-preview, and that preview features are not recommended for production. For generally available alternatives it names minimal, extractive knowledge-base retrieval with API 2026-04-01, or classic RAG with the application generating the answer.

Those paths are not feature-equivalent. Migrating is an application change, and the page says it is not automatic. Plan for a different response shape and a different way of producing citations.

### snake-case-migration
- title: Old camel-case clients miss the new schema
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Why would a client written for the extensions path stop seeing citations?

---

At API version 2024-02-15-preview the path became /chat/completions, names became snake_case, the type became azure_search, and citations moved to the assistant message context root with an explicit schema.

A parser looking for the old tool-message location will see an empty citation list while the new context.citations array is populated. Read content, title, url, filepath, and chunk_id from that array.

### retrieved-doc-scores
- title: Original score and rerank score are both available
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

What scores does an On Your Data retrieved document carry?

---

original_search_score is required on the retrieved-document object. rerank_score is optional. search_queries and data_source_index are required.

filter_reason tells you which score caused a drop. If you only read the assistant text, you cannot tell a strictness drop from a top-n drop. Request all_retrieved_documents when you need that trace.

### single-source-array
- title: You cannot pass two data_sources entries
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Can one On Your Data request search two indexes?

---

The reference says the data_sources array must contain exactly one element.

Multi-source retrieval is the agentic knowledge-base feature, not this array. If you need SharePoint and a search index together, the RAG overview puts that on a knowledge base with multiple knowledge sources. Stuffing two entries into data_sources violates the schema.

### playground-token-indicator
- title: History and the question share a token budget
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

What does the playground's token indicator track?

---

The quickstart says the input token progress indicator tracks the token count of the question you submit, and that including past messages adds context and consumes tokens.

Retrieved chunks also occupy the prompt. top_n_documents and the history length compete. A long history plus 20 chunks is how you blow the context window even when each chunk is small.

### three-to-twenty
- title: The playground will not return the whole index
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

What chunk counts does the On Your Data playground allow?

---

Retrieved documents can be 3, 5, 10, or 20, default 5. The quickstart says chats are constrained to that range, and that a question about all titles would need a full scan.

Raising the count from 5 to 20 improves coverage and spends tokens. It still does not scan the corpus. Aggregation and counting questions remain the documented failure mode.

### semantic-helps-high-strictness
- title: Semantic rank helps when the threshold is harsh
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart

Why does the playground mention semantic search next to strictness 5?

---

It says strictness 5 filters very aggressively, and that semantic search can help because the ranking models do a better job of inferring intent.

The API side requires semantic_configuration when query_type is semantic or vector_semantic_hybrid. Turning the concept on in the playground without that configuration in the API call does not give you the same rerank.

### in-scope-false-risk
- title: Leaving the index is a choice
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What does in_scope false allow?

---

in_scope asks whether queries should be restricted to indexed data, and the default is true. False removes that restriction.

The playground warning on low strictness is that answers can include information that is not in the index. If the product requirement is grounding, leave the restriction on and treat an answer that needed outside knowledge as a missed retrieval, not as a better answer.

### vector-simple-hybrid
- title: Hybrid on On Your Data has two enum names
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What is the difference between vector_simple_hybrid and vector_semantic_hybrid?

---

The reference describes vector_simple_hybrid as the simple query strategy combined with vector data, and vector_semantic_hybrid as semantic search combined with vector data.

Both require an embedding dependency. Only the semantic hybrid requires a semantic configuration. Choosing the semantic hybrid without that configuration is an invalid request, not a silent fallback to simple hybrid.

### system-assigned-sample
- title: The sample uses a managed identity, not a key in the body
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

How does the Azure AI Search data source sample authenticate?

---

The Python and REST samples set authentication type to system_assigned_managed_identity and do not put a search key in the body. The prerequisites assign Search Index Data Reader and Search Service Contributor to that identity.

An API key is a different authentication type, with a key field. The access-token type carries an access token. Picking the managed identity and forgetting the role assignment fails at the search call.

### filepath-in-citation
- title: The citation can point at a file and a chunk
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Which optional fields let a user open the source of an On Your Data answer?

---

A citation may include url, filepath, title, and chunk_id, along with the required content.

The sample builds a link from the url and shows the filepath and chunk id. If your index uses different field names, map them with url_field, filepath_field, and title_field. Otherwise the citation content exists and the link does not.

### ignore-intent
- title: Do not round-trip the intent string
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/on-your-data?tabs=python

Should your client send the previous intent back on the next On Your Data turn?

---

The context schema says intent is the detected intent from chat history, that passing the previous intent back is no longer needed, and that you should ignore the property.

Send the conversation as messages if you want the next turn to have context. The playground quickstart is the place that explains the token cost of those messages. intent is not the memory mechanism.

### partial-result-all-fail
- title: Partial results still fail when every query fails
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

allow_partial_result is true and the user still gets an error. When is that consistent with the spec?

---

When it is true, partial results are allowed and the request fails if all the queries fail. A complete failure of every rewritten query is still a failure.

When the flag is false or omitted, any single query failure fails the request. If your rewrites are flaky, the flag changes the failure mode from one-strike to all-strike. It does not invent results for a query that failed.

### embedding-endpoint-no-api-version
- title: The embeddings URL must not carry api-version
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

What URL shape does the endpoint vectorization source require?

---

It must look like https://{resource}.openai.azure.com/openai/deployments/{deployment}/embeddings. The reference says the api-version query parameter is not allowed. Authentication is an API key.

dimensions on that source is supported in API version 2024-10-21, and only for text-embedding-3 and later. Putting api-version on the URL is a documented invalid shape, separate from the chat completion's api-version.

### reader-and-contributor
- title: Two search roles appear in the sample prerequisites
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python

Why does the sample ask for both Search Index Data Reader and Search Service Contributor?

---

The prerequisites list both roles for the Azure OpenAI system-assigned managed identity on the search service, and Cognitive Services OpenAI User for the caller on the Azure OpenAI resource.

Data Reader is what a query needs to read documents. The sample lists Contributor as well. A deployment that copies only one of the two search roles does not match the sample's prerequisite list. Test the retrieve step before you judge the model.

### file-search-purpose-assistants
- title: The upload purpose in the file search guide is assistants
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/tools-file-search

What purpose does the file search guide set when it uploads a file?

---

The upload sample calls the Files API with purpose assistants, then adds the file to a vector store.

The retrieval guide's model is the same split: a file object, then a vector_store.file once the file is chunked and embedded. Searching before that processing finishes returns nothing useful. Check the file status on the vector store before you blame the query.

### max-num-results-fifty
- title: Fifty is the top of the documented search window
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

Can OpenAI vector store search return 100 chunks?

---

The retrieval guide says the response contains 10 results by default and that you can set up to 50 with max_num_results.

The file search tool uses the same parameter name and warns that lowering it can hurt answer quality while saving tokens and latency. There is no documented setting above 50 on that guide. Wider recall means a different indexing or filtering strategy, not a larger page.

### hybrid-weight-zero
- title: A zero weight on both sides is invalid
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What constraint does the retrieval guide put on hybrid search weights?

---

embedding_weight, also called rrf_embedding_weight, and text_weight, also called rrf_text_weight, balance semantic matches against keyword matches inside reciprocal rank fusion. At least one weight must be greater than zero.

Raise the embedding weight when paraphrases matter. Raise the text weight when the exact tokens matter. Setting both to zero removes both signals. The guide does not define a default numeric pair in that paragraph, so tune from measured queries.

### score-threshold-excludes
- title: A high threshold can hide the only useful chunk
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

You raised score_threshold and the assistant stopped answering a question it used to answer. Why is that expected?

---

The retrieval guide says a higher score_threshold, on a 0.0 to 1.0 scale, limits results to more relevant chunks and may exclude useful ones.

The chunk is still in the store. It is under the cutoff. Lower the threshold or improve the chunk, and confirm with the returned scores. A threshold is a filter on the score, not a change to the embedding.

### compound-filter-precedence
- title: and and or nest the way you nest them
- version: Core
- level: experienced
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

How is the guide's top-secret project filter structured?

---

The complex example is an or whose first branch is an and of a project-code or and a confidentiality eq, and whose second branch is a language eq.

A flat list of eq filters does not mean the same thing. Write the nesting explicitly. Remember the filename key in the simpler examples is a custom attribute, not the automatic file name. The wrong key matches nothing.

### storage-parsed-chunks
- title: You pay for chunks and embeddings, not the PDF bytes
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/retrieval

What size is vector store storage measured on?

---

The retrieval guide says charges use the total storage of parsed chunks and their embeddings across all vector stores. The first 1 GB is free, then 0.10 US dollars per GB per day.

Overlap duplicates text, so a 400-token overlap on 800-token chunks stores a lot of repeated tokens. Expiration deletes the files and stops the charge. Compressing the original PDF does not shrink the embedding storage.

### cl100k-before-upload
- title: Count tokens before you hit the embedding cap
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

How do you know a string will fit in text-embedding-3-small?

---

The FAQ says to tokenize with tiktoken and the cl100k_base encoding for third-generation models. The model table lists a max input of 8,192 tokens.

A character guess will disagree with cl100k_base on some strings. Count before you send an input that might pass 8,192 tokens, which is the max the model table lists for text-embedding-3-small.

### normalized-euclidean
- title: Euclidean and cosine agree on OpenAI embeddings
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

You rank OpenAI embeddings with Euclidean distance and with cosine. What does the FAQ predict?

---

Because the embeddings are normalized to length 1, cosine similarity and Euclidean distance produce identical rankings. Cosine can also be computed as a dot product, which is slightly faster.

The FAQ still recommends cosine. The identical ranking is a consequence of length 1. It says the choice of distance function typically does not matter much for these embeddings, and a dot product is the faster way to compute cosine.

### september-2021
- title: New jargon can embed poorly on the v3 models
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

A product launched in 2025 is in your documents and retrieves badly by its new name alone. What limitation does the embeddings FAQ name?

---

text-embedding-3-small and text-embedding-3-large lack knowledge of events after September 2021. The FAQ says this matters less than it does for generation, and that some edge cases still lose quality.

The FAQ treats this as an edge-case quality drop, smaller than the same cutoff would be for a generation model. A brand-new name can still land in a weak neighborhood because the model never saw the event that coined it.

### search-clustering-not-rag
- title: Classification by nearest label is a different embedding use
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

The embeddings guide mentions classification. Is that RAG?

---

Classification, in that guide, means assigning a string to the most similar label. Search means ranking results by relevance to a query. RAG is the search use, followed by a generation step over the retrieved text.

A classifier does not quote a passage. If the interview question is grounding, talk about retrieved chunks and citations. If it is routing, talk about the nearest label. They share an embedding and they do not share a failure mode.

### diversity-measurement
- title: Embeddings can measure how alike a set is
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What does the embeddings guide mean by diversity measurement?

---

It says diversity measurement is analyzing similarity distributions, and anomaly detection is finding outliers with little relatedness.

Those are offline analyses of vectors you already have. They are not the query path that returns a chunk to a model. A RAG evaluation set can use the same vectors, and the user-facing answer still depends on retrieval plus grounding.

### recommendation-use
- title: Recommendations are nearest items, not grounded answers
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

How does the embeddings guide describe recommendations?

---

Recommendations are items whose text embeddings are related. Search is a separate bullet: results ranked by relevance to a query string.

A recommendation carousel does not need citations. A RAG answer does, because the user is being told a fact. Use the citation guide's rule that the cited text has to support the sentence when the product claims the corpus said it.

### float-encoding
- title: The embeddings example asks for a float vector
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What does the embeddings guide's JavaScript example request as encoding_format?

---

It sends encoding_format float, the model name, and the input string. The response data contains the embedding array, an index, and usage token counts.

You store that array. The guide says you can put it in a vector database and use it for the listed use cases. It recommends a vector database when you need k nearest neighbors quickly, and it points at cookbook examples rather than naming one database as required.

### vector-db-for-knn
- title: OpenAI tells you to use a vector database at scale
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

How does the embeddings FAQ say you should retrieve k nearest vectors quickly?

---

It says to use a vector database, and it points to cookbook examples that combine those databases with the API.

The FAQ does not name a required vendor. It points you at a vector database when the set is large enough that you need the k nearest vectors quickly, and at cookbook examples for wiring those databases to the API.

### owned-but-lawful
- title: Ownership does not waive the content rules
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

The FAQ says you own your embeddings. What obligation does the same answer include?

---

You are responsible for ensuring that the content you send to the API does not violate applicable law or the terms of use.

Ownership of the vector sits in the same answer as that duty. The FAQ does not treat the embedding as exempt from the rules that apply to the text you submitted.

### pages-per-dollar
- title: The pricing table assumes about 800 tokens a page
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What assumption is behind the embeddings guide's pages-per-dollar column?

---

The guide says the column assumes about 800 tokens per page. Under that assumption it lists about 62,500 pages per dollar for text-embedding-3-small, about 9,615 for text-embedding-3-large, and about 12,500 for text-embedding-ada-002.

Your pages are not 800 tokens. A scanned PDF with little text, or a dense contract, will not match the column. Bill from input tokens, which is the actual charge, and use the column only as the guide's illustration.

### ada-still-listed
- title: ada-002 remains in the embeddings model table
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

Does the embeddings guide still list text-embedding-ada-002?

---

Yes. The table includes it with a max input of 8,192 tokens and an MTEB figure of 61.0 percent, beside the two v3 models. The guide calls the v3 models the third-generation models, marked by -3 in the id.

It is a separate row from text-embedding-3-small and text-embedding-3-large. Those v3 models are the ones with documented default lengths of 1,536 and 3,072. A vector from ada-002 is not one of those v3 vectors.

### index-zero
- title: Read the vector out of the embeddings object
- version: Core
- level: intermediate
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

What is the index field on an embedding object?

---

The sample response is a list. The embedding object inside it has index 0 and the embedding array. usage reports prompt_tokens and total_tokens.

Read the vector from that object. The rest of the payload is metadata about the call. Saving the whole JSON object as if it were the float list stores the wrong value.

### relatedness-direction
- title: Small distance means more related
- version: Core
- level: beginner
- status: verified
- source: https://developers.openai.com/api/docs/guides/embeddings

How should you interpret the distance between two OpenAI embeddings?

---

The guide says small distances suggest high relatedness and large distances suggest low relatedness. The vector is a list of floats.

A larger distance is the less related pair. If you sort the other way, you rank the least related strings first. The guide's search use case wants the small distances.

### rag-agentic-start
- title: New RAG work starts on agentic retrieval
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What does the RAG overview recommend for a new implementation?

---

It says to start with agentic retrieval for new RAG implementations, and to consider migrating existing solutions for the accuracy and context gains it describes.

It also says to stay on classic RAG when you need GA features, speed, existing orchestration, or fine control. The recommendation is not a ban on classic RAG. It is a default for new work, with those exceptions.

### security-trimming-classic
- title: Classic RAG trims documents
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

What document-level control does classic RAG list?

---

The classic security section lists document-level security trimming, Entra ID permission metadata for indexed Azure Storage content, filter-based security at query time for other sources, and private endpoints.

Trimming has to happen before the passage is given to the model. A filter that runs only in the UI still lets the model see the forbidden chunk if the query did not include it. The agentic path adds knowledge-source access control and SharePoint permission inheritance for remote SharePoint.

### response-time-parallel
- title: Parallel subqueries are the latency design
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

How does the RAG overview say agentic retrieval stays inside a few seconds?

---

It lists parallel subquery execution, adjustable reasoning effort of minimal, low, or medium, and semantic ranking that is already in the pipeline so you do not orchestrate a second hop yourself.

Classic RAG's answer to the same problem is a single millisecond-scale query and a simpler architecture. If you add sequential calls to several indexes yourself, you have rebuilt the slow path the overview is trying to avoid.

### token-select-and-top
- title: Concise results are a query setting
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Which classic RAG controls keep the prompt small?

---

The overview names semantic ranking of the top 50, top-k for vectors, top-n for text, minimum thresholds, scoring profiles that boost critical content, and a select list of fields.

Each control can also drop the one passage you needed. Log the ids that survived. A small prompt that omitted the rule is a retrieval configuration bug, and the model will answer without that rule.

### synonym-map-terminology
- title: Synonyms cover terminology mismatch
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

Besides vectors, what does the RAG overview offer for words that do not match?

---

It lists synonym maps and semantic ranking for terminology mismatches. Vectors cover similarity. Analyzers cover language-specific tokenization.

A synonym map is explicit: you say that two tokens are equivalent. A vector might place them near each other and might not. The semantic ranker applies the map during reranking only when the field is in the semantic configuration and synonym support is enabled.

### ocr-then-embed
- title: OCR output is what the embedding sees
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview

A scanned contract retrieves nothing. What skill category does the overview point at?

---

It lists OCR, image analysis, image verbalization, and document extraction skills for images and PDFs.

Until one of those skills runs, the index has no text to embed or to match with BM25. Check the skill output before you retune k. An empty content field is an ingestion failure.

### knowledge-base-unifies
- title: One retrieve call can cover several sources
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What does a knowledge base unify?

---

The agentic overview says the knowledge base orchestrates the pipeline, manages the knowledge sources, and holds the query parameters. You call it once with the retrieve action.

Each source still has its own content and its own permissions. Unification is the query interface, not a merge of the underlying access rules. A source the caller cannot read should contribute nothing to the merged grounding data.

### low-effort-default
- title: Low effort is the default planning level
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What retrieval reasoning effort do you get if you do not set one?

---

The overview says reasoning effort defaults to low and is configured on the knowledge base. Low and medium send the query and history to a planning model. Minimal skips that step.

Medium is the level the relevance overview associates with a possible second pass. If you wanted that second pass and left the default, you are on low, which plans once and does not invoke L3.

### extractive-ga
- title: GA agentic retrieval is minimal and extractive
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What does the generally available agentic path return?

---

The overview assigns API 2026-04-01 to production workloads that use GA knowledge source types with minimal, extractive retrieval.

Extractive means the service returns retrieved content rather than a preview answer-synthesis paragraph. If you need a written answer on the GA path, your application calls the model, which is the classic handoff. Preview synthesis stays on the preview API.

### cost-fewer-sources
- title: Fewer sources mean less fan-out
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What cost controls does the agentic overview actually list?

---

Read the activity log, reduce the number of knowledge sources so fan-out and token volume drop, lower the reasoning effort, and organize content so the answer can be found in fewer documents, for example with curated summaries or tables.

The page's dollar example uses hypothetical prices and an assumed chunk size. Use it as an illustration of the method, and use the pricing pages for rates. The controls above are the operational advice that does not depend on those hypothetical rates.

### curated-summaries
- title: A summary chunk can be the thing you retrieve
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Why does the cost section mention curated summaries or tables?

---

It says organizing content so the relevant information is found in fewer sources and documents lowers token use. Curated summaries or tables are the example.

A summary is still a document you must keep in sync with the policy. A stale summary is the same freshness bug as a stale PDF, and it can outrank the longer source because it is denser. Keep the source chunk available to cite.

### web-result-summary
- title: An LLM can summarize web results inside the pipeline
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Which preview stages can the language model perform in agentic retrieval?

---

The component table says the LLM can plan queries and select knowledge sources, summarize web results, and generate citation-backed answers through answer synthesis. Planning, source selection, and answer synthesis are marked preview.

Semantic reranking of each subquery is the search service's ranker, not that LLM. If web summarization is on, the grounding text may be a summary of a page rather than the page. Cite the reference the pipeline returns, and know that a summary can drop a condition.

### retrieve-action
- title: You call retrieve, not a free-form agent loop
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What operation does application code call on a knowledge base?

---

The overview says you call the retrieve action, passing the query and the conversation history. The knowledge base then plans, executes, and synthesizes the response.

Your code handles that response. It does not have to issue each subquery. If you also run your own search beside it, you now have two retrieval paths and two places a filter can be forgotten.

### preview-terms
- title: Preview agentic features are not the production default
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What caution does the agentic overview attach to preview features?

---

It says preview features are not covered by a service-level agreement, are not recommended for production, and might change or be constrained before general availability. The preview REST version it names is 2026-08-01-preview.

The On Your Data retirement page says the same thing about the migration sample's auto and answer-synthesis path. Production, in both articles, is the GA extractive or classic path. Build the demo on preview if you need it, and do not promise the preview contract as stable.

### region-select-agentic
- title: Agentic retrieval is not in every region
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Is agentic retrieval available everywhere Azure AI Search runs?

---

The overview says to review regional availability, and that agentic retrieval is available in select regions. Limits on knowledge sources and knowledge bases vary by pricing tier and by reasoning effort.

Vector search, by contrast, is documented as all regions and all tiers. A design that assumes agentic retrieval in every region where vectors work will fail the region check. Confirm the region before you promise the pipeline.

### semantic-built-in
- title: You do not add a second rerank hop for agentic retrieval
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Do you call the semantic ranker yourself during agentic retrieval?

---

The overview says each subquery is semantically reranked inside the pipeline, and the semantic ranker is listed as a component used internally for L2.

Classic RAG makes semantic ranking optional on the query. Agentic retrieval includes it. You still pay for it, on the agentic token meter rather than the per-query semantic meter described for the classic pipeline.

### merged-always
- title: You always get the merged chunks back
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

If you turn off answer synthesis, what is left in the response?

---

Merged content is always returned. References and the activity log are optional. Synthesis is an optional preview that adds a formulated answer.

The merged content is the grounding payload. Your model call should use that payload. If synthesis is on, you still want the references so the formulated answer can be checked against the chunks.

### spelling-reason
- title: Spelling mistakes are a stated reason to use agentic retrieval
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

Which query defects does the agentic overview say it can absorb?

---

It lists multi-ask questions, dependence on conversation context, rewriting through synonym maps and LLM paraphrases, and spelling mistakes.

Semantic query rewrite also claims typo correction, up to 10 variants, as a preview feature on the semantic ranker. Agentic retrieval can use that class of rewrite as part of a larger plan. A misspelled query on classic keyword search, with no rewrite, still depends on exact tokens.

### hotel-example-multiask
- title: One sentence can contain three retrieval problems
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What multi-ask example does the agentic overview use?

---

It uses a request for a hotel near the beach, with airport transportation, that is within walking distance of vegetarian restaurants.

A single vector string averages those constraints. Subqueries can chase each part. Filters still have to express hard constraints such as city or tenant. The planner does not replace a filter.

### chat-history-required-input
- title: History is an input to retrieve
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview

What inputs does the retrieve action take?

---

The overview says the application provides a query and conversation history.

An empty history makes a follow-up question ambiguous. The planning model cannot recover context you did not send. This is separate from On Your Data's intent field, which that schema tells you to ignore.

### internal-semantic
- title: L2 is mandatory inside agentic retrieval
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Is semantic ranking optional for agentic retrieval?

---

The relevance overview says semantic ranking is optional for text queries and for vector queries that contain text, and required for agentic retrieval. It says the ranking algorithm for agentic retrieval is the semantic ranker, even though several queries are sent.

You cannot turn that L2 step off to save the semantic model while keeping the agentic pipeline. The billing section shows it as part of the retrieval-token charge. Classic search is where the semantic ranker is optional.

### filter-only-not-rag
- title: A filter-only request is not a RAG retrieval
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

You query with a filter and no search text, then paste the hits into a prompt. What ranking did you skip?

---

The relevance overview says a filter-only query does not run a ranking algorithm and returns a uniform score of 1.0.

The hits are an unranked set that satisfied the filter. They may be irrelevant to the question. RAG retrieval needs a query that scores relevance, then a filter that enforces permissions, in the mode you chose.

### geospatial-unranked
- title: A geo query alone does not rank by meaning
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Does a geospatial query produce a relevance ranking?

---

The relevance overview lists geospatial search among the query forms that do not run relevance ranking, with autocomplete, suggestions, fuzzy search, and regular expressions.

The hybrid overview still uses a geo filter together with search text and vectors, and that combination does rank. The filter restricts the set. The text and vector queries rank it. A geo predicate by itself does not know which hotel description answers the question.

### fuzzy-not-semantic
- title: Fuzzy search is not semantic ranking
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Is fuzzy search the same as semantic ranking?

---

The relevance overview lists fuzzy search as a specialized form that does not run the relevance ranking algorithm. Semantic ranking is the L2 model that rescores BM25 or RRF text.

Fuzzy matching tolerates character differences. Semantic ranking compares meaning on the top 50. Query rewrite may also fix typos, in preview. They are three different mechanisms, and only the semantic path produces @search.rerankerScore.

### regex-unranked
- title: A regular expression does not produce a relevance order
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

You search with a regular expression and the scores are all 1.0. Is the index broken?

---

No. Regular expression search is in the list of query forms that skip ranking. The uniform 1.0 score means no ranking algorithm ran.

Use the regex as a filter-like constraint beside a ranked query if you need both an exact pattern and a relevance order. The score will then come from BM25, a vector metric, or RRF, and you can read it on that scale.

### top-1000-profile
- title: A scoring profile on text looks at the top 1,000 BM25 hits
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

How many BM25 hits does a scoring profile consider on a text query?

---

The relevance overview says that for standalone text queries, scoring profiles identify the top 1,000 BM25 matches, and the top 50 are returned.

A document at BM25 rank 1,001 never gets the freshness boost. If the boost was supposed to save an older-token document that is newly updated, it has to be inside that 1,000 first. This is a cousin of the semantic ranker's top-50 cutoff.

### pure-vector-profile
- title: A scoring profile can still touch the payload of a vector hit
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

If the query is vector-only, can a scoring profile do anything?

---

The relevance overview says that if the k matching documents include nonvector fields, the profile is applied to those nonvector fields.

The vector ranking article says vector queries do not have scoring-profile or term boosting as vector tuning features. Read together, the boost applies to the text or numeric fields on the hits, not to the distance. A title weight can reorder equal neighbors. It does not change the embedding.

### final-boost-after-rrf
- title: The profile is reapplied after fusion
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Why does the relevance overview say hybrid text hits are restored to BM25 order?

---

The scoring profile first identifies the top 1,000 text matches. Those hits are then restored to original BM25 order so RRF can fuse them with the vector hits. After fusion, the profile is applied to the merged results, with vector weighting, and semantic ranking is last.

If you inspect the text list after the profile and before fusion, you are not looking at the final order. The final order also depends on the vector list and, if you asked for it, the semantic score.

### reranker-boosted-unlimited
- title: The boosted semantic score is not capped at 4
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

Why might @search.rerankerBoostedScore be 12 when the semantic scale stops at 4?

---

The relevance table says @search.rerankerScore is 0.00 to 4.00, and @search.rerankerBoostedScore runs from 0 with no upper limit. The prose says boosted scores can be significantly higher than 4.

The 4-to-0 meanings describe the unboosted semantic score. Apply those labels only to @search.rerankerScore. The boosted value includes the scoring profile and can be used for ordering when rankingOrder says so.

### image-l1
- title: Images are ranked with the vector L1 algorithms
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What score does a multimodal image hit get first?

---

The relevance overview says image and multimodal searches are vector queries and use the L1 vector ranking algorithms.

L2 semantic ranking needs text. A hit that is only an image vector can be nearest in embedding space and still have nothing for the semantic ranker to read unless you stored a caption or a verbalization beside it.

### two-strategies
- title: Classic hybrid and agentic retrieval are the two documented strategies
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What two relevance strategies does the relevance overview highlight?

---

Hybrid search with the semantic ranker, and agentic retrieval with LLM query planning and answer synthesis in preview, over a knowledge base that defines the search domain.

Both still depend on grounding data of enough quantity and quality. The overview says you can list multiple knowledge sources to widen what is searchable, and retrieval instructions to pick among them. A second strategy does not repair a corpus that lacks the fact.

### agentic-decomposes
- title: The planner can narrow or widen a question
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What query transformations does the relevance overview attribute to the planning model?

---

It says the model can decompose a complex question into targeted subqueries, refine a vague request, or generalize a narrow one. It uses chat history and retrieval instructions.

Generalizing a narrow question can pull in extra documents. That helps recall and can hurt precision. The activity log is how you see whether the plan widened the query. If it widened past the user's constraint, put the constraint in a filter.

### grounding-quantity
- title: Relevance needs enough good text
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What non-algorithm requirement does the relevance overview state?

---

It says relevance also depends on grounding data of sufficient quantity and quality.

No ranker creates a policy that was never ingested. Quantity matters because the answer might be split across chunks. Quality matters because a duplicate or a stale copy can outrank the current one. Both show up before the model is at fault.

### diagram-ranking-order
- title: rankingOrder picks the score you sort by
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

What does rankingOrder control?

---

The relevance overview says that if you use semantic ranking, rankingOrder decides whether results follow @search.rerankerScore or the boosted @search.rerankerBoostedScore created after the scoring profile.

Leave it unset and you may be looking at a different order than the one you explain in an interview. Name the property you sorted by when you discuss a result. The sample hybrid semantic response in that article shows both the RRF score and the reranker score.

### example-hybrid-semantic-fields
- title: The sample hybrid semantic query sends the same text twice
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/search-relevance-overview

How does the relevance overview's sample query feed the vector side?

---

The sample sets search to a text string and a vector query of kind text with the same string, targeting a text vector field and an image vector field. queryType is semantic, with a semantic configuration, and top is 5.

kind text means the service vectorizes the string, which is the integrated-vectorization query path. You do not have to send a raw float array when a vectorizer is configured. The fields list is what gets searched, including the image vector if that field is in the list.

### kind-text-vectorizer
- title: A text vector query uses the index vectorizer
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

How can a query avoid sending a raw embedding array?

---

Integrated vectorization says you formulate a vector query that specifies the text string to vectorize, using the vectorizer on the index. That vectorizer must be the same model that built the stored vectors.

The relevance sample uses kind text for that pattern. If the vectorizer is missing, the service cannot encode the string. If it is a different model, it encodes the string into the wrong space. Both failures look like poor recall.

### chunk-free-embed-not
- title: Splitting is free and embedding is not
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Which integrated-vectorization step can exhaust an Azure OpenAI quota?

---

The embedding skill or vectorizer calls the model. Token quotas apply. The Text Split skill is the step the article says is free.

A failure during embedding leaves you with chunks and without vectors, or with a partial index if some batches succeeded. The built-in retry does not expand the quota. A scheduled rerun is the documented recovery.

### five-minute-example
- title: Five minutes is an example schedule, not a requirement
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Does integrated vectorization require a five-minute indexer schedule?

---

The article recommends a schedule and gives every 5 minutes as an example, so throttled documents get another chance and changes in storage, SQL, or Cosmos DB flow through the pipeline.

The interval is an example. The requirement is that something reruns the pipeline when data changes or when a batch was throttled. A manual run you forget about is how the index goes stale.

### primary-parent-fields
- title: The parent index holds the bibliographic fields
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

What does the article say the primary index contains in the PDF example?

---

Basic information such as title, date, author, and description. The secondary index holds chunks of searchable content.

A RAG prompt that receives only the parent may be too coarse. A prompt that receives only the chunk may lack the title. The pattern the article describes returns the parent when the chunk matches, so the caller can use both. Your select list still decides what the model actually reads.

### nonconfigurable-retry
- title: You cannot set the indexer retry count
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Can you configure the embedding retry policy on the indexer?

---

The article says batching and retry logic are built in and are not configurable. Azure AI Search retries throttling errors from the Azure OpenAI token quota. If the quota is exhausted, retries fail.

The lever you do have is a schedule that tries again later, and a separate deployment so query traffic does not consume the indexing quota. There is no documented setting for retry count or backoff on that page.

### sites-group-id
- title: Custom embedders use the sites private-link group
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Which private-link group id does the article assign to a custom embedding endpoint?

---

sites, for App Service and Azure Functions that host an embedding model other than the Azure OpenAI models. openai_account is the group for Azure OpenAI.

Shared private link is Azure-to-Azure only. An OpenAI API host on the public internet is out of scope for that private link. Plan the network path before you promise a fully private embedding call.

### vector-store-scenario
- title: A vector-only index still has a key
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Can every field except the key be a vector?

---

The article says you can build a vector store where all fields are vectors and the document id, which a search index requires, is the only string field. You query for ids, then send those vectors to another model.

That pattern does not give a language model a passage to read. RAG needs the text fields. Use the vector-only shape for a store that returns ids, and keep chunk text when the next step is generation.

### add-semantic-later
- title: The diagram is not the whole search service
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization

Does integrated vectorization prevent semantic ranking?

---

The article says the diagram focuses on vectorization and that you can still add skills, a knowledge store, semantic ranking, and relevance tuning.

Vectorization fills the vector field. Semantic ranking reads the text fields. You need both in the index if you want the hybrid-plus-semantic strategy the relevance overview recommends.

### portal-import
- title: The portal wizard is the no-code start
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Which no-code start does the vector overview mention?

---

It lists the Import data wizard in the Azure portal, alongside the REST APIs and the SDKs for .NET, Python, and JavaScript, and Microsoft Foundry.

The wizard is a way to create the pipeline. The concepts stay the same: embeddings, an index, and a query that asks for k neighbors. A wizard-created index can still lack a semantic configuration until you add one.

### langchain-common
- title: Azure AI Search is used from LangChain
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Does the vector overview mention an open-source integration?

---

It says Azure AI Search is commonly used in open-source frameworks like LangChain.

The chunking article also names LangChain text splitters as an external chunking option. The framework does not change HNSW, filters, or semantic ranking. Those are still Azure AI Search behaviors, and the interview answers should cite those behaviors.

### sbirt-example
- title: Open-source embedders are allowed
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Does vector search require Azure OpenAI embeddings?

---

The overview's similarity-search scenario says you can encode text with embedding models or open-source models, and it names OpenAI embeddings and SBERT as the examples. It recommends Azure OpenAI for text and the image vectorize API for images.

A recommendation is not a protocol requirement. Whatever model you choose has to embed both the corpus and the query. SBERT vectors and Azure OpenAI vectors do not share a space.

### filtered-vector-scenario
- title: Filtered vector search is a named scenario
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Is filtering a supported vector scenario or a workaround?

---

The vector overview lists filtered vector search as a scenario. The request includes a vector query and a filter expression. Filters apply to text and numeric fields and can include or exclude results.

The scenario exists because metadata constraints are normal: category, date, tenant. The vector field stays unfilterable. Design the filterable fields at index time. You cannot add a filter later on a value you never stored.

### hybrid-defined
- title: Hybrid means same request, both query types
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

How does the vector overview define hybrid search?

---

It defines hybrid search as vector search and keyword search in the same request. Vector support is at the field level. If the index has both kinds of fields, one query can target both. The queries run in parallel and the results are merged and ranked.

That definition matches the hybrid overview: one request, parallel execution, RRF. Two separate API calls whose results you merge in application code are not the hybrid query those pages describe, and they will not apply RRF for you.

### memory-knowledge-grounding
- title: Three jobs for a vector index
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What applications does the vector overview name for a vector index?

---

Long-term memory, a knowledge base, grounding data for RAG, and an application that uses vectors.

Grounding data is the RAG job: the passages the model must follow. Long-term memory is a store the agent queries later. Both need a freshness story and a filter story. The index does not supply either by being a vector index.

### all-tiers
- title: Vector search is on every pricing tier
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Do you need a specific Azure AI Search tier for vector queries?

---

The overview says vector search is available in all regions and on all tiers, with no extra charge for the vector search feature itself.

Quotas still differ, including the higher vector quotas on services created after 3 April 2024. Semantic ranking and agentic retrieval have their own regional limits. A free-tier vector query can work in a region where the semantic ranker does not.

### model-provider-charges
- title: The embedding bill is not the search bill
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

You enabled vector search and the Azure OpenAI bill went up. Why does the overview say that can happen?

---

It says generating embeddings or using AI enrichment for vectorization might incur charges from the model provider. The search feature itself has no extra charge.

Integrated vectorization makes those calls for you, at index time and at query time, so both paths can bill tokens. A query-time vectorizer on every user question is a steady embedding cost, not only an indexing cost.

### sdk-list
- title: REST and three SDKs are the programmatic options
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Which clients does the vector overview list?

---

The Import data wizard, the Search REST APIs, the Azure SDKs for .NET, Python, and JavaScript, and other Azure offerings such as Microsoft Foundry.

The behavior is the service's, not the SDK's. A Python sample and a REST call that set the same k, filter, and semantic configuration get the same ranking. Debug the request body when two clients disagree.

### field-level-vectors
- title: Vectors live on fields, not on a separate index type
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

Where do embeddings sit in an Azure AI Search index?

---

The vector overview says vector support is implemented at the field level, and that the service creates vector indexes for each vector field. An index can hold vector fields and ordinary fields together.

That is why hybrid search is one index, not two systems you keep aligned. It is also why a filterable tenant field can sit beside the vector. A second index for vectors only is optional, as in the parent and chunk pattern, not required.

### nearest-neighbors-placement
- title: Indexing places similar vectors near each other
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What does the vector overview say the index does with embeddings?

---

On the indexing side, Azure AI Search uses a nearest-neighbors algorithm to place similar vectors close together. Internally it creates a vector index per vector field.

The ranking article names that algorithm as HNSW for the approximate case, plus exhaustive KNN when you ask for an exact scan. Closeness is defined by the similarity metric you configured. A cosine index and a Euclidean index of the same floats are not the same neighbor graph.

### query-encode-step
- title: The query is encoded before it is compared
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What happens to user text before a vector query runs?

---

The client collects the user input, usually as a prompt. An encoding step turns it into a vector, either in the application or through integrated vectorization. Azure AI Search then returns the k nearest documents.

If you skip the encoding step and send the raw string in the vector array, the query is not in the embedding space. Use a vector query kind that accepts text when a vectorizer exists, or embed the string with the same model first.

### better-together
- title: The overview's result claim for hybrid
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What does the vector overview claim about hybrid results versus either method alone?

---

It says hybrid scenarios that run vector and keyword search in parallel and return one result set often provide better results than vector or keyword search alone.

Often is the word on the page. The hybrid overview adds that benchmarks showed significant gains when the semantic ranker is included. Neither page gives you a percentage you can quote as universal. Measure your corpus.

### dog-canine
- title: Conceptual match is the vector pitch
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What example does the vector overview use for conceptual likeness?

---

It uses dog and canine as words that are conceptually similar and linguistically distinct.

The strings share no requirement to share tokens. The overview pairs this conceptual match with hybrid search when you also need keyword precision, and with a filter on a text or numeric field when similarity alone must not decide membership.

### dog-hund
- title: Cross-language match is a vector feature
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What example does the vector overview use for multilingual vector search?

---

dog in English and hund in German.

This works when the embedding model maps those words near each other. It is not the language analyzer. The overview says to use analyzers when you want translation-style control on the nonvector part of a hybrid query.

### dog-image
- title: A word can match an image embedding
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

What example does the vector overview use for multiple content types?

---

The word dog and an image of a dog, when both are encoded with a multimodal embedding.

A text embedding of the alt text is a different system. The overview names CLIP and GPT-4 Turbo with Vision for the shared space. If you only embedded captions, you are doing text search over captions, and an image with a bad caption will not be found.

### open-source-skill
- title: You can call an open-source model from a skill
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/search/vector-search-overview

How does a non-Azure embedding model get into the indexer?

---

The overview says that if you have embedding models and chat models trained for multiple languages, you can call them through custom or built-in skills on the indexing side, or through vectorizers on the query side.

The integrated vectorization article is the mapping from skill to vectorizer. Both sides must use the same model. A custom skill that is only wired at indexing time will leave queries unencoded or encoded by a different model.
