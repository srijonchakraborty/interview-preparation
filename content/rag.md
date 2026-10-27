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
