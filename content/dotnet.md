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
