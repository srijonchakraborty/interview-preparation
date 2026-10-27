# .NET

### support-window
- title: LTS versus STS, and what is supported now
- version: Core
- level: beginner
- status: verified
- source: https://devblogs.microsoft.com/dotnet/announcing-dotnet-10/

Which .NET releases should a new production service target, and when do .NET 8 and .NET 10 leave support?

---

Even-numbered releases are long-term support for three years. Odd-numbered releases are standard-term support for 24 months. .NET 10 shipped on 11 November 2025 as the current LTS release and is supported until 10 November 2028.

.NET 8 (LTS) and .NET 9 (STS) both reach end of support on 10 November 2026. After that date they do not receive patches. A new service should start on .NET 10. Knowing .NET 6 APIs is still useful in interviews, but .NET 6 has been out of support since November 2024, so do not recommend it for production.

### dependency-injection
- title: Transient, scoped, and singleton
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection

What is the lifetime of a service registered with `AddScoped`, and what is a captive dependency?

---

The Microsoft dependency-injection container has three lifetimes. **Transient** creates a new instance every time the service is requested. **Scoped** creates one instance per scope. In ASP.NET Core, a scope is a request, so scoped services are shared inside that request and disposed at the end of it. **Singleton** creates one instance for the container.

A captive dependency is a longer-lived service that takes a shorter-lived service. The classic bug is a singleton constructor that accepts a scoped `DbContext`: the singleton captures the first scope's instance and keeps it after that scope is disposed. Fix it by narrowing the singleton, or by injecting `IServiceScopeFactory` and creating a scope at the point of use. Do not resolve scoped services from the root provider.

### ienumerable-versus-iqueryable
- title: IEnumerable executes locally, IQueryable builds a query
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/api/system.linq.iqueryable

You pass an EF Core `DbSet` through a helper that returns `IEnumerable<Order>` and then add `.Where(o => o.IsOpen)`. Where does that filter run?

---

`IQueryable<T>` holds an expression tree. Until you materialize it (`ToList`, `foreach`, `First`, `Count`), EF Core can translate further operators into SQL. The return type is what matters, not the runtime object alone. If the helper's static type is `IEnumerable<Order>`, later LINQ operators bind to `Enumerable` and run in memory after the rows are pulled.

`AsEnumerable()` is the explicit switch. Call it only after the selective `Where`, `Select`, and paging so the database does the filtering. A predicate that EF cannot translate throws, or worse, silently runs locally if you switched to `IEnumerable` first. In an interview, say where the SQL stops.

### nullable-references
- title: Nullable reference types are a compiler feature
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references

With `<Nullable>enable</Nullable>`, what is the difference between `string` and `string?` at runtime? What does `null!` do?

---

Nullable reference types are annotations. The CLR type is still `System.String`. `string` means the compiler should treat the value as non-null. `string?` means null is expected and must be handled before a member access. The compiler warns; it does not insert a null check for you, and reflection will not see a different runtime type.

`null!` is the null-forgiving operator. It suppresses the warning at that expression and does not change the value. Use it when you know a value is initialized by a framework, not as a habit. Flow analysis understands assignments and null checks. It does not understand an arbitrary helper unless you annotate that helper with attributes such as `NotNullWhen`.

### records
- title: Records add value equality and with-expressions
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records

How does a `record class` differ from a normal class, and when is a `record struct` the better choice?

---

A `record class` is still a reference type. The compiler adds value-based equality, `GetHashCode`, and a deconstructor for the primary constructor parameters. `with` copies the record and changes the properties you name. `init` setters make those properties immutable after construction. A mutable property inside the record, such as a `List<T>`, is still shared with the copy.

A normal class uses reference equality unless you override it. Use a record for a DTO or a message where two instances with the same data should compare equal. Use a `record struct` when you want value equality without a heap object. Do not claim records are immutable by default if their members are mutable reference types.

### minimal-apis
- title: Minimal APIs are still the ASP.NET Core pipeline
- version: .NET 6
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis

What did minimal APIs add in ASP.NET Core 6, and which pipeline pieces do you still own?

---

Minimal APIs let you map routes on `WebApplication` without a controller class:

```csharp
app.MapGet("/orders/{id}", (int id, OrderService orders) => orders.Get(id));
```

Parameters bind from the route, query, headers, or body, and services inject from DI. Filters, status codes, and `TypedResults` grew in later versions, but the model started in .NET 6.

You still build the same host. Middleware order matters: authentication, authorization, and exception handling run as middleware you register. There is no hidden controller pipeline. Choose minimal APIs for a small HTTP surface and controllers or endpoint groups when a large API needs structure. Both are supported production styles.

### span
- title: Span is a ref struct and cannot be boxed
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/api/system.span-1

Why can `Span<T>` slice a buffer without allocating, and why can't you store one in a class field or across an `await`?

---

`Span<T>` and `ReadOnlySpan<T>` are `ref struct` types. They can point at stack memory, an array, or a substring interior without copying those bytes. Because they may point at the stack, the compiler refuses to box them, put them in a class or array field, or capture them in a way that would let them outlive that stack.

An `async` method turns locals into fields of a state machine, so a `Span<T>` cannot live across an `await`. Use `Memory<T>` or `ReadOnlyMemory<T>` when the slice must be stored or awaited. C# 14 allows some `ref struct` interface implementations; that does not make `Span<T>` boxable. If an API needs a heap object, it was the wrong type.

### extension-members
- title: C# 14 extension members
- version: .NET 10
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14

C# has had extension methods for years. What did C# 14 add, and where do those members have to live?

---

C# 14 ships with .NET 10 and adds extension members beyond methods. An `extension` block in a non-generic static class can add instance or static members, including properties, to a type you do not own:

```csharp
static class ListExtensions
{
    extension(List<int> source)
    {
        public int Sum => source.Aggregate(0, (a, b) => a + b);
    }
}
```

Existing extension methods keep working. The new block is how you add an extension property or a static extension without pretending the member is declared on the original type. The receiver is only in scope inside the block. This is a compile-time rewrite, same as extension methods; it does not change the target type's runtime layout.

### field-keyword
- title: The field keyword in C# 14
- version: .NET 10
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14

How do you trim a string in a property setter without declaring your own backing field?

---

C# 14 lets an accessor refer to the compiler-generated backing field with the contextual keyword `field`:

```csharp
public string Name
{
    get => field;
    set => field = value?.Trim() ?? string.Empty;
}
```

You no longer need a hand-written `_name` field just to add a guard. `field` is in scope only inside that property's accessors. If the type already has a member named `field`, the keyword can be shadowed; use `@field` or rename so the contextual keyword is unambiguous. This is separate from primary constructors and from `required` properties, which already existed.

### value-type-assignment-copy
- title: Assigning a struct copies its value
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/

You assign one `Point` struct variable to another, then change the second variable. What happens to the first one?

---

Assigning a value type copies its value. The two `Point` variables are independent after the assignment, so changing the second one does not change the first.

Structs hold their own data. Each variable has its own copy, which is the behavior to defend in an interview.
### reference-assignment-shares-object
- title: Assigning a class reference
- version: Core
- level: beginner
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/

Two variables are assigned the same `List<int>`, and one variable adds an item. Why does the other variable see it?

---

Classes are reference types. Assigning the list variable copies a reference, so both variables refer to the same list object and a mutation through either reference is visible through the other.

Reassigning one variable is different: it changes that variable’s reference, not the object previously shared by both variables.

### boxing-to-object
- title: Boxing a value type
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing

What occurs when `int count` is assigned to an `object` variable?

---

The assignment boxes the value: the runtime creates an object that contains a copy of the `int` value. Boxing is an implicit conversion from a value type to `object` or to an implemented interface.

That allocation is why repeatedly storing value types in nongeneric object-based APIs can add avoidable overhead.

### unboxing-exact-type
- title: Unboxing requires a compatible value type
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing

An `object` contains a boxed `int`. Can you unbox it directly as a `short`?

---

No. Unboxing checks that the object contains a boxed value of the requested value type, so a boxed `int` must first be unboxed as `int`.

An explicit numeric conversion can follow after unboxing. Treating unboxing itself as numeric conversion leads to an `InvalidCastException`.

### gc-generation-zero
- title: Generation 0 collection
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals

Why does the garbage collector put a newly allocated short-lived object in generation 0?

---

New managed objects start in generation 0. The generational collector is based on the observation that many objects have short lifetimes, so collecting young objects can be efficient.

If an object survives a collection, it can be promoted to an older generation. Generation is not an ownership or disposal mechanism.

### gc-reachability
- title: Reachability and collection
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals

You set a local reference to `null`. Does that immediately destroy the object?

---

No. Garbage collection reclaims managed objects that are no longer reachable; setting one reference to `null` only removes that reference.

The runtime chooses when to collect. Code that needs timely release of a file handle or socket must use disposal instead of waiting for collection.

### await-does-not-create-thread
- title: Awaiting I/O without a new thread
- version: Core
- level: beginner
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/

An HTTP call is awaited in an ASP.NET Core request. Does `await` itself create a worker thread to wait for it?

---

No. `await` suspends the asynchronous method until the awaited operation completes; it does not by itself create a thread.

This distinction matters when diagnosing thread-pool starvation: asynchronous I/O is not made scalable merely by wrapping work in `Task.Run`.

### async-cpu-bound-work
- title: CPU-bound work in an async method
- version: Core
- level: intermediate
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/

Your async endpoint performs a long CPU calculation before its first `await`. What is it doing during that calculation?

---

The calculation runs synchronously on the thread executing the method until the code reaches an incomplete awaited operation. Marking a method `async` does not make CPU work asynchronous.

For CPU-bound work, decide deliberately whether to run it on another thread or move it out of the request path; do not confuse that choice with asynchronous I/O.

### task-composition
- title: Task represents an operation
- version: Core
- level: beginner
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/

Why should a method return `Task` instead of blocking until its operation finishes?

---

A `Task` represents asynchronous work that callers can await and compose with other tasks. Returning it lets the caller decide when and how to await completion.

Blocking with `.Result` or `.Wait()` consumes a thread while waiting and changes the asynchronous flow into a synchronous wait.

### valuetask-single-consumption
- title: ValueTask consumption rules
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask

Why is it risky to await the same `ValueTask` twice?

---

A `ValueTask` can wrap a source whose result may be consumed only once. Its documentation warns that callers should await it directly rather than assuming it has the same reuse behavior as `Task`.

Use `Task` as the default return type. Choose `ValueTask` only when its supported consumption pattern and allocation trade-off are justified.

### linq-query-runs-on-enumeration
- title: A deferred LINQ query
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/standard/linq/deferred-execution-lazy-evaluation

You create `var adults = people.Where(p => p.Age >= 18);` and then add a person before the `foreach`. Can the new person appear?

---

Many LINQ operators use deferred execution, so the query is evaluated when it is enumerated rather than when it is declared. The later `foreach` can therefore see the current source data.

That behavior is useful for composition but surprising when the source changes or when enumeration performs expensive work more than once.

### linq-materialize-snapshot
- title: Materializing a LINQ result
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios

How do you keep a LINQ result from being reevaluated each time it is enumerated?

---

Materialize the sequence, for example with `ToList`, to evaluate it and store the resulting elements. Enumerating that list does not rerun the original deferred query.

Materialization trades laziness for a snapshot and memory use. It is appropriate when repeated evaluation or changing source data would be wrong.

### transient-service-instances
- title: Transient service lifetime
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/service-lifetimes

Two constructors request the same service registered with `AddTransient`. Should they receive the same instance?

---

No. A transient service is created each time it is requested from the service container. Register it with `AddTransient`.

In apps that process requests, the container disposes those instances at the end of the request. That lifetime allocates a new instance on every resolve.
### scoped-service-per-request
- title: Scoped service lifetime
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/service-lifetimes

Two components handle the same ASP.NET Core request and receive a scoped service. What lifetime relationship should they expect?

---

A scoped service is created once per scope. In ASP.NET Core, a scope is created for each request, so components in that request receive the same scoped instance.

The instance is disposed when its scope ends. It must not be retained by an object that lives longer than that scope.

### singleton-service-lifetime
- title: Singleton service lifetime
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/service-lifetimes

A cache is registered as a singleton. What must its implementation be prepared for?

---

A singleton is created once for the service container and is reused for the application lifetime. The same instance can be used by many requests.

Singleton state therefore needs appropriate thread-safety. It also cannot safely depend directly on a scoped service.

### captive-scoped-dependency
- title: A singleton captures a scoped service
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/service-lifetimes

A singleton service takes a scoped `DbContext` in its constructor. What is wrong, and what do you do instead?

---

The singleton outlives the scoped `DbContext`, creating a captive dependency. A longer-lived service must not capture a shorter-lived service.

Make the dependent service scoped, or create a scope at the point of use through `IServiceScopeFactory`. This preserves the scoped object’s intended lifetime.

### middleware-short-circuit
- title: Middleware that ends the pipeline
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/

A middleware writes a response and never calls its `next` delegate. Which later middleware runs?

---

It short-circuits the request pipeline. Middleware registered after it does not run for that request.

Short-circuiting is useful for terminal handlers and cached responses, but accidental short-circuiting can prevent authentication, endpoints, or error handling from running.

### middleware-registration-order
- title: Middleware order is execution order
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/

Why does moving exception handling after an endpoint-producing middleware change what errors it can handle?

---

Middleware runs in the order it is registered on the way into the pipeline. A component can only wrap work that occurs later in that order.

Place cross-cutting handling before the components it should protect. Pipeline order is executable behavior, not just organization.

### httpclient-reuse
- title: Reusing HttpClient
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines

Why is constructing and disposing an `HttpClient` for every outgoing request a production problem?

---

Each `HttpClient` instance manages its own connection pool. Repeatedly creating and disposing clients creates unnecessary connection churn and can exhaust available ports under high request rates.

Reuse a client for multiple requests or use `IHttpClientFactory`. The important resource is the underlying handler and connection pool, not only the managed client object.

### httpclient-dns-lifetime
- title: HttpClient and DNS changes
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines

A long-lived `HttpClient` keeps sending requests to an old server address after DNS changes. Which setting addresses that?

---

Set `SocketsHttpHandler.PooledConnectionLifetime` so pooled connections are replaced after the chosen lifetime and a later connection can resolve the host again.

`HttpClient` does not independently honor DNS time-to-live values. Reuse must be paired with an intentional connection lifetime when addresses can change.

### using-disposes-resource
- title: The using statement
- version: Core
- level: beginner
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose

What guarantee does a `using` statement give for a stream that implements `IDisposable`?

---

A `using` statement ensures that `Dispose` is called when control leaves the associated scope, including when an exception leaves it.

That deterministic cleanup is for resources such as handles and connections. Garbage collection alone does not provide the same timing guarantee.

### dispose-owned-resource
- title: Disposing owned resources
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose

Your class creates a `FileStream` and keeps it in a field. What should its `Dispose` implementation do?

---

If a class creates an `IDisposable` and stores it in a field, that class owns the instance and should dispose it from its own `Dispose` method. The `FileStream` is that kind of owned resource.

`Dispose` should be idempotent: calling it again must not throw, and later calls should do nothing.
### record-with-expression
- title: Record with-expression copies first
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records

You write `var revised = original with { Status = "Paid" };`. Does this modify `original`?

---

No. A `with` expression creates a new record instance by copying the original and applying the specified member changes to that copy.

The copy is nondestructive mutation, not an in-place update. It is especially useful when a value-like data model needs a revised version.

### record-shallow-copy
- title: Record copies are shallow
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records

A record contains a mutable array, and you make a `with` copy. Are the two arrays independent?

---

No. A `with` expression copies the record's members. It does not clone objects those members refer to, so both records can share the same array.

A shared mutable array is still shared after the copy. Record immutability does not deep-clone the objects inside the record.
### nullable-annotations-compile-time
- title: Nullable annotations do not change the CLR type
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/null-safety/nullable-reference-types

With nullable reference types enabled, what runtime type difference exists between `string` and `string?`?

---

There is no different runtime reference type. Nullable reference types are compiler analysis and annotations that warn about possible null dereferences.

The annotations improve contracts in source code, but they do not insert a runtime check or prevent a null value at runtime.

### null-forgiving-operator
- title: The null-forgiving operator
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/null-forgiving

What does the `!` in `customer!.Name` do if `customer` is actually null?

---

In a nullable annotation context, the postfix `!` operator suppresses the compiler's nullable warnings for that expression.

It is a warning suppression. The page does not describe it as a runtime conversion or a null check.
### span-class-field
- title: Span cannot be a class field
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/

Why does the compiler reject a `Span<byte>` field in an ordinary class?

---

`Span<T>` has to be allocated on the stack. A field in a class cannot be of type `Span<byte>`, and a span cannot be used in an asynchronous operation.

Those limits keep a span from outliving stack memory it may point at. They are lifetime rules, not a claim that every span is faster.
### memory-across-await
- title: Memory can cross an await
- version: Core
- level: experienced
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/

An API must retain a buffer slice across an `await`. Why should it use `Memory<byte>` rather than `Span<byte>`?

---

`Memory<T>` is designed to be stored and used across asynchronous boundaries, while `Span<T>` has ref-struct lifetime restrictions.

Use a span for synchronous, short-lived access to memory. Use memory when the slice must survive after the current synchronous frame.

### switch-expression-first-match
- title: Switch expression arm order
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression

In a switch expression, a broad discard arm appears before a more specific arm. Can the specific arm ever run?

---

No. Switch expression arms are evaluated in text order. A discard matches every remaining value, so a later arm cannot be chosen.

The compiler reports an error when a lower arm cannot be chosen because a higher arm already matches all of its values. Put specific patterns before a discard.
### switch-expression-nonexhaustive
- title: A nonexhaustive switch expression
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression

What happens if a switch expression receives a value that matches none of its arms?

---

If no pattern matches, modern .NET throws `System.Runtime.CompilerServices.SwitchExpressionException`. The compiler also warns when it cannot prove that every input is covered.

An exhaustive switch makes a new case a compile-time decision instead of a runtime miss.
### event-publisher-control
- title: Events restrict who can raise them
- version: Core
- level: intermediate
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/events-overview

Why expose an event instead of a public delegate field for order notifications?

---

An event lets outside code subscribe and unsubscribe, but only the declaring type can raise it. This preserves the publisher’s control over its notification.

A public delegate can be invoked or replaced by other code. Events express the intended publisher-subscriber boundary.

### event-unsubscribe
- title: Event subscriptions keep references
- version: Core
- level: experienced
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/csharp/events-overview

A short-lived view subscribes to a long-lived publisher and is never unsubscribed. Why can that be a leak?

---

Subscribing couples the event source to the event sink. The sink should unsubscribe when it is no longer interested in the event.

Leaving the subscription in place keeps that coupling after the view is gone, so a long-lived publisher still refers to a short-lived subscriber.
### configuration-last-provider-wins
- title: Configuration provider precedence
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/configuration

The same key is in `appsettings.json` and an environment variable. Which value does the application use?

---

Configuration providers are added in order, and a later provider can override a value supplied by an earlier provider. The configured provider order determines the effective value.

This makes environment variables useful for deployment-specific overrides, but it also means an unexpected later provider can silently change a setting.

### configuration-hierarchical-keys
- title: Configuration hierarchy
- version: Core
- level: beginner
- status: unverified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/configuration

How can a configuration provider represent a nested setting such as `Logging:LogLevel:Default`?

---

The configuration system represents settings as key-value pairs and supports hierarchical keys separated by `:`. Providers map their own formats into that common view.

Read configuration through `IConfiguration` or bind it to options rather than coupling application code to one particular provider’s file format.

### logging-level-filter
- title: Logging levels filter events
- version: Core
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/logging/overview

Why should a high-volume diagnostic message be logged at `Debug` instead of `Error`?

---

Log levels classify event severity, and logging configuration can filter events by level. `Debug` is intended for information useful during development and troubleshooting, while `Error` indicates a failure.

Correct levels keep production logs actionable. Calling every message an error makes real failures harder to identify.

### logging-message-template
- title: Structured logging templates
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/dotnet/core/extensions/logging/overview

Why use `logger.LogInformation("Processed {Count} orders", count)` rather than interpolate `count` into the message?

---

The logging API takes a message template with a named placeholder, such as `{Count}`, and a separate argument for the value. The provider keeps that name and value as structured data along with the rendered message.

Structured values can be filtered later. Building the sentence with interpolation first discards that structure.
### ef-tracked-entity-save
- title: Saving a tracked entity
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/ef/core/change-tracking/

You query an entity with a `DbContext`, change a property, and call `SaveChanges`. Why does EF Core issue an update without `Update`?

---

The context tracks entities returned by tracking queries and detects changes to their properties. `SaveChanges` persists those detected changes.

This is convenient within a unit of work. It also means the context should have a bounded lifetime rather than accumulate unrelated tracked entities.

### ef-no-tracking-read
- title: Read-only EF Core query
- version: Core
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/ef/core/querying/tracking

You display products without editing them. Why might `AsNoTracking()` be appropriate?

---

No-tracking queries return entities that are not tracked by the context. This avoids change-tracking work when the result is only read.

Do not expect later property edits on those returned objects to be saved automatically; attach or update them deliberately if that is required.

### minimal-api-route-binding
- title: Minimal API route parameter binding
- version: .NET 6
- level: beginner
- status: verified
- source: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/parameter-binding

For `app.MapGet("/orders/{id}", (int id) => ...)`, where does the `id` parameter come from?

---

The route template supplies the `id` value, and minimal API parameter binding binds it to the handler parameter when the request matches the endpoint.

Binding failures should be considered part of the endpoint contract. Choose parameter names and types that make the route input clear.

### minimal-api-service-binding
- title: Minimal API service parameter binding
- version: .NET 6
- level: intermediate
- status: verified
- source: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/parameter-binding

A minimal API handler takes an application service as a parameter. How does the framework supply it?

---

Parameter binding can take a service from dependency injection. `[FromServices]` names that source explicitly, and the handler receives the registered service when the endpoint runs.

Keep the parameter list to request data plus the services that handler needs. A long list is a sign that the work belongs in a service.
