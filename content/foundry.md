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

### foundry-one-management-plane
- title: One resource for agents, models, and tools
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What does Microsoft Foundry put under a single management grouping?

---

Microsoft Foundry unifies agents, models, and tools under one management grouping, with tracing, monitoring, evaluations, and enterprise setup on that platform. Access control, networking, and policies sit under one Azure resource provider namespace.

Do not describe Foundry as a portal skin on a pile of unrelated accounts. The interview point is one management plane for the agents, models, and tools you run there.

### catalog-over-ten-thousand-models
- title: The catalog holds more than 10,000 models
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

How large is the model set an interviewer should expect you to name for Microsoft Foundry?

---

The product overview says you can access more than 10,000 models from Microsoft, OpenAI, Anthropic, Meta, and others through the Foundry Models catalog.

Do not quote a small fixed list as the catalog. Name the catalog, then say a given model still has to be available for your deployment option and region.

### upgrade-openai-keeps-keys
- title: Upgrading Azure OpenAI keeps the endpoint and keys
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What survives when you upgrade an Azure OpenAI resource to a Foundry resource?

---

The Foundry overview says you can upgrade an Azure OpenAI resource to a Foundry resource while preserving the endpoint, API keys, and existing state.

The trap is planning a cutover that rotates every key and rewrites every endpoint. Check the upgrade path before you assume the client configuration must change.

### hub-projects-stay-in-classic
- title: Hub-based projects stay in the classic portal
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Where do hub-based projects live after the move to Microsoft Foundry?

---

Hub-based projects remain accessible in the Foundry (classic) portal. New investment is focused on Foundry projects in the new portal.

Do not tell a team to recreate a hub project in the new portal and expect the same project type. New work targets Foundry projects. Classic hub projects stay on the classic portal.

### prompt-agent-is-declarative
- title: A prompt agent is instructions, a model, and tools
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What is a prompt agent, and what do you not have to run yourself?

---

A prompt agent is the declarative end of the spectrum. You specify instructions, choose a model, and attach tools in the portal or with the SDK. Foundry hosts and runs it, with no application code or containers to maintain.

If the interviewer says every Foundry agent is a container, correct that. Containers are the hosted-agent path. A prompt agent is configuration Foundry runs for you.

### hosted-agent-is-your-container
- title: A hosted agent runs your code in Foundry
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

When would you deploy a hosted agent instead of a prompt agent?

---

A hosted agent is the full-code end of the spectrum. You bring your own code or a framework such as Microsoft Agent Framework, LangGraph, or Semantic Kernel, package it as a container, and Foundry runs it with a managed endpoint, scaling, identity, and observability.

You can start with a prompt agent and move to code as the need grows. Do not jump to a container when instructions, a model, and tools are enough.

### single-model-call-without-agent
- title: Skip the agent when you only need a completion
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

When should a Foundry app skip agents and just call a model?

---

If you only need to send prompts to a model, with no tools and no orchestration, start with a single model call.

The trap is standing up Agent Service for a one-shot completion. Agents are for a model paired with instructions and tools that can reason and take action.

### foundry-developer-surfaces
- title: Portal, SDKs, azd, VS Code, and MCP
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Which developer surfaces does Microsoft Foundry document?

---

Foundry documents the portal for exploring models and building prompt agents without code, SDKs for Python, C#, JavaScript, and Java, the Azure Developer CLI for hosted-agent projects, Visual Studio Code with the Foundry extension, and coding agents through the Foundry Skill and MCP server.

Many developers combine them, for example prototyping in the portal and then moving to code. Do not treat the portal as the only supported way to build.

### azure-ai-services-are-foundry-tools
- title: Azure AI Services is now Foundry Tools
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What is the current name for what used to be called Azure AI Services?

---

The evolution table maps the brand Azure AI Services to Foundry Tools. The same table maps the portal Foundry (classic) to Foundry.

Say Foundry Tools when you mean that brand. Microsoft Foundry is the platform name, not a synonym you should invent for every old Cognitive Services product.

### responses-api-replaces-assistants
- title: Agents v2 uses the Responses API
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Which API should a new Foundry agent call, and what did it replace?

---

The evolution table maps the Assistants API, called Agents v0.5/v1, to the Responses API, called Agents v2. Monthly api-version parameters map to v1 stable routes under /openai/v1/.

Do not start new work on the Assistants API. The current agent API in that table is the Responses API on the v1 route.

### old-sdks-became-one-project-client
- title: One project client replaces the old SDK split
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What client does the Foundry evolution table tell you to use instead of the old inference packages?

---

The table maps multiple packages, including azure-ai-inference, azure-ai-generative, azure-ai-ml, and AzureOpenAI(), against five or more endpoints, to a unified project client, azure-ai-projects 2.x, plus OpenAI() against one project endpoint.

The trap is keeping a production dependency on the retired split. New code targets the project client and one project endpoint.

### threads-became-conversations
- title: Threads and runs became conversations and responses
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What are the current names for threads, messages, runs, and assistants?

---

The evolution table maps Threads, Messages, Runs, and Assistants to Conversations, Items, Responses, and Agent Versions.

If an interviewer still says thread and run, translate it. Those words are the previous terminology, not the current Foundry names.

### observability-dashboards-are-preview
- title: Built-in monitoring dashboards are preview
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Is Foundry monitoring generally available just because tracing is on the platform?

---

The overview lists observability as tracing and evaluating agents and models, and monitoring them with built-in dashboards, and it marks those dashboards as preview. It also says some platform capabilities are in preview and points you at the general availability overview for status.

Do not call every observability surface GA. Separate tracing from the preview dashboards, and check the GA table before you promise a production monitor.

### voice-agent-uses-voice-live
- title: Voice agents are hosted through Voice Live
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Who runs the speech orchestration for a voice-based prompt agent?

---

You configure the model, instructions, audio settings, an optional greeting, and tools, then connect through Voice Live. Foundry manages the agent lifecycle and voice orchestration, so you do not host that infrastructure yourself.

A voice-based prompt agent is still a prompt agent with speech, not a reason to build your own speech pipeline first.

### cognitive-services-is-the-provider
- title: Foundry uses Microsoft.CognitiveServices
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Which resource provider does the architecture doc assign to Microsoft Foundry?

---

Microsoft.CognitiveServices supports agentic and generative application development. The Foundry resource type is Microsoft.CognitiveServices/accounts with kind AIServices, and it lists Agents, Evaluations, Azure OpenAI, Speech, Vision, Language, and Content Understanding.

A Foundry project is the child type Microsoft.CognitiveServices/accounts/projects, also kind AIServices. Speech, Language, and Vision accounts are the same provider with kinds Speech, Language, and Vision.

### search-is-a-separate-provider
- title: Azure AI Search is not the Foundry provider
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Which provider does the architecture use for knowledge retrieval?

---

Microsoft.Search supports knowledge retrieval over your data through Azure AI Search. Foundry itself stays on Microsoft.CognitiveServices.

The trap is assuming a Foundry resource includes Search as a child. Search is a connected resource with its own provider and its own governance.

### upgrade-keeps-existing-rbac-actions
- title: An OpenAI upgrade keeps existing RBAC actions
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Do custom Azure Policy and RBAC actions break when you upgrade Azure OpenAI to Foundry?

---

Foundry resources share the Microsoft.CognitiveServices provider namespace with Azure OpenAI, Speech, Vision, and Language. The architecture doc says that if you upgrade from Azure OpenAI to Foundry, existing custom Azure policies and Azure RBAC actions continue to apply.

Shared provider aliases are why. Do not plan a new RBAC action namespace as part of that upgrade.

### project-holds-files-agents-evals
- title: Projects scope files, agents, and evaluations
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What is a project allowed to hold, compared with the Foundry resource?

---

The resource is where you manage governance such as networking, security, and model deployments. A project is the development boundary where teams build and evaluate use cases, and project assets are files, agents, evaluations, and related artifacts.

Projects reuse model deployments and connections that already exist on the resource. Do not recreate the resource just to give a team a place to build.

### connected-resources-own-governance
- title: Storage, Key Vault, and Search govern themselves
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Who owns networking and access policy for a storage account connected to Foundry?

---

Connected resources such as Storage, Key Vault, and Azure AI Search are independent Azure resources. You manage their networking, access policies, and compliance settings separately from the Foundry resource.

A private endpoint on Foundry does not automatically become the network policy for those accounts. Plan each connection as its own boundary.

### translator-api-is-resource-scoped
- title: Translator stays on the resource, not the project
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Why might a workload need the Foundry resource endpoint instead of the project endpoint?

---

Most new APIs are available at the project scope. Some capabilities that started at the account level, including the Translator API, are available only from the Foundry resource, not at the project scope.

The trap is assuming every API moved to the project. Check the API scope before you standardize on the project endpoint alone.

### control-plane-versus-data-plane
- title: Deployments are control plane, agents are data plane
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Which Foundry operations are control plane, and which are data plane?

---

Control plane actions include creating deployments and projects. Data plane actions include building agents, running evaluations, and uploading files. Azure RBAC actions map to the control plane, and dataActions map to the data plane.

You can scope role assignments at the resource or the project, and you can assign managed identities at either scope. A role that can create a deployment is not the same thing as a role that can call an agent.

### role-names-changed-ids-did-not
- title: Foundry role names changed, the IDs did not
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What should you trust when a portal still says Azure AI User?

---

Foundry User, Foundry Owner, Foundry Account Owner, and Foundry Project Manager were previously Azure AI User, Azure AI Owner, Azure AI Account Owner, and Azure AI Project Manager. The architecture doc says the role IDs and core permissions are unchanged, and the old names can still appear during the rename.

In automation, assign by role definition ID rather than by the display name you happen to see.

### metrics-split-by-resource-and-project
- title: Token metrics are resource scope, agent metrics are project scope
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Where do you look for token use versus agent activity?

---

Azure Monitor segments metrics by scope. Resource-level metrics include token consumption, model latency, request counts, and error rates across projects. Project-level metrics include evaluation outcomes, agent invocation counts, and file operation activity.

Diagnostic settings can send logs to Log Analytics, Storage, or Event Hubs. Do not expect project agent activity on the resource-wide token chart alone.

### speech-to-speech-versus-cascaded
- title: Voice can be one model or three stages
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What is the difference between a speech-to-speech voice agent and a cascaded one?

---

A speech-to-speech model such as GPT-Realtime takes audio in and produces spoken output in one model. A cascaded experience uses separate speech recognition, a text model, and speech synthesis.

Choose from latency, model, voice, and language needs. The models and regions you can use still depend on the Foundry model deployment you selected.

### byo-vnet-delegates-to-app-environments
- title: Bring-your-own network injects a delegated subnet
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

How does a customer-managed virtual network attach to Foundry agents?

---

You provide the virtual network and a dedicated subnet delegated to Microsoft.App/environments. The platform injects into that subnet so agents can talk to private resources on the same network. A managed virtual network is the alternative where Foundry manages the network and you give up some customization.

Deployments that use private endpoints and block all public access are not configurable in the portal UI. Those cases use the SDK or CLI.

### workloads-are-isolated-per-resource
- title: Customer code does not share another tenant's container
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

How does Foundry isolate one customer's agent runtime from another's?

---

Workloads run in logically isolated environments per Foundry resource. Customer code does not share runtime containers with other tenants.

That is logical isolation per resource, not a promise that every connected storage account is single-tenant. Say which boundary you mean.

### no-automatic-regional-failover
- title: Foundry does not fail over to another region for you
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What do you deploy if the business requires two regions?

---

Foundry does not support automatic cross-region failover. For multi-region availability you deploy separate Foundry resources in each region and handle synchronization and routing in the application.

A global deployment type is not that failover design. Global processing can route inference. It does not give you a second resource automatically.

### basic-agent-storage-is-microsoft-managed
- title: Basic setup stores agent state in Microsoft storage
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Where does agent state live if you do not bring your own storage?

---

With the basic agent setup, the Agent service stores threads, messages, and files in Microsoft-managed multitenant storage, with logical separation. With the standard setup, you bring your own Azure resources for files, conversations, and vector stores, and that data is isolated by project inside your storage accounts.

Default file upload can also use Microsoft-managed storage that is logically separated, including for OpenAI models and agents, without a customer storage account. Bring your own storage when evaluations or batch jobs must read and write accounts you own.

### default-encryption-is-microsoft-managed
- title: Data is encrypted at rest without a code change
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What encryption do you get before you turn on customer-managed keys?

---

By default, Azure services encrypt Foundry data at rest and in transit with Microsoft-managed keys, using FIPS 140-2 compliant 256-bit AES. No code change is required.

Customer-managed keys are the extra control. Before you enable them, Key Vault must be in the same region, with soft delete and purge protection, and the managed identity needs key permissions such as Key Vault Crypto User when you use Azure RBAC.

### one-key-vault-for-connection-secrets
- title: One Key Vault holds every connection secret
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Where do API-key connection secrets go, and can each project have its own vault?

---

By default, Foundry stores API-key connection secrets in a managed Key Vault. If you connect your own vault, one Key Vault connection manages all project-level and resource-level connection secrets.

Do not plan a vault per project for those connection secrets. The documented model is one connection for the resource and its projects.

### entra-for-production-keys-for-prototypes
- title: Use Entra ID in production, keys for a prototype
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

Which authentication method does Foundry recommend for production?

---

Foundry supports Microsoft Entra ID and API keys. Entra ID is the production choice because it gives conditional access, managed identities, and least-privilege RBAC. API keys are for rapid prototyping and isolated tests.

A key is a static secret scoped to the whole Foundry resource. It cannot express a user, and Microsoft does not recommend it for enterprise production.

### token-scope-ai-azure-default
- title: Foundry tokens use the ai.azure.com scope
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

What scope do you request when you authenticate to Foundry with Entra ID?

---

Microsoft Entra ID uses OAuth 2.0 bearer tokens scoped to https://ai.azure.com/.default. The sample resource endpoint is `https://{resource-name}.services.ai.azure.com`.

A 401 often means the token is missing, expired, or requested for the wrong scope. A 403 means the token was accepted and the RBAC assignment is missing. A custom subdomain is required before token authentication works. A regional endpoint without one fails that check.

### api-key-header-is-api-key
- title: Key auth sends an api-key header
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

How does a caller present a Foundry API key?

---

The key sample sends the secret in the api-key header, not as a bearer token. Keys provide full access to the resource and cannot be scoped to a user or an action.

Rotate keys and keep them out of source control. Immediate revocation for a key means rotating it. For Entra ID, you remove the role or disable the principal, and the token lifetime still applies.

### agents-and-evals-reject-api-keys
- title: Agents, evaluations, and toolboxes require Entra ID
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

Which Foundry features refuse an API key?

---

The support matrix marks the agents service, evaluations, and the toolbox as Entra ID only. Basic chat and embeddings, fine-tuning, content-safety analyze calls, batch inferencing, and the playground accept either a key or Entra ID.

Least privilege, managed identity, and per-request user attribution are Entra-only because a key is all-or-nothing on the resource. Do not debug an agent 401 by minting a key. That feature row does not accept one.

### playground-uses-project-connection
- title: The playground can use a key or Entra ID
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

Does the Foundry playground force Microsoft Entra ID?

---

The matrix says portal playground usage supports both API keys and Entra ID, and that the playground uses project connection mode.

Do not confuse the playground with the agents service. Calling agents, running evaluations, and using the toolbox are the rows that require Entra ID.

### four-identity-types
- title: Users, apps, and two kinds of managed identity
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

Which identity types can call Foundry?

---

The auth doc lists a user principal, a service principal from an app registration with a secret or certificate, a system-assigned managed identity bound to one resource, and a user-assigned managed identity that can attach to multiple resources.

Pick a managed identity when an Azure workload should call Foundry without a stored secret. A service principal still has a secret or certificate to rotate.

### who-can-assign-foundry-roles
- title: Role assignment needs Owner or User Access Administrator
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry

Who is allowed to grant a Foundry role?

---

You need the Owner role or the User Access Administrator role at the scope where you assign access. The doc's starter mapping is Foundry User for developers using pre-deployed models, Foundry Project Manager for team leads, Foundry Account Owner for resource administrators, and Foundry Owner when one person needs both planes.

During the rename, assign the role definition GUID, not the display name. Foundry User is 53ca6127-db72-4b80-b1b0-d745d6d5456d, Foundry Owner is c883944f-8b7b-4483-af10-35834be79c4a, Foundry Account Owner is e47c6f54-e4a2-4754-9501-8e0985b135e1, and Foundry Project Manager is eadc314b-1a2d-4efa-be10-5d325db5065e.

### keys-ignore-rbac
- title: An API key skips Foundry RBAC
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Does a Foundry API key honor the Foundry User role?

---

RBAC applies when you authenticate with Microsoft Entra ID. A key grants full access without role restrictions.

If the design needs least privilege, the key is the wrong credential. Entra ID is what makes the built-in roles mean something.

### agent-consumer-is-invoke-only
- title: Foundry Agent Consumer can call an agent and nothing else
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which role do you give a service that only calls the Responses API?

---

Foundry Agent Consumer grants access to interact with agent endpoints and is the least-privilege role for that caller. It does not grant project reads, data-plane build rights, model management, publishing, or role assignment.

Foundry User is the developer role. It can build and test, read projects and the resource, and call agent endpoints, but it cannot create projects, manage models, publish agents, or assign roles.

### quota-reader-is-subscription-scope
- title: Quota visibility is a subscription role
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why can a Foundry Owner still see an empty quota page?

---

Viewing quota and deployment eligibility needs Cognitive Services Usages Reader, or another role that includes Microsoft.CognitiveServices/locations/usages/read, at the subscription scope. Assignments on the resource group, Foundry resource, or project do not authorize that subscription usage API.

Except for that usages reader, do not assign built-in roles whose names start with Cognitive Services for Foundry work. Those roles target AI Services resources directly and do not apply to Foundry scenarios.

### portal-auto-assigns-foundry-user
- title: The portal assigns Foundry User, the SDK does not
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why does a project created in the portal work, while the same project created with the CLI looks unauthorized?

---

If the creator can assign roles, for example as Azure Owner on the subscription or resource group, creating the project in the Foundry portal assigns Foundry User to the user and to the project managed identity. That automatic assignment does not happen when you deploy from the SDK or CLI.

After a CLI create, assign Foundry User yourself. Also assign it to the project managed identity on the Foundry resource, which is the documented minimum for the identity to use Foundry features.

### azure-ai-developer-is-not-foundry-user
- title: Azure AI Developer is an Azure Machine Learning role
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Should you assign Azure AI Developer on a Foundry project?

---

No. Despite the name, Azure AI Developer is scoped to Azure Machine Learning workspaces and Foundry hubs, not to Foundry projects or Foundry hosted agents. For a Foundry project, use Foundry User or Foundry Owner.

The same page says not to reuse the older Cognitive Services built-in roles for Foundry scenarios, aside from Cognitive Services Usages Reader when someone must see quota.

### rbac-matrix-project-manager
- title: Project Manager builds and publishes, but does not manage models
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Can a Foundry Project Manager create a model deployment?

---

On the built-in role matrix, Foundry Project Manager can build in a project, assign only the Foundry User role, read projects and accounts, publish agents, and call agent endpoints. Create-project, create-account, and manage-models are not granted.

Foundry Account Owner is the inverse on the data plane. That role can create accounts and projects and manage models, and it can assign Foundry User plus ACR and monitoring roles, but it cannot build in a project, publish agents, or call agent endpoints. Foundry Owner is the role that has both.

### azure-owner-cannot-call-the-data-plane
- title: Azure Owner does not include Foundry data actions
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why can a subscription Owner create a Foundry resource and still fail to chat with a model?

---

The Azure Owner role can create projects and accounts, assign any role, read, manage models, and publish agents. The matrix marks data-plane build rights and agent-endpoint interaction as not included. Contributor can create resources and manage models, but cannot assign roles, build in the data plane, publish, or call endpoints. Reader is read-only.

Publishing agents needs at least Foundry Project Manager on the Foundry resource scope. A subscription Owner is not a substitute for a Foundry data-plane role.

### enterprise-persona-mapping
- title: Admins own the subscription, developers get Foundry User
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

How does the RBAC doc map a typical enterprise team?

---

The sample puts Owner on the subscription for the IT admin, Foundry Account Owner on the resource for managers who deploy models and connections but do not build, Foundry Project Manager on the resource for a team lead who creates projects and builds, Foundry User on the project plus Reader on the resource for developers, and Foundry Agent Consumer on the project or on one agent for callers.

Managers who need to build must be given Foundry User. Account Owner alone does not include data-plane development.

### agent-scope-is-endpoint-only
- title: A role on one agent does not manage that agent
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

What does a role assignment on a single agent actually grant?

---

Agent scope uses the resource path `accounts/{account}/projects/{project}/agents/{agent}`. The service currently evaluates that scope only for agent endpoint access. It does not grant control-plane or management permissions on that agent.

Any role you can assign on a project can also be assigned on an agent, and it still only affects endpoint access. Foundry Agent Consumer's role ID is eed3b665-ab3a-47b6-8f48-c9382fb1dad6. The Azure portal assigns that role only at account scope, so use the CLI for project or agent scope.

### fine-tune-needs-both-planes
- title: Fine-tuning needs a data role and a control role
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which built-in role can fine-tune a model by itself?

---

Fine-tuning needs data-plane and control-plane permissions, and deploying the fine-tuned model is control plane. The only built-in role with both is Foundry Owner. The alternative is Foundry User plus Foundry Account Owner.

Foundry User alone can build, but the matrix does not give it model management. Account Owner alone can manage models, but it has no data-plane build rights.

### cli-deploy-skips-foundry-user
- title: Portal deploys assign Foundry User, templates do not
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Who gets Foundry User when the resource is created from a template?

---

If your user can assign roles and you create the resource from the Azure portal or the Foundry portal, Foundry User is assigned to that user. The RBAC doc says this does not apply when you deploy from the SDK or CLI.

To purge or view deleted Foundry accounts you need Contributor at the subscription. Contributor can also deploy models. Creating a custom role requires Owner on the resource scope, and the CLI role-definition shape is not the same JSON as an ARM template.

### managed-compute-role-gap
- title: A locations wildcard misses managed compute capacity
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why can a custom role deploy standard models and still fail to read managed compute capacity?

---

Managed compute control-plane operations use managedComputeDeployments and Microsoft.CognitiveServices/managedComputeCapacities/read. A locations/*/read wildcard matches usages reads and does not match managedComputeCapacities/read. There is no Microsoft.CognitiveServices/capacities/read action.

Foundry User and Foundry Project Manager can read managed compute deployments, capacities, and usage, and they cannot create or delete them. Foundry Owner and Foundry Account Owner can. Calling the deployment still needs Foundry User on the account, or the account API key.

### outside-resources-need-their-own-roles
- title: Connected storage does not inherit Foundry RBAC
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

What extra role do you add when Foundry reads a storage account you created yourself?

---

Creating the Foundry resource grants access to that resource. A storage account created outside Foundry still needs its own assignment. The example is to add the Foundry account managed identity to Storage Blob Data Reader on that account. Azure AI Search likewise needs its own role assignments.

Do not expect the Foundry User role on the cognitive account to open a storage container or a search index.

### new-portal-is-ga-for-core-scenarios
- title: The new portal is GA for defined core scenarios
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

What does general availability mean for the Microsoft Foundry portal?

---

The new portal is generally available for production use of defined core scenarios in Foundry projects, with support across the portal, APIs, SDKs, and CLI. GA is a production milestone, not a freeze. Some capabilities stay in preview.

Core coverage is model discovery, deployment, inference, and deployment management, agent development with evaluations, tracing, monitoring, red teaming, and fine-tuning where supported, and operate tasks such as policy and quota where supported.

### standalone-openai-not-in-new-portal
- title: A standalone OpenAI resource is not a new-portal project
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Can you open a standalone Azure OpenAI resource in the new Foundry portal?

---

No. Standalone Azure OpenAI resources are not supported in the new portal. You keep using the classic portal, or you upgrade to a Foundry project. Hub-based classic projects are also outside the new portal.

The new portal's GA scope is Foundry projects. If the workload is still a single-service resource with no Foundry project, plan on the classic portal.

### assistants-stay-in-classic-portal
- title: Assistants and v1 agents are edited in the classic portal
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Can you author an assistant in the new Foundry portal?

---

No. Assistant creation and authoring are out of scope for the new portal. The new portal supports Agents v2. Existing assistants and v1 agents are not supported there, so you edit them in the classic portal until an upgrade path exists.

Do not confuse that portal limit with the service retirement. New development still moves to Foundry agents rather than starting another assistant.

### api-keys-are-not-universal
- title: Several portal areas reject API keys
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Where does the GA overview say an API key is not enough?

---

Foundry supports API keys for most areas. The exceptions named on the GA page are evaluations, the dataset tab, Content Understanding, agents, and workflows, which require Microsoft Entra ID.

A key also does not give the same permission granularity as Entra ID with RBAC. For a governed production workload, use Entra ID.

### preview-features-are-listed
- title: Voice Live, memory, and monitoring are still preview
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Which familiar Foundry features does the GA table still mark as preview?

---

The table marks Instant Access Models, model leaderboards, the video playground, Voice Live, traces inside the agent builder, workflows, managed compute, tracing for workflow and external agents, tracing over a virtual network, memory, agent guardrails, guardrail controls and intervention, monitoring, stored completions, and AI Gateway as preview. Operate overview, assets, and compliance are preview too.

Agents core, routines, model flows, fine-tuning, toolboxes, evaluations, model guardrails, red teaming, and quota management are GA on that table. Tools are GA, but you still check the label on each tool. Workflows are called out for retirement on 1 December 2026, with Microsoft Agent Framework named for new development.

### tracing-ga-depends-on-agent-type
- title: Tracing is GA for prompt and hosted agents only
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Is agent tracing generally available for every agent you can register?

---

Tracing, including trace replay, is GA for prompt agents and hosted agents. It is preview for workflow agents and external agents. Tracing over a virtual network is preview.

The rollout notes also say traces and workflow agents do not yet fully support network isolation. Do not promise a private-network trace pipeline from the GA label alone.

### private-acr-cutoff-date
- title: Private registries depend on when the project was created
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Can every Foundry project pull a hosted agent from a private container registry?

---

The GA rollout notes say a private Azure Container Registry is supported only for Foundry projects created after 25 June 2026. Projects created before that date require public access to the registry.

That date is a project-creation cutoff, not a setting you flip later. Check the project age before you lock the registry down.

### content-understanding-stays-classic
- title: Content Understanding is not in the new portal GA scope
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Where do you train a Speech or Vision custom model, or open Content Understanding?

---

The unsupported-at-GA list includes Content Understanding, the audio playground, and AI service fine-tuning such as Speech or Vision custom model training. Model fine-tuning through Foundry projects is GA.

Do not send a speech custom-model job to the new portal because model fine-tuning is GA. Those are different features.

### foundry-iq-api-is-ahead-of-the-portal
- title: Foundry IQ is GA at the API and preview in the portal
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Is Foundry IQ generally available?

---

The GA table marks Knowledge (Foundry IQ) as partial GA: the API is GA, and portal access remains preview.

Say which surface you mean. An API-level GA feature can still be a preview experience in the portal.

### some-networking-remains-preview
- title: Virtual network integration is in, and some network UX is not
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability

Does GA mean every networking screen is production-ready?

---

The GA statement includes virtual network integration among the enterprise capabilities for supported scenarios, together with RBAC, audit logs, and compliance controls. The same section says monitoring, alerting, and some networking experiences remain in preview.

Read the feature row before you treat the whole network surface as GA. The pitfalls section also warns that not every GA feature works behind a virtual network.

### allow-project-management-is-immutable
- title: Project management is chosen at resource creation
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Can you turn on Foundry projects after the resource exists?

---

The create flow sets kind AIServices and SKU S0, enables a system-assigned identity, and sets allowProjectManagement to true. The CLI notes say you cannot change allow-project-management after you create the resource.

Project creation also fails if the resource has no managed identity. The CLI flag is --assign-identity. The custom domain must be globally unique or the create fails with CustomDomainInUse.

### cli-280-for-project-create
- title: Project CLI commands need Azure CLI 2.80.0
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Which Azure CLI version does the project article require?

---

The project create steps require Azure CLI 2.80.0 or later, and Contributor or Owner on the resource group. The sample Python management client uses api-version 2025-04-01-preview.

An older CLI is a reason for a failed create, not a reason to invent another resource type. Check az version before you debug the template.

### default-project-has-more-surfaces
- title: The default project is the only home for some OpenAI jobs
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Which features work only on the default Foundry project?

---

The first project is the default. You can see the default tag in the UX and the is_default property in code. OpenAI Batch, fine-tuning, and stored completions run on the default project and not on the others. Speech fine-tuning is also default-only.

Other projects still get model inference, playgrounds, agents, evaluations, tracing, datasets, indexes, the Foundry SDK, content understanding, and language fine-tuning. Their OpenAI SDK surface is Responses, Files, and Conversations. If you delete the default project, the next project you create becomes the default, and a deleted project cannot be recovered.

### projects-share-network-and-deployments
- title: Extra projects share the resource network and deployments
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

What do two projects on one Foundry resource share?

---

Projects are child resources and can have their own access control, but they share network security, deployments, and Azure tool integration from the parent. That is the pattern for several teams in a locked-down subscription.

Creating another project does not create another network boundary or another set of model deployments. Those stay on the resource.

### agent-storage-inheritance
- title: Changing account storage defaults does not rewrite old projects
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

If you change the account-level agent storage settings, do existing projects pick them up?

---

A project inherits each store it does not set itself, and a GET returns the effective configuration. Changing the account defaults later does not update existing projects.

For those capability-setting calls, the caller needs Storage Blob Data Contributor on the storage account and Cosmos DB Operator on the Cosmos DB account. Azure AI Search does not require a caller role for that request. Runtime access for the project managed identity is a separate assignment.

### sdk-cannot-assign-roles
- title: The Python management SDK does not assign Foundry roles
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Can the Cognitive Services Python SDK grant Foundry User to a teammate?

---

No. The create-project article says to use the Azure CLI or the Foundry portal for role assignments. The Python SDK does not support role assignment operations.

The minimum role it tells you to give teammates so they can build and test is Foundry User. In code, pass the role definition GUID because the display names were renamed.

### project-home-shows-endpoint-and-key
- title: The project page shows an endpoint and a key
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Where do you read the project endpoint after you create a project?

---

On the project home page you see the project endpoint and an API key. You do not need the API key when the caller uses Microsoft Entra ID.

Treat the key as a secret for key-based callers. Entra ID callers use the endpoint and a token, not that key.

### serverless-versus-managed-compute
- title: Serverless API and managed compute are the two deploy paths
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

What are the two ways Foundry deploys a model?

---

Foundry offers a Serverless API deployment for Foundry Models sold by Azure and selected partner and community models, and managed compute in preview for open-source, partner, and custom models on dedicated GPU capacity. Foundry picks the option from the model you choose.

Serverless API is the preferred path and covers standard, provisioned, batch, and developer types. Managed compute is a preview GPU platform, has no service-level agreement, and is not recommended for production.

### openai-resource-shows-fewer-models
- title: An Azure OpenAI resource does not list the full catalog
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Why does the catalog look smaller on an Azure OpenAI resource?

---

Serverless API deployments work on Foundry resources and on Azure OpenAI resources. On an Azure OpenAI resource, the catalog shows only Azure OpenAI models. Upgrade to a Foundry resource for the full set of Foundry Models.

Neither option requires an AI Hub. If the missing model is a partner model, the resource type is the first thing to check.

### managed-compute-endpoint-and-gpus
- title: Managed compute stays on the project endpoint
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

How do you call a managed compute deployment, and who picks the GPU?

---

Managed compute is served on the same Foundry project endpoint, with the same keys, Entra ID, and private networking. Routes use /managed-deployments/, and chat-completions-compatible runtimes also work on /openai/v1/ with the OpenAI SDK. Foundry sizes the instance from model size, architecture, context length, and whether you optimize for latency or throughput. You do not pick a virtual machine SKU.

The documented runtimes are Microsoft-curated vLLM, SGLang, and NVIDIA NIM. Accelerator families named on the page are A100 80 GB, H100 80 GB, and MI300X 192 GB. Microsoft patches the serving runtime on live deployments.

### managed-compute-quota-is-not-vm-quota
- title: Managed compute quota is per accelerator, not per VM
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Can you reuse Azure VM quota for a managed compute deployment?

---

No. Quota is granted per accelerator SKU per region through the Foundry quota process, and it is separate from Azure VM quota. Existing VM quota cannot be applied. Billing is hourly per accelerator SKU.

Managed compute is currently available for global deployment. Content filtering is not available on it in public preview. The deployment resource for serverless API is the Foundry resource. For managed compute, it is the Foundry project.

### start-with-global-standard
- title: Global Standard is the default deployment type
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Which serverless deployment type should you start with?

---

For most workloads, start with Global Standard. It launches first when a new model is released, has the lowest price, and has the broadest region coverage. New types arrive as Global, then Data Zone, then geography-based. Geography-based types have no guaranteed availability date.

Move off Global Standard only for a specific reason, such as data residency, reserved throughput, or asynchronous batch. Not every model supports every type.

### deployment-sku-names
- title: Deployment types have stable SKU codes
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

What SKU name do you put in a template for each serverless deployment type?

---

The codes are GlobalStandard, GlobalProvisionedManaged, GlobalBatch, DataZoneStandard, DataZoneProvisionedManaged, DataZoneBatch, Standard, ProvisionedManaged for Regional Provisioned, and DeveloperTier.

Global types may process inference in any Azure region. Data Zone types stay in the US, EU, or Asia Pacific zone. Standard and Regional Provisioned process inside the customer-specified Azure geography, and may still move between regions inside that geography for operations. Data at rest stays in the designated geography for every type.

### data-zones-are-us-eu-apac
- title: Data Zone means US, EU, or Asia Pacific
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

What boundary does a Data Zone deployment actually keep?

---

Data Zone processing stays inside the Microsoft-specified zone: anywhere in the United States, inside the Azure EU Data Boundary, or inside the Asia Pacific zone. The EU zone can include EFTA countries such as Norway and Switzerland. Microsoft can add regions to the EU or APAC zone without prior notice.

Data Zone Standard has higher default quota than geography-based types while keeping that zone. It is not the same thing as a single-region Standard deployment.

### global-batch-is-half-price
- title: Batch is asynchronous and priced at half of Global Standard
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

When is Global Batch the right deployment type?

---

Global Batch processes groups of requests from a file, with a separate enqueued token quota, a 24-hour target turnaround, and a 50 percent lower cost than Global Standard. Data Zone Batch is the same pattern inside the data zone. Batch has no real-time SLA and can take longer than 24 hours.

Use it for large jobs that can wait, such as dataset analysis or bulk summarization. The separate quota is there so batch does not consume the online deployment's quota. Do not put a user-facing chat on it.

### developer-tier-lasts-one-day
- title: Developer deployments exist for one day and have no SLA
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

What is the Developer deployment type for?

---

DeveloperTier is only for evaluating a fine-tuned model. It is pay-per-token, can run in any Azure region, has no data-residency guarantee and no SLA, and is deleted automatically after a fixed 24-hour lifetime.

Do not use it for production traffic or for a latency target. Provisioned types are the ones that reserve capacity and lower latency variance. Standard types are best effort.

### global-standard-flex-and-priority
- title: Global Standard can take Flex or Priority processing
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

What extra processing choices does Global Standard have?

---

Global Standard supports request-level processing tiers. Flex is the lower-cost, delay-tolerant option. Priority is the faster pay-as-you-go option. Data Zone Standard supports priority processing as well.

Those tiers do not change the deployment into provisioned throughput. Provisioned types are still the reserved-capacity choice when latency variance has to stay low at high volume.

### standard-deployments-are-bursty
- title: Geography-based Standard fits bursty, lower volume
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

When does the single-region Standard type fit better than Global Standard?

---

Standard is pay-per-token inside an Azure geography, and the page describes it as suited to low-to-medium volume with high burstiness. High sustained volume can see more latency variability. Models and throughput in a region can be limited.

If the requirement is the geography plus reserved throughput, the matching type is Regional Provisioned, SKU ProvisionedManaged, measured in provisioned throughput units. Minimum PTU counts vary by model.

### global-standard-outage-stays-regional
- title: A regional interruption still hits Global Standard traffic
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Does Global Standard fail over when its primary region is down?

---

For Global Standard and Data Zone Standard, if the primary region has a service interruption, traffic that was routed to that region is affected. The deployment-types page points you at the high availability guide for that case.

Dynamic routing is not a promise that an in-flight region failure is invisible. Design for that if the workload cannot tolerate it.

### policy-can-match-deployment-sku
- title: Azure Policy can match a deployment SKU
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

How would you stop a subscription from creating a Global Standard deployment?

---

The deployment-types page shows an Azure Policy rule that matches type Microsoft.CognitiveServices/accounts/deployments when Microsoft.CognitiveServices/accounts/deployments/sku.name equals a SKU such as GlobalStandard. You replace GlobalStandard with the SKU you want to restrict.

Use the SKU code, not the marketing name. Global Provisioned is GlobalProvisionedManaged, and Regional Provisioned is ProvisionedManaged.

### three-agent-kinds
- title: Prompt, voice, and hosted are the three agent types
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

What agent types does Foundry Agent Service describe?

---

The overview covers three types. Prompt agents are instructions, a model, and tools, with no code to run. Voice-based prompt agents are the same idea for spoken conversations over Voice Live. Hosted agents are your code, shipped as a container image or a zip that Foundry builds, with a managed endpoint, scaling, and identity.

A fourth pattern is not a stored agent at all. Calling the Responses API from your own process is an ephemeral agent whose definition lives in your application.

### voice-agents-are-preview
- title: Voice agents are preview and have no SLA
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Can you put a voice-based prompt agent in production on the strength of Agent Service being available?

---

The agent overview says voice-based agents, and some monitoring, evaluation, avatar, WebRTC, and telephony capabilities, are in preview. Preview has no service-level agreement and is not recommended for production until you review support, security, compliance, and availability.

You connect over a real-time WebSocket, not by posting one text request at a time. Direct SIP is not a supported customer flow. Phone channels named on the page are Teams Phone extensibility and Twilio.

### hosted-agent-frameworks
- title: Hosted agents can come from several frameworks
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Which frameworks does the agent overview name for hosted agents?

---

Hosted agents can be built with Agent Framework, LangGraph, the OpenAI Agents SDK, the Anthropic Agent SDK, the GitHub Copilot SDK, or your own code. The container calls the Foundry project endpoint for models and tools.

Platform tools named there include file search, code interpreter, and web search, plus SharePoint, WorkIQ, and Fabric IQ. Prompt agents have no runtime code to maintain. Hosted agents do.

### toolbox-is-one-mcp-endpoint
- title: A toolbox is one governed MCP endpoint
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

What is a toolbox for, compared with attaching tools one agent at a time?

---

A toolbox curates tools once, such as web search, file search, code interpreter, MCP servers, and custom functions, and shares them through one managed MCP endpoint with centralized authentication, governance, and versioning.

You version the toolbox, test it, and promote a version to default. You do not rewire every agent to change a tool. Remote MCP options include a service such as Azure DevOps or a Functions endpoint at /runtime/webhooks/mcp.

### mcp-auth-choices
- title: Tool connections can use a key, Entra, OAuth, or nothing
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Which authentication options does Agent Service document for MCP and other tool connections?

---

The overview lists key-based access, Microsoft Entra using the agent or project managed identity, OAuth identity passthrough with On-Behalf-Of, and unauthenticated access where that is appropriate.

Pick the option in the tool configuration. On-Behalf-Of is for when a user token should flow through. It is not the identity the agent uses when no user is present.

### a2a-v1-is-ga
- title: Agent-to-agent v1.0 is generally available
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Which agent-to-agent protocol version is GA?

---

Foundry Agent Service supports OpenResponses and Activity Protocols for Microsoft 365 publishing, an Invocations protocol for custom apps, and A2A for agent-to-agent calls. A2A v1.0 is generally available, and v0.3 remains in preview.

Versions of a Foundry agent are snapshotted as you iterate, and you can roll back. Publishing promotes a version to a stable endpoint. Do not describe preview A2A v0.3 as the GA contract.

### voice-eval-and-tracing-limits
- title: Voice traces do not have a response ID
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

What evaluation and tracing limits apply to voice agents?

---

Full-conversation evaluation from existing conversations is supported. Single-turn and simulated-conversation evaluation are not currently supported for voice agents. Voice traces use one trace-oriented view because they do not have a Responses API response_id. Creating a dataset from the trace page is not available for voice.

Avatar output is browser video over WebRTC. Telephone callers get audio only. The standard text-agent card is not the phone integration path. Monitoring cards for voice need Application Insights.

### speech-architectures-on-the-overview
- title: Native speech and cascaded speech are both supported
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

What two voice architectures does the agent overview describe?

---

Native speech-to-speech sends caller audio to a realtime speech model and gets spoken audio back. Cascaded speech does recognition, then a text model, then synthesis, which offers more model and voice choice and adds latency at each stage.

A fully managed Voice Live model means you do not deploy a separate audio model. Customer-deployed models are supported where the service allows them. Browser testing is from the agent playground.

### private-networking-differs-by-agent-type
- title: Prompt agents and hosted agents isolate differently
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Is private networking the same feature for prompt agents and hosted agents?

---

The overview says private networking is available for prompt agents. Hosted agents support a bring-your-own virtual network, where each session runs in a VM-isolated sandbox connected to that network.

Content filters on the service are there to reduce prompt injection, including cross-prompt injection, and unsafe outputs. Identity, RBAC, and those filters are separate controls from the network choice.

### hosted-when-to-choose
- title: Choose a hosted agent for code, protocols, or sandbox size
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

When does the hosted-agent article say to prefer hosted agents over prompt agents?

---

Choose hosted agents when you need your own code, custom protocols such as webhooks or non-OpenAI payloads through Invocations, explicit CPU and memory for the sandbox, files and state across turns in $HOME and the /files endpoint, or long-running work that must survive a process interruption.

You package a container and push it to Azure Container Registry. At deploy time the service pulls the image, assigns a dedicated Entra agent identity, and exposes an endpoint. Publishing is not required before programmatic access.

### hosted-session-isolation
- title: Each hosted session gets its own sandbox
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

How are hosted-agent sessions isolated?

---

Hosted agents run in per-session VM-isolated sandboxes. Each session has a persistent filesystem at $HOME and /files. Sessions are isolated from each other, and state is restored when a session resumes after idle.

The platform provisions compute on use and deprovisions it at the idle timeout. You own the code inside the sandbox. Foundry owns the endpoint, identity, scaling, and session state.

### hosted-protocols
- title: Responses, Invocations, Activity, and A2A can share one agent
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

Which protocol should a hosted agent expose?

---

Start with Responses when the platform should manage conversation history, streaming, and background mode. Use Invocations when the caller sends arbitrary JSON, a webhook payload, or a non-OpenAI stream such as AG-UI. Use the WebSocket invocations protocol for bidirectional audio. Activity is bridged for you when a Responses agent is published to Teams or Microsoft 365.

One agent can expose more than one protocol. Responses clients can be any OpenAI-compatible SDK. Invocations clients are yours. A2A v1.0 and preview v0.3 are also endpoint protocols on the hosted agent.

### hosted-endpoints-by-protocol
- title: Each hosted protocol has its own path
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

Where do you send a request to a hosted agent?

---

Responses uses {project_endpoint}/agents/{name}/endpoint/protocols/openai/responses. Invocations uses the invocations path under the same prefix. The WebSocket form is wss://{account}.services.ai.azure.com/api/projects/{project}/agents/{name}/endpoint/protocols/invocations_ws with api-version=v1. A2A uses the a2a path.

Which paths are live depends on the protocols declared for that agent version, in azure.yaml under azure.ai.agent or through protocol_versions in the SDK. The endpoint exists as soon as the deployment finishes.

### agent-identity-versus-project-identity
- title: The agent identity is not the project managed identity
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

Which identity does a hosted agent use at runtime?

---

Every hosted agent gets its own Entra agent identity at deploy time. That identity calls models, tools, and downstream Azure services. The project system-assigned identity is for platform work such as Container Registry Repository Reader, not for the agent's runtime calls.

Model inferencing through the project endpoint and session storage work by default. Your own storage account still needs an RBAC assignment on the agent identity. With a user token, On-Behalf-Of can call downstream services as the user. Without a user token, the agent uses its own identity.

### session-timeout-and-retention
- title: Hosted sessions idle out, then expire after 30 days
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

How long does a hosted-agent session keep its compute and its state?

---

The idle timeout is configurable per agent version from 2 minutes through 240 minutes, and the default is 15 minutes. After that, compute is removed and the state is kept. The platform permanently deletes a session after 30 days of inactivity.

Conversation history is a different store. A conversation ID is durable in Foundry and can be opened from the playground, the API, or a published channel even when compute is gone.

### hosted-state-store
- title: The state store is your key-value partition
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

Where should a LangGraph checkpoint live on a hosted agent?

---

The state store is a server-backed key-value store for application state Foundry does not manage for you. Each store name is its own partition, items are JSON, and a store can also partition by end user. Items default to a 30-day idle window that writes renew, or you can configure the store not to expire.

Use it for framework checkpoints and your own state. It survives crashes, restarts, and idle eviction. It is not the same thing as $HOME, which is the session filesystem.

### runtime-trio
- title: Agents, conversations, and responses are the runtime trio
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components

What three runtime objects does Foundry Agent Service tell you to compose?

---

An agent supplies a reusable model, instructions, and tools. A conversation persists input and output items across turns. A response is one execution of a model or agent against input, and it produces output items.

Start with a response for a single interaction. Add an agent when many calls need the same behavior, and add a conversation when later turns need server-side history. You can use a response with neither.

### context-without-a-conversation
- title: You can continue without a conversation object
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components

How do you carry context forward if you do not create a conversation?

---

Without a conversation, the application can reference a previous stored response or resend earlier items. A conversation is the option that stores those items on the server.

Streaming and background mode change how the client receives a response. They do not change the relationship among agents, conversations, and responses.

### projects-sdk-versions-on-the-page
- title: The runtime article pins sample SDK versions
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components

Which SDK versions does the runtime-components article install?

---

The Python sample installs azure-ai-projects 2.0.0 or newer, plus azure-identity. The JavaScript sample uses @azure/ai-projects and tells you to use Node.js 22 or later with @azure/ai-projects 2.8.0. The Java sample uses azure-ai-agents 2.2.0.

Those are the versions in that article's samples, not a promise that every older client still works. Match the sample surface you are following.

### agent-limits-are-two-layers
- title: Agent caps and model quotas are different limits
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

An agent call returns 429. Which limit did you hit?

---

Agent Service enforces its own caps on files, messages, and tools, and the model deployment enforces tokens per minute and requests per minute. A 429 with rate_limit_exceeded is the model deployment. A 429 with session_quota_exceeded is the hosted-session quota.

The file, message, and tool caps are fixed service limits. The page says they cannot be increased. Model quota and the concurrent hosted-session limit are the ones you can ask to raise.

### basic-versus-standard-data-plane
- title: Basic and standard setups store agent data in different places
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Where do files, vectors, and threads live in each agent setup?

---

Basic setup stores files, vector stores, and threads in Microsoft-managed storage or Microsoft-managed vector search, logically separated. Standard setup stores files in your Blob Storage, vectors in your Azure AI Search, and threads, messages, and agent definitions in your Cosmos DB.

Agent Service endpoints are regional, and the page says data is stored in the same region as the endpoint. Standard setup is how you put that data in resources you own.

### agent-file-and-message-caps
- title: Files, messages, and tools have hard caps
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What default caps does Agent Service put on files, messages, and tools?

---

The fixed caps are 10,000 files per agent or thread, 512 MB for a file uploaded for a prompt agent, 300 GB for all uploaded agent files, 2,000,000 tokens when attaching a file to a vector store, 100,000 messages per thread, 1,500,000 characters of text in one message, 128 tools per agent, and 1,000 versions per agent.

These apply to every Foundry project, regardless of subscription type or region. Oversized files return HTTP 400 file_size_exceeded. An over-long message returns content_size_exceeded. Too many tools returns tool_limit_exceeded. A thread at the message cap returns message_limit_exceeded, and the remedy is a new thread.

### version-cap-is-terminal
- title: The 1,000-version error is not a retry
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What do you do when creating an agent version returns HTTP 400 UserError?

---

An agent allows 1,000 versions. Past that, the service returns HTTP 400 and tells you the maximum was exceeded. The page calls this error terminal. Retrying the same create without deleting versions keeps failing.

Delete older versions, then create the new one. Do not treat it like a 429.

### hosted-session-regional-caps
- title: Concurrent hosted sessions are capped per region
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

How many hosted-agent sessions can run at once?

---

The default concurrent hosted-session limit is 2,000 in Canada Central, East US 2, Japan East, North Central US, South Africa North, Southeast Asia, and Sweden Central. Other regions where hosted agents are available default to 1,000. The cap counts sessions across every Foundry account and project in that subscription and region.

A session counts while compute is provisioning or running. An idle or stopped session keeps its state and does not count. Resuming it needs free quota. session_quota_exceeded means you stop or delete sessions, or request a raise. regional_session_quota_exceeded means you back off or use another region.

### subnet-exhausted-is-429
- title: A full delegated subnet returns subnet_exhausted
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What error do you get when the agent subnet has no free IP addresses?

---

The limits page lists HTTP 429 with error code subnet_exhausted when the delegated subnet has no available IP addresses. You stop sessions that do not need compute, or you configure a larger subnet.

This is not a model quota problem. Raising tokens per minute will not free an IP address.

### voice-session-is-sixty-minutes
- title: A voice session lasts at most 60 minutes
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

How long can one voice session run, and how long is its audio kept?

---

The limits table sets the maximum voice session duration at 60 minutes. Stored voice conversations and Microsoft-managed audio are retained for 60 days.

Voice can also hit Voice Live, audio, and channel limits beyond the text-agent caps. Do not design a voice call as an unbounded thread.

### file-search-missing-in-two-regions
- title: File search is absent in Italy North and Brazil South
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Why would file search be missing when the agent region looks supported?

---

Not every tool exists in every region. The limits page calls out that file search is not available in Italy North and Brazil South, and it tells you to check the tool-by-region table before you deploy.

Agent Service itself is listed in those regions. Tool support is a second check. Poland Central and Spain Central support agents and private virtual networks on that table, and they do not support voice-based agents.

### image-tool-needs-two-models
- title: Image generation needs gpt-image-1 and an orchestrator
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What has to be in the project before an agent can use the image generation tool?

---

The limits page says the image generation tool needs both the gpt-image-1 model and a large language model as the orchestrator, in the same Foundry project.

A chat model that supports other tools is not a substitute for gpt-image-1. Deploy both in that project.

### computer-use-model-is-narrow
- title: computer-use-preview only supports the Computer Use tool
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Which tools can you attach to computer-use-preview?

---

On the model-by-tool table, computer-use-preview supports Computer Use and does not support file search, functions, MCP, web search, SharePoint, or the other listed tools.

Do not pick that model as a general orchestrator. Tool support is per model as well as per region. Agent Service in Azure Government is a further subset, in US Gov Virginia and US Gov Arizona.

### foundry-resource-matches-vnet-region
- title: The Foundry resource and its virtual network share a region
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Can the Foundry resource sit in a different region from the virtual network?

---

For a private network such as a network-secured standard agent, the Foundry resource and the virtual network must be in the same region. Cosmos DB, Azure AI Search, and Storage may be in other regions, with the cross-region cost that implies.

Grounding with Bing Search on a private network is only supported in the regions the limits page lists, including West Europe, East US, and UK South, and not in every Agent Service region. Check that list before you promise Bing grounding inside the virtual network.

### quota-is-tpm-per-subscription
- title: Quota is tokens per minute, per subscription, region, and model
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/quota

What unit is Foundry model quota measured in?

---

Azure assigns quota per subscription, per region, and per model, in tokens per minute. Standard and Provisioned deployments do not share the same quota mechanics.

The quota page has a tokens-per-minute tab and a provisioned-throughput-unit tab. After you edit an allocation or submit a request, allow up to 15 minutes for the change to show up.

### shared-quota-is-for-tests
- title: Shared quota is a temporary test pool
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/quota

Should you run production on the Foundry shared quota pool?

---

No. The shared pool lets users in different regions borrow quota for testing for a limited time, so you can try catalog models without a support ticket. Billing is usage-based. Production endpoints should use dedicated quota that you request.

The page says to use the shared pool only for temporary test endpoints. It is not a substitute for an approved quota increase.

### who-can-request-quota
- title: Seeing quota and requesting quota are different roles
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/quota

Which roles does the quota article require?

---

Cognitive Services Usages Reader at the subscription lets you view allocations. Owner or Contributor on the subscription lets you request an increase. Editing allocations in the portal needs Cognitive Services Contributor plus Cognitive Services Usages Reader.

An empty quota page usually means the usages reader role or the wrong subscription. A disabled Request quota button points at Owner or Contributor, or at a model and region that does not allow an increase.

### instant-access-uses-leftover-global-quota
- title: Instant access spends the global quota you have not reserved
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/quota

How does instant access relate to Global Standard quota?

---

Instant access draws from a per-model global quota pool that is separate from the regional quota you manage for deployments. A Global Standard deployment reserves part of the global quota. Instant access uses what remains. You do not partition that global pool yourself.

If instant calls are throttled, request a global quota increase or create a deployment with reserved capacity. The quota article points at the instant-access page for how global and regional quota interact.

### subscription-quota-started-may-2026
- title: Some models now share one quota pool per subscription
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

What changed about quota after 7 May 2026?

---

Subscription-level quota management started after 7 May 2026. It begins with Realtime Translate and Realtime Transcribe, and the page says all models are moving that way. For an onboarded model, every Global Standard deployment of the same model and version in the subscription shares one pool across regions. Data Zone Standard shares one pool per data zone.

On the quota page, a Scope of Global or Data Zone means that subscription pool. A scope that names a region, such as East US, means the older per-region quota. Approved quota is kept and applied at the new scope. You do not re-request it.

### resource-count-limits
- title: A subscription can hold 100 Foundry resources in one region
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

What hard counts does the Foundry Models quota page put on resources, projects, and deployments?

---

Per subscription and region, the page lists 100 Foundry resources, 250 projects on one resource, and 32 model deployments on one resource. These numbers are for models that are not yet on subscription-level quota management.

Quotas are not enforced at the tenant. The highest quota scope on that page is the subscription. Tokens per minute, requests per minute, and concurrency are then defined per region, per subscription, and per model or deployment type.

### custom-header-limit
- title: More than 10 custom headers returns HTTP 431
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

Why would a Foundry request fail with HTTP 431?

---

Current APIs allow up to 10 custom headers, which the pipeline passes through. More than that returns HTTP 431. Future API versions will not pass custom headers through at all.

Do not design a protocol that depends on custom headers surviving. Reduce the header count to clear the 431, and keep them out of the long-term design.

### partner-models-mostly-cannot-raise-quota
- title: Most partner models cannot get a quota increase
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

Which catalog models can you ask Microsoft to give more quota?

---

You can request increases for Foundry Models sold by Azure, Azure OpenAI models, and Anthropic models. Except for Anthropic, models from partners and community do not support quota increases.

Requests are processed in order, and priority goes to customers who already use the quota they have. An unused allocation is a reason a request can be denied.

### default-rate-limits-for-open-models
- title: Many non-OpenAI models share one default rate limit
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

What default rate limit does the quota page give Llama 3.3 70B Instruct?

---

Llama 3.3 70B Instruct and Llama-4-Maverick-17B-128E-Instruct-FP8 are listed at 400,000 tokens per minute, 1,000 requests per minute, and 300 concurrent requests. The page applies that same trio to the rest of the models that are not called out separately. Azure OpenAI models vary by model and SKU.

Flux.2-Pro is request-based, with default, medium, and enterprise tiers of 15, 30, and 100 requests per minute. FLUX-1.1-pro and Flux.1-Kontext Pro are listed at 2 capacity units, described as 6 requests per minute. Do not apply the 400,000 TPM row to those image models.

### grok-capacity-unit
- title: Grok 4.7 capacity is 1,000 TPM and 1 RPM per unit
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

How does a capacity unit map to rate limits for Grok 4.7?

---

Grok 4.7 version 1 uses subscription-level quota. Each unit of deployment capacity provides 1,000 tokens per minute and 1 request per minute. The Global Standard free tier is listed as 0 TPM and 0 RPM.

The deployment's limit is its configured capacity and allocated quota, not the tier ceiling alone. A free-tier subscription cannot call that Global Standard deployment until it is on a tier with quota.

### usage-tier-is-tenant-wide
- title: Latency variability is measured across the tenant
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

Why can one busy subscription affect latency for another subscription in the same company?

---

Global Standard routes to capacity, and the page says customers with high sustained usage can see more latency variation. Usage for that threshold is defined per model as the total tokens consumed across all deployments, all subscriptions, and all regions for a given tenant.

That usage measure is wider than subscription quota. Quota can be per subscription while the latency threshold looks at the tenant.

### timeouts-for-reasoning-models
- title: Reasoning calls can run up to 29 minutes
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

How long should the client wait on a reasoning model?

---

The quota page says to set the client timeout below the service guidance. Reasoning models, including streaming, can take up to 29 minutes because reasoning tokens are generated and summarized before the first response token. Non-reasoning streaming calls are guided at up to 60 seconds, and non-streaming calls at up to 29 minutes.

Twenty-nine minutes is an upper bound, not a typical latency. If you leave the timeout to the HTTP library, it may not match these limits. A 429 should honor the Retry-After header and use backoff.

### retry-and-ramp-workload
- title: Ramp traffic and retry, or you will trip the limit
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

What does the quota page tell you to do before you ask for more quota?

---

Retry in the application, avoid sharp workload jumps, ramp gradually, and test the ramp. You can also move quota from another deployment onto the one that is short.

A 429 means the token or request limit was exceeded. A quota page that shows zero available means the subscription or regional quota is fully allocated. A model missing from a region means it is not deployed there, not that the quota request failed.

### guardrail-is-a-named-policy
- title: A guardrail is a named set of controls
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

What is a Foundry guardrail?

---

A guardrail is a named collection of controls. Each control names a risk, the intervention points to scan, and the action to take. Risks are flagged by classification models. Agent guardrails are in preview. Model guardrails can be assigned to one or many models and agents in a project.

The system applies to Foundry Models sold by Azure, except prompts and completions processed by audio transcription models. It applies to agents built in Foundry Agent Service, not to other agents that are only registered in the Foundry Control Plane.

### four-intervention-points
- title: Filters can run on input, tools, and output
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

Where can a guardrail inspect an agent call?

---

The four intervention points are user input, tool call, tool response, and output. Tool call and tool response are preview and apply only to agents. Models scan user input and output.

Hosted agents can also take network egress controls, in preview, in the same guardrail. Those egress rules apply only to hosted agents, not to prompt agents.

### agent-guardrail-overrides-the-model
- title: The agent guardrail replaces the model guardrail
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

If the model blocks violence at High and the agent blocks it at Low, which one runs?

---

Risks on an agent are detected from the guardrail assigned to the agent, not from the model's guardrail. The agent guardrail fully overrides the model. In the page's example, user input and final output are scanned at Low, and tool calls and tool responses are not scanned if the agent has no control there.

A stricter model deployment does not protect an agent that was given a looser guardrail. Set the agent policy to the level you actually want.

### agents-cannot-annotate-only
- title: Agents block, models can annotate without blocking
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

Can an agent guardrail log a risk without blocking it?

---

Models support Annotate and Annotate and block. Agents support Annotate and block only. Annotate by itself is not an agent action on that table.

Spotlighting and Groundedness are preview risks that apply to models and not to agents. If those controls are on a shared guardrail, they still run for models and do not take effect for the agent.

### default-guardrail-is-defaultv2
- title: Models start on Microsoft.DefaultV2
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

Which guardrail does a model get if you never assign one?

---

Models are assigned Microsoft.DefaultV2 by default. An agent uses a custom guardrail if you assign one. If you do not, it inherits the guardrail of its model deployment. It uses Microsoft.DefaultV2 only when that deployment uses it, or when you assign DefaultV2 yourself.

An agent on a deployment with a custom policy named MyCustomGuardrails inherits that policy until you assign another one. Do not assume every agent is on the Microsoft default.

### blocking-levels-are-inverted-names
- title: Low blocking stops only high-severity content
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

What does a Low blocking level actually block?

---

For hate, sexual, self-harm, and violence, Low blocks high-severity content only and is the least restrictive. Medium blocks medium and high. High blocks low, medium, and high and is the most restrictive. Off blocks nothing for that risk.

All customers can turn content harms off for inputs. Turning them off for outputs requires approval for modified guardrails. Safe content is annotated and is not filtered, and that is not configurable.

### harm-categories-and-languages
- title: Four harm categories, eight trained languages
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-severity-levels

Which harm categories do Foundry guardrails classify?

---

The content filtering system classifies hate, sexual, violence, and self-harm for text and images, using multiclass classifiers. Severity labels are Safe, Low, Medium, and High. Safe is annotated and never filtered.

The text classifiers are trained and tested on Chinese, English, French, German, Italian, Japanese, Portuguese, and Spanish. Other languages can be classified, and the page says performance can vary. A Safe result means that category was not found at a higher severity. It does not mean the text is true, compliant, or appropriate.

### text-severity-is-zero-to-seven
- title: Text severity is 0 through 7, images are trimmed
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-severity-levels

What numeric scale does Azure AI Content Safety use inside Foundry?

---

The text model supports the full 0 through 7 scale, and it can return the trimmed scale 0, 2, 4, and 6 by pairing adjacent levels. The image model returns only 0, 2, 4, and 6. Image-with-text uses the full scale and can also be trimmed.

Guardrail blocking levels are the High, Medium, and Low settings, not these raw numbers. Do not configure a threshold of 3 and expect the image model to return it.

### prompt-shields-two-attacks
- title: Prompt Shields separate user attacks from document attacks
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields

What two attacks do Prompt Shields look for?

---

User prompt attacks try to bypass system instructions or safety training and are scanned at user input. Document attacks are hidden instructions in documents, email, or web pages. For model calls they are scanned at user input. For agents they can also be scanned on tool responses for supported tools, in preview.

User prompt attack detection is on by default. Document attack detection is off until you enable it. The annotation uses the jailbreak object with detected and filtered booleans. In Foundry, a block happens before the model sees the input. The standalone Content Safety API does not block. Your application decides.

### prompt-shields-are-not-harm-filters
- title: Prompt Shields do not judge harm or truth
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields

Does a clean Prompt Shields result mean the prompt is safe and true?

---

No. Prompt Shields detect attempts to manipulate the model through user input or document content. They do not decide whether content is harmful, accurate, grounded, compliant, or on task.

Use the harm categories and the rest of the guardrail for those risks. The user-prompt and document models are trained and evaluated primarily on English, so non-English attacks need their own evaluation. The feature was previously called jailbreak risk detection.

### spotlighting-encodes-documents
- title: Spotlighting base64-encodes untrusted documents
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields

What does Spotlighting change about a retrieved document?

---

Spotlighting, in preview, marks third-party documents as lower trust by base64-encoding them so the model treats them as less trustworthy than user and system prompts. It is off by default, has no direct charge, and increases token count. It is only available for models called through the Chat Completions API.

A known side effect is that the model mentions the base64 encoding even when nobody asked. Large documents can also exceed the input limit. Turn it off if those mentions break the experience.

### defaultv2-blocks-medium-and-high
- title: DefaultV2 blocks medium and high severity
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/default-safety-policies

What does the default safety policy block on a text model?

---

Default safety policies apply to Foundry Models except transcription models. For text, hate, violence, sexual, and self-harm run on prompts and completions at a Medium threshold, which blocks medium and high severity. User prompt attacks run on prompts. Protected material for text and for code runs on completions.

Document attack detection stays off until you enable it. A blocked input returns an error. A blocked output can return a filtered completion. Transcription models use a different safety configuration, so do not assume DefaultV2 covers them.

### image-defaults-add-people-and-politics
- title: Image generation has extra default blocks
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/default-safety-policies

Which extra risks does DefaultV2 apply to image generation?

---

Image generation keeps the four harm categories at Medium on prompts and completions, and adds content credentials on completions, plus deceptive generation of political candidates, depictions of public figures, user prompt attacks, protected material for art and studio characters, and profanity on prompts.

Vision-enabled chat models add identification of individuals and inference of sensitive attributes on prompts. Do not describe the text-model default as the image-model default.

### cmk-is-optional-and-regional
- title: Customer-managed keys add a key you can revoke
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

What do customer-managed keys add on top of Microsoft-managed encryption?

---

Foundry already encrypts persisted data. Customer-managed keys, stored in Key Vault or Managed HSM, add control over rotation, revocation, and auditing. Encryption stays FIPS 140-2 256-bit AES and does not require an application change.

Because of Azure AI Search capacity, CMK is only available in select regions. Check that list before you promise CMK in every region the model supports.

### prompt-agents-need-byo-for-cmk
- title: Prompt-agent CMK requires your own data stores
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Can you turn on customer-managed keys for a prompt agent that uses Microsoft-managed storage?

---

No. The coverage table says prompt agents do not support CMK on Foundry-managed storage. You bring your own resources and configure CMK separately on Cosmos DB, Storage, and Azure AI Search. Hosted agents are the same for those stores, and the session $HOME volume is platform-managed, is not CMK-encrypted, and cannot currently be disabled.

Fine-tuning does support CMK on Microsoft-managed storage, and it does not offer bring-your-own storage. OpenAI Assistants are deprecated and did not support CMK. Connected services such as Search, Logic Apps, and Functions keep their own keys.

### revoking-a-cmk-keeps-old-deployments
- title: Revoking the key stops new fine-tunes, not live ones
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

What keeps working after you revoke a customer-managed key?

---

While CMK stays enabled, revoking the key blocks access to data encrypted with it. You cannot download training data or results, create a new fine-tuned model, or deploy a fine-tuned model.

A fine-tuned model that was already deployed keeps serving, because its artifacts were loaded at deployment time. After you delete that deployment, you cannot recreate it unless you restore the key. You can delete Files API training data and fine-tuned models yourself at any time.

### cmk-does-not-cover-ephemeral-compute
- title: CMK covers stored data, not the live GPU
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Does customer-managed key encryption cover the disk where a job is running?

---

CMK protects customer data at rest in persistent stores. Runtime compute is ephemeral. Data is unwrapped for processing and wrapped again when it is written back. Training jobs leave temporary files that are not CMK-encrypted and that exist only for the job.

Hosted-agent sandbox root disks last up to 24 hours, and $HOME is retained for 30 days on platform storage without CMK. Do not tell an auditor that the running container disk is customer-key encrypted.

### default-network-is-public
- title: A new Foundry resource is public until you change it
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options

What network posture do you get if you never open the networking blade?

---

Inbound, the endpoint is on the public internet for any caller with a valid credential. Outbound, agents reach public endpoints only. Storage is Microsoft-managed unless you bring your own.

Nothing is private until you choose an option. A private endpoint on an otherwise public egress setup protects callers, and it does not isolate agent egress.

### three-egress-models
- title: Public, bring-your-own, and managed networks
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options

Which egress models does Agent Service offer?

---

Public egress can pair with public inbound, selected IP addresses, or a private endpoint. A bring-your-own virtual network and a managed virtual network both force inbound through a private endpoint. Bring-your-own is for when you control ranges, peering, and routing. Managed is for when you cannot manage IP space or your addresses overlap.

Isolation is at the Foundry account and project, and it covers hosted agents, prompt agents, and the other resources in the account. Start from the egress choice, because it decides which inbound options exist.

### vnet-injection-is-create-time
- title: You cannot add network injection after the account exists
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options

Can you attach a virtual network to a Foundry account that is already deployed?

---

No. The networking article says to set virtual network configuration when you create the account. Injection cannot be added later, it takes effect when you create the first hosted agent, and you cannot change it afterward. Moving designs means new projects.

The subnet is delegated to Microsoft.App/environments, it cannot be shared by more than one Foundry resource, and it must be at least /27. You cannot resize it after assignment. Azure reserves five addresses in every subnet. A /24 is the recommendation for production hosted agents.

### hosted-agents-consume-ips
- title: Each hosted session takes a subnet address
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options

How do you size the agent subnet?

---

Hosted agents run in a dedicated micro VM with its own network interface, so each one consumes an address. New revisions also consume addresses while old and new revisions run together. Prompt agents do not take an address per revision. They use a small static pool, up to about 10 addresses per project.

All projects in the account share the subnet, so size it for every project and every concurrent session. Public IP ranges are not supported. Use RFC 1918 space, or RFC 6598 space inside 100.64.0.0/10 excluding the three ranges the page lists.

### byo-data-or-platform-data
- title: Bring-your-own network can still use platform data stores
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options

If you bring the virtual network, must you also bring storage, search, and Cosmos DB?

---

No. With a bring-your-own virtual network you can use platform-managed data resources or your own Storage, Azure AI Search, and Cosmos DB. The managed virtual network is the option where Microsoft runs the network requirements for you.

Choose your own data resources when agent data must stay in your tenant. The Foundry resource and the virtual network must be in the same region. Private DNS zones are required for the account and for each data resource you bring. Not every tool works behind the virtual network, so check tool support before you commit.

### pna-has-three-settings
- title: Public network access can be off, selected, or open
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

How do you control who can reach a Foundry project?

---

The public network access flag can require a private endpoint, allow selected IP addresses and virtual networks, or allow public access. Private Link covers the PaaS pieces such as the project, storage, Key Vault, the container registry, and monitoring. Agent outbound isolation uses virtual network injection into a subnet you delegate.

Standard setup means you bring Storage, Azure AI Search, and Cosmos DB so agent data stays in your tenant. Basic setup leaves those fields empty and lets the platform create them.

### private-dns-keeps-the-same-hostname
- title: Private Link does not change the connection string
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Do clients inside the virtual network use a different Foundry hostname?

---

No. They use the same connection string. Azure points the CNAME at a privatelink alias and creates a private DNS zone. Inside the virtual network the name resolves to the private IP. Outside it, the name still resolves to the public endpoint.

A custom DNS server must resolve the name to the private IP, usually by delegating the privatelink subdomain. Confirm the private endpoint connection is Approved, then resolve the name from a machine on that network.

### removing-a-private-endpoint-stays-private
- title: Deleting the private endpoint does not open the resource
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

What happens if you delete the private endpoint to fix a connection problem?

---

Removing the private endpoint disconnects that virtual network. It does not make the project public. You turn public access back on separately, on Firewalls and virtual networks, by selecting All networks.

Turning public access on does not delete existing private endpoints. Traffic that stays on those endpoints remains private. You have added a public path, not replaced the private one.

### byo-private-endpoints-are-manual
- title: Data-plane private endpoints are not created for you
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Does Foundry create private endpoints for storage, search, and Cosmos DB?

---

No. The private-link article says private endpoints to Azure AI Search, Storage, and Cosmos DB are not auto-created with the Foundry resource. You create them on those resources.

Calls from tools to endpoints outside Foundry also need a capability host at the project, not only at the account. Without the project capability host, those calls fail with errors such as name or host unknown.

### trusted-services-exception
- title: A short list of Azure services can be trusted through the firewall
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Which Azure services can you exempt when Foundry is locked to a virtual network?

---

The private-link article lists Foundry Tools as Microsoft.CognitiveServices, Azure AI Search as Microsoft.Search, and Azure Machine Learning as Microsoft.MachineLearningServices. Those services still authenticate with a managed identity that has the right role.

You add the exception with the REST API or the portal. It is not a general allow-list of every Microsoft service.

### reach-a-private-resource-three-ways
- title: VPN, ExpressRoute, or a Bastion jump box
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

How do developers reach a Foundry resource that has no public endpoint?

---

The article lists a virtual network gateway, either point-to-site or site-to-site, ExpressRoute through a connectivity provider, or an Azure VM in the virtual network that you reach with Azure Bastion.

The jump box works because it is on the network, so it resolves the private endpoint. A laptop on the public internet does not, unless the name is still publicly resolvable and public access is on.

### catalog-two-collections
- title: Models sold by Azure are not the partner catalog
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

How is the Foundry model catalog split?

---

The catalog has Foundry Models sold by Azure, which Microsoft hosts under Microsoft Product Terms, with Microsoft support and enterprise SLAs, and Foundry Models from partners and community, which are the majority and are developed and supported by those providers.

Anthropic models are in the partner set, and the page says to use Microsoft Support for them. Hugging Face models are supported through Hugging Face. Non-Microsoft models are Non-Microsoft Products under the Product Terms.

### about-fifty-models-a-month
- title: About 50 models are added each month
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

How fast does the Foundry catalog change?

---

The models overview says the catalog includes over 10,000 models and that about 50 new models are published each month, from foundation and reasoning models through small, multimodal, domain, and industry models.

You are still responsible for choosing a model, reading its card, and applying controls such as Azure AI Content Safety. A large catalog is not a review of your use case.

### some-azure-models-share-ptu
- title: Some Azure-sold models share provisioned throughput
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

Can one provisioned-throughput reservation cover every model sold by Azure?

---

The overview says some models sold by Azure offer fungible provisioned throughput, so you can use quota and reservations across any of those models. It does not say every model sold by Azure is fungible.

Check the model before you promise that a PTU pool can move to it. Partner and community models are a separate category with their own deployment rules.

### catalog-filters-and-cards
- title: The catalog filters by region, SKU, and task
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

What can you filter on in the model catalog?

---

The overview lists filters for provider collection, region, deployment option, deployment SKU, lifecycle, industry, supported features such as reasoning and tool calling, and inference task. A model card has quick facts, details, deployments, benchmarks, and license.

Leaderboard and benchmark numbers exist for select models, not for every row. You can also request a model that is not in the catalog from the catalog search page.

### classic-hub-for-managed-compute-models
- title: Some managed-compute models still use a classic hub
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

Where do you deploy a Hugging Face model that targets managed compute?

---

The models overview says that to work with models deployable on managed compute, such as Hugging Face models, you use a hub-based project in the Foundry (classic) portal. The provider chooses whether a partner model is serverless, managed compute, or both.

On that page, managed compute billing is described as virtual machine core hours, and content safety is the Azure AI Content Safety APIs rather than filters built into the inference API. Serverless deployments bill for input and output, and their content filters are integrated and billed separately. Managed networks for serverless follow the resource public-network flag.

### instant-access-is-west-us-3
- title: Instant access preview exists only in West US 3
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

Where can you call a model by name without creating a deployment?

---

Instant access, in preview, lets you pass a supported model name such as gpt-5-mini to the same Responses API you use for deployments. During preview the project must be in West US 3, and the caller needs the Foundry User role on the project or the account.

The project endpoint shape in the sample is https://resource_name.services.ai.azure.com/api/projects/project_name. New models support instant access by default when they release. The set changes, so read it from the catalog filter Instant or from the models API capability flag.

### instant-version-pinning
- title: A bare model name tracks the latest version
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

How do you stop instant access from moving to a newer model version?

---

By default, instant access uses the latest evergreen version. To pin a version, append the version date, for example model-name-2025-04-01. A bare model name always tracks the latest.

Pinning is opt-in. If the application needs a stable version, the suffix is required. A deployment is still how you lock an endpoint when you need that as configuration rather than a string in code.

### when-instant-access-is-not-enough
- title: Deploy when you need residency, PTU, or a custom filter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

When does the instant-access page say you still need a deployment?

---

Use instant access for a prototype or for a model that just released. Create a deployment when you need reserved or provisioned throughput, data residency, a custom content filter or guardrail, an endpoint version lock, fine-grained quota per team, or a fine-tuned model.

Both can exist in the same project. Fine-tuned models are not available through instant access. All instant models use default guardrails, and you cannot set a different RAI policy per instant model. One account-level policy applies to all of them.

### deployment-name-hides-instant-model
- title: A deployment name wins over an instant model name
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

What happens if a deployment is named the same as an instant-access model?

---

New deployments cannot use a name that matches an existing model name. If an older deployment already collides, that deployment takes precedence and instant access for that model name is unavailable in the project.

Renaming is the way back to instant access for that name. Do not debug it as a quota or region fault first.

### disable-instant-with-an-empty-allow-list
- title: An empty model allow list turns instant access off
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

How does an administrator turn off instant access?

---

The instant-access page shows an account update, api-version 2026-01-15-preview, that sets properties.instant.raiPolicyName to Microsoft.DefaultV2 and properties.instant.modelAllowList to an empty list. Azure Policy can also block models or providers, or disable instant access at the subscription.

An empty allow list is the off switch in that sample. A non-empty list would be a different policy. Global Standard deployments reserve global quota that instant access would otherwise use. Regional Standard and Provisioned quota do not reduce instant capacity.

### responses-can-omit-the-agent
- title: A response can run with no stored agent
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components

Do you need to create an agent before you can call the Responses API?

---

No. A response is the unit of execution and can run with or without an agent and with or without a conversation. You add an agent when the model, instructions, and tools should be reused, and a conversation when the service should store the history.

The lifecycle on the page is select an agent, create a conversation, add an input item, run a response, then run another response on the same conversation for the follow-up. That is the stateful path, not the only path.

### guardrail-actions-and-preview-risks
- title: Task adherence applies to agents, Spotlighting does not
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview

Which preview risks run on an agent?

---

The applicability table marks hate, sexual, self-harm, violence, user prompt attacks, indirect attacks, protected material for code and text, personally identifiable information, and task adherence as applicable to agents in preview. Spotlighting and Groundedness apply to models and not to agents.

Controls that an agent cannot run are skipped for that agent and still run for models that share the guardrail. If an agent does not behave like its policy, check for those unsupported risks and confirm the agent actually has the guardrail assigned.

### user-prompt-attack-subtypes
- title: Prompt Shields name four user-attack patterns
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields

What kinds of user prompt attacks do Prompt Shields classify?

---

The page lists attempts to change system rules, embedding a fake conversation to confuse the model, role-play that swaps the system persona, and encoding attacks such as ciphers or character transforms.

Document attacks add categories such as manipulated content, information gathering, fraud, and malware, and they are scanned from the documents you submit. A no-attack result does not mean the text is benign or aligned with your system. Customers define where the text came from. The service does not prove provenance.

### enterprise-network-goals
- title: Pick the network template from the isolation goal
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options

Which networking option matches a private endpoint with public egress still allowed?

---

The scenario table recommends public egress plus a private endpoint when you only need to restrict callers. Full isolation with your own data resources is a bring-your-own virtual network. Full isolation without managing data resources can still be bring-your-own, using platform-managed data. Overlapping IP space points at the managed virtual network.

On-premises access is a bring-your-own virtual network plus VPN or ExpressRoute. An API Management front is the bring-your-own option with Azure API Management. The fastest path with no isolation is public networking and Microsoft-managed storage.

### quota-upgrade-takes-the-greater-limit
- title: A model upgrade keeps the larger quota
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

What global quota do you get when a model moves to subscription-level management?

---

The new Global or Data Zone limit is the greater of the tier limit and the total quota already assigned to existing deployments of that model inside the quota scope. Five regional deployments are summed, and that sum wins if it beats the tier.

You do not lose allocated quota in the move. The page says existing approved quota is retained and applied at the subscription level with no action required.

### microsoft-decision-rpm
- title: Microsoft-Decision-1 is limited in requests per minute
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

How is Microsoft-Decision-1 quota expressed?

---

The Foundry Models quota page lists Microsoft-Decision-1 Global Standard and Data Zone Standard limits in requests per minute by subscription tier, from 60 at tier 1 to 900 at tier 6. The deployment's own limit still depends on configured capacity and allocated quota.

Do not read that table as tokens per minute. Grok 4.7 on the same page is the model that uses tokens per minute, at 1,000 TPM per capacity unit.

### fine-tune-cmk-on-managed-storage
- title: Fine-tunes are encrypted on Microsoft storage
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Where are fine-tuning files encrypted when you enable customer-managed keys?

---

Uploaded files and the trained fine-tuned models are CMK-encrypted on Microsoft-managed storage. Trained models are logically isolated by Azure subscription. Weights are unwrapped when a deployment is instantiated.

Batch uploads are also CMK-encrypted at rest on Microsoft-managed storage, and that account is virtually mounted on the compute nodes for the scoring job. Evaluation assets stored by Foundry are CMK-protected as well.

### content-understanding-requires-your-storage
- title: Content Understanding requires bring-your-own storage
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Can Content Understanding run on Foundry-managed storage?

---

The CMK coverage table says bring-your-own storage is required to use Content Understanding. CMK on Foundry-managed storage is not applicable for that capability.

Speech is the other row that needs your storage for CMK, covering training data, batch transcription, real-time transcription logs, and custom speech. Language can use either Microsoft-managed or customer-managed keys when you do not bring storage.

### hugging-face-weights-are-microsoft-hosted
- title: Hugging Face weights in Foundry stay on Microsoft storage
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Can you store Hugging Face model weights on your own account for managed compute?

---

The CMK table says those weights are stored on Azure Storage managed by Microsoft, and they cannot be stored on your own storage. CMK on your storage is not applicable for that row.

Plan encryption for the data you send at inference time separately from the weight files. The weights are not a bring-your-own-key blob you control.

### catalog-responsibility
- title: You still own model choice and acceptable use
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

Who is responsible for how a catalog model is used?

---

The models overview says you comply with the law, read the model card and provider documentation, select an appropriate model, and implement measures, including Azure AI Content Safety, so use meets the Acceptable Use Policy and the Microsoft Enterprise AI Services Code of Conduct.

Models sold by Azure go through Microsoft's Responsible AI review, and the page says those reviews do not guarantee that risks are mitigated. You still evaluate the model for your application.

### serverless-content-filters-billed-apart
- title: Integrated content filters are a separate bill
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

Are content filters included in the serverless token price?

---

For serverless deployments, the models overview says Azure AI Content Safety filters are integrated with the inference APIs and billed separately. Pricing for the model itself is shown before you deploy, typically per token.

Keys and Entra ID both work for serverless and for managed compute on that comparison table. Do not assume the filter charge is inside the token price.

### data-processing-choices-on-serverless
- title: Serverless lets you pick regional, data zone, or global
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

What data-processing choices does a Serverless API deployment give you?

---

Serverless API deployments can process regionally, in a data zone, or globally, and they include integrated content filters you can customize, Entra ID or keys, private networking, and provisioned throughput units when you need reserved capacity.

Managed compute, in the same comparison, is global only, and content filtering is not available in public preview. Use serverless when you need those controls.

### batch-and-provisioned-billing-words
- title: Provisioned capacity is hourly, batch is batch pricing
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

How does the architecture page describe billing for each deployment family?

---

Global, Data Zone, and regional Standard types are pay-per-token. The provisioned types are hourly reserved capacity. The batch types use batch token pricing. Developer is pay-per-token for fine-tuned evaluation only, with a 24-hour lifetime and no SLA.

That table is the short version of the deployment-types page. Use it to separate how you pay from where the data is processed. Developer still has no residency guarantee.

### agents-batch-and-evals-are-managed
- title: Microsoft runs agent, evaluation, and batch compute
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Who operates the computers behind agents, evaluations, and batch jobs?

---

The architecture page says agents, evaluations, and batch jobs are fully managed by Microsoft. Agent workloads run in the platform's container infrastructure, which can integrate with a virtual network. Evaluations call model endpoints, grade outputs, and store results in the project. Batch queues requests for asynchronous execution at lower per-token pricing.

You reach the results through the portal or the SDK. You do not provision those machines yourself. Content filters can still be configured per model deployment, and they run inline with the request.

### guardrails-scan-tools-in-preview
- title: Tool calls and tool responses are preview scan points
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Where does the architecture page say a guardrail can intervene?

---

Guardrails define the risks to detect, the intervention points to scan, and the action when a risk is found. The points named there are user input, output, tool calls in preview, and tool responses in preview.

Content filters run inline with model requests and can be set per deployment. A system prompt is not that configuration. The filter is the guardrail on the deployment or the agent.

### project-endpoint-for-most-new-work
- title: Prefer the project scope unless the API is account-only
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Should new application code call the Foundry resource or the project?

---

The architecture page says most new APIs are at the project scope, and that some older account-level capabilities, with Translator given as the example, exist only on the Foundry resource.

Build against the project unless you have checked that the API is one of the resource-only leftovers. A project is also the unit that reuses deployments without another IT request.

### monitor-eval-on-the-project
- title: Evaluation metrics do not roll up as agent metrics
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Which metrics stay on the project even though tokens are visible on the resource?

---

Resource metrics cover token consumption, model latency, request counts, and error rates for every project. Project metrics cover evaluation run outcomes, agent invocation counts, and file operations.

If an evaluation looks missing from the resource chart, open the project scope. Diagnostic settings are what export the logs to Log Analytics, Storage, or Event Hubs.

### first-developer-gets-one-resource
- title: One resource and one project is the starting shape
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What shape does the architecture recommend for a single developer?

---

For single-developer exploration, the architecture page recommends one Foundry resource with one project. A standalone Azure OpenAI resource might be enough only when the workload needs completions and does not need agent hosting or evaluation.

When several teams need isolated projects but can share model deployments and centralized governance, the page points at projects under that resource, not at a new resource per team.

### kind-aiservices-is-the-foundry-account
- title: Kind AIServices is the Foundry account
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

How do you tell a Foundry account from a Speech account in the same provider?

---

Both are Microsoft.CognitiveServices/accounts. Foundry uses kind AIServices. Speech, Language, and Vision use kinds Speech, Language, and Vision. The project is a child of the AIServices account.

Resource types in that provider share management APIs, similar RBAC actions, networking configuration, and Azure Policy aliases. That is why an Azure OpenAI policy can still apply after an upgrade to Foundry.

### voice-live-region-depends
- title: Voice availability depends on region, model, and preview flags
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

What do you check before you promise a voice agent in a region?

---

The overview says availability depends on the Foundry resource region, the model, the voice, the subscription, and enabled preview features. Check the portal before you depend on a specific model.

Charges can include model tokens, speech recognition and synthesis, custom voice, avatar, Application Insights, Azure Communication Services, Teams telephony, and connected tools. Voice is not priced as token inference alone.

### publish-channels
- title: Published agents can show up in Copilot, Teams, and Entra
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Where can a published Foundry agent be shared?

---

The overview says you can share published agents through Microsoft Copilot, Teams, and the Entra Agent Registry. Publishing promotes an agent to a managed resource with a stable endpoint, and that published agent inherits the project's identity and access controls.

Versions are snapshotted as you iterate, so you can roll back. Publishing is that promotion step, not a synonym for saving a draft.

### optimizer-is-preview
- title: The agent optimizer rewrites instructions automatically
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

What does the agent optimizer change?

---

The overview describes the agent optimizer, in preview, as evaluating behavior and generating better instructions, skills, tool descriptions, and model selections for prompt agents and hosted agents.

It is an optimization pass, not a second agent you have to host. Treat it as preview when you talk about a production change-control process.

### swap-the-model-keep-the-agent
- title: You can change the model without rewriting the agent
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

Do you rebuild an agent to try a different catalog model?

---

The overview says Agent Service works with many catalog models, with GPT-4o, Llama, and DeepSeek given as examples, and that you can swap models without changing the agent code.

The swap is a model change, not a rewrite of the agent. Confirm the replacement is a catalog model the service can run. The overview does not say every model supports every tool you already attached.

### background-mode-versus-resilience
- title: Background mode is not the same as crash recovery
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

What is the difference between background mode and resilient execution on a hosted agent?

---

Background mode lets work continue after the HTTP request returns. Resilient execution preserves work after the hosting process stops. The hosted-agent page says they solve different problems, and that recovery has its own application responsibilities.

Opt into resilient recovery separately when a Responses handler must survive a process interruption. Do not assume background: true restarts a dead process.

### responses-history-is-platform-managed
- title: Responses keeps history, Invocations does not
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

Who stores conversation history for a hosted agent?

---

With the Responses protocol, Foundry stores history through the conversation ID and manages the streaming lifecycle. With Invocations, you store sessions yourself, in memory, Cosmos DB, or another store, and you format the server-sent events.

Teams and Microsoft 365 delivery is a bridge from Responses to the Activity protocol. You do not implement that bridge in the container.

### idle-compute-restores-home
- title: Idle compute comes back with the same files
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

What is still there after a hosted session scales to zero?

---

The page says $HOME and /files persist across turns and across idle periods, and that state is restored when compute is provisioned again, including on new infrastructure.

The idle timeout only removes compute. It does not delete the session. Permanent deletion happens after 30 days without activity, unless you delete the session sooner.

### obo-needs-a-user-token
- title: On-Behalf-Of runs only when a user token is present
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents

When does a hosted agent act as the user instead of as itself?

---

If a user token is present, the platform can run OAuth 2.0 On-Behalf-Of so downstream calls use the user's delegated permissions, subject to tenant policy. If no user token is present, the agent authenticates with its own Entra identity.

The agent keeps its own identity in both cases, for audit. For MCP tools, the page says to connect them through a toolbox, using FoundryToolbox in Python or AddFoundryToolboxes in .NET when the agent uses Microsoft Agent Framework.

### tool-limit-error-code
- title: Too many tools is HTTP 400, not a quota ticket
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What should the application do when agent create fails with tool_limit_exceeded?

---

The limits page maps that code to HTTP 400 and says to remove unused tools. The cap is 128 tools registered on one agent, and it is a fixed limit.

Do not open a quota increase for it. The same page says the file, message, and tool limits cannot be raised. Prefer fewer reusable tools.

### vector-store-token-cap
- title: A vector-store file can fail at two million tokens
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Why would attaching a file to a vector store return token_limit_exceeded?

---

The maximum file size for a vector-store attachment is 2,000,000 tokens. The service returns HTTP 400 with token_limit_exceeded. Split the file or cut the content.

That cap is separate from the 512 MB upload limit for a prompt-agent file and from the 300 GB cap on all uploaded agent files. A file can pass the byte limit and still fail the token limit.

### message-size-versus-file-search
- title: Oversized message text should be a file
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What do you do when a message hits content_size_exceeded?

---

The text content of one message is capped at 1,500,000 characters. The page says to send a smaller message, or to put the large content in a file and use file search.

Threads themselves cap at 100,000 messages. Plan to rotate long conversations onto a new thread instead of appending forever.

### gov-cloud-is-a-subset
- title: Azure Government agents are a subset
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Is every Foundry agent feature in Azure Government?

---

The limits page says Foundry Agent Service is available in Azure Government, in US Gov Virginia and US Gov Arizona, with a subset of agent types and tools. It points at the government feature-availability article for the list.

Do not copy a commercial-region design into a government region without checking that subset. Model availability also varies by region in the commercial cloud.

### gpt5-registration
- title: Some GPT-5 models require registration
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Why is a GPT-5 model missing even in a region that lists it?

---

The troubleshooting section says that if you are using GPT-5 models, registration is required, and access is granted under Microsoft's eligibility criteria. It also says to confirm you are on the right deployment-type tab, global standard versus provisioned.

A missing tool is a different failure. Check the tool-by-region table, and do not assume file search exists because the agent region is supported.

### provisioned-failure-is-ptu
- title: A failed provisioned deployment is often missing PTUs
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What do you check first when a provisioned agent deployment fails?

---

The limits page says to confirm you have enough provisioned throughput units in the region, and to review provisioned throughput and spillover.

That failure is capacity, not the 128-tool cap. Spillover is the documented companion control when reserved capacity is not enough on its own.

### exponential-backoff-for-429
- title: Back off with jitter on agent 429s
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

What retry behavior does the agent limits page recommend?

---

For rate limits and for regional session capacity, it says to retry with exponential backoff and jitter. Sustained high throughput should look at provisioned throughput and at the Azure OpenAI tokens-per-minute caps.

session_quota_exceeded is the exception to a blind retry. You need to free a session or raise the limit. A retry storm will not create capacity.

### data-residency-follows-deployment-type
- title: Stored data stays in the geography you chose
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Where does Foundry store data, as opposed to where it runs inference?

---

The architecture page says Foundry stores all data at rest in the designated Azure geography. Inference follows the deployment type. Global deployments might route to any Azure region. Data zone deployments stay in the US or EU zone on that page. Standard or regional deployments process in the deployment region.

Use the deployment-types article when you need the Asia Pacific zone called out. This architecture sentence is the at-rest rule plus the processing split. There is still no automatic cross-region failover.

### customer-managed-vnet-tradeoff
- title: Bring-your-own network costs you the operations
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What do you give up with a managed virtual network?

---

A customer-managed virtual network gives you full control and requires you to run the network. A managed virtual network is the simpler setup and limits customization. The architecture page points at the managed-virtual-network article for that option.

Both exist so agents can reach private resources. The delegated subnet for the customer-managed case is Microsoft.App/environments. Portal-only setup is not enough when public access is fully disabled.

### encryption-in-transit-too
- title: Microsoft-managed keys cover rest and transit
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Do you have to enable encryption for a new Foundry resource?

---

No. The architecture page says Azure services encrypt data at rest and in transit with Microsoft-managed keys, FIPS 140-2 256-bit AES, and that no code change is required.

Turn on customer-managed keys only when you need to control the key. The prerequisites are a same-region Key Vault, soft delete, purge protection, and a key permission such as Key Vault Crypto User.

### batch-price-is-lower-per-token
- title: Batch trades latency for a lower token price
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Why would you queue inference instead of calling the model online?

---

The architecture page says batch processing queues requests for asynchronous execution at reduced per-token pricing, and that results are available through the portal or the SDK.

Use batch when the caller can wait. The page describes it as asynchronous and cheaper per token, not as a low-latency online deployment.

### evaluation-results-stay-in-the-project
- title: Evaluation output is stored on the project
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Where do evaluation results live?

---

The architecture page says evaluations invoke model endpoints, compare outputs to grading criteria, and store results within the project scope.

That is why project metrics include evaluation outcomes, and why a project is the boundary for those artifacts. The resource is the governance boundary, not the place those results are scoped.

### connections-are-resource-settings
- title: Connections to other Azure services are resource governance
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Who creates the connection to Key Vault or Search?

---

The architecture page puts establishing connectivity with other Azure services, along with security and deployments, on the top-level Foundry resource. Projects isolate the development work.

Developers reuse those connections. They should not each create a new Key Vault connection. One Key Vault connection covers project and resource secrets.

### policy-aliases-survive-upgrade
- title: Policy aliases are shared across the provider
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Why can an existing Azure Policy still see a Foundry resource after an upgrade?

---

Resource types under Microsoft.CognitiveServices share management APIs, similar RBAC actions, networking configuration, and aliases for Azure Policy. The page says existing custom policies and RBAC actions continue to apply when you upgrade from Azure OpenAI to Foundry.

Test the policy. Do not rewrite it just because the product name changed. The resource type is still Microsoft.CognitiveServices/accounts.

### content-filters-per-deployment
- title: Each deployment can have its own content filter
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Can two deployments of the same model use different filters?

---

The architecture page says content filters run inline with model requests and can be configured per deployment. Guardrails name the risk, the intervention point, and the action.

Two deployments can therefore carry different filters. Do not assume one account-wide setting is the only control the architecture describes for deployed models.

### logical-separation-is-not-your-tenant
- title: Basic storage is logically separated, not your account
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

Does basic agent setup put files in the customer's storage account?

---

No. Basic setup uses Microsoft-managed multitenant storage with logical separation for threads, messages, and files. Standard setup is the one that puts files, conversations, and vector stores in your accounts, isolated by project.

Say logical separation when that is the control you have. Say customer-managed storage only after you have brought the accounts.

### regional-availability-check
- title: Confirm the region before you create the resource
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture

What should you verify before you pick a Foundry region?

---

The architecture page says model availability, deployment types, and features such as agents or evaluations can differ by region. Confirm the target region before you provision.

Creating the resource in a region that lacks the model or the agent feature is expensive to unwind, especially if network injection was set at creation and cannot be moved.

### fips-is-the-default-cipher
- title: The default cipher is 256-bit AES
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Which algorithm does Foundry use for Microsoft-managed encryption?

---

The customer-managed key article says Foundry data is encrypted and decrypted with FIPS 140-2 compliant 256-bit AES, and that the operations are transparent to your code.

CMK changes who holds the key. It does not change the algorithm the article names, and it does not cover every ephemeral disk.

### delete-training-files-yourself
- title: You can delete fine-tune files and models
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

How do you get training data out of Foundry when a job is finished?

---

The CMK article says you can delete training, validation, and training-results data uploaded through the Files API at any time, and you can permanently delete fine-tuned models and deployments.

Deletion is your action through the DELETE APIs. Revoking a customer-managed key is a different operation. It blocks access. It is not the documented way to erase a deployment that is already serving.

### workload-isolation-per-resource
- title: Runtimes do not share execution containers
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/customer-managed-keys

Do customers share execution containers on Foundry compute?

---

The CMK article says Foundry workloads run in logically isolated environments for a specific Foundry resource, and that customer code, agent execution, and workload runtimes do not share execution containers with other tenants. Runtime caches are isolated at the tenant or resource boundary.

That isolation is the control for ephemeral compute. CMK is the control for persisted data. Quote the one the question is about.

### selected-ip-inbound
- title: Selected networks are the middle inbound setting
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Is the inbound choice only public or private?

---

No. Besides public access and a private endpoint, the private-link article describes Enabled from selected IP addresses, which allows the addresses you list.

Use selected IPs when specific offices or build agents must call a still-public endpoint. Use a private endpoint when the endpoint should not be public.

### private-endpoint-same-region
- title: Create the private endpoint in the virtual network's region
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Which region do you pick for a Foundry private endpoint?

---

The create steps say to select the same region as the virtual network. In the portal, the private-endpoint target is labeled as an account. You select the Foundry resource.

A private endpoint in another region is not the configuration those steps describe. DNS still has to resolve the name to that endpoint from inside the network.

### contributor-approves-the-endpoint
- title: A private endpoint can sit in Pending
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Why would a new private endpoint stay in Pending?

---

Creating the endpoint needs Network Contributor, or equivalent, on the virtual network, and Contributor or Owner on the Foundry project resource. If you cannot approve the connection, it stays Pending until an owner approves it.

Private DNS Zone Contributor is the extra role when you manage the DNS zone that is linked to the virtual network. A Pending connection is an authorization problem, not a model problem.

### injection-subnet-minimum
- title: Injection needs a /27 delegated to Microsoft.App/environments
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

What subnet does the portal ask for when you enable virtual network injection?

---

After you disable public access and add the inbound private endpoint, you select a virtual network and a subnet delegated to Microsoft.App/environments with size /27 or larger. The private-link article says that delegation and size are required.

Basic setup on the storage tab leaves Storage, Azure AI Search, and Cosmos DB empty. Standard setup selects those three. Do not expect their private endpoints to appear on their own.

### three-isolation-zones
- title: Plan inbound, outbound, and agent egress separately
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

What three network paths does the private-link article tell you to design?

---

Inbound access to the Foundry resource, outbound access from the Foundry resource to other Azure services, and outbound access from the Agent client to private data, Azure PaaS, or approved internet endpoints through virtual network injection.

Private Link is how the PaaS resources are reached. Injection is how the agent client enters your subnet. Locking down only the inbound private endpoint leaves agent egress on the public path if you never chose an isolated egress model.

### portal-label-says-account
- title: The private endpoint wizard says account
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

The private-endpoint wizard asks for an account. What do you select?

---

The private-link steps say the target is labeled as an account in the portal UI, and that you select your Foundry resource.

Do not go looking for a different Azure resource type because of that label. The Foundry resource is the account.

### expressroute-or-vpn
- title: On-premises networks use a gateway or ExpressRoute
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

How does an office network reach a private Foundry endpoint?

---

Point-to-site VPN puts a client on each computer. Site-to-site VPN uses a device to connect the office network. ExpressRoute is a private connection through a connectivity provider. A Bastion VM is the option when users should work from a machine that already sits in the virtual network.

All of these exist because a disabled public endpoint is not reachable from the public internet, even with a valid key or token.

### firewall-all-networks
- title: All networks is how you restore public access
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link

Which blade turns public access back on?

---

On the project, under Networking, the Firewalls and virtual networks tab has All networks. Saving that re-enables public access.

Do that only when you mean to. Deleting a private endpoint is not this step, and this step does not remove private endpoints that are still there.

### agent-service-ga-with-preview-parts
- title: Agent Service is GA, and some parts are preview
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Is Foundry Agent Service generally available?

---

The limits page says Foundry Agent Service is generally available, and that some sub-features are in public preview and might have different constraints.

Voice is one of those preview surfaces on the agent overview. Quote the sub-feature's own status. Do not treat the service GA line as a GA line for every tool and every channel.

### concurrent-sessions-need-a-support-request
- title: Session quota increases go through support
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

How do you raise the hosted-session cap?

---

The limits page says the 1,000 and 2,000 concurrent session numbers are defaults. To raise them you create an Azure support request with the subscription, the region, and the number of concurrent sessions you expect. The increase depends on regional capacity.

Model quota uses the Foundry quota flow. The file, message, and tool caps are not part of either request. They stay fixed.

### deployment-type-tab
- title: Check the deployment-type tab when a model is missing
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

A model is missing in the portal. What does the limits page tell you to click first?

---

Confirm you selected the tab for the deployment type you intend, such as global standard versus provisioned, and try a region that supports both the model and the Responses API.

GPT-5 can also be missing because registration is required. Those are catalog and eligibility checks, not quota-page failures.

### rest-of-models-rate
- title: Unlisted models share the 400,000 TPM default
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

What rate limit applies to a Foundry model that has no row of its own?

---

The quota page says the rest of the models, other than the Azure OpenAI and the specifically listed ones, are at 400,000 tokens per minute, 1,000 requests per minute, and 300 concurrent requests.

Azure OpenAI models are the exception that varies by model and SKU. Image models such as Flux are the other exception, because their limits are in requests or capacity units, not that token row.

### header-future-removal
- title: Do not depend on custom headers being echoed
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

Can you use custom headers as a permanent part of a Foundry client?

---

The quota page allows up to 10 custom headers today and says the pipeline passes them through and returns them. It also says future API versions will not pass custom headers through, and that you should not depend on them.

Stay at or under 10 to avoid HTTP 431 now, and remove the dependency before you adopt a later API version.

### anthropic-is-the-partner-exception
- title: Anthropic can request quota, other partners cannot
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/quotas-limits

A partner model is throttling. Can you file a quota increase?

---

The quota page says increases are available for models sold by Azure, Azure OpenAI models, and Anthropic models. Other models from partners and community do not support quota increases.

If the model is not Anthropic and not sold by Azure, design inside the published limit. A support ticket will not raise it.

### fifteen-minute-quota-lag
- title: Quota edits can take 15 minutes to appear
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/quota

You changed a deployment's quota and the page still shows the old number. What now?

---

The quota article says to allow up to 15 minutes after an edit or a request, then refresh. If the new allocation is still missing after 24 hours, contact Azure support.

An empty page is more likely the Cognitive Services Usages Reader role at subscription scope, or the wrong subscription. Do not file a capacity ticket in the first 15 minutes.

### instant-models-share-global-pool
- title: Instant models in one subscription share global quota
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

Do two projects compete for instant-access quota?

---

The instant-access page says the global quota pool is per model, assigned to the subscription, and shared automatically across all instant model usage. You do not allocate it per project.

A Global Standard deployment in that subscription reserves part of the same global quota. Regional Standard and Provisioned deployments use regional quota and do not take from the instant pool. Throttling means you request more global quota or create a reserved deployment.

### playground-lists-instant-models
- title: The playground can switch to an instant model
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

How do you try an instant-access model without writing code?

---

From the project home page, open Test in playground and use the model dropdown. The dropdown lists deployed models and instant-access models. You can also open a model from the catalog and choose Open playground.

The project still has to be in West US 3 during preview. A model that shows up with no quota can appear in the list and still throttle. The page points at the quota article for that case.

### policy-blocks-instant-models
- title: Azure Policy applies to instant access too
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

Can governance block an instant-access model the way it blocks a deployment?

---

The instant-access page says Azure Policy definitions apply to instant access the same way they apply to deployments, including blocking specific models or providers. Administrators can also disable instant access at the subscription.

Per-model content filters are not available on instant access. If two models need different guardrails, deploy them. The account-level RAI policy is uniform for every instant model.

### new-models-are-instant-by-default
- title: A newly released model is instant unless excluded
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

Do you wait for a deployment type before you can try a brand-new model?

---

The instant-access page says new models support instant access by default when they are released. You pass the model name. You do not create a deployment first.

That default is still preview and still limited to West US 3 projects. Data residency, provisioned throughput, and fine-tuned models remain deployment features.

### same-client-for-instant-and-deployed
- title: Instant access uses the same SDK as a deployment
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

Do you need a second client library for instant-access models?

---

No. The page says the same API, SDK, and client work for instant access and for deployments. The samples use the project client and then the Responses API, with the model name in the model field.

There is no separate instant-access SDK. The difference is the string you pass and the lack of a deployment, not a new programming surface.

### rai-policy-is-uniform
- title: One RAI policy covers every instant model
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

Can finance and healthcare instant models use different content filters?

---

No. The page says you cannot configure custom guardrails or RAI policies per instant model. You can set a default RAI policy at the account, and it applies uniformly to all instant models.

Deploy the models that need different filters. An empty modelAllowList on the account is how the sample turns instant access off entirely, with Microsoft.DefaultV2 still named as the RAI policy.

### west-us-3-project-required
- title: The instant-access role is Foundry User
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models

What access does a developer need to call an instant model?

---

The prerequisites are a Foundry project in West US 3 and the Foundry User role on the project or the account. The page repeats that the Foundry role names replaced the Azure AI role names and that the role IDs did not change.

A key-only caller is not what those prerequisites describe. Foundry User is the data-plane role for building and calling with a pre-deployed or instant model.

### catalog-request-a-model
- title: You can ask Microsoft to add a missing model
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

What do you do when a model is not in the catalog?

---

From the catalog search page, search for the name and choose Request a model. The overview documents that path for a model the catalog does not contain.

Requesting a model is not a deployment and not a quota increase. Partner models that are already listed are deployed the way their provider allows, serverless or managed compute.

### model-card-has-a-license-tab
- title: Read the license tab before you ship a model
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

Where do you read the legal terms for a catalog model?

---

The model card includes a license tab, plus details, existing deployments, and benchmarks for select models. The overview says models from providers other than Microsoft are Non-Microsoft Products and follow the terms provided with the model.

Benchmarks are optional. A missing Benchmarks tab does not mean the model is unlicensed. It means those metrics are not published for it.

### industry-filter
- title: The catalog can filter by industry training data
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

How do you find a model trained for a domain such as health or retail?

---

The overview lists an industry filter for the industry-specific dataset used to train models, with health, retail, and manufacturing as examples. Other filters cover collection, region, deployment option, SKU, lifecycle, features, and task.

An industry filter is not a compliance certification. You still review the model card and evaluate the model for your application.

### lifecycle-filter
- title: Preview, GA, and deprecated are catalog lifecycle values
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

How do you avoid a deprecated model in the catalog?

---

The lifecycle filter includes Preview, Generally available, and Deprecated. Use it before you standardize on a model that happens to top a search.

Lifecycle is separate from deployment SKU. A generally available model can still lack the deployment type or region you need. Check those filters too.

### support-split-by-who-sold-the-model
- title: Microsoft supports Azure-sold models, providers support the rest
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

Who do you call when a catalog model misbehaves?

---

Models sold by Azure come with Microsoft support. Partner and community models are supported by their providers, with the integration guidance coming from Azure. The page specifically sends Anthropic questions to Microsoft Support and Hugging Face questions to Hugging Face.

Do not open a Microsoft support case for a community model and expect the same SLA as a model sold by Azure. The support owner follows the catalog category.

### managed-compute-classic-billing
- title: Classic managed compute bills VM core hours
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

How does the models overview describe managed-compute billing?

---

It says model weights go to dedicated virtual machines, a managed compute can host one or more deployments behind a REST API, and you are billed for the virtual machine core hours those deployments use.

That billing sentence sits next to the instruction to use a hub-based project in the classic portal for models that deploy on managed compute. Keep the VM-hour description with that classic hub path.

### serverless-auth-is-key-or-entra
- title: Serverless inference accepts a key or Entra ID
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview

How do you authenticate a serverless model call?

---

The models overview says both managed compute and serverless deployments support keys and Microsoft Entra authentication.

Content safety is the part that differs. Serverless can use integrated filters. The managed-compute column on that table points you at the Content Safety service APIs instead.

### deployment-comparison-no-hub
- title: New Foundry deployments do not need an AI Hub
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Does a Foundry project need an AI Hub before you can deploy a model?

---

The deployment comparison says neither Serverless API nor managed compute requires an AI Hub. Serverless deployments live on the Foundry resource. Managed compute deployments live on the Foundry project.

An Azure OpenAI resource can host serverless Azure OpenAI models only. The full catalog is a reason to use a Foundry resource, not a reason to add a hub.

### managed-compute-preview-disclaimer
- title: Managed compute preview has no SLA
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Should you run production traffic on managed compute?

---

The deployment overview says managed compute is in public preview, is provided without a service-level agreement, and is not recommended for production. Some features are unsupported or limited.

Use Serverless API when the model is offered there. Managed compute is the path for open-source and custom weights that need dedicated GPU capacity, including examples such as Qwen, NVIDIA Nemotron, and selected Meta and Mistral models.

### observability-on-managed-compute
- title: Managed compute emits latency and token metrics
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

What metrics does a managed compute deployment emit?

---

Each deployment emits API call count by status code and response-time percentiles. Chat-completion models also emit input and output token counts, time-to-first-token percentiles, and total response-time percentiles.

Those metrics do not add content filtering. The same page says content filtering is not available on managed compute in public preview. You still get the call and latency signals.

### global-only-managed-compute
- title: Managed compute processes globally
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Can you pin a managed compute deployment to one Azure region for data processing?

---

The comparison table says managed compute data processing is global. Serverless API is the option with regional, data zone, and global choices.

If the requirement is a data zone or a single geography, do not choose managed compute and expect a residency switch. That control is on the serverless deployment type.

### ptu-is-a-serverless-feature
- title: Provisioned throughput is a serverless capability
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Where do provisioned throughput units apply?

---

The deployment overview lists provisioned throughput on Serverless API deployments. You reserve capacity in provisioned throughput units for predictable, lower-latency performance.

Managed compute does not use that PTU model. Its quota is accelerator SKUs per region, and its bill is hourly per accelerator. Do not buy PTUs and expect them to cover a GPU managed-compute deployment.

### huggingface-on-managed-compute
- title: Hugging Face models are a managed-compute example
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

How do open models from Hugging Face get deployed in the deployment overview?

---

The page says you can deploy models from the Hugging Face collection with managed compute, and it gives Qwen, NVIDIA Nemotron, selected Meta models, and selected Mistral models as examples.

The collection changes. Use the catalog for the current list. The overview also says Foundry chooses GPUs for you from model size, architecture, context, and the latency or throughput goal.

### patches-apply-live
- title: Microsoft patches managed-compute runtimes in place
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Who patches the container that serves a managed compute model?

---

The deployment overview says Microsoft owns the serving runtimes, base images, and security patches, and that updates are applied to live deployments automatically.

You do not own a VM image to patch. That is also why the page can say you do not pick VM SKUs. Your responsibility is the model you selected and the traffic you send.

### chat-route-for-managed-compute
- title: Some managed-compute models answer on the OpenAI route
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/deployments-overview

Can the OpenAI SDK call a managed compute chat model?

---

Yes, when the runtime is chat-completions compatible. Those models work on the standard /openai/v1/ route. Other calls use /managed-deployments/ on the project endpoint.

Authentication stays the project key or Entra ID. You do not get a separate endpoint host for managed compute. Content filters are still not part of that preview path.

### sku-launch-order
- title: Geography deployments arrive last
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Why is a new model missing as a Standard deployment in your region?

---

The deployment-types page says types become available as Global, then Data Zone, then geography-based. Geography-based types arrive last, depend on capacity freed by retiring models, and have no guaranteed date.

Global Standard is the type that exists first. Waiting for a regional Standard deployment is not the way to try a model on the day it launches.

### regional-provisioned-sku
- title: Regional provisioned capacity uses ProvisionedManaged
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Which SKU name is Regional Provisioned, and what does a PTU mean?

---

The SKU is ProvisionedManaged. Throughput is a count of provisioned throughput units. Each model-version pair needs a different number of PTUs and returns a different amount of throughput per PTU. Minimums vary by model.

Global Provisioned is a different SKU, GlobalProvisionedManaged, and it can place inference in any region. Use Regional Provisioned when the processing has to stay in the Azure geography.

### eu-data-boundary
- title: The EU data zone includes more than EU member states
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Does EU Data Zone processing stay inside EU member states only?

---

The deployment-types page says the EU Data Zone follows the Azure EU Data Boundary, which can include EFTA countries and regions such as Norway and Switzerland in addition to EU member states.

If the contract requires member states only, EU Data Zone is the wrong control to cite without reading the boundary. APAC is its own zone, and Microsoft can add regions to either zone without notice.

### priority-on-data-zone
- title: Data Zone Standard supports priority processing
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Can you buy faster responses on Data Zone Standard without moving to provisioned throughput?

---

Yes. The page says Data Zone Standard supports priority processing for faster responses on a pay-as-you-go basis. Global Standard adds both Flex, for cheaper delay-tolerant work, and Priority.

Priority is still pay-as-you-go. It does not reserve PTUs and it does not remove the latency variability the page warns about at high sustained volume.

### batch-quota-is-separate
- title: Batch has its own enqueued token quota
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Will a large batch job starve your online Global Standard deployment?

---

Global Batch uses a separate enqueued token quota so it does not disrupt online workloads. You submit many requests in one file instead of one request at a time.

The discount is 50 percent versus Global Standard, with a 24-hour target and no real-time SLA. Data Zone Batch keeps the same price pattern inside the data zone. Online latency is the wrong success metric for either one.

### developer-tier-auto-deletes
- title: Developer deployments delete themselves
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

What happens to a Developer deployment after the evaluation?

---

It has a fixed 24-hour lifetime and is automatically deleted when that lifetime ends. It exists to evaluate a fine-tuned model, it is pay-per-token, and it includes neither an SLA nor a data-residency guarantee.

Do not point production traffic at it, and do not expect the deployment to still be there tomorrow. A real rollout of a fine-tuned model uses a deployment type that is meant to last.

### not-all-models-all-types
- title: Model support for deployment types is not universal
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Can you deploy every catalog model as Data Zone Provisioned?

---

No. The deployment-types page says not all models support all deployment types, and it tells you to check Foundry Models sold by Azure for availability by type and region.

If the type is missing in the portal, the model does not offer it. Switching regions or waiting for the launch order is the next check, not a support bug by default.

### provisioned-lower-variance
- title: Provisioned types are the low-variance choice
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Which deployment category do you pick when latency has to be predictable?

---

The page says provisioned types provide guaranteed throughput and lower latency variance. Standard types are best effort. Developer has no SLA and is not for latency-sensitive work.

High sustained volume on Global Standard or Data Zone Standard can increase latency variability. That is the case the page sends to provisioned throughput.

### troubleshooting-deployment-quota
- title: Deployment failures are often quota or region
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

A deployment create fails. What causes does the deployment-types page list?

---

The type can be unavailable because the model does not support it. Quota exceeded means the subscription token-per-minute limit was reached. The region can lack the model. Provisioned capacity can be absent in that region, in which case you try another region or Global Provisioned.

Match the error to that list before you change the application. A quota failure is a subscription limit. A missing type is a model capability.

### data-zone-higher-default-quota
- title: Data Zone Standard has higher default quota than regional Standard
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Why would someone pick Data Zone Standard instead of regional Standard?

---

Data Zone Standard keeps processing inside the US, EU, or APAC zone and, the page says, provides higher default quotas than geography-based deployment types.

It can still show latency variability at high volume. Provisioned Data Zone is the reserved-capacity version of the same zone. Regional Standard is the tighter geography, with more limited throughput.

### global-gets-features-first
- title: New models land on global deployments first
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Where do new model features show up first?

---

The deployment-types page says global deployments receive new models and features first, and that they offer the highest initial throughput limits and the broadest model availability.

That is why the recommendation is to start on Global Standard unless residency, reserved capacity, or batch pricing forces a different type.

### standard-geography-wording
- title: Standard processes inside the geography, not one datacenter
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types

Does a Standard deployment stay inside a single Azure region for every token?

---

The residency note says Standard and Regional Provisioned prompts and responses are processed within the customer-specified Azure geography and might be processed between regions inside that geography for operational purposes.

Do not describe Standard as a single-building pin. The customer choice is the geography. Global is any Azure region. Data Zone is the US, EU, or APAC zone.

### foundry-user-minimum-on-resource
- title: Developers and project identities both need Foundry User
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

What two Foundry User assignments does a new project need?

---

The RBAC article's minimum is Foundry User on the Foundry resource for the user principal, and Foundry User on the Foundry resource for the project's managed identity. If the creator can assign roles, the portal adds both.

Someone who only calls agents should get Foundry Agent Consumer instead. Foundry User is for people and identities that build and test, not for every downstream caller.

### reader-on-resource-for-developers
- title: Developers get Reader on the resource and User on the project
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why does the enterprise sample give developers two roles?

---

The sample assigns Foundry User on the project scope and Reader on the Foundry resource scope. That lets them build with pre-deployed models and existing connections without making them resource administrators.

Foundry User at the resource would be broader than that sample. The sample keeps resource administration with the IT admin and the managers.

### account-owner-assigns-user-to-self
- title: Account Owners must grant themselves Foundry User to build
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

A manager has Foundry Account Owner and cannot open the playground. Why?

---

The enterprise sample says managers deploy models, audit connections, and create shared connections, and they cannot build in projects until they assign Foundry User to themselves or to someone else.

Account Owner includes model management and excludes data-plane build rights on the permission matrix. The missing piece is Foundry User, not a second account.

### project-manager-assigns-only-user
- title: Project Manager can assign Foundry User and no other role
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Can a Foundry Project Manager grant Foundry Owner to a teammate?

---

No. The matrix says Foundry Project Manager can complete role assignments only for the Foundry User role. Foundry Owner and Foundry Account Owner can assign Foundry User, ACR, and monitoring roles. Azure Owner can assign any role.

A team lead can invite builders. They cannot promote someone to Foundry Owner. That assignment belongs to a principal who holds a broader role-assignment right.

### custom-role-data-action
- title: A custom role must list data actions separately
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why would a custom role that can read the account still fail to call an agent?

---

Control-plane permissions go in Actions. Data-plane permissions go in DataActions. The sample custom role includes Microsoft.CognitiveServices/accounts/AIServices/agents/* as a data action, plus read actions on the control plane.

Copying only the Actions block does not grant agent calls. The CLI accepts Name and DataActions at the top level. ARM wraps the same fields in properties and uses camel case, such as roleName.

### owner-scope-for-custom-roles
- title: Creating a custom role requires Owner
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Who can create a custom Foundry role?

---

The RBAC notes say you need the Owner role on the resource scope to create custom roles there. Contributor can deploy models and, at subscription scope, can view and purge deleted Foundry accounts. Contributor cannot assign roles.

If the built-in roles do not meet the requirement, the page says to create a custom role that allows precise control over actions and scopes. Contributor still cannot assign roles. Owner is the role that can create the custom role.

### agent-consumer-portal-limitation
- title: The portal can only assign Agent Consumer on the account
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Why is the portal the wrong place to grant least privilege on one agent?

---

The Azure portal currently supports assigning Foundry Agent Consumer only at the Foundry account scope. Account scope is wider than one project. The CLI can assign the role, ID eed3b665-ab3a-47b6-8f48-c9382fb1dad6, at the project or at the agent.

Project scope lets the caller hit every agent endpoint in the project. Agent scope hits one endpoint and still does not grant management rights. Use the CLI when the portal would over-grant.

### usages-read-action
- title: Quota read is Microsoft.CognitiveServices/locations/usages/read
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which action allows the quota page to load?

---

The RBAC article names Microsoft.CognitiveServices/locations/usages/read, granted by Cognitive Services Usages Reader or by another subscription role that includes it. The assignment has to be on the subscription.

A Foundry Owner assignment on the resource does not include that subscription action. If deployments cannot be validated because quota will not load, fix the subscription role first.

### automatic-user-role-exception
- title: Only an interactive portal create assigns Foundry User
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which create path assigns Foundry User automatically?

---

The RBAC notes say the assignment happens when the creating user can assign roles and the resource is deployed from the Azure portal or the Foundry portal. SDK and CLI deployments do not add that assignment.

Infrastructure-as-code pipelines must assign Foundry User to people and to the project identity themselves. Otherwise the resource exists and nobody can call the data plane.

### storage-reader-for-byo
- title: Bring-your-own blobs need Storage Blob Data Reader
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which identity do you add to a storage account that Foundry did not create?

---

The example in the RBAC notes is to add the Foundry account's managed identity to Storage Blob Data Reader on that storage account. A new Azure AI Search source needs its own role assignments for Foundry.

Foundry User on the cognitive account does not grant those data-plane roles on storage or search. Add them on the target resource.

### managed-compute-five-actions
- title: Managed compute has five control-plane operations
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which actions does a custom role need to manage managed compute?

---

The RBAC page lists read, write, and delete on Microsoft.CognitiveServices/accounts/managedComputeDeployments, plus Microsoft.CognitiveServices/managedComputeCapacities/read and Microsoft.CognitiveServices/locations/usages/read.

Foundry User includes the reads and not the write or delete. Inference is separate again. It needs Foundry User on the account, or the account key. A locations wildcard does not cover the capacities read.

### cognitive-services-contributor-for-gpu
- title: Deploying managed compute can use Cognitive Services Contributor
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Which role does the RBAC page recommend for operating managed compute deployments?

---

It says to assign Cognitive Services Contributor on the Foundry account to deploy and operate them, because that role has all five control-plane operations. Foundry Owner and Foundry Account Owner also have full CRUD.

That recommendation is specific to managed compute operations. The same page still says not to use Cognitive Services roles for ordinary Foundry scenarios. Read the section you are implementing. A viewer can use Cognitive Services User or Foundry User.

### project-manager-reads-gpu-quota
- title: Project Managers can see managed compute and cannot create it
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

Can the person who manages the project also create a managed compute deployment?

---

The recommended assignment for someone who manages a project but does not deploy models is Foundry Project Manager. That role can read managed compute deployments and quota, and it cannot create or delete them.

Put create and delete on Foundry Account Owner, Foundry Owner, or Cognitive Services Contributor. Do not widen the project manager to Owner just to read quota.

### delete-project-is-permanent
- title: Deleting a project cannot be undone
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Can you restore a Foundry project from the portal trash?

---

The create-project article says you cannot recover a project after it is deleted. The portal, the SDK, and the CLI all expose delete, and a show after the CLI delete returns not found.

Deleting the default project also changes which project is default. The next project created becomes the default, and the default is the only project with OpenAI batch, fine-tuning, and stored completions.

### speech-finetune-default-only
- title: Speech fine-tuning stays on the default project
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Can a second project fine-tune speech?

---

The feature table marks speech fine-tuning as available on the default project and not on other projects. Language fine-tuning is available on both. OpenAI batch, fine-tuning, and stored completions are default-only too.

Agents, evaluations, tracing, and content understanding are available on every project in that table. Put speech fine-tuning on the default project on purpose, not on whichever project a team created last.

### nondefault-openai-surface
- title: Other projects get a smaller OpenAI surface
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

What can the OpenAI SDK do on a project that is not the default?

---

The table limits other projects to Responses, Files, and Conversations. Batch, fine-tuning, and stored completions are marked only for the default project.

The Foundry SDK and API column is available on every project. If a sample uses an OpenAI batch API, run it against the default project or it is outside that table.

### security-group-instead-of-users
- title: Grant Foundry User to a security group
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

How do you give a whole team access without inviting each person?

---

The create-project article says to use a Microsoft Entra security group instead of individual addresses. The CLI sample sets assignee-principal-type to Group and passes the group's object ID, with the Foundry User role GUID, scoped to the project resource ID.

The caller still needs permission to assign roles, such as Owner on the project. The Python management SDK cannot make that assignment.

### home-page-key-is-optional
- title: Entra ID callers ignore the project API key
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Should every developer copy the API key from the project home page?

---

The page shows the project endpoint and an API key, and it says you do not need the key if you use Microsoft Entra ID.

Copy the endpoint. Leave the key for a prototype that is actually using key authentication. Production callers should be on Entra ID, where the key is unused and still a secret if it leaks.

### east-us-sample-is-not-a-requirement
- title: The create sample uses East US as an example
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Does a Foundry project have to be in East US?

---

No. The Python and CLI samples use eastus as the location they create. The article tells you to see the region-support page for supported regions, and the portal lets you select a location.

Pick the region that has the models and features you need. The sample location is an illustration, not a service restriction.

### system-assigned-on-project
- title: Projects are created with a system-assigned identity
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Does a new project get a managed identity?

---

The Python and CLI create samples set the project's identity type to SystemAssigned. The resource create also assigns a system identity, and project management fails without it.

That project identity is what you later grant Foundry User on the resource. It is not the per-agent identity a hosted agent receives at deploy time.

### allow-project-management-flag
- title: allowProjectManagement cannot be flipped later
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Which property enables projects on a Foundry account?

---

The create sample sets properties.allowProjectManagement to true, and the CLI exposes it as --allow-project-management. The article says you cannot change that setting after you create the resource.

Create the resource with project management enabled if you will need projects. A resource created without it cannot be switched on later by a portal toggle.

### custom-domain-in-use
- title: The custom domain is globally unique
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

The resource create fails with CustomDomainInUse. What is wrong?

---

The CLI notes say --custom-domain must be globally unique. If the name is taken, the command fails with CustomDomainInUse and you choose another name.

This is not a region quota error. The custom domain is also what token authentication requires, so the name you pick becomes part of the keyless setup.

### contributor-on-the-group
- title: Creating the resource needs Contributor or Owner
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Which role does the CLI article assume on the resource group?

---

The project article says the CLI steps need Contributor or Owner on the resource group, plus Azure CLI 2.80.0 or later.

Foundry User is not that role. Foundry User cannot create the account. The person who runs the create is an Azure resource administrator, and builders are granted Foundry User afterward.

### inheritance-get-is-effective
- title: A project GET shows inherited storage plus overrides
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

How do you see which storage account a project actually uses?

---

The article says a project inherits each agent-storage setting it does not set, and a GET returns the effective configuration, combining inherited account values with project overrides.

Changing the account default later does not update projects that already exist. Read the project if you need the live setting. Do not assume it matches the account blade.

### search-caller-role-not-required
- title: Capability settings do not need a search role on the caller
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Which roles does the caller need when setting agent capability stores?

---

The article says the caller needs Storage Blob Data Contributor on the storage account and Cosmos DB Operator on the Cosmos DB account. Azure AI Search does not require a caller role for that request.

Runtime access for the project managed identity is configured separately. A successful settings write does not mean the project identity can read the index at runtime.

### multiple-projects-for-locked-subscriptions
- title: Extra projects are the self-serve pattern
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Why create many projects on one resource in a locked-down subscription?

---

The article says multiple projects let teams collaborate and share security, deployments, and connected tools, which suits restricted subscriptions where developers need to explore inside a preconfigured environment.

The projects can still have their own access control. They do not get their own network or their own model deployments. Those stay shared from the parent.

### verify-provisioning-state
- title: A successful create returns provisioningState Succeeded
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

How do you confirm the CLI finished creating the resource and the project?

---

The article shows az cognitiveservices account show and az cognitiveservices account project show, querying properties.provisioningState. The expected value is Succeeded.

Any other state means you check permissions, region availability, and quotas. A managed-identity error on the project show means the resource was created without --assign-identity.

### portal-new-foundry-toggle
- title: Project steps assume the New Foundry toggle is on
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

Which portal mode do the create-project steps describe?

---

The article says to sign in to Microsoft Foundry with the New Foundry toggle on, and that the steps refer to Foundry (new). You then create a project from the project picker.

The classic portal is a different surface. Hub-based projects are not this flow. If the toggle is off, you are not following the new-project article.

### resource-group-per-project-tip
- title: A new resource group makes cleanup easier
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

What does the portal suggest when you are just starting?

---

The advanced options say that, especially when getting started, you should create a new resource group for the project so the project and its resources can be managed together.

The location you pick is the region where the project resources are hosted. The portal can also create the Foundry resource for you as part of creating the project.

### add-project-from-manage
- title: You add a project from Resource details
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

How do you add a second project to an existing Foundry resource in the portal?

---

The article says to open Manage, select Resource details, and select Add project. The CLI equivalent is az cognitiveservices account project create against the existing account.

That second project shares the parent's network and deployments. Confirm whether it needs to be the default before you put batch or fine-tuning work on it.

### role-assignment-verify
- title: List the role assignment after you grant access
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

How do you prove a teammate was granted Foundry User?

---

The CLI steps query the project resource ID, assign role 53ca6127-db72-4b80-b1b0-d745d6d5456d at that scope, and then list role assignments on the project for that role.

If the person still cannot sign in, the article says to check the assignment, the email or group ID, and that their account is in the same Entra tenant.

### delete-resource-deletes-projects
- title: Deleting the resource deletes its projects
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects

What does the Python sample do before it deletes the Foundry account?

---

It lists projects, deletes each one, and then deletes the account. The article also shows a single-project delete.

There is no recover step after either delete. Delete the projects you mean to delete, not the account, if other projects must keep running.

### foundry-tools-brand
- title: Foundry Tools is the new name for Azure AI Services
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

An architecture diagram still says Azure AI Services. What is the current brand?

---

The evolution table on the Foundry overview maps Azure AI Services to Foundry Tools, and Azure AI Studio or Azure AI Foundry to Microsoft Foundry.

Use the current brand and mention the old one so both of you mean the same product. The resource provider underneath Foundry remains Microsoft.CognitiveServices.

### resource-model-collapsed
- title: Hubs and separate OpenAI accounts became one Foundry resource
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What resource model replaced the hub plus Azure OpenAI plus Azure AI Services?

---

The evolution table maps that previous combination to a single Foundry resource with projects.

That is why new projects hang off one cognitive account instead of a hub. Hub-based projects that already exist stay in the classic portal.

### terminology-items
- title: Messages are now items
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What is the current word for a message inside a conversation?

---

The evolution table maps Messages to Items, Threads to Conversations, Runs to Responses, and Assistants to Agent Versions.

Use the current words in new designs. If a sample still says thread and run, it is using the previous terminology.

### v1-routes
- title: Stable calls use the /openai/v1/ route
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What replaced monthly api-version query parameters?

---

The evolution table maps monthly api-version parameters to v1 stable routes under /openai/v1/.

New clients should target that stable route. A sample that still pins a monthly api-version is on the previous versioning scheme.

### governance-list
- title: Entra, RBAC, filters, network, and Policy
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Which governance controls does the Foundry overview list?

---

It lists Microsoft Entra identity, role-based access control, content filters, network isolation, and Azure Policy, and it points at the Foundry control plane.

Those are platform controls. A sentence in a system prompt is not a substitute for the content filter, and a key is not a substitute for RBAC.

### recommended-path
- title: The documented path starts with a model call
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What sequence does Foundry recommend for a new developer?

---

Make a first model call, set up the CLI and SDK, choose a model from the catalog, build a prompt agent or go straight to a hosted agent, then add tools, retrieval, and memory. Memory is marked preview on that list.

The toolbox overview is the recommended way to add tools. You do not have to start with a container.

### coding-agents-via-mcp
- title: Coding agents drive Foundry through a skill and MCP
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

How can GitHub Copilot or Claude Code operate Foundry?

---

The surfaces table includes coding agents, with GitHub Copilot and Claude Code as examples, using the Foundry Skill and an MCP server.

That is a developer surface on top of the same platform. It does not replace the project, the role assignment, or the deployment.

### azd-for-hosted-agents
- title: The Azure Developer CLI targets hosted agents
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

When does the overview point you at the Azure Developer CLI?

---

It lists azd for scaffolding, running, testing, and deploying hosted-agent projects from the command line.

Prompt agents can be built in the portal or with the SDK without that CLI. Pick azd when the thing you are shipping is a hosted agent project.

### java-sdk-is-supported
- title: Foundry SDKs include Java
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Which languages does the Foundry overview name for application SDKs?

---

The surfaces table lists SDKs for Python, C#, JavaScript, and Java.

The portal remains the no-code surface. The language list is for building applications, not a claim that every preview feature has a helper in every language.

### most-projects-center-on-an-agent
- title: Most Foundry projects are built around an agent
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What does the overview say most Foundry projects center on?

---

An agent: a model paired with instructions and tools that can reason over a request and take action. The main decision is how much of the runtime you want to customize, from a prompt agent to a hosted agent.

A single model call is the explicit alternative when you have no tools and no orchestration. Do not create an agent for that case out of habit.

### voice-greeting-optional
- title: A voice agent can start with a greeting
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What do you configure on a voice-based prompt agent besides the model?

---

The overview lists instructions, audio settings, an optional greeting, and tools, then a connection through Voice Live.

Foundry manages the lifecycle and the voice orchestration. You configure the agent. You do not host the speech pipeline for that managed voice agent.

### preview-status-pointer
- title: Preview status lives on the GA overview
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Where do you check whether a Foundry capability is still in preview?

---

The product overview says some capabilities are in preview and points you to the general availability overview for current status.

Do not infer GA from a marketing sentence. The same page marks built-in monitoring dashboards and memory as preview, and it sends you to the general availability overview for the rest.

### unified-rbac-networking-policy
- title: One namespace for RBAC, networking, and policy
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What management problem is the single resource provider meant to solve?

---

The overview says Foundry streamlines management through unified RBAC, networking, and policies under one Azure resource provider namespace.

That is the reason the architecture can say OpenAI policies keep working after an upgrade. The provider did not change when the product name did.

### tools-memory-retrieval
- title: Tools, memory, and retrieval extend an agent
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

How does the overview say you extend an agent past the model?

---

With built-in tools, memory, and retrieval, using a Foundry toolbox. The recommended path marks memory as preview and points at the toolbox overview.

The toolbox is the shared, versioned place for tools. Adding a tool inside one agent definition does not give you that reuse.

### from-declarative-to-code
- title: You can start declarative and move to code
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Do you have to choose hosted agents on day one?

---

No. The overview says you can start declarative and move to code as your needs grow. Prompt agents have the least to manage. Hosted agents have the most control.

The comparison article for hosted agents is where that decision is spelled out. A prototype should not begin as a container unless you already need custom code.

### enterprise-setup-is-customizable
- title: Enterprise setup is part of the platform, not an add-on
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What enterprise capabilities does the overview claim are built in?

---

It names tracing, monitoring, evaluations, and customizable enterprise setup, plus Entra identity, RBAC, content filters, network isolation, and Azure Policy.

Some of those surfaces are preview, which the same page tells you to check. The claim is that they belong to the platform, not that every screen is GA.

### preserve-state-on-upgrade
- title: Upgrade preserves existing state
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

What state survives an Azure OpenAI to Foundry upgrade?

---

The overview says the upgrade preserves the endpoint, the API keys, and the existing state.

Plan the upgrade as a resource change that keeps those three. Do not design a migration that assumes every key and every stored artifact must be recreated, unless a later page for your specific feature says otherwise.

### classic-portal-still-exists
- title: The classic portal remains for hub projects
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Is the classic portal gone?

---

No. The overview says hub-based projects are accessible in the Foundry (classic) portal, and that new investments focus on Foundry projects in the new portal.

Use the new portal for new Foundry projects. Use the classic portal when the workload is still a hub-based project.

### agents-in-portal-or-sdk
- title: Prompt agents can be built in the portal or the SDK
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

Do you have to use the SDK to create a prompt agent?

---

No. The overview says you build declarative prompt agents and managed voice-based prompt agents in the portal or the SDK, and you deploy hosted agents when the agent is your code.

The portal is enough for a prompt agent. The SDK is how you put that agent in a pipeline. Hosted agents are the path that brings a container.

### one-project-endpoint-client
- title: OpenAI() talks to one project endpoint
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

How many endpoints does the current client model use?

---

The evolution table contrasts the old packages against five or more endpoints with a unified project client, azure-ai-projects 2.x, plus OpenAI() against one project endpoint.

Point the OpenAI client at the project endpoint. Do not keep a separate host per retired package if you have moved to that client.
