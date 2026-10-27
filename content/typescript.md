# TypeScript

### structural-typing
- title: TypeScript types are structural
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html

Two interfaces both have `id: string` and `name: string`. Neither extends the other. Can you pass one where the other is required? What is the exception people hit with classes?

---

TypeScript uses structural typing for objects. If the required properties are present and compatible, the value is assignable. The type's name does not matter. A function that accepts `{ id: string }` accepts any object with at least that property; extra properties are allowed when the object is already stored in a variable.

Fresh object literals are checked for excess properties, so a literal with a typo key fails at the call site even though a variable of a wider type would pass. Classes are still structural unless a private or protected member makes the type nominal: only instances of that class are assignable then, because the private member is part of the type.

### unknown-versus-any
- title: unknown makes you narrow, any turns checking off
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

A JSON payload arrives as `unknown`. Why is that a better boundary type than `any`, and what must you do before reading a property?

---

`any` disables type checking for that value and for whatever you pass it into. `unknown` accepts any value but lets you do almost nothing with it until you narrow. You cannot read a property, call it, or pass it to a function that expects `string` without a check.

Narrow with `typeof`, `Array.isArray`, an `instanceof` test, or a custom type predicate `function isUser(value: unknown): value is User`. Use `unknown` at boundaries: `JSON.parse`, `catch (err: unknown)`, and untyped library results. Use `any` only at a last-resort escape hatch, and keep it local.

### interface-versus-type
- title: interface and type alias
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

When can you use either an interface or a type alias, and which one can describe a union or add a call signature later through declaration merging?

---

For an object shape, `interface User` and `type User =` are both fine. Interfaces support declaration merging: two `interface User` blocks in the same scope combine. Type aliases do not merge. That merging is why library authors sometimes prefer an interface for a public object type that downstream code may augment.

A type alias can name a union, intersection, tuple, primitive, or mapped type directly: `type Id = string | number`. An interface cannot be a union. Choose an interface for an extendable object contract. Choose a type alias when the type is a union or a composition. Consistency in a codebase matters more than a blanket ban on either one.

### discriminated-unions
- title: Discriminated unions make impossible states unrepresentable
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

A request is either `{ status: "loading" }`, `{ status: "ok"; data: User }`, or `{ status: "error"; message: string }`. How do you make `data` safe to read, and what should the `default` branch do?

---

Use a shared literal discriminant, here `status`. After `if (result.status === "ok")`, TypeScript narrows `result` to the success member and `data` is in scope. In the `"error"` branch, `message` is in scope and `data` is not.

In a `switch`, a `never` check in `default` catches a new variant you forgot to handle:

```ts
default: {
  const exhaustive: never = result;
  return exhaustive;
}
```

This is the usual way to model loading, success, and failure without optional fields that can appear in the wrong state. Keep the discriminant a string literal union, not a boolean soup.

### strict-null
- title: strictNullChecks changes what null means
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strictNullChecks.html

With `strictNullChecks` off, why does a function returning `User | null` still let you read `.name`? What do you turn on in practice?

---

Without `strictNullChecks`, `null` and `undefined` are assignable to every type, so the compiler will not force a check before `.name`. The flag puts `null` and `undefined` in the value's type only when you write them. `User | null` then requires a guard.

Enable the `strict` family rather than this flag alone. `strict` includes `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and the other safety flags. A non-null assertion `user!.name` silences the error and throws at runtime if you were wrong. Prefer a guard or early return.

### satisfies
- title: satisfies checks a value without widening the variable
- version: 4.9
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html

You want an object to be checked against a `Record<string, Route>` constraint, but you still want `routes.home` to keep its literal path. Why does a type annotation lose that, and what does `satisfies` do?

---

A annotation `const routes: Record<string, Route> = { home: { path: "/" as const } }` checks the value, then types the variable as the wide annotation. Specific keys and literal values are no longer visible on `routes`.

`satisfies`, added in TypeScript 4.9, checks assignability and leaves the inferred type in place:

```ts
const routes = {
  home: { path: "/" },
} satisfies Record<string, Route>;
```

`routes.home.path` stays narrow, and a missing required field is still an error. Use it for config objects, theme maps, and route tables. It does not replace a return-type annotation on an exported function when callers need a stable contract.

### const-type-parameters
- title: const type parameters infer literals
- version: 5.0
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html

A helper `function routeNames<T extends readonly string[]>(names: T) { return names; }` infers `string[]` from `routeNames(["home", "edit"])`. How do you infer the tuple of literals without making every caller write `as const`?

---

TypeScript 5.0 adds `const` type parameters. Write `function routeNames<const T extends readonly string[]>(names: T)`. The argument is inferred as if the caller had written `as const`, so the result is the tuple `readonly ["home", "edit"]` rather than `string[]`.

Callers can still pass a wider `string[]`; the constraint decides what is legal. Use this on small builders where the literal values are the API, such as route names, event names, and column keys. Do not put `const` on a type parameter that must stay wide, or callers will find their mutable arrays inferred as readonly tuples.

### using-keyword
- title: using disposes at the end of the scope
- version: 5.2
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html

What does `using` bind, when does disposal run, and which method does a disposable object implement? How is `await using` different?

---

TypeScript 5.2 adds `using` and `await using` for the Explicit Resource Management proposal. `using file = openFile()` binds `file` like `const`. At the end of the scope, including when the scope throws, TypeScript emits a call to the disposable's `Symbol.dispose` method.

`await using` is for objects whose cleanup returns a thenable. Those objects implement `Symbol.asyncDispose`, and the function that declares them must be `async`. Disposal runs in reverse order of declaration. This is the typed replacement for a `try/finally` that only exists to close a handle. The runtime method still has to exist; the keyword does not invent cleanup for a plain object.
