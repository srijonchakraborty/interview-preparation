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

### string-number-boolean
- title: The basic primitive types
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

Which primitive types do `string`, `number`, and `boolean` describe in TypeScript?

---

`string`, `number`, and `boolean` are TypeScript's names for the corresponding JavaScript primitive types. A `number` includes integers and floating-point values.

Use lowercase type names. `String`, `Number`, and `Boolean` are object wrapper types and are not the usual annotation for primitive values.

### array-type
- title: Array element types
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

How do you annotate an array of strings, and what does the type constrain?

---

Write `string[]` or `Array<string>` for an array whose elements are strings. The two forms describe the same array element type.

The element type is checked when values are read or written. It does not mean an array has a fixed length; use a tuple when positions have distinct types.

### tuple-type
- title: Tuples describe positions
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

When should you use a tuple instead of an ordinary array type?

---

A tuple type is an array type with a known number of elements whose types are known at particular positions, such as `[string, number]`. Indexing a known position gives that position's type.

An ordinary `string[]` says every element is a string but says nothing about length or position. Do not model a record-like object as a positional tuple when names would be clearer.

### readonly-array
- title: Readonly arrays prevent mutation
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

What does `readonly string[]` prevent, and can it be passed to a function that expects `string[]`?

---

`readonly string[]` permits reading array elements but prevents mutating methods such as `push`. `ReadonlyArray<string>` is the longer spelling.

A readonly array is not assignable to a mutable array parameter because that parameter could mutate it. Design a function to accept `readonly T[]` when it only reads its input.

### literal-types
- title: Literal types restrict values
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What is a string literal type, and why is it useful with a union?

---

A string literal type represents one exact string, for example `"left"`. A union such as `"left" | "right"` restricts a value to those alternatives.

Literal unions make invalid states a type error and support narrowing by comparison. They are often preferable to an unconstrained `string` for a small fixed set of choices.

### literal-inference
- title: Const and literal inference
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

Why does a `const` variable usually keep a literal type while a `let` variable is widened?

---

A `const` binding cannot be reassigned, so TypeScript can infer a literal type such as `"hello"` for it. A `let` binding can later receive another string, so its type is normally widened to `string`.

This is inference for the binding, not deep immutability. An object stored in a `const` binding can still have mutable properties unless its type makes them readonly.

### null-undefined
- title: Null and undefined types
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strictNullChecks.html

How do `null` and `undefined` behave when `strictNullChecks` is enabled?

---

With `strictNullChecks`, `null` and `undefined` are distinct types and must be included in a union when a value can be absent. A `string | undefined` therefore requires handling before use as a string.

Without the flag, they are effectively ignored in the type system, which can hide absent-value errors. Prefer enabling `strictNullChecks`.

### optional-property
- title: Optional properties may be absent
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

What does the `?` mean on an object property?

---

An optional property such as `name?: string` may be omitted. Reading it produces a value that may be `undefined`.

Check for `undefined` before using an optional property where a `string` is required. Optionality is different from requiring a property whose value type explicitly includes `undefined`.

### optional-chaining
- title: Optional chaining short-circuits nullish values
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does `obj?.prop` do, and what values make it stop?

---

Optional property access checks whether the value before `?.` is `null` or `undefined`; if so, it evaluates to `undefined` instead of reading the property. It also narrows the need for a manual null check in that expression.

It does not short-circuit on other falsy values such as `0` or an empty string. It also does not validate that a later operation, such as arithmetic on the result, is safe.

### nullish-coalescing
- title: Nullish coalescing has a narrow fallback
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

When should you use `??` rather than `||` for a default value?

---

`a ?? b` uses `b` only when `a` is `null` or `undefined`. It preserves valid falsy values such as `0`, `false`, and `""`.

`a || b` uses the fallback for every falsy value. Use `??` when absence, rather than general falsiness, is the condition for a default.

### non-null-assertion
- title: Non-null assertions remove a check
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does the postfix `!` non-null assertion do?

---

The expression `value!` tells TypeScript to remove `null` and `undefined` from the expression's type. It does not emit a runtime check.

Use it only when an invariant outside the type system truly guarantees a value. A mistaken assertion can still cause a runtime failure, so a guard is usually safer.

### object-type
- title: Object type members
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

How do you describe an object with a required `name` and optional `age`?

---

An object type can list properties, for example `{ name: string; age?: number }`. Semicolons or commas separate members.

The type describes required and optional members structurally. It does not construct an object or add properties at runtime.

### excess-property-checks
- title: Fresh object literals get extra checks
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

Why can an object literal with a misspelled property fail even when a variable with extra properties is assignable?

---

When an object literal is assigned to an object type or passed as an argument, TypeScript performs excess property checking to catch likely misspellings. A property not present in the target type can be reported.

This is a special check on fresh literals, not a general prohibition on extra runtime properties. Fix a genuine typo rather than suppressing the check with an assertion.

### index-signature
- title: Index signatures describe unknown keys
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

How do you type an object whose string keys all have numeric values?

---

An index signature such as `{ [key: string]: number }` says that string-indexed properties have `number` values. It is useful when keys are not known ahead of time.

Named properties must also be compatible with the index-signature value type. Otherwise indexing by a string could produce a value inconsistent with the signature.

### readonly-property
- title: Readonly properties are assignment restrictions
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

What guarantee does `readonly` on a property provide?

---

A `readonly` property can be initialized but cannot be assigned through that type after construction. It is a compile-time restriction on assignment.

`readonly` is not a deep immutability guarantee and does not freeze an object at runtime. A referenced object can still be mutated through another mutable path.

### function-property
- title: Function properties have call signatures
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

How do you type a callback that receives a string and returns nothing?

---

Use a function type such as `(value: string) => void`. The parameter and return types describe calls through that value.

The `void` return type means callers should not rely on a return value. It does not require an implementation to literally return no value in every callback assignment case.

### call-signature
- title: Call signatures combine callable values and properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

How do you model a function value that also has a property?

---

Put a call signature inside an object type, for example `{ description: string; (value: number): boolean }`. This models JavaScript functions that carry properties.

The call signature uses `:` between parameter names and types, like a function declaration. The arrow syntax is for a standalone function type.

### construct-signature
- title: Construct signatures type newable values
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What is a construct signature used for?

---

A construct signature describes a value invoked with `new`, for example `new (s: string) => SomeObject`. It describes the instance type produced by construction.

It is different from a call signature because JavaScript functions can sometimes be called, constructed, or both. Model the operations your API actually supports.

### union-basics
- title: Unions accept alternatives
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does `string | number` mean for a value?

---

The union `string | number` means a value may be either a string or a number. Before narrowing, only operations valid for every union member are safe.

It does not mean the value is both types at once. Narrow with a runtime check before calling a string-only or number-only method.

### union-common-members
- title: Union operations require common members
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

Why cannot you call every method from a member of a union?

---

TypeScript allows an operation on a union only when that operation is valid for all members. A method available only on `string` cannot be called on `string | number` without narrowing.

Think of a union as a value with one possible member type at runtime. The compiler cannot assume which member it is until evidence narrows it.

### intersection-basics
- title: Intersections combine requirements
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

What does an intersection type such as `A & B` require?

---

An intersection type combines multiple object types, so a value of `A & B` must satisfy both `A` and `B`. It is often used to compose object capabilities.

If overlapping properties are incompatible, the intersection can be difficult or impossible to inhabit. Do not confuse an intersection with a union of alternatives.

### type-alias
- title: Type aliases name types
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What can a type alias name besides an object shape?

---

A type alias can name any type expression, including primitives, unions, tuples, intersections, and mapped types. For example, `type ID = number | string` gives a reusable name to a union.

An alias creates a name for a type; it does not create a new runtime value. It also cannot be reopened for declaration merging.

### interface-extension
- title: Interfaces extend object contracts
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

How does one interface inherit members from another?

---

An interface can use `extends` to inherit members from another object type, such as `interface ColorfulCircle extends Colorful, Circle {}`. The resulting type has all inherited members.

Inherited members with the same name must be compatible. Use intersections for type composition when an interface declaration is not the right form.

### declaration-merging
- title: Interfaces can merge declarations
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-merging.html

What happens when two interface declarations have the same name?

---

Multiple interface declarations with the same name are merged into one interface with the members of both declarations. Later declarations can add members to an existing interface.

This behavior supports declaration augmentation but can make global names surprising. Type aliases do not participate in declaration merging.

### typeof-narrowing
- title: Typeof narrows primitive values
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

How does a `typeof value === "string"` check affect a union?

---

A `typeof` comparison is a type guard. In the true branch of `typeof value === "string"`, TypeScript narrows a union to its string-compatible members.

Use JavaScript's actual `typeof` result strings such as `"string"` and `"number"`. The `typeof null === "object"` historical behavior remains a common trap.

### truthiness-narrowing
- title: Truthiness narrows but can hide values
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

What is the risk of using a broad truthiness check to narrow a value?

---

In a truthiness check, TypeScript narrows away falsy possibilities in the true branch. This can be convenient for values that are only nullish or present.

It can accidentally exclude meaningful values such as `0` or `""`. Prefer an explicit nullish comparison when those values must remain valid.

### equality-narrowing
- title: Equality checks narrow unions
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

How can equality narrowing find a common type between two values?

---

When two values are compared with equality, TypeScript narrows each to types that could be equal. If one is `string | number` and the other is `string | boolean`, equality makes both strings in the matching branch.

Equality narrowing follows the runtime comparison. It is useful when the same runtime value links two otherwise broad unions.

### in-operator-narrowing
- title: The in operator narrows object unions
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

How does `"swim" in animal` narrow an object union?

---

The `in` operator checks whether a property exists on an object. TypeScript narrows the true branch to union members that have that property and the false branch to members that do not.

Optional properties can appear in both branches because a type may have the property optionally. A discriminant property is often clearer for mutually exclusive variants.

### instanceof-narrowing
- title: Instanceof narrows class instances
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

When does `value instanceof Date` narrow a value?

---

An `instanceof` check uses JavaScript's prototype-chain behavior and narrows the true branch to the instance type associated with the constructor. It is useful for class-based runtime values such as `Date`.

It only works when the runtime constructor identity is meaningful. It is not a structural property check for plain object data from JSON.

### assignment-narrowing
- title: Assignments use the declared type
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

Why can a variable narrowed to `number` later receive a string?

---

Control-flow analysis narrows a variable's observed type at a program point, but assignments are checked against its declared type. A `let x: string | number` may later be assigned either member.

After an assignment, TypeScript uses the assigned value's type for subsequent flow analysis. Narrowing does not permanently change the declared annotation.

### control-flow-analysis
- title: Control flow drives narrowing
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

What does control-flow analysis mean in TypeScript narrowing?

---

TypeScript follows reachable paths through conditions, returns, and assignments to refine a variable's type at each location. An early return can leave only a narrower type after the branch.

The narrowing is based on JavaScript control flow, so a later assignment or an uncertain path can change what is known. Keep checks close to the use they protect.

### type-predicate
- title: User-defined type predicates
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

How do you write a custom type guard that narrows to `Fish`?

---

A type predicate has the form `parameterName is Type`, for example `function isFish(pet: Fish | Bird): pet is Fish`. When the function returns true, TypeScript narrows that parameter to `Fish`.

The predicate is a claim made by your implementation, so it must accurately test the runtime shape. A mistaken guard gives the compiler unsound information.

### assertion-function
- title: Assertion functions narrow on return
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

What does an assertion signature such as `asserts value is string` express?

---

An assertion function signature tells TypeScript that if the function returns normally, a condition holds. A signature like `asserts value is string` narrows `value` after the call.

The function should throw or otherwise not return when the assertion fails. The type system trusts the signature, so its implementation must enforce the stated condition.

### never-exhaustiveness
- title: Never checks exhaustive unions
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

How does assigning a value to `never` help with an exhaustive switch?

---

After every member of a discriminated union is handled, the remaining value has type `never`. Assigning it to a `never` variable in a default branch makes an unhandled new member a compile error.

This technique relies on a discriminant with a finite union of literal values. It turns an omitted case into a type-checking failure rather than a silent runtime path.

### generic-identity
- title: Generic functions preserve types
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

Why is `function identity<T>(arg: T): T` more useful than an `any` identity function?

---

The type parameter `T` captures the caller's argument type and returns that same type. Calling it with a number returns a number type, and calling it with a string returns a string type.

An `any` version loses that relationship and disables checking on the result. Generics express a reusable relationship between input and output types.

### generic-inference
- title: Generic arguments are often inferred
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

Must callers always write a generic type argument?

---

TypeScript can infer type arguments from function arguments in many generic calls. For `identity("hello")`, it infers `T` as `string`.

Callers can specify a type argument when inference needs help or a wider intended type is important. Supplying one unnecessarily can make an API harder to use.

### generic-constraint
- title: Constraints require capabilities
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

How do you require a generic argument to have a `length` property?

---

Constrain the parameter with `extends`, as in `T extends { length: number }`. The function can then read `arg.length` because every permitted argument has that member.

A constraint does not force the argument to be exactly that shape; it accepts any subtype with the required capability. This is why arrays and strings can both satisfy a length constraint.

### generic-key-constraint
- title: Key constraints protect property access
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

How do you constrain a key argument to keys of an object argument?

---

Use a dependent constraint such as `Key extends keyof Type`. It permits only property names present in the object type.

That constraint lets a helper safely return `obj[key]` with type `Type[Key]`. Without it, an arbitrary string might name no property at all.

### generic-default
- title: Generic defaults make parameters optional
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

What does a default generic type parameter provide?

---

A default type parameter such as `T = HTMLElement` is used when inference cannot choose a type argument and the caller omits it. Required type parameters cannot follow optional defaulted ones.

Defaults reduce repetition for common cases while preserving an override for callers. A default is not a runtime default value.

### generic-class
- title: Generic classes parameterize instance sides
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

Which side of a generic class uses its type parameter?

---

The generic type parameter of a class applies to its instance side, including instance properties and methods. Different instantiations such as `GenericNumber<number>` and `GenericNumber<string>` have distinct instance types.

Static members cannot use the class's type parameters because there is only one static side shared by all instantiations. Put per-instance generic data on the instance side.

### keyof-operator
- title: Keyof produces keys
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/keyof-types.html

What does `keyof` do to an object type?

---

`keyof` produces a union of an object type's property keys. For `{ x: number; y: number }`, it produces `"x" | "y"`.

With a string index signature, `keyof` includes `string` and `number`. JavaScript coerces numeric property keys to strings.

### typeof-type-operator
- title: Typeof refers to a value type
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/typeof-types.html

How do you refer to the type of a value named `config`?

---

In a type position, write `typeof config` to obtain the type of that value. This bridges a value declaration and a type expression.

TypeScript permits type-query `typeof` on identifiers and their properties. It does not run an arbitrary expression.

### indexed-access
- title: Indexed access looks up property types
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html

What does `Person["age"]` mean in a type?

---

`Person["age"]` is an indexed access type that looks up the type of the `age` property on `Person`. It evaluates to that property's declared type.

The index must be a type, not a value variable. Use `typeof key` if a value's type is intended.

### indexed-union
- title: Indexed access accepts key unions
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html

What is the result of indexing a type with `"name" | "age"`?

---

Indexing an object type with a union of keys produces a union of the corresponding property types. `Person["name" | "age"]` is the type of either selected property.

An invalid key is a type error. Combine `keyof T` with `T[keyof T]` to obtain the union of an object's property values.

### array-element-access
- title: Number indexes array element types
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html

How do you obtain an array type's element type with indexed access?

---

For an array type `T`, `T[number]` is its element type. For an array value, `typeof values[number]` first gets the array type and then its element type.

This works because numeric indexing retrieves array elements. It does not mean every numeric index exists at runtime.

### mapped-type
- title: Mapped types transform properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

What does a mapped type iterate over?

---

A mapped type iterates over a union of property keys, often `keyof T`, to create a new property for each key. It can reuse or transform each property's value type.

Mapped types are type-level transformations only. They do not loop over an object at runtime.

### mapped-readonly
- title: Mapped types can add readonly
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

How can a mapped type make every property readonly?

---

Place `readonly` before the mapped property declaration, as in `{ readonly [P in keyof T]: T[P] }`. The resulting properties cannot be reassigned through that type.

This changes the top-level property modifiers in the resulting type. It does not recursively freeze nested values.

### mapped-remove-readonly
- title: Mapped types can remove readonly
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

What does `-readonly` do in a mapped type?

---

The `-readonly` modifier removes readonly from mapped properties. It can turn a readonly object type into a mutable property type.

Without a `+` or `-` prefix, mapped modifiers preserve or add their normal form. Modifier changes are purely type-level.

### mapped-optional
- title: Mapped types can add optionality
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

How does a mapped type make every property optional?

---

Place `?` after the mapped property name, as in `{ [P in keyof T]?: T[P] }`. Every property can then be omitted.

An optional property may read as `undefined`, so callers still need absence handling. This pattern underlies `Partial<T>`.

### mapped-remove-optional
- title: Mapped types can require properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

What does `-?` do in a mapped type?

---

The `-?` modifier removes optionality from each mapped property. It creates required properties from the source keys.

It changes a property modifier, not the property value's own union type. A property typed `string | undefined` can remain so while required.

### key-remapping
- title: Mapped types can remap keys
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

What is the `as` clause in a mapped type for?

---

The `as` clause remaps each key while mapping, for example to form new property names with a template literal type. It can also produce `never` to omit a key.

Key remapping operates on types. Ensure the remapped key is a valid property key type.

### conditional-type
- title: Conditional types choose by assignability
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html

How does `T extends U ? X : Y` choose a type?

---

A conditional type chooses `X` when `T` is assignable to `U`; otherwise it chooses `Y`. It expresses a type-level relationship between input and output.

Its power is greatest with a generic `T`, where the result can vary per caller. It is not a runtime conditional expression.

### conditional-true-branch
- title: Conditional branches add information
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html

Why can a conditional type access a property in its true branch?

---

In the true branch of `T extends { message: unknown } ? T["message"] : never`, TypeScript knows `T` has a `message` property. The check supplies the needed constraint there.

Moving a constraint into the conditional lets the false branch handle types without that property. This often makes reusable utility types more flexible.

### infer-keyword
- title: Infer captures a type inside a condition
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html

What does `infer` do inside a conditional type?

---

`infer` introduces a type variable while matching a type in a conditional type. For example, `T extends Array<infer Item> ? Item : T` captures an array's element type.

It is available in the true branch of a conditional pattern. It avoids manually indexing into a known structure when matching is clearer.

### distributive-conditional
- title: Naked type parameters distribute over unions
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html

When does a conditional type distribute across a union?

---

A conditional type whose checked side is a naked type parameter distributes over a union argument. `T extends any ? T[] : never` applied to `string | number` becomes `string[] | number[]`.

Wrap each side of `extends` in square brackets to prevent distribution. This changes the test to operate on the union as a whole.

### template-literal-type
- title: Template literal types construct strings
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

What can a template literal type do with literal types?

---

A template literal type constructs new string literal types by concatenating literal types in a type position. For example, `` `get${"Name"}` `` is `"getName"`.

It is a type-level construct with syntax similar to a JavaScript template string. It does not format a runtime string.

### template-union-cross-product
- title: Template literal unions expand combinations
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

What happens when a template literal type interpolates unions?

---

Each union in an interpolated position is cross-multiplied with the others, producing every possible string combination. This is useful for small finite name sets.

Large combinations can create very large unions. The handbook recommends ahead-of-time generation for large string unions.

### uppercase-intrinsic
- title: Uppercase transforms string literals
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

What does the intrinsic `Uppercase<T>` type do?

---

`Uppercase<T>` converts each character in a string literal type to uppercase. It can be used inside a template literal type.

It is a compiler-provided intrinsic string manipulation type. It does not mutate a runtime string.

### lowercase-intrinsic
- title: Lowercase transforms string literals
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

What does `Lowercase<T>` do?

---

`Lowercase<T>` converts each character in a string literal type to lowercase. It produces a transformed string literal type.

Like the other intrinsic string manipulation types, it works in the type system. It is not locale-aware according to the handbook's implementation details.

### capitalize-intrinsic
- title: Capitalize transforms the first character
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

What does `Capitalize<T>` do?

---

`Capitalize<T>` converts the first character of a string literal type to uppercase. It is useful when deriving conventional property names.

It affects only the type-level string representation. It does not change a supplied JavaScript value.

### uncapitalize-intrinsic
- title: Uncapitalize transforms the first character
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

What does `Uncapitalize<T>` do?

---

`Uncapitalize<T>` converts the first character of a string literal type to lowercase. It is the counterpart of `Capitalize<T>`.

It is useful for type-level naming transformations. The input must be used in a type context.

### parameter-optional
- title: Optional function parameters
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What does `x?: number` mean in a function parameter list?

---

An optional parameter may be omitted by the caller. Inside the function, its type includes `undefined`.

Optional parameters must follow required parameters. Use a default value when the implementation needs a concrete fallback.

### parameter-default
- title: Default parameters are optional to callers
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

How does a default parameter affect callers and the implementation?

---

A parameter with a default initializer is treated as optional to callers. Inside the function body, the default ensures a value of the parameter's base type.

The default value is JavaScript runtime behavior. It is not the same as merely making a parameter optional.

### rest-parameters
- title: Rest parameters collect arguments
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

How do you type a rest parameter of numbers?

---

Write a rest parameter as `...args: number[]` to collect remaining arguments into an array. The function may then be called with zero or more numeric arguments.

Rest parameters are arrays at runtime. A tuple rest type can describe a fixed sequence of argument types.

### rest-tuple
- title: Rest tuples preserve argument positions
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Why use a tuple type for a rest parameter?

---

A rest parameter typed as a tuple can model a known sequence of argument types and optional positions. It preserves positional information that `unknown[]` would lose.

This is useful for forwarding arguments or representing a function's parameter list. The tuple still becomes a JavaScript array at runtime.

### function-overloads
- title: Overloads describe multiple call shapes
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What are overload signatures for?

---

Overload signatures describe multiple ways callers may invoke one implementation. The implementation signature must be compatible with those overloads.

Callers see the overload signatures, not the implementation signature. Prefer a union parameter when all calls have the same return type and one implementation shape is enough.

### overload-implementation
- title: The implementation signature is hidden
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Can a caller use only a function's implementation signature?

---

No. A caller must match one declared overload signature; the implementation signature is not visible from outside the function. It exists to implement the overload set.

Write overloads that represent real supported calls. An overly broad implementation signature does not create a public overload.

### callback-void
- title: Void callbacks may return values
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Does a callback assigned to `() => void` have to return `undefined`?

---

A function type with return `void` means the caller will not use the return value. A function that returns another value can still be assigned where a void-returning callback is expected.

This rule supports callbacks such as those passed to array methods. It does not mean a function explicitly declared to return `void` may return arbitrary values.

### this-parameter
- title: This parameters are type-only
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What is the special first `this` parameter in a function type?

---

A parameter literally named `this` is a fake parameter used to declare the function's `this` type. It is erased from emitted JavaScript and is not supplied by callers.

It helps type callbacks whose receiver matters. Use an arrow function when lexical `this` is intended instead.

### never-type
- title: Never represents impossible values
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What does `never` represent as a function return type?

---

`never` represents values that never occur. A function that always throws or never finishes can have return type `never`.

`never` is also useful when an exhaustive union has no remaining members. It is not the same as `void`, which represents an ignored return value.

### any-type
- title: Any disables type checking
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What is the main effect of annotating a value as `any`?

---

`any` opts a value out of TypeScript's type checking, allowing arbitrary property access and calls. It can spread unchecked types into later expressions.

Use it only as a local escape hatch when necessary. Prefer a more specific type or `unknown` at an untrusted boundary.

### unknown-type
- title: Unknown requires narrowing
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

How is `unknown` different from `any`?

---

Every value is assignable to `unknown`, but an `unknown` value cannot be used without narrowing or assertion. This preserves safety at an uncertain boundary.

`any` permits unchecked use immediately. Choose `unknown` when data is present but its shape has not been verified.

### object-vs-object-type
- title: Object is not an object-shape type
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Why is `object` usually better than `Object` in a parameter type?

---

The lowercase `object` type represents non-primitive values. The uppercase `Object` type should generally be avoided in TypeScript code.

Neither form describes a particular property shape. Use an object type or interface when the function needs named members.

### void-type
- title: Void means ignored return value
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What does `void` communicate in a function type?

---

`void` communicates that a caller should not use a function's return value. It is commonly used for callbacks and functions with no meaningful result.

It is distinct from `undefined` and `never`. Do not use it to mean a function cannot return at all.

### partial-utility
- title: Partial makes properties optional
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Partial<T>` construct?

---

`Partial<T>` constructs a type with all properties of `T` set to optional. It represents every subset of the original properties.

It is useful for update-like inputs. It is shallow, so nested object properties are not recursively made optional.

### required-utility
- title: Required makes properties required
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Required<T>` construct?

---

`Required<T>` constructs a type with all properties of `T` set to required. It is the opposite modifier transformation to `Partial<T>`.

It does not remove `undefined` from a property's own value type. It only changes whether the property can be omitted.

### pick-utility
- title: Pick selects properties
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Pick<T, K>` construct?

---

`Pick<T, K>` constructs a type by selecting the properties named by `K` from `T`. `K` can be a string-literal key or a union of keys.

It is useful for a focused view of an existing object type. It does not pick runtime properties from an object.

### omit-utility
- title: Omit removes selected properties
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Omit<T, K>` construct?

---

`Omit<T, K>` constructs a type from `T` with the keys in `K` removed. It is the inverse selection idea of `Pick`.

Use it when a derived type should exclude known fields. It is a static type transformation, not a runtime object copy.

### record-utility
- title: Record maps keys to one value type
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Record<K, V>` construct?

---

`Record<K, V>` constructs an object type with property keys `K` and property values `V`. It is useful for a finite map keyed by a literal union.

It describes the required static keys when `K` is a literal union. It does not create a JavaScript object or initialize values.

### exclude-utility
- title: Exclude removes union members
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Exclude<T, U>` do?

---

`Exclude<T, U>` removes from union `T` every member assignable to `U`. For example, excluding `"a"` from `"a" | "b"` leaves `"b"`.

It compares assignability rather than exact textual equality. It is a type-level utility for union transformations.

### extract-utility
- title: Extract keeps matching union members
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Extract<T, U>` do?

---

`Extract<T, U>` keeps from union `T` the members assignable to `U`. It is the complementary filtering operation to `Exclude`.

Use it to select matching variants from a union. It does not inspect runtime values.

### returntype-utility
- title: ReturnType extracts returns
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `ReturnType<F>` produce?

---

`ReturnType<F>` constructs the return type of a function type `F`. It can be used with `typeof someFunction` to derive an existing function's result type.

For overloaded functions, it uses the last signature. It requires a function type rather than an arbitrary type.

### parameters-utility
- title: Parameters extracts arguments
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Parameters<F>` produce?

---

`Parameters<F>` constructs a tuple type from the parameter types of a function type `F`. It is useful for forwarding a function's call shape.

For overloaded functions, it uses the last signature. It requires a function type with a compatible call signature.

### class-fields
- title: Class fields
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

How are class fields declared?

---

Class fields may have type annotations and initializers.

Their values exist on class instances at runtime.

### class-methods
- title: Class methods
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

How are class methods typed?

---

Methods use parameter and return type annotations like functions.

Their types describe calls on an instance.

### class-constructor
- title: Class constructors
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What initializes a class instance?

---

A constructor runs when an instance is created with `new`.

It should initialize required instance state.

### class-implements
- title: Implements checks an instance contract
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What does `implements` check?

---

`implements` checks that a class instance satisfies an interface or type.

It does not change the class type or infer members.

### class-extends
- title: Extends inherits a base class
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What does `extends` do on a class?

---

`extends` creates a derived class from a base class.

The derived constructor must call `super` before using `this`.

### public-members
- title: Public is the default
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What accessibility do class members have by default?

---

Class members are public by default.

Public members are accessible from outside the class.

### protected-members
- title: Protected members
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Who can access a protected member?

---

Protected members are visible within the declaring class and subclasses.

They are not accessible through an instance from unrelated code.

### private-members
- title: Private members
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What does TypeScript `private` restrict?

---

`private` restricts access to within the declaring class.

Private members also affect structural compatibility.

### ecmascript-private
- title: Hash private fields
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

How do `#` private fields differ from TypeScript private?

---

`#field` is JavaScript private-field syntax with runtime privacy.

It is distinct from TypeScript's `private` modifier.

### readonly-class-field
- title: Readonly class fields
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

When can a readonly class field be assigned?

---

A readonly field can be assigned in its declaration or constructor.

It cannot be assigned through the instance afterward.

### parameter-properties
- title: Parameter properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What is a parameter property?

---

An accessibility modifier on a constructor parameter creates and initializes a class property.

It is TypeScript shorthand for a common class pattern.

### accessors
- title: Getters and setters
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

How are accessors typed?

---

Getters and setters can control reads and writes of a property.

Getter and setter types must be compatible.

### static-members
- title: Static members belong to the class
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Where does a static member live?

---

Static members are accessed on the class constructor, not instances.

They cannot use class instance type parameters.

### abstract-class
- title: Abstract classes
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Can you instantiate an abstract class?

---

An abstract class cannot be instantiated directly.

It may contain implementation and abstract members.

### abstract-method
- title: Abstract methods
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

What must a derived class do with an abstract method?

---

A non-abstract derived class must implement inherited abstract members.

The abstract declaration supplies the required contract.

### class-initialization-order
- title: Field initialization order
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

A derived class sets `name = "derived"`, but the base constructor logs `this.name` and prints `"base"`. Why?

---

JavaScript initializes classes in this order: base fields, then the base constructor, then derived fields, then the derived constructor. The base constructor therefore still sees the base field value, because the derived field initializer has not run.

That order is why reading an overridable field inside a base constructor is a trap. The derived assignment cannot have happened yet.

### class-type-only
- title: Classes have runtime values
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Why can a class name be used as both a type and value?

---

A class declaration creates a runtime constructor value and an instance type.

The two namespaces are related but serve different roles.

### enum-numeric
- title: Numeric enums
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/enums.html

What is the default first numeric enum value?

---

A numeric enum member without an initializer starts at `0`.

Following auto-incrementing members receive subsequent numbers.

### enum-string
- title: String enums
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/enums.html

Why give every string enum member a value?

---

String enum members require constant string initializers.

Their runtime values are readable strings rather than generated numbers.

### enum-union
- title: Literal enum members form a union
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/enums.html

How can an enum help exhaustiveness checking?

---

When enum members are literal values, they can form a union type.

Comparisons can then narrow to a specific member.

### const-enum
- title: Const enums
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/enums.html

What is the defining behavior of a const enum?

---

Const enum references are inlined at use sites.

They have trade-offs, especially across published package boundaries.

### enum-runtime-object
- title: Enums are runtime objects
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/enums.html

Do enums exist at runtime?

---

Unlike most TypeScript features, regular enums are real runtime objects.

An `as const` object is an alternative in some designs.

### enum-reverse-mapping
- title: Numeric enum reverse mapping
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/enums.html

Which enums get reverse mappings?

---

Numeric enum members get reverse mappings from value to name.

String enum members do not get reverse mappings.

### module-export
- title: Export makes a module member public
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What does `export` do?

---

`export` makes a declaration available to importing modules.

Unexported declarations remain module-local.

### module-import
- title: Import consumes module exports
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What does an import bind?

---

An import binds an exported module member into the current module.

It does not create a global variable.

### default-export
- title: Default exports
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

How is a default export imported?

---

A default export is imported without braces, such as `import value from "./mod"`.

Its import name is chosen by the consumer.

### named-export
- title: Named exports
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

How is a named export imported?

---

Named exports are imported with braces, such as `import { value } from "./mod"`.

The imported name normally matches the exported name.

### type-only-import
- title: Type-only imports
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What does `import type` communicate?

---

`import type` imports a declaration only for type positions.

It is erased from JavaScript output.

### type-only-export
- title: Type-only exports
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What does `export type` communicate?

---

`export type` exports a declaration only for type use.

It has no runtime export in emitted JavaScript.

### module-scope
- title: Modules have their own scope
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What creates module scope?

---

A file with a top-level import or export is a module.

Its declarations are scoped to that module.

### module-specifier
- title: Module specifiers name dependencies
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What is the string in an import statement?

---

The import string is a module specifier used to locate a module.

Its resolution depends on configured module resolution rules.

### re-export
- title: Re-exports expose another module
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What does `export { x } from "./x"` do?

---

A re-export exposes an imported module's export from the current module.

It can provide a public module entry point.

### namespace-not-module
- title: Namespaces differ from modules
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

Why should you distinguish modules and namespaces?

---

Modules are files with imports or exports and use module loading.

Namespaces are a separate TypeScript feature for organizing declarations.

### declaration-file
- title: Declaration files describe JavaScript
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html

What is the purpose of a `.d.ts` file?

---

A declaration file describes the type surface of JavaScript code.

It supplies types without providing an implementation.

### declaration-module
- title: Module declarations describe packages
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html

When is a module declaration useful?

---

A module declaration can describe an external JavaScript module's exports.

It is useful when a package has no bundled types.

### ambient-declare
- title: Declare introduces ambient names
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html

What does `declare` mean in a declaration file?

---

`declare` describes a value or type assumed to exist elsewhere.

It does not emit an implementation for that declaration.

### declaration-augmentation
- title: Declaration augmentation adds members
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-merging.html

What can module augmentation do?

---

Module augmentation can add declarations to an existing module.

It uses declaration merging rules for the augmented declarations.

### global-augmentation
- title: Global augmentation
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-merging.html

What does `declare global` allow?

---

`declare global` adds declarations to the global scope from a module.

Use it deliberately because global names affect all files.

### strict-mode
- title: Strict enables safety checks
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strict.html

What does the `strict` compiler option do?

---

`strict` enables a family of stricter type-checking options.

New strict checks can be added in future TypeScript versions.

### no-implicit-any
- title: No implicit any
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noImplicitAny.html

What does `noImplicitAny` report?

---

`noImplicitAny` reports expressions and declarations with implied `any` types.

Annotate or improve inference instead of accepting accidental `any`.

### strict-null-checks
- title: Strict null checks
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strictNullChecks.html

What risk does strict null checking prevent?

---

`strictNullChecks` makes nullable values explicit in types.

It prevents using a possibly absent value without handling it.

### strict-function-types
- title: Strict function types
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strictFunctionTypes.html

What does strict function checking affect?

---

`strictFunctionTypes` checks function parameter positions more strictly.

It helps catch unsafe function assignments.

### strict-property-initialization
- title: Strict property initialization
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strictPropertyInitialization.html

What does strict property initialization require?

---

It checks that class properties are initialized in the constructor.

It applies when `strictNullChecks` is enabled.

### use-unknown-catch
- title: Unknown catch variables
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/useUnknownInCatchVariables.html

What type does this option give a catch variable?

---

`useUnknownInCatchVariables` types catch-clause variables as `unknown`.

Narrow the error before reading its members.

### no-implicit-override
- title: Explicit overrides
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noImplicitOverride.html

What does `noImplicitOverride` require?

---

It requires the `override` modifier for methods that override base members.

This helps catch accidental overrides after base-class changes.

### no-implicit-this
- title: No implicit this
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noImplicitThis.html

What does `noImplicitThis` check?

---

`noImplicitThis` reports expressions with an implied `any` `this` type.

Annotate `this` or use a context with a known receiver type.

### strict-bind-call-apply
- title: Strict bind call apply
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/strictBindCallApply.html

What does strict bind-call-apply improve?

---

`strictBindCallApply` checks `bind`, `call`, and `apply` method arguments.

It uses the target function's parameter types.

### partial-extra
- title: Partial is global
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

Must you import `Partial`?

---

`Partial` is one of TypeScript's globally available utility types.

It transforms a type; it is not a runtime helper.

### readonly-utility
- title: Readonly utility
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Readonly<T>` construct?

---

`Readonly<T>` makes all properties of `T` readonly.

It prevents property reassignment through the resulting type.

### nonnullable-utility
- title: NonNullable utility
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `NonNullable<T>` remove?

---

`NonNullable<T>` excludes `null` and `undefined` from `T`.

It is a type transformation, not a runtime check.

### awaited-utility
- title: Awaited utility
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `Awaited<T>` model?

---

`Awaited<T>` models recursively unwrapping promise-like types.

It follows the type behavior of `await`.

### instance-type
- title: InstanceType utility
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `InstanceType<C>` produce?

---

`InstanceType<C>` constructs the instance type of a constructor type.

It requires a constructor-compatible type.

### constructor-parameters
- title: ConstructorParameters utility
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does `ConstructorParameters<C>` produce?

---

`ConstructorParameters<C>` constructs a tuple of a constructor's parameter types.

It requires a constructor-compatible type.

### satisfies-operator
- title: Satisfies validates without replacement
- version: 4.9
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html

Which release introduced `satisfies`?

---

TypeScript 4.9 introduced the `satisfies` operator.

It validates compatibility while preserving the expression's inferred type.

### const-generics-release
- title: Const type parameters release
- version: 5.0
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html

Which release introduced const type parameters?

---

TypeScript 5.0 introduced `const` type parameters.

They give const-like inference for generic arguments.

### using-release
- title: Using declarations release
- version: 5.2
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html

Which release introduced `using` declarations?

---

TypeScript 5.2 added `using` and `await using`.

They support explicit resource management disposal.

### function-declaration
- title: Function declarations
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

How is a function return type written?

---

Put the return type after the parameter list.

Inference can often determine it when omitted.

### function-expression
- title: Function expressions
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Can a function expression have a type?

---

A function expression can be contextually typed by its location.

Its parameters can then receive inferred types.

### anonymous-function
- title: Contextual typing
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What is contextual typing for a callback?

---

The surrounding expected type can provide callback parameter types.

It avoids repeating types already known by an API.

### generic-call-signature
- title: Generic call signatures
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Where can a generic call signature put its type parameter?

---

A call signature can declare its own type parameter before parameters.

Each call can infer a fresh type argument.

### generic-interface
- title: Generic interfaces
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

What does a generic interface parameterize?

---

A generic interface uses a type parameter in its member types.

Users supply or infer a type argument when using it.

### generic-variance
- title: Generic relationships
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/generics.html

Why should type parameters appear in members?

---

A type parameter should relate input, output, or member types.

Unused parameters add no useful relationship.

### array-generic
- title: Generic array syntax
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does `Array<T>` mean?

---

`Array<T>` describes an array with elements of type `T`.

`T[]` is the common shorthand form.

### union-literals
- title: Literal union choices
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

Why use a literal union for an option?

---

A literal union restricts values to known alternatives.

It also enables comparison-based narrowing.

### discriminant-property
- title: Discriminant properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

What makes a union discriminated?

---

Its members share a property with distinct literal values.

Checking that property narrows to a member.

### switch-narrowing
- title: Switch narrowing
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

Does a switch narrow a discriminated union?

---

Each matching switch case narrows by the discriminant value.

A `never` default can check omitted cases.

### array-is-array
- title: Array.isArray guard
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

How can you narrow an unknown value to an array?

---

`Array.isArray(value)` is a JavaScript type guard.

TypeScript narrows the value in its true branch.

### null-object-trap
- title: Null typeof trap
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

Why is `typeof null` a trap?

---

JavaScript reports `typeof null` as `"object"`.

Check null separately when an object must be present.

### optional-property-in
- title: Optional properties and in
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html

Can an optional property appear in both in branches?

---

Yes, optional properties can occur in both branches of an `in` check.

They do not uniquely identify a union member.

### assertion-type
- title: Type assertions
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does `value as Type` do?

---

A type assertion changes the compiler's view of an expression.

It does not validate or convert the value at runtime.

### double-assertion
- title: Double assertions
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

Why are double assertions risky?

---

An assertion through `unknown` can force otherwise incompatible types.

It bypasses checking and should be rare.

### optional-element-access
- title: Optional element access
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does `arr?.[0]` do?

---

It reads an element only when the array is non-nullish.

Otherwise the expression evaluates to `undefined`.

### optional-call
- title: Optional calls
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What does `fn?.()` do?

---

It calls `fn` only when it is non-nullish.

Otherwise it evaluates to `undefined`.

### bigint-type
- title: Bigint type
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What type describes bigint values?

---

The `bigint` type describes JavaScript bigint values.

Bigints are distinct from numbers.

### symbol-type
- title: Symbol type
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

What type describes symbol values?

---

The `symbol` type describes JavaScript symbol values.

Symbols can be used as property keys.

### object-unknown-properties
- title: Unknown object properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

How do index signatures model arbitrary keys?

---

An index signature gives values a common type by key kind.

Known members must be compatible with it.

### callable-interface
- title: Callable interfaces
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Can an interface describe a callable value?

---

An interface can contain a call signature.

It may also contain ordinary properties.

### overload-order
- title: Overload order
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Why is overload order important?

---

Overload resolution uses the declared call signatures.

Write clear signatures for the supported calls.

### implementation-compatibility
- title: Overload compatibility
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

What must an overload implementation satisfy?

---

The implementation signature must be compatible with its overloads.

It is not callable directly by consumers.

### class-structural
- title: Classes are structural
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Are classes structurally compared?

---

Classes are generally compared by their instance members.

Private and protected members add compatibility restrictions.

### class-private-origin
- title: Private origin compatibility
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Why can matching private members still be incompatible?

---

Private members must originate from the same class declaration.

Their names alone do not make classes compatible.

### super-call
- title: Super calls
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

When is `super()` needed?

---

A derived constructor must call `super()` before accessing `this`.

It initializes the base-class portion of the instance.

### class-method-this
- title: Method this
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Why can an extracted method lose its receiver?

---

JavaScript method calls determine `this` from the call form.

Bind or use an arrow property when lexical behavior is needed.

### interface-extends-class
- title: Interface extends class
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/classes.html

Can an interface extend a class?

---

An interface can extend a class type's instance side.

It inherits members, including private and protected ones.

### module-alias
- title: Import aliases
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

Can an import rename an export locally?

---

An import can use `as` to create a local alias.

The module's original export name is unchanged.

### export-alias
- title: Export aliases
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

Can an export be renamed?

---

An export list can use `as` to expose another name.

The local declaration name need not change.

### module-side-effect
- title: Side-effect imports
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/modules.html

What is an import with no bindings for?

---

An import with no bindings loads a module for its side effects.

It creates no local imported name.

### ambient-module
- title: Ambient external modules
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html

What does an ambient module declaration describe?

---

It provides types for a module implemented elsewhere.

It contains declarations rather than module code.

### declaration-merge-functions
- title: Function declaration merging
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-merging.html

Can functions merge with namespaces?

---

TypeScript supports some declaration merge combinations.

The merge rules determine which members combine.

### declaration-merge-enums
- title: Enum declaration merging
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/declaration-merging.html

Can enums participate in merging?

---

TypeScript documents declaration merging for supported declarations.

Use merging only when its combined API is intentional.

### no-unchecked-indexed-access
- title: Unchecked indexed access
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html

What does `noUncheckedIndexedAccess` add to an index signature?

---

An index signature already types unknown keys as the declared value type. With this flag, TypeScript adds `undefined` to any field that was not explicitly declared, because that lookup may be missing at runtime.

A declared property such as `NAME: string` stays `string`. A key that exists only through the index signature becomes `string | undefined`, so you have to narrow it before treating it as present.

### exact-optional-properties
- title: Exact optional properties
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html

What does exactOptionalPropertyTypes change?

---

It interprets optional properties exactly as written.

It distinguishes absence from assigning `undefined`.

### no-fallthrough-cases
- title: Fallthrough case checking
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noFallthroughCasesInSwitch.html

What does noFallthroughCasesInSwitch report?

---

It reports switch cases that fall through without a break.

This can catch unintended control flow.

### no-implicit-returns
- title: Implicit returns
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noImplicitReturns.html

What does noImplicitReturns check?

---

It reports when not all code paths return a value.

It helps find incomplete function branches.

### no-unused-locals
- title: Unused locals
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noUnusedLocals.html

What does noUnusedLocals report?

---

It reports declared local variables that are never read.

It can keep code free of unused declarations.

### no-unused-parameters
- title: Unused parameters
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/tsconfig/noUnusedParameters.html

What does noUnusedParameters report?

---

It reports function parameters that are never read.

Prefixing with `_` is an allowed exemption.

### no-implicit-any-index
- title: Implicit any indexes
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/tsconfig/suppressImplicitAnyIndexErrors.html

What does `suppressImplicitAnyIndexErrors` turn off, and why is enabling it a poor fix?

---

It suppresses the error TypeScript reports when you index an object with a key that is not known on that type. On `{ x: number }`, `obj["foo"]` is an implicit-`any` error unless the flag hides it.

The tsconfig page calls the flag a drastic approach because it hides those errors for the whole program. Prefer a narrower escape, such as `@ts-ignore` on the one line, or a type that actually allows that index.

### key-remap-filter
- title: Key remapping filters
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html

How can a mapped type remove a key?

---

Remap that key to `never` with an `as` clause.

The resulting type omits that property.

### conditional-flatten
- title: Conditional flattening
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html

How can a conditional type get an array element type?

---

Test whether `T` extends an array and index with `number`.

Otherwise return `T` unchanged.

### infer-return
- title: Infer function returns
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html

How can infer capture a return type?

---

Match a function type with `infer` in its return position.

The true branch can then use the inferred type.

### template-event-name
- title: Template event names
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

How can a type derive changed-event names?

---

A template literal type can append `"Changed"` to keys.

Combine it with `keyof` for valid event names.

### template-infer-key
- title: Template literal inference
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html

Can template literals infer a key prefix?

---

Conditional template matching can infer a string portion.

That key can index the original object type.

### readonly-tuple
- title: Readonly tuples
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

What does `readonly` do to a tuple?

---

A readonly tuple cannot be written through its readonly type.

Its positional element types remain available for reading.

### named-tuple-members
- title: Named tuple members
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

Do tuple member labels affect assignability?

---

Tuple labels improve readability in type displays.

They do not change how the tuple is structurally checked.

### function-assignability
- title: Function assignability
- version: Core
- level: experienced
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/functions.html

Why does a callback parameter type matter?

---

Function types describe what arguments a callback can receive.

An incompatible callback can fail when the API invokes it.

### utility-global
- title: Utility types are global
- version: Core
- level: beginner
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

Where are built-in utility types available?

---

TypeScript utility types are available globally.

They facilitate common type transformations.

### structural-extra-properties
- title: Structural extra properties
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/objects.html

Can a value have more properties than a target type?

---

Structural assignment checks required compatible members.

Fresh literals additionally receive excess-property checks.

### type-value-spaces
- title: Type and value spaces
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/2/typeof-types.html

Why is `typeof` useful in a type expression?

---

Values and types are separate namespaces in TypeScript.

Type-query `typeof` obtains a value's type for a type expression.

### record-literal-keys
- title: Record literal keys
- version: Core
- level: intermediate
- status: verified
- source: https://www.typescriptlang.org/docs/handbook/utility-types.html

What does a literal-union Record require?

---

`Record` maps each key in its key type to the value type.

A literal-union key type describes those named properties.
