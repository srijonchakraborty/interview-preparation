# Microsoft Foundry

### what-is-foundry
- title: Microsoft Foundry is the current name of Azure AI Foundry
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/navigate-from-classic

An interviewer says "Azure AI Foundry" and the portal says "Microsoft Foundry". What are you looking at, and what was it called before?

---

It is one platform that has been renamed. Microsoft's docs map the names in order: Azure AI Studio, then Azure AI Foundry, then Microsoft Foundry. The Azure resource type did not follow the marketing name. It is still `Microsoft.CognitiveServices/accounts`.

Use the current name, Microsoft Foundry, and mention the older names so you and the interviewer mean the same product. The resource you deploy did not get a new type. It is still `Microsoft.CognitiveServices/accounts`.

### resource-versus-project
- title: One Foundry resource, several projects
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

When do you create a new Foundry project instead of a new Foundry resource? When is a standalone Azure OpenAI resource enough?

---

The Foundry resource is the governance boundary: private networking, customer-managed encryption, and RBAC. Projects under it isolate development work. A single developer should start with one resource and one project.

Create another resource when the network boundary, the encryption key, or the RBAC boundary has to differ. A standalone Azure OpenAI resource is enough only when the workload needs completions and does not need agent hosting or evaluation. Several teams that can share those resource controls should be separate projects, not separate resources.

### foundry-models
- title: A deployment type chooses residency, price, and throughput
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

You deploy a model in Microsoft Foundry. What does the deployment type decide, and when is there no deployment at all?

---

For a Serverless API deployment, the type decides three things: where inference is processed (global, a data zone, or an Azure geography), how you pay (pay-per-token or reserved capacity), and the performance limits (latency variance and throughput). The main categories are standard (pay-per-token), provisioned (reserved capacity), and batch (discounted asynchronous processing). A Developer type exists for evaluating a fine-tuned model.

Open-source and custom models on managed compute do not use these serverless types. Data stored at rest stays in the designated Azure geography. Global processing may run in any Azure region. Data-zone processing stays in the US, EU, or Asia Pacific zone. There is also an instant-access preview where you call a supported model by name and do not create a deployment first, so "we always create a deployment" is too strong.

### agent-service
- title: Foundry Agent Service replaced the Assistants API
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/navigate-from-classic

What should a new agent use on Azure, and what happened to the Assistants API on 26 August 2026?

---

New work uses the generally available Microsoft Foundry Agent Service. The classic-portal migration note sets 26 August 2026 as the sunset for the Assistants API and tells you to move those workloads to Foundry agents. The same note retires the `azure-ai-inference` package on that date and points callers at the `openai` package.

Do not start a new assistant on the retired API, and do not keep a production dependency on the retired package. The migration is a client and service change, not a prompt rewrite.

### content-safety
- title: Content filters are a separate control from the system prompt
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview

Where do you enforce that a Foundry app blocks violent content or jailbreak attempts, and why is a sentence in the system prompt not that control?

---

Azure AI Content Safety is a separate service from the prompt. Analyze text scans for sexual content, violence, hate, and self harm, and it reports severity. Prompt Shields scans text for the risk of a user-input attack on a language model. Those APIs return a moderation result. A sentence in the system prompt does not.

For a Foundry app, name Content Safety as the place a block decision is made. Identity and RBAC are a separate control, covered on their own. Do not describe the prompt as the filter.

### identity-and-rbac
- title: RBAC and secrets sit on the Foundry resource
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Which identity does the architecture doc assign, and which controls belong on the Foundry resource rather than on a prompt?

---

Projects isolate development work. The resource is the governance boundary. The documented access example is each project managed identity assigned the Foundry User role at the Foundry resource scope. RBAC can also be scoped at the project.

Private networking and customer-managed encryption are resource settings. API-key connection secrets go in Key Vault: a managed vault by default, or your own vault connected to the resource. A key in a notebook is a stored secret, not a role assignment. Use a standalone Azure OpenAI resource only when the workload needs completions and does not need agent hosting or evaluation.
