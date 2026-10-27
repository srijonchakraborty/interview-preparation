# JavaScript

### temporal-dead-zone
- title: let and const exist in a temporal dead zone
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let

What does this log, and why is it different from `var`?

```js
console.log(a);
let a = 1;
```

---

It throws a `ReferenceError`. `let` and `const` are block-scoped and hoisted, but they stay uninitialized from the start of the block until their declaration runs. That gap is the temporal dead zone. Reading or writing the binding there throws.

`var` hoists as `undefined` and is function-scoped, so the same pattern logs `undefined` instead of throwing. `typeof undeclared` is `"undefined"`, but `typeof` on a `let` binding still in the TDZ throws. Each iteration of `for (let i ...)` gets a fresh binding, which is why a closure inside that loop sees the right `i`.

### arrow-this
- title: Arrow functions capture this lexically
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions

A method is defined as a class field arrow function, and another is a normal method passed to `setTimeout`. Which one still sees the instance, and which tricks fail on an arrow function?

---

An arrow function does not bind its own `this`, `arguments`, or `super`. It uses the enclosing lexical `this`. `call`, `apply`, and `bind` cannot change that `this`. It also cannot be used as a constructor: `new` throws.

A normal method gets `this` from the call site. Passing `obj.method` to `setTimeout` calls it with a different receiver, so `this` is not the instance. A class-field arrow is created per instance and closes over the instance `this`, so it survives being passed as a callback. That also means it is not shared on the prototype.

### promise-states
- title: Fulfilled, rejected, and resolved are not the same word
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise

Name the states of a promise. Why can a promise be resolved and still not be fulfilled?

---

A promise is **pending**, then **fulfilled** with a value, or **rejected** with a reason. Fulfilled and rejected are both **settled**. A settled promise never changes state.

**Resolved** means it is locked to a value or to another thenable. If you resolve a promise with a thenable, it stays pending until that thenable settles, then adopts its state. So "resolved" does not always mean "fulfilled". `then` and `catch` return new promises. Errors thrown inside an executor reject the promise.

### modules
- title: What an ES module changes about scope and loading
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules

How is a `<script type="module">` different from a classic script? What does `export` actually share?

---

Modules are always strict mode. They are deferred by default, run after the document is parsed, and execute once per URL. Top-level `this` is `undefined`, not `window`. Imports are live bindings and are read-only from the importer: if the exporter reassigns a `let`, importers see the new value, but they cannot assign to the import.

A module and a classic script do not share scope. `import` and `export` are syntax, not function calls, so they cannot be conditional. Cyclic imports are allowed but easy to observe before initialization. Use modules for application code; do not expect module scope to see globals created by a later classic script unless they are real global properties.

### async-await
- title: async functions return a promise
- version: ES2017
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function

What does an `async` function return if you `return 1`, if you `throw`, and if you `await` a rejection without `try/catch`?

---

An `async` function always returns a promise. `return 1` fulfills that promise with `1`. A thrown exception, or an `await` of a rejection that you do not catch, rejects the returned promise. `await` pauses that function until the awaited promise settles, then resumes it as a microtask. It does not block the thread or the call stack.

`try/catch` around `await` catches the rejection. Without it, the caller must handle the returned promise. `await` on a non-promise wraps the value in a fulfilled promise. Prefer `async/await` for sequential reads, and `Promise.all` when the operations are independent.

### optional-chaining
- title: Optional chaining stops on null or undefined only
- version: ES2020
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining

What do `user?.address?.city` and `user?.getName()` return when `user` is `null`? What if `user` exists but `getName` does not, and you wrote `user?.getName()`?

---

`?.` returns `undefined` instead of throwing when the base is `null` or `undefined`, and it skips the rest of the chain. It does not treat `0`, `""`, or `false` as missing.

`user?.getName` short-circuits only on `user`. If `user` exists and `getName` is missing, `user?.getName()` still tries to call `undefined` and throws. `user?.getName?.()` short-circuits the call too. Optional chaining does not replace a check you need when a missing value is a bug.

### nullish-coalescing
- title: ?? is not ||
- version: ES2020
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing

`count` is `0` and `label` is `""`. What do `count || 10` and `count ?? 10` return, and why does that show up in UI defaults?

---

`||` returns the right side for any falsy value: `0`, `""`, `false`, `NaN`, `null`, and `undefined`. `??` returns the right side only for `null` or `undefined`. So `0 || 10` is `10`, and `0 ?? 10` is `0`. An empty string is preserved by `??` and replaced by `||`.

Use `??` when `0` or `""` are legitimate values, which is common for counts, indexes, and text inputs. `||` still fits a "any empty value means missing" check. You cannot mix `??` and `||` without parentheses; the grammar makes that a syntax error.

### promise-allsettled
- title: all, allSettled, any, and race
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled

You fire five requests and need every result, including failures. Which combinator do you use, and what does the fulfilled value look like?

---

`Promise.allSettled` waits for every promise to settle and never short-circuits on rejection. Its fulfillment value is an array of outcome objects, in input order: `{ status: "fulfilled", value }` or `{ status: "rejected", reason }`.

`Promise.all` rejects on the first rejection and is the right tool when one failure should fail the batch. `Promise.any` fulfills with the first fulfillment and rejects with an `AggregateError` if all reject. `Promise.race` settles with whichever promise settles first, fulfillment or rejection. `allSettled` shipped in ES2020; `any` shipped in ES2021.

### top-level-await
- title: Top-level await blocks the module graph
- version: ES2022
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#top_level_await

Where is `await` legal at the top level, and what does it do to modules that import that file?

---

Top-level `await` is legal in ES modules, not in classic scripts and not in a non-module function body unless that function is `async`. The module waits for the promise before it finishes evaluating. Importers of that module wait too. Sibling modules that do not depend on it can still evaluate.

Use it for a one-time bootstrap dependency, such as loading config before exporting a client. Do not use it for optional work: it delays every dependent module and turns a rejected await into a module evaluation failure. Tests and tools must load the file as a module or the syntax is a parse error.

### class-fields
- title: Public and private class fields
- version: ES2022
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Public_class_fields

When do public field initializers run, and how is `#id` different from a `_id` convention?

---

Public instance fields are created on the instance, not the prototype. Base-class fields initialize before derived fields, and field initializers run at construction time before the constructor body continues. A field arrow closes over the instance `this`.

`#id` is a hard-private field. Code outside the class body cannot read it; a `._id` property is only a naming convention and is fully public. Private fields are not inherited as accessible bindings of the subclass body, and `obj.#id` throws if `obj` is not the right brand, rather than returning `undefined`.

### error-cause
- title: Chain errors with cause
- version: ES2022
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause

You catch a `TypeError` from `JSON.parse` and want the caller to see a domain error without losing the original. How do you attach it?

---

Pass a `cause` in the error options:

```js
throw new Error("Config file is not valid JSON", { cause: err });
```

Callers read `error.cause`. That keeps the low-level error for logs and gives the caller an error they can branch on. Do not stringify the original into the message and drop the object. `cause` can be any value, not only an `Error`. It does not replace `stack`; each error has its own stack, and the cause is a separate property.

### array-tosorted
- title: toSorted copies, sort mutates
- version: ES2023
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted

What is the bug in `users.sort(...)` inside a React render or a Redux reducer, and what does `toSorted` change? How does the default compare treat numbers?

---

`sort()`, `reverse()`, and `splice()` mutate the receiver and return it. That is a defect in React state, a Redux reducer, or any shared cache. ES2023 adds copying methods: `toSorted()`, `toReversed()`, `toSpliced()`, and `with(index, value)`. They return a new array and leave the original in place.

The default compare converts each value with `ToString`. `[1, 10, 2].sort()` becomes `[1, 10, 2]` because `"10" < "2"` is true (`"1"` is less than `"2"`). Numeric order needs an explicit compare, `(a, b) => a - b`, and `toSorted` uses that same compare.

### object-groupby
- title: Object.groupBy versus Map.groupBy
- version: ES2024
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy

You want to group orders by status string, and later by a customer object. Which grouping function fits each case?

---

`Object.groupBy(items, callback)` groups by the string key the callback returns. The result is a null-prototype object, so keys do not collide with `Object.prototype` names such as `toString` or `constructor`. Use it for string keys like status.

`Map.groupBy(items, callback)` returns a `Map`. Keys can be objects, because `Map` uses SameValueZero equality rather than string property names. Use it when the key is an object or you need to preserve non-string keys. Neither method mutates the input. Both shipped in ES2024.

### promise-withresolvers
- title: Promise.withResolvers avoids the executor assignment
- version: ES2024
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/withResolvers

Show the old pattern of assigning `resolve` outside a `Promise` constructor, and the ES2024 replacement. Does the new API change rejection behavior?

---

The old pattern leaks the resolver out of the executor:

```js
let resolve, reject;
const promise = new Promise((res, rej) => {
  resolve = res;
  reject = rej;
});
```

ES2024 replaces that with:

```js
const { promise, resolve, reject } = Promise.withResolvers();
```

The promise follows the same rules as any other promise: the first call to `resolve` or `reject` wins, resolving with a thenable adopts that thenable, and later calls are ignored. The helper only removes the awkward assignment. It does not add cancellation.
