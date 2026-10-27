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

### var-function-scope
- title: var is function-scoped and hoisted
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var

What is the scope of a `var` declared inside an `if` block, and what value does it have before the line that declares it?

---

A `var` is scoped to the nearest function, or to the global scope, not to the block. Its declaration is hoisted, so the variable exists from the top of that scope with the value `undefined` until the assignment runs. Redeclaring the same `var` is allowed.

The trap is a variable that leaks out of an `if` or `for` block and is shared by everything in the function. Prefer `let` and `const`, which are block-scoped and throw in the temporal dead zone instead of silently reading `undefined`.

### const-binding
- title: const freezes the binding, not the value
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const

If `const user = { name: "A" }`, can you run `user.name = "B"`? Can you run `user = {}`?

---

`const` creates a binding that cannot be reassigned, and it must be initialized in the declaration. `user = {}` throws a `TypeError`. The object itself is not immutable, so `user.name = "B"` works.

Interviewers use this to check that you separate the variable from the value it points to. If you need the object to stay unchanged, use `Object.freeze`, which is shallow.

### let-redeclaration
- title: let cannot be redeclared in the same scope
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let

What happens if you write `let x = 1; let x = 2;` in the same block? What about declaring `let x` inside a nested block?

---

Redeclaring a `let` in the same scope is a `SyntaxError`, reported before any code runs. Declaring `let x` inside a nested block is fine: it creates a new binding that shadows the outer one.

This catches accidental reuse of a name that `var` would allow silently. A `switch` statement body is one block, so two `case` clauses that each declare `let x` collide unless you wrap each case in braces.

### function-declaration-hoisting
- title: Function declarations are hoisted with their body
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function

Can you call a function on a line above its `function greet() {}` declaration? Why?

---

Yes. A function declaration is hoisted to the top of its enclosing function or global scope together with its body, so it can be called before the line where it appears.

That is different from a function expression assigned to a variable. With `var greet = function () {}`, only the `var` is hoisted, so an early call throws a `TypeError` because `greet` is `undefined`.

### function-expression-hoisting
- title: Function expressions are not hoisted
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function

What error do you get calling `const f = function () {}` before that line, and how does that differ from the same code with `var`?

---

Function expressions are not hoisted. With `const` or `let`, calling `f` before the declaration throws a `ReferenceError` because the binding is in the temporal dead zone. With `var`, the binding exists as `undefined`, so the call throws a `TypeError` saying `f` is not a function.

The error type tells you which declaration was used. Code that depends on call-before-define should use a function declaration on purpose, not rely on an accident of `var`.

### named-function-expression
- title: The name of a function expression is local to its body
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function

In `const fact = function inner(n) { ... }`, where can you use the name `inner`?

---

The name of a named function expression is bound only inside the function body. You can call `inner` recursively from inside, but `inner` is not defined in the surrounding scope.

This is useful for recursion that keeps working even if the outer variable is reassigned, and the name shows up in stack traces. Calling `inner()` from outside throws a `ReferenceError`.

### global-let-not-property
- title: Top-level let does not create a global property
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let

In a classic browser script, you write `var a = 1; let b = 2;` at the top level. What are `globalThis.a` and `globalThis.b`?

---

`globalThis.a` is `1`, because a top-level `var` in a script creates a property on the global object. `globalThis.b` is `undefined`, because top-level `let`, `const`, and `class` declarations do not create properties on `globalThis`.

Both are still global variables that other classic scripts can read by name. In a module, neither creates a global property, because module top-level code has its own scope.

### loop-closure-var
- title: Closures in a var loop share one variable
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures

What does this print, and what is the smallest fix?

```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i));
}
```

---

It prints `3` three times. All three callbacks close over the same function-scoped `i`, and by the time they run the loop has finished and `i` is `3`.

The smallest fix is `let i`. A `let` in a `for` head creates a new binding for each iteration, so each callback captures its own value. The older fix is an extra function that receives `i` as a parameter.

### strict-mode
- title: What strict mode changes
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode

Name three things `"use strict"` turns from silent mistakes into errors. Where is strict mode on without the directive?

---

Assigning to an undeclared variable throws a `ReferenceError` instead of creating a global. Assigning to a non-writable property throws a `TypeError` instead of failing silently. Duplicate parameter names and the `with` statement are syntax errors. In a plain function call, `this` is `undefined` instead of the global object.

Module code and class bodies are always strict, so you never need the directive there. The directive must be the first statement of a script or function to take effect.

### globalthis
- title: globalThis is the portable global object
- version: ES2020
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis

Library code must reach the global object in a browser page, a web worker, and Node.js. What do you use?

---

`globalThis` refers to the global object in every environment. Historically you had to pick `window` in pages, `self` in workers, or `global` in Node.js.

Use it instead of environment sniffing. Do not confuse it with module scope: top-level declarations in a module are not properties of `globalThis`.

### class-declaration-tdz
- title: Class declarations are in the temporal dead zone
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/class

Can you write `new User()` above `class User {}` the way you can call a hoisted function declaration?

---

No. A class declaration is hoisted like `let`: the binding exists but is uninitialized until the declaration runs. Using it earlier throws a `ReferenceError`.

That is the main difference from function declarations, which are usable before their line. Order class declarations before code that instantiates them, including subclasses that `extends` them.

### closure-definition
- title: What a closure is
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures

Define a closure in one sentence, and show a function that uses one.

---

A closure is a function bundled together with references to its surrounding state, the lexical environment. An inner function can read and update variables of the outer function even after the outer function has returned.

```js
function makeAdder(x) {
  return (y) => x + y;
}
const add5 = makeAdder(5);
```

A closure captures variables, not snapshots of values. If the outer variable changes later, the inner function sees the new value. Closures are created every time a function is created.

### closure-private-state
- title: Closures can hide state
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures

Build a counter whose count cannot be changed from outside except through `increment`. Do two counters share a count?

---

Keep the count in a local variable of a factory function and return functions that close over it:

```js
function makeCounter() {
  let count = 0;
  return { increment: () => ++count, value: () => count };
}
```

Each call to `makeCounter` creates a new lexical environment, so two counters have independent counts. This is the module pattern, and it is how private state was emulated before private class fields.

### closure-method-cost
- title: Methods created in a constructor cost memory per instance
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures

You define methods by assigning functions to `this` inside a constructor. What is the cost compared with methods on the prototype?

---

Every construction creates new function objects and closures for those methods. Methods on the prototype are created once and shared by all instances.

Creating closures inside other functions when you do not need them hurts both processing speed and memory use. Put shared behavior on the prototype or in a class body, and only use per-instance closures when each instance truly needs private captured state.

### iife
- title: Immediately invoked function expressions
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Glossary/IIFE

What is `(function () { ... })();` for, and why do you see it less in modern code?

---

It is an IIFE, a function expression that runs as soon as it is defined. Its variables live in the function scope and do not pollute the enclosing or global scope.

Block-scoped `let` and `const` and ES modules now give you a private scope without the wrapper. You still see IIFEs in older bundles and for running `async` code at the top of a classic script.

### this-call-site
- title: this depends on how a function is called
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this

`const f = obj.method; f();` What is `this` inside `method` in strict mode, and in sloppy mode?

---

For a normal function, `this` is decided at the call site. `obj.method()` sets `this` to `obj`. Calling the extracted `f()` has no receiver: `this` is `undefined` in strict mode and the global object in sloppy mode.

That is why passing a method as a callback loses its object. Fix it with `bind`, a wrapping arrow function, or a class-field arrow.

### function-bind
- title: bind returns a new function
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind

What does `fn.bind(obj, 1)` return, and what does the `1` do?

---

`bind` returns a new bound function. When it is called, `this` is `obj` and `1` is inserted before any arguments passed at call time. The original `fn` is unchanged.

Extra arguments give partial application. Each `bind` call creates a new function, so binding inside a render or an `addEventListener` call means you need to keep the reference if you want to remove the listener later.

### call-vs-apply
- title: call versus apply
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply

What is the difference between `fn.call(obj, a, b)` and `fn.apply(obj, [a, b])`?

---

Both call `fn` immediately with `this` set to `obj`. `call` takes the arguments one by one. `apply` takes them as a single array or array-like object.

With spread syntax, `fn.call(obj, ...args)` covers most uses of `apply`. Neither changes `this` for an arrow function.

### bind-twice
- title: A bound function cannot be rebound
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind

`const g = f.bind(a).bind(b);` What is `this` when `g()` runs?

---

`this` is `a`. Binding an already bound function creates another bound function, but its new `this` value is ignored because the target already has a bound `this`. Extra arguments from the second `bind` are still appended.

The exception is `new`: calling a bound function with `new` ignores the bound `this` and constructs a new object instead.

### new-operator
- title: What new does
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new

List the steps `new Foo()` performs. What happens if `Foo` returns `{ x: 1 }`? What if it returns `5`?

---

`new` creates a blank object, sets its prototype to `Foo.prototype`, runs `Foo` with `this` bound to that object, and returns the object.

If the constructor returns an object, that object is the result instead. If it returns a primitive such as `5`, the return value is ignored and the new object is returned.

### arrow-no-arguments
- title: Arrow functions have no arguments object
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions

Inside an arrow function you read `arguments`. What do you get, and what should you write instead?

---

Arrow functions do not have their own `arguments`. The name resolves to the `arguments` of the nearest enclosing normal function, or throws a `ReferenceError` if there is none.

Use rest parameters, `(...args) => args.length`, which give a real array.

### arrow-as-method
- title: An arrow function as an object method
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions

`const obj = { n: 1, get: () => this.n };` What does `obj.get()` return, and why?

---

It does not return `1`. An arrow function has no `this` of its own, so `this` is whatever it was where the object literal was written, often `undefined` in a module or the global object in a sloppy script.

Arrow functions are best for non-method functions. Use method shorthand, `get() { return this.n; }`, when the function needs the object as `this`.

### prototype-chain
- title: Property lookup walks the prototype chain
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain

When you read `obj.x` and `obj` has no own `x`, what does JavaScript do?

---

Every object has an internal link to another object, its prototype. If `obj` has no own `x`, the lookup continues on the prototype, then that object's prototype, until it finds `x` or reaches `null`. If it reaches `null`, the result is `undefined`.

That is how arrays get `map` from `Array.prototype`. Long chains cost lookup time, and a missing property walks the whole chain.

### prototype-vs-proto
- title: prototype versus the object's prototype
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain

What is the difference between `Foo.prototype` and `Object.getPrototypeOf(foo)` where `foo = new Foo()`?

---

`Foo.prototype` is an ordinary property of the constructor function. It is the object that becomes the prototype of instances created with `new Foo()`. `Object.getPrototypeOf(foo)` reads the actual prototype of `foo`, which is `Foo.prototype` here.

So `Foo.prototype` is not the prototype of `Foo` itself; that is `Function.prototype`. Prefer `Object.getPrototypeOf` over the `__proto__` accessor.

### object-create
- title: Object.create sets the prototype directly
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create

How do you make a new object whose prototype is `animal` without writing a constructor?

---

`Object.create(animal)` returns a new empty object whose prototype is `animal`. An optional second argument takes property descriptors, the same shape as `Object.defineProperties`.

It is the direct way to build a prototype chain. Properties set on the new object shadow those on `animal`; reads that miss fall through to `animal`.

### object-create-null
- title: Object.create(null) makes a dictionary with no prototype
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create

Why would you create a lookup table with `Object.create(null)` instead of `{}`?

---

An object made with `Object.create(null)` has no prototype. It does not inherit `toString`, `hasOwnProperty`, or `constructor`, so a key like `"constructor"` cannot collide with an inherited property.

The cost is that inherited methods are missing: `String(obj)` and `obj.hasOwnProperty(k)` throw. Use `Object.hasOwn` with it, or use a `Map` when keys come from user input.

### object-hasown
- title: Object.hasOwn replaces hasOwnProperty
- version: ES2022
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn

Why is `Object.hasOwn(obj, "id")` recommended over `obj.hasOwnProperty("id")`?

---

`Object.hasOwn` returns `true` if the property is an own property of the object, without looking up the prototype chain. It is a static method, so it works on objects created with `Object.create(null)` and on objects that override `hasOwnProperty`.

`obj.hasOwnProperty` is inherited from `Object.prototype`, so it can be missing or shadowed.

### instanceof-check
- title: How instanceof decides
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof

What does `x instanceof Foo` actually check, and why can it fail for an array from an iframe?

---

It checks whether `Foo.prototype` appears anywhere in the prototype chain of `x`. A class can customize the check with a static `Symbol.hasInstance` method.

Each realm, such as an iframe, has its own built-ins, so an array from another frame is not `instanceof` this frame's `Array`. Use `Array.isArray` for arrays. Changing an object's prototype after creation also changes the result.

### setprototypeof-cost
- title: Changing a prototype after creation is slow
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/setPrototypeOf

Why does MDN warn against `Object.setPrototypeOf` on existing objects, and what do you use instead?

---

Changing the prototype of an existing object is a very slow operation in every engine, because engines optimize property access based on an object's shape and prototype. The slowdown can spread to any code that touches the object.

Set the prototype when the object is created, with `Object.create(proto)` or a class.

### property-shadowing
- title: Assigning a property shadows the prototype
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain

An object inherits `color` from its prototype. You write `obj.color = "red"`. Does the prototype change?

---

No. Assignment creates an own `color` property on `obj`, which shadows the inherited one. Other objects that share the prototype still see the old value.

Reads find the own property first. If you `delete obj.color`, reads fall back to the prototype value again.

### for-in-inherited
- title: for...in includes inherited enumerable keys
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in

Why can `for...in` give you keys you did not put on the object, and what do you use for own keys only?

---

`for...in` iterates every enumerable string-keyed property, including inherited ones from the prototype chain. It skips symbol keys.

Use `Object.keys(obj)` or `Object.entries(obj)` for own enumerable keys. For arrays, prefer `for...of` or a numeric loop, because `for...in` visits keys as strings and can include extra properties.

### class-is-function
- title: A class is a special function
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes

What is `typeof` a class, and where do its methods live?

---

`typeof` a class is `"function"`. Classes are built on prototypes: methods declared in the class body go on `ClassName.prototype` and are shared by all instances.

Unlike an old constructor function, a class cannot be called without `new`; doing so throws a `TypeError`. Class bodies are always strict mode.

### super-before-this
- title: Call super before using this
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/constructor

In a derived class constructor you set `this.name` before calling `super()`. What happens?

---

It throws a `ReferenceError`. In a derived class, `this` is not initialized until `super()` returns, because the parent constructor creates the object.

If a derived class has no constructor, the default one calls `super(...args)` for you. A derived constructor that never calls `super()` and does not return an object also throws.

### static-methods
- title: Static methods belong to the class
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static

Given `class User { static create() {} }`, can you call `new User().create()`?

---

No. A static method is a property of the class itself, so you call `User.create()`. Instances do not have it.

Static methods are for factories and helpers related to the class. Inside a static method, `this` is the class it was called on, which lets subclasses inherit static factories.

### static-blocks
- title: Static initialization blocks
- version: ES2022
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Static_initialization_blocks

What is a `static { }` block in a class, and when does it run?

---

A static block runs once, when the class is evaluated, with `this` set to the class. It can contain statements such as `try/catch`, and it can read private fields of the class.

A class can have several static blocks. They run in order with static field initializers. Use them for setup that is more than a single expression.

### private-methods
- title: Private methods and accessors
- version: ES2022
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_properties

How do you declare a method that code outside the class cannot call?

---

Prefix the name with `#`: `#validate() {}`. Private methods, getters, setters, and static members are accessible only inside the class body. Referencing them outside is a syntax error.

This is enforced by the language, not by convention. Subclasses cannot access a parent's private names either.

### private-in
- title: Brand checks with #field in obj
- version: ES2022
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_properties

A static `equals(a, b)` method reads `a.#id`. How do you check that `a` is an instance with that private field without a `try/catch`?

---

Use `#id in a`. It returns `true` if the object has the private field and `false` otherwise, without throwing.

Reading `a.#id` on an object without that field throws a `TypeError`. The `in` form is a brand check that works even when the prototype chain has been tampered with, unlike `instanceof`.

### getter-setter
- title: get and set define accessor properties
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get

What does `get fullName() {}` in an object or class do, and how do you read it?

---

`get` binds a property to a function that runs when the property is read. You read it like a field, `user.fullName`, without parentheses. A matching `set` runs on assignment.

A getter with no setter is read-only: assignment is ignored, or throws in strict mode. Getters run on every read, so keep them cheap.

### extends-builtins
- title: Extending built-ins like Array
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/extends

You write `class Stack extends Array {}`. What type does `stack.map(...)` return?

---

It returns a `Stack`. Array methods that create a new array use `Symbol.species` to pick the constructor, which defaults to the subclass.

`extends` works with built-ins such as `Array`, `Error`, and `Map`. If you want derived methods to return plain arrays, override the static `Symbol.species` getter.

### new-target
- title: new.target detects how a function was called
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new.target

How can a base class throw if someone writes `new Shape()` directly but still allow `new Circle()`?

---

Check `new.target` in the constructor. It refers to the constructor that `new` was called on, so in `new Circle()` it is `Circle` even inside `Shape`'s constructor.

```js
if (new.target === Shape) throw new TypeError("abstract");
```

In a normal function call, `new.target` is `undefined`, which also lets a function detect a missing `new`.

### default-vs-named-export
- title: Default versus named exports
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export

How many default exports can a module have, and how does importing a default differ from importing a named export?

---

A module can have many named exports but at most one default export. Named imports must use the exported name, `import { parse } from "./x.js"`, or rename with `as`. A default import can use any local name, `import anything from "./x.js"`.

Named exports make renames visible to tooling and catch typos at link time. Teams often prefer them for that reason.

### import-hoisting
- title: import declarations are hoisted
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import

You put `console.log("start")` above an `import` line. Does the log run before the imported module's code?

---

No. `import` declarations are hoisted, and the module graph is loaded and linked before the importing module runs. The imported module's top-level code runs first.

`import` must appear at the top level of a module, not inside a function or `if`. For conditional or lazy loading, use dynamic `import()`.

### dynamic-import
- title: import() loads a module on demand
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import

How do you load a module only when a user opens a settings panel, and what does the call return?

---

Call `import("./settings.js")`. It returns a promise that fulfills with the module namespace object, whose properties are the module's exports, including `default`.

Unlike the `import` declaration, `import()` can be used anywhere, with a computed specifier, and even in classic scripts.

### import-meta
- title: import.meta.url
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import.meta

How does a module find the URL of a file that sits next to it?

---

`import.meta` is an object with metadata about the current module. `import.meta.url` is the module's full URL, so `new URL("./data.json", import.meta.url)` resolves a sibling file.

`import.meta` is only valid inside modules. Using it in a classic script is a syntax error.

### namespace-import
- title: import * gives a namespace object
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import

After `import * as utils from "./utils.js"`, can you add or reassign `utils.format`?

---

No. `utils` is a module namespace object. Its properties are live bindings to the module's exports, and you cannot add, delete, or assign properties on it.

The default export appears as `utils.default`. Use the namespace form when you want to group many exports under one name.

### export-from
- title: Re-exporting with export from
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export

How do you build an `index.js` that re-exports `Button` from `./button.js`? Is `Button` then usable inside `index.js`?

---

Write `export { Button } from "./button.js";`. It re-exports the binding without creating a local variable, so `Button` is not in scope inside `index.js` unless you also import it.

`export * from "./mod.js"` re-exports all named exports but not the default export. Re-export the default explicitly with `export { default } from "./mod.js"`.

### module-cycles
- title: Cyclic imports
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules

Module A imports B, and B imports A. Is that an error? When does it break?

---

Cyclic imports are allowed. Because imports are live bindings, each module can refer to the other's exports, but a module that reads an import during its top-level evaluation can hit a binding that is not initialized yet and get a `ReferenceError`.

Cycles work when the other module's exports are only used later, such as inside functions called after loading. If a cycle breaks at startup, move shared code into a third module.

### then-returns-promise
- title: then returns a new promise
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then

In `p.then(f).then(g)`, what does `g` receive if `f` returns `5`, returns a promise, or throws?

---

`then` returns a new promise. If `f` returns `5`, that promise fulfills with `5` and `g` receives `5`. If `f` returns a promise, the new promise adopts its eventual state. If `f` throws, the new promise rejects, and `g` is skipped unless it is a rejection handler.

That is why chains flatten. Each step must return the value or promise the next step needs.

### catch-is-then
- title: catch is then with only a rejection handler
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/catch

Does the chain stop after a `.catch()`? What does `p.catch(f).then(g)` do when `p` rejects?

---

`catch(f)` is shorthand for `then(undefined, f)` and returns a new promise. If `f` returns normally, that promise fulfills with the return value, so `g` runs.

To keep the chain rejected, rethrow inside the handler. Put `catch` at the end of a chain to handle any earlier failure.

### promise-all
- title: Promise.all fails fast
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all

What does `Promise.all([a, b, c])` fulfill with, and what happens if `b` rejects?

---

It fulfills with an array of the fulfillment values, in the input order, not the order they finished. If any input rejects, the returned promise rejects with that first rejection reason.

The other operations keep running; `Promise.all` does not cancel them. Non-promise values in the input are treated as already fulfilled.

### promise-race
- title: Promise.race settles with the first to settle
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race

How would you add a timeout to a fetch with `Promise.race`, and what does `Promise.race([])` do?

---

Race the request against a promise that rejects after a delay. `Promise.race` settles with the state of the first input promise to settle, whether it fulfills or rejects.

With an empty iterable, the returned promise stays pending forever. The losing request still runs; racing does not abort it.

### promise-resolve
- title: Promise.resolve and thenables
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/resolve

What does `Promise.resolve(x)` return when `x` is already a native promise, and when `x` is an object with a `then` method?

---

If `x` is a native promise, `Promise.resolve(x)` returns `x` itself. If `x` is a thenable, the returned promise follows it, calling its `then` method to adopt its state. Any other value gives a promise fulfilled with that value.

This is how promise code interoperates with other promise libraries. Do not create objects with an accidental `then` method, because they will be treated as thenables.

### executor-sync
- title: The Promise executor runs synchronously
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/Promise

In what order do these log?

```js
new Promise((r) => { console.log(1); r(); }).then(() => console.log(3));
console.log(2);
```

---

`1`, `2`, `3`. The executor function runs synchronously inside the `Promise` constructor. The `then` callback is always called asynchronously, even when the promise is already resolved.

If the executor throws, the promise rejects. Calling `resolve` or `reject` again after the first time has no effect.

### unhandled-rejection
- title: Unhandled rejections
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises

A promise rejects and nothing handles it. What happens in a browser, and how can you log every case?

---

The browser fires an `unhandledrejection` event on the global scope. If a handler is attached later, a `rejectionhandled` event fires. Listening for `unhandledrejection` lets you report errors that no `catch` handled.

Node.js has its own `unhandledRejection` process event. The real fix is to return promises from functions and end chains with a `catch`.

### forgotten-return
- title: Forgetting to return inside then
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises

What goes wrong here?

```js
fetchUser().then((u) => { fetchOrders(u.id); }).then((orders) => render(orders));
```

---

The first handler calls `fetchOrders` but does not return its promise. The chain continues immediately with `undefined`, so `render` gets `undefined`, and a rejection from `fetchOrders` is not caught by the chain.

Always return the inner promise, or use an expression-bodied arrow. This floating promise is one of the most common promise mistakes.

### then-second-argument
- title: then(onFulfilled, onRejected) versus catch
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then

What is the difference between `p.then(ok, fail)` and `p.then(ok).catch(fail)`?

---

In `p.then(ok, fail)`, `fail` handles only a rejection of `p`. If `ok` throws, `fail` does not see it, and the returned promise rejects.

In `p.then(ok).catch(fail)`, `fail` handles a rejection of `p` and also an error thrown in `ok`. Use the two-argument form only when you deliberately want to handle the source failure separately.

### sequential-await
- title: await in a loop runs one at a time
- version: ES2017
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises

A loop does `for (const id of ids) await fetchItem(id);`. Ten items take ten times as long as one. How do you run them concurrently?

---

Each `await` waits for the previous request before starting the next. Start them all first and wait once:

```js
const items = await Promise.all(ids.map(fetchItem));
```

Keep the sequential loop when each step depends on the previous one or you must limit load on a server. Use `Promise.allSettled` if one failure should not hide the other results.

### foreach-async
- title: forEach does not wait for async callbacks
- version: ES2017
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach

Why does `items.forEach(async (x) => await save(x)); console.log("done");` log `done` before the saves finish?

---

`forEach` expects a synchronous function and ignores its return value. An async callback returns a promise that `forEach` discards, so nothing waits for it.

Use `for...of` with `await` for sequential work, or `await Promise.all(items.map(save))` for concurrent work.

### try-catch-no-await
- title: try/catch only catches awaited rejections
- version: ES2017
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await

Inside an `async` function, `try { return load(); } catch (e) { return fallback; }`. If `load()` rejects, do you get the fallback?

---

No. `return load()` returns the promise without waiting, so the rejection happens after the `try` block has exited and the `catch` never runs. The caller sees the rejection.

Write `return await load();` inside `try` when you want the local `catch` to handle the failure. Outside a `try`, `return await` and `return` behave the same for the caller.

### microtask-order
- title: Sync code, then microtasks, then tasks
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide

What order do these log?

```js
setTimeout(() => console.log("timeout"));
Promise.resolve().then(() => console.log("promise"));
console.log("sync");
```

---

`sync`, `promise`, `timeout`. The synchronous code finishes first. Promise callbacks are microtasks, which run as soon as the current task and call stack are done. The `setTimeout` callback is a task and runs in a later turn of the event loop.

This ordering question is a staple. The key rule is that the microtask queue is drained before the next task starts.

### task-vs-microtask
- title: Tasks versus microtasks
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide

What is the difference between a task and a microtask, and what happens to microtasks queued while microtasks are running?

---

A task is scheduled work such as running a script, a `setTimeout` callback, or an event handler. A microtask is a short function queued by promise reactions or `queueMicrotask`. After each task, the event loop runs every microtask in the queue before the next task or rendering.

Microtasks queued by other microtasks are added to the same queue and run in the same drain. That is why a loop of microtasks can delay timers and rendering.

### settimeout-zero-delay
- title: setTimeout with 0 is not immediate
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout

Does `setTimeout(fn, 0)` run `fn` right away?

---

No. It schedules `fn` to run after at least the delay, as a later task. It cannot run until the current call stack is empty and pending microtasks have run, and the actual delay can be longer than requested.

Browsers clamp nested timeouts to a minimum delay and may throttle timers in background tabs. Use it to yield to the event loop, not for precise timing.

### run-to-completion
- title: Run to completion
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model

Can a click handler interrupt a long synchronous loop that is already running?

---

No. Each job runs to completion before another job starts, so a running function cannot be preempted by other JavaScript on the same thread.

That makes reasoning about shared state simple, but a long synchronous loop blocks event handling and rendering until it ends. Split heavy work into chunks or move it to a worker.

### microtask-starvation
- title: Microtasks can starve the event loop
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide

A function queues a microtask that queues itself again forever. What happens to timers and page rendering?

---

They never get a turn. The event loop keeps draining the microtask queue while it is not empty, and new microtasks are added to the same queue, so the next task and rendering are blocked.

Use a task such as `setTimeout` when you want to yield to the browser. Use `queueMicrotask` only for short work that must run before control returns to the event loop.

### iterable-protocol
- title: The iterable protocol
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols

What makes an object usable in `for...of` and spread?

---

The object must be iterable: it has a method under the key `Symbol.iterator` that returns an iterator. Arrays, strings, `Map`, `Set`, and `arguments` are built-in iterables.

Plain objects are not iterable, so `for (const x of {})` throws a `TypeError`. Use `Object.entries(obj)` to iterate an object's own properties.

### iterator-protocol
- title: The iterator protocol
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols

Write the minimal object that `for...of` can consume to produce `1, 2, 3`.

---

An iterator has a `next()` method that returns objects shaped `{ value, done }`. Iteration stops when `done` is `true`.

```js
const it = {
  [Symbol.iterator]() {
    let n = 0;
    return { next: () => (n < 3 ? { value: ++n, done: false } : { value: undefined, done: true }) };
  },
};
```

A generator function is the shorter way to write the same thing.

### for-of-vs-for-in
- title: for...of versus for...in
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of

On `["a", "b"]`, what does `for...in` give you, and what does `for...of` give you?

---

`for...in` gives the enumerable property keys as strings, `"0"` and `"1"`, including inherited enumerable keys. `for...of` uses the iterable protocol and gives the values, `"a"` and `"b"`.

Use `for...of` for arrays, strings, maps, and sets. Use `for...in` only when you need the keys of a plain object, and prefer `Object.keys` if inherited keys matter.

### generator-function
- title: Generator functions pause at yield
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*

What does calling a `function*` return, and when does its body start running?

---

Calling a generator function does not run its body. It returns a generator object, which is an iterator. Each `next()` call runs the body until the next `yield`, then pauses and returns `{ value, done: false }`.

When the body returns, `next()` returns `{ value: returnValue, done: true }`. Generators make lazy and infinite sequences easy to write.

### generator-return
- title: generator.return() and finally
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator/return

What does `gen.return(5)` do to a paused generator that is inside a `try` with a `finally` block?

---

`return(5)` acts as if a `return 5` statement were inserted at the paused point. The generator finishes and returns `{ value: 5, done: true }`.

If the paused point is inside `try...finally`, the `finally` block runs first. If `finally` yields, the generator is not finished yet and `return` gives that yielded value instead.

### yield-delegation
- title: yield* delegates to another iterable
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/yield*

What does `yield* other()` do inside a generator, and what is the value of the `yield*` expression?

---

`yield*` delegates to another iterable or generator: it yields each of its values in turn. Calls to `next()` on the outer generator are forwarded to the inner one.

The value of the `yield*` expression is the inner generator's return value, the `value` of its final `done: true` result. It works with any iterable, such as `yield* [1, 2]`.

### generator-next-value
- title: next(value) resumes yield with a value
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator/next

In `const x = yield 1;`, what sets `x`? Why is the argument to the first `next()` ignored?

---

The argument passed to the next call of `next(value)` becomes the result of the paused `yield` expression, so it is assigned to `x`.

The first `next()` starts the generator and runs to the first `yield`. There is no paused `yield` yet to receive a value, so its argument is ignored.

### spread-iterables
- title: Spread uses the iterable protocol
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax

Why does `[...new Set([1, 1, 2])]` work but `[...{ a: 1 }]` throws?

---

Spread in an array literal or function call iterates its operand. A `Set` is iterable, so it expands to `[1, 2]`. A plain object is not iterable, so array spread throws a `TypeError`.

Object spread, `{ ...obj }`, is different: it copies own enumerable properties and does not need an iterable.

### iterator-return-on-break
- title: break calls the iterator's return method
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols

A generator holds a resource in `try...finally`. A `for...of` loop over it hits `break`. Does the `finally` run?

---

Yes. When a `for...of` loop exits early through `break`, `return`, or a thrown error, it calls the iterator's `return()` method if it has one. For a generator, that runs pending `finally` blocks.

Custom iterators should implement `return()` when they hold resources such as file handles.

### generator-iterate-once
- title: A generator object can be consumed only once
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator

`const g = gen();` You spread `[...g]` twice. Why is the second array empty?

---

A generator object is an iterator, and its `Symbol.iterator` method returns the generator itself. The first spread runs it to completion. The second spread gets the same finished iterator, so it yields nothing.

To iterate again, call the generator function again, or return an object whose `Symbol.iterator` method creates a new generator each time.

### map-vs-object
- title: Map versus plain object
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map

When do you use a `Map` instead of an object for key-value data?

---

A `Map` accepts keys of any type, including objects and functions, has no default keys from a prototype, keeps insertion order, and has a `size` property. It is iterable directly and performs better for frequent additions and removals.

Use a plain object for a fixed record shape or data you send as JSON. `JSON.stringify` does not serialize a `Map`'s entries.

### map-key-equality
- title: Map keys use SameValueZero
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map

After `m.set({ id: 1 }, "a")`, what is `m.get({ id: 1 })`? And can `NaN` be a key?

---

`undefined`. Map keys are compared with SameValueZero, so objects match only by identity, and a new object literal is a different key. Keep the original reference to look it up.

SameValueZero treats `NaN` as equal to `NaN`, so `NaN` works as a key, and `+0` and `-0` are the same key.

### set-dedupe
- title: Remove duplicates with a Set
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set

How do you remove duplicate values from an array in one line? Does it dedupe objects with the same content?

---

`[...new Set(arr)]`. A `Set` stores each value only once and keeps insertion order. It compares with SameValueZero, so primitives with the same value collapse.

Two different objects with equal content are still two values, because objects compare by identity. Dedupe objects by a key with a `Map` instead.

### weakmap-keys
- title: WeakMap holds keys weakly
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap

You cache data per DOM node. Why use a `WeakMap`, and why can't you iterate it?

---

A `WeakMap` does not keep its keys alive. When a key object is no longer reachable elsewhere, the entry can be garbage collected, so per-object caches do not leak.

Because entries can disappear at any time, a `WeakMap` is not enumerable: there is no `size`, `keys()`, or iteration. Keys must be objects or non-registered symbols, not strings.

### weakset-use
- title: WeakSet for tagging objects
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet

What can a `WeakSet` contain, and what is a good use for it?

---

A `WeakSet` holds objects or non-registered symbols, weakly. It only supports `add`, `has`, and `delete`, and it is not enumerable.

It fits "have I seen this object?" checks, such as marking visited nodes in a graph walk without keeping them alive after the walk ends.

### symbols-as-weakmap-keys
- title: Symbols as WeakMap keys
- version: ES2023
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap

ES2023 lets symbols be `WeakMap` keys. Which symbols are still rejected, and why?

---

Non-registered symbols, such as `Symbol("tag")`, can be keys. Registered symbols made with `Symbol.for` are rejected with a `TypeError`.

A registered symbol can always be recreated from its string with `Symbol.for`, so it is never garbage collected, which would make a weak key pointless.

### strict-vs-loose-equality
- title: === versus ==
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness

What is the difference between `===` and `==`, and which do you default to?

---

`===` compares without type conversion: different types are never equal. `==` converts operands to a common type before comparing, so `"1" == 1` is `true`.

Default to `===`. A common deliberate use of `==` is `x == null`, which matches both `null` and `undefined`.

### nan-not-equal
- title: NaN is not equal to itself
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN

`const x = NaN;` What is `x === x`, and how do you test for `NaN`?

---

`x === x` is `false`. `NaN` compares unequal to every value, including itself, with both `==` and `===`.

Test with `Number.isNaN(x)` or `Object.is(x, NaN)`. `indexOf` uses strict equality and cannot find `NaN`.

### object-is
- title: Object.is versus ===
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is

In which two cases does `Object.is(a, b)` disagree with `a === b`?

---

`Object.is(NaN, NaN)` is `true`, while `NaN === NaN` is `false`. `Object.is(+0, -0)` is `false`, while `+0 === -0` is `true`. Otherwise they agree, and neither converts types.

Use it when you must tell `-0` from `+0` or need `NaN` to match itself.

### samevaluezero
- title: SameValueZero
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness

Which equality does `Map`, `Set`, and `includes` use, and how is it different from `===`?

---

They use SameValueZero. It is like `===` except that `NaN` equals `NaN`. Like `===`, it treats `+0` and `-0` as equal.

So `[NaN].includes(NaN)` is `true` while `[NaN].indexOf(NaN)` is `-1`, because `indexOf` uses strict equality.

### null-loose-equality
- title: null == undefined
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality

What are `null == undefined`, `null == 0`, and `null === undefined`?

---

`null == undefined` is `true`. `null == 0` is `false`: with `==`, `null` and `undefined` are equal only to each other. `null === undefined` is `false` because they are different types.

That makes `value == null` a short check for "missing". Write it on purpose and leave a comment, because linters often flag `==`.

### object-identity
- title: Objects compare by reference
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Strict_equality

Why is `{ a: 1 } === { a: 1 }` false, and how do you compare two objects by content?

---

When both operands are objects, `===` returns `true` only if they refer to the same object. Two literals create two objects, so they are not equal.

There is no built-in deep equality operator. Compare the fields you care about, or use a tested deep-equal function. `JSON.stringify` comparison breaks on key order and on values JSON cannot represent.

### addition-concatenation
- title: + concatenates if either side is a string
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Addition

What are `"1" + 2`, `1 + 2 + "3"`, and `"5" - 2`?

---

`"1" + 2` is `"12"`. `+` converts both operands to primitives, and if either is a string, it concatenates. `1 + 2 + "3"` evaluates left to right: `3 + "3"` is `"33"`.

`"5" - 2` is `3`, because `-` is numeric only. Convert inputs explicitly with `Number()` before adding values from forms.

### falsy-values
- title: The falsy values
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Glossary/Falsy

List the falsy values in JavaScript.

---

`false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN`. In browsers, `document.all` is also falsy for legacy reasons. Every other value is truthy.

The trap is that `0` and `""` are often valid data. Use `??` or explicit checks when only `null` and `undefined` mean missing.

### truthy-objects
- title: Empty arrays and objects are truthy
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Glossary/Truthy

Is `if ([])` taken? What about `if ("0")` and `if (new Boolean(false))`?

---

All three are taken. Every object is truthy, including empty arrays, empty objects, and wrapper objects such as `new Boolean(false)`. Non-empty strings, including `"0"` and `"false"`, are truthy.

Check `arr.length` for an empty array and `Object.keys(obj).length` for an empty object.

### symbol-toprimitive
- title: Symbol.toPrimitive controls conversion
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toPrimitive

How does an object decide what `+obj`, `` `${obj}` ``, and `obj + ""` produce?

---

If the object has a `Symbol.toPrimitive` method, JavaScript calls it with a hint: `"number"` for `+obj`, `"string"` for a template literal, and `"default"` for `obj + ""`. The method must return a primitive, or a `TypeError` is thrown.

Without it, conversion calls `valueOf` and `toString`, in an order chosen by the hint. `Date` uses this to turn `date + ""` into a string.

### loose-equality-algorithm
- title: How == converts operands
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality

Walk through `[] == false`. Why is it `true` when `[]` is truthy?

---

If the types match, `==` behaves like `===`. `null` and `undefined` equal only each other. If one operand is an object and the other a primitive, the object is converted to a primitive. Booleans are converted to numbers, and a string compared with a number is converted to a number.

So `false` becomes `0`, `[]` becomes `""`, and `""` becomes `0`. `0 == 0` is `true`. Truthiness is a different conversion from `==`, which is why `[]` is truthy yet `== false`.

### unary-plus
- title: Unary plus converts to a number
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Unary_plus

What are `+"42"`, `+""`, `+"4px"`, and `+true`?

---

`42`, `0`, `NaN`, and `1`. Unary `+` converts its operand to a number the same way `Number()` does: an empty or whitespace-only string is `0`, and any trailing garbage gives `NaN`.

Unary `+` on a BigInt throws a `TypeError`. Use `parseInt` or `parseFloat` when you want to read a leading number out of a string like `"4px"`.

### parseint-radix
- title: parseInt parses a prefix
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt

What are `parseInt("4px")`, `Number("4px")`, and `parseInt(0.0000005)`? Why pass a radix?

---

`parseInt("4px")` is `4`, because it parses digits until the first invalid character. `Number("4px")` is `NaN`. `parseInt(0.0000005)` is `5`, because the number is first converted to the string `"5e-7"`, and parsing stops at `e`.

Always pass a radix, such as `parseInt(s, 10)`, so input like `"0x1F"` is not read as hexadecimal by accident. Do not pass numbers to `parseInt`; use `Math.trunc` instead.

### typeof-null
- title: typeof null is "object"
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof

What is `typeof null`, and how do you check that a value is a non-null object?

---

`typeof null` is `"object"`. It is a bug from the first version of JavaScript that was kept for compatibility.

Check `value !== null && typeof value === "object"`. Functions report `"function"`, so include that case if callable objects count.

### typeof-function
- title: typeof for functions, classes, and arrays
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof

What does `typeof` return for a function, a class, and an array?

---

`"function"` for both a function and a class, because a class is a function. `"object"` for an array.

`typeof` cannot tell arrays from other objects. Use `Array.isArray`. `typeof` on an undeclared variable returns `"undefined"` instead of throwing.

### bigint-literal
- title: BigInt for integers beyond 2^53
- version: ES2020
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt

How do you create a BigInt, and what is `5n / 2n`?

---

Append `n` to an integer literal, `10n`, or call `BigInt(10)` without `new`. `typeof 10n` is `"bigint"`. BigInt represents integers of arbitrary size exactly.

`5n / 2n` is `2n`: division truncates toward zero, because BigInt has no fractional part. Use it for IDs or values that exceed `Number.MAX_SAFE_INTEGER`.

### bigint-mixing
- title: BigInt and Number do not mix in arithmetic
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt

What happens with `1n + 1`, `1n == 1`, `1n === 1`, and `JSON.stringify({ id: 1n })`?

---

`1n + 1` throws a `TypeError`: you must convert one side explicitly. `1n == 1` is `true` and `1n === 1` is `false`. Comparisons such as `1n < 2` work.

`JSON.stringify` throws a `TypeError` on a BigInt by default. `Math` methods do not accept BigInt. Converting a large BigInt to a Number can lose precision.

### finally-overrides-return
- title: return in finally wins
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch

What does this function return?

```js
function f() {
  try { return "try"; } finally { return "finally"; }
}
```

---

It returns `"finally"`. The `finally` block always runs, and a `return` inside it overrides the return value of `try` or `catch`. It also discards an exception thrown from `try` or `catch`.

Use `finally` for cleanup only. A `return` or `throw` inside it hides the real outcome and makes bugs hard to find.

### built-in-error-types
- title: Built-in error types
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error

Which error type do you get for calling `undefined()`, reading an undeclared variable, and `new Array(-1)`?

---

Calling a non-function throws a `TypeError`. Reading an undeclared variable throws a `ReferenceError`. `new Array(-1)` throws a `RangeError` because the length is invalid. Bad syntax passed to `eval` or `JSON.parse` throws a `SyntaxError`.

All of these inherit from `Error`, so they have `name` and `message`. Branch on `instanceof` for the type rather than parsing the message text.

### custom-error-class
- title: Custom error classes
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error

How do you define a `ValidationError` that callers can catch with `instanceof`?

---

Extend `Error`, pass the message to `super`, and set `name`:

```js
class ValidationError extends Error {
  constructor(message, options) {
    super(message, options);
    this.name = "ValidationError";
  }
}
```

Forwarding `options` keeps support for `cause`. Setting `name` makes logs and `toString()` show the right type.

### throw-any-value
- title: You can throw any value
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/throw

Is `throw "failed"` legal? Why do style guides say to throw `Error` objects?

---

It is legal: `throw` accepts any expression, and the value goes to the nearest `catch`. Execution of the current function stops.

A string has no stack trace and no `name` or `cause`, so it is harder to debug and to branch on. Throw an `Error` or a subclass.

### floating-point-sum
- title: Why 0.1 + 0.2 is not 0.3
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number

Why is `0.1 + 0.2 === 0.3` false, and how should you handle money?

---

JavaScript numbers are 64-bit IEEE 754 double-precision floating point. Values like `0.1` cannot be represented exactly in binary, so the sum is `0.30000000000000004`.

Compare floats with a tolerance, and store money as integer minor units such as cents. Format for display with `Intl.NumberFormat`.

### number-epsilon
- title: Number.EPSILON
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/EPSILON

What is `Number.EPSILON`, and is `Math.abs(a - b) < Number.EPSILON` a safe comparison for any two numbers?

---

`Number.EPSILON` is the difference between `1` and the smallest number greater than `1` that can be represented, about `2.22e-16`.

It is a reasonable tolerance only for values near `1`. For larger values, the gap between representable numbers grows, so scale the tolerance with the magnitude of the values you compare.

### max-safe-integer
- title: Number.MAX_SAFE_INTEGER
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER

What is the largest integer a Number can represent exactly, and what goes wrong above it?

---

`Number.MAX_SAFE_INTEGER` is `2^53 - 1`, which is `9007199254740991`. Above it, integers can no longer all be represented exactly, so `Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2` is `true`.

Large IDs from a database can be silently corrupted when parsed as numbers. Check with `Number.isSafeInteger`, and keep such IDs as strings or BigInt.

### isnan-vs-number-isnan
- title: isNaN versus Number.isNaN
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isNaN

What are `isNaN("abc")` and `Number.isNaN("abc")`?

---

`isNaN("abc")` is `true`, because the global `isNaN` converts its argument to a number first. `Number.isNaN("abc")` is `false`, because it does not convert and returns `true` only for the value `NaN`.

Prefer `Number.isNaN`. The global one answers "would this become NaN?", which is rarely the question.

### number-isinteger
- title: Number.isInteger does not convert
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isInteger

What are `Number.isInteger(5.0)`, `Number.isInteger("5")`, and `Number.isInteger(Infinity)`?

---

`true`, `false`, and `false`. `5.0` is the same number as `5`. A string is not a number and is not converted. `Infinity` and `NaN` are not integers.

Validate form input by converting with `Number()` first, then checking `Number.isInteger`.

### tofixed-string
- title: toFixed returns a string
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed

What type does `(1.5).toFixed(2)` return, and can you add its result to another number?

---

It returns the string `"1.50"`. Adding it with `+` concatenates instead of summing, so convert back with `Number()` if you need math.

Rounding works on the binary value of the number, so some results look wrong in decimal. Use `toFixed` for display, not for financial rounding.

### divide-by-zero
- title: Division by zero does not throw
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Infinity

What are `1 / 0`, `-1 / 0`, and `0 / 0` in JavaScript?

---

`Infinity`, `-Infinity`, and `NaN`. Number division by zero follows floating-point rules and does not throw.

Check with `Number.isFinite` before using a result. BigInt is different: `1n / 0n` throws a `RangeError`.

### string-immutability
- title: Strings are immutable
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Glossary/Primitive

`let s = "cat"; s[0] = "b";` What is `s` now? Does `s.toUpperCase()` change `s`?

---

`s` is still `"cat"`. Strings are primitives, and all primitives are immutable: the existing value cannot be altered. String methods such as `toUpperCase` return a new string.

Do not confuse the value with the variable. The variable can be reassigned to the new string: `s = s.toUpperCase()`.

### template-literal
- title: Template literals
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals

What can a backtick string do that a quoted string cannot?

---

Template literals support interpolation with `${expression}` and can span multiple lines without `\n`. The expression result is converted to a string.

Interpolation does not escape anything. Inserting user input into HTML with a template literal is an injection risk unless you escape it or use a safe API.

### tagged-template
- title: Tagged templates
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals

What does a tag function receive in ``sql`SELECT * FROM t WHERE id = ${id}` ``?

---

The tag function receives an array of the literal string parts as its first argument, then each substituted value as a separate argument. The strings array also has a `raw` property with the unprocessed text.

The tag returns any value, not necessarily a string. Libraries use tags to escape values, build queries with parameters, or parse a small language.

### string-raw
- title: String.raw keeps backslashes
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/raw

How do you write a Windows path like `C:\new\table` in a template literal without doubling every backslash?

---

Use the built-in tag ``String.raw`C:\new\table` ``. It returns the raw string, so escape sequences such as `\n` stay as a backslash followed by `n`. Substitutions with `${}` are still processed.

It is also handy for building regular expression sources that contain many backslashes.

### string-padstart
- title: padStart and padEnd
- version: ES2017
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padStart

How do you turn `"7"` into `"007"`, and what if the string is already longer than the target?

---

`"7".padStart(3, "0")` returns `"007"`. The first argument is the target length, and the pad string repeats and is truncated to fit. The default pad is a space.

If the string is already at or above the target length, it is returned unchanged. `padEnd` pads on the right.

### string-at
- title: String.prototype.at
- version: ES2022
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/at

How do you get the last character of a string with negative indexing?

---

`str.at(-1)`. `at` accepts negative integers, which count back from the end. An index out of range returns `undefined`.

`str[-1]` looks up a property named `"-1"` and is `undefined`. Like bracket access, `at` returns a single UTF-16 code unit, which can be half of an emoji.

### string-length-utf16
- title: length counts UTF-16 code units
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/length

Why is `"😀".length` equal to `2`? How do you count it as one?

---

`length` counts UTF-16 code units. Characters outside the Basic Multilingual Plane, such as most emoji, use two code units, a surrogate pair.

`[..."😀"].length` is `1`, because string iteration goes by code points. For what users see as one character, such as a flag or a family emoji, use `Intl.Segmenter` with grapheme granularity.

### string-includes
- title: includes, startsWith, and endsWith
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes

How do you check whether a string contains `"error"` regardless of case? What happens if you pass a regular expression to `includes`?

---

`includes` is case-sensitive, so compare lowercased strings: `msg.toLowerCase().includes("error")`. It returns a boolean, unlike `indexOf`.

Passing a regular expression to `includes`, `startsWith`, or `endsWith` throws a `TypeError`. Use `regex.test(str)` for patterns.

### slice-vs-substring
- title: slice versus substring
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/substring

What are `"hello".slice(-3)` and `"hello".substring(-3)`? What does `substring(4, 1)` do?

---

`slice(-3)` is `"llo"`: negative indexes count from the end. `substring(-3)` treats negative values as `0`, so it returns `"hello"`.

`substring(4, 1)` swaps the arguments when the start is greater than the end and returns `"ell"`. `slice(4, 1)` returns `""`. Prefer `slice` for predictable behavior.

### string-iswellformed
- title: isWellFormed and toWellFormed
- version: ES2024
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/isWellFormed

`encodeURIComponent` throws a `URIError` on some user text. What is wrong with the string, and what do ES2024 string methods offer?

---

The string contains a lone surrogate, half of a UTF-16 surrogate pair. `isWellFormed()` returns `false` for such strings. `toWellFormed()` returns a copy with each lone surrogate replaced by U+FFFD, the replacement character.

Check or repair strings before passing them to APIs that require well-formed Unicode, such as `encodeURIComponent` or `TextEncoder`.

### codepointat
- title: codePointAt versus charCodeAt
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/codePointAt

What is the difference between `"😀".charCodeAt(0)` and `"😀".codePointAt(0)`?

---

`charCodeAt(0)` returns the first UTF-16 code unit, which is only half of the emoji. `codePointAt(0)` returns the full Unicode code point when the index is at the start of a surrogate pair.

The reverse direction is `String.fromCodePoint`. Iterate with `for...of` to step through code points instead of code units.

### localecompare
- title: Sorting strings with localeCompare
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare

Why does `names.sort()` misplace `"émile"`, and what is the fix? What do you use for very large lists?

---

The default sort compares UTF-16 code units, not language rules. `names.sort((a, b) => a.localeCompare(b))` uses locale-aware comparison and returns a negative number, zero, or a positive number.

For many comparisons, create one `Intl.Collator` and use its `compare` function, which is faster than calling `localeCompare` repeatedly.

### regexp-v-flag
- title: The RegExp v flag
- version: ES2024
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/unicodeSets

What does the `v` flag add over the `u` flag?

---

The `v` flag enables `unicodeSets` mode. It includes everything `u` does and adds set operations in character classes, such as difference with `--` and intersection with `&&`, plus properties of strings like `\p{RGI_Emoji}`.

`u` and `v` cannot be used together. Some characters must be escaped inside `v`-mode character classes, so an old pattern may need edits before you add `v`.

### regexp-d-flag
- title: The RegExp d flag returns match indices
- version: ES2022
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/hasIndices

How do you get the start and end positions of each capture group from `exec`?

---

Add the `d` flag. The match result then has an `indices` property: an array of `[start, end]` pairs for the whole match and each capture group, with `indices.groups` for named groups.

The flag is off by default because it costs extra work. `regex.hasIndices` reports whether it is set.

### string-matchall
- title: String.prototype.matchAll
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll

`str.match(/(\w)=(\d)/g)` loses the capture groups. How do you get every match with its groups?

---

`str.matchAll(regex)` returns an iterator of match results, each with capture groups and `index`. Use `for...of` or spread it into an array.

The regular expression must have the `g` flag. Without it, `matchAll` throws a `TypeError`.

### regexp-lastindex
- title: A global regex remembers lastIndex
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test

`const re = /a/g;` Why does `re.test("a")` return `true` and then `false` on the second call?

---

With the `g` or `y` flag, `test` starts at `re.lastIndex` and updates it after a match. The second call starts at index `1`, finds nothing, returns `false`, and resets `lastIndex` to `0`.

Do not reuse a global regex for independent `test` calls. Drop the `g` flag, or reset `lastIndex` yourself.

### array-from
- title: Array.from
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from

How do you turn a `NodeList` into an array, and how do you build `[0, 1, 2, 3, 4]` in one call?

---

`Array.from(nodeList)` creates a new shallow-copied array from any iterable or array-like object. A second argument maps each element.

`Array.from({ length: 5 }, (_, i) => i)` builds `[0, 1, 2, 3, 4]`: the object is array-like because it has a `length`.

### array-of
- title: Array.of versus Array(n)
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/of

What is the difference between `Array(3)` and `Array.of(3)`?

---

`Array(3)` creates an array with `length` 3 and three empty slots. `Array.of(3)` creates `[3]`. `Array.of` always treats its arguments as elements.

The single-number case of the `Array` constructor is the trap. Array literals avoid it entirely.

### reduce-initial-value
- title: reduce and its initial value
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce

What does `[].reduce((a, b) => a + b)` do, and why should you usually pass an initial value?

---

It throws a `TypeError`, because an empty array with no initial value has nothing to start the accumulator with. Without an initial value, `reduce` uses the first element as the accumulator and starts at the second.

Passing an initial value, as in `reduce((sum, x) => sum + x, 0)`, makes empty arrays safe and fixes the accumulator type.

### find-vs-filter
- title: find versus filter
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/find

What do `find` and `filter` return when nothing matches?

---

`find` returns the first matching element, or `undefined` if none match, and stops at the first match. `filter` always returns a new array, which is empty when nothing matches.

Use `findIndex` when you need the position; it returns `-1` on no match. `find` returning `undefined` is ambiguous if the array itself contains `undefined`.

### array-findlast
- title: findLast and findLastIndex
- version: ES2023
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/findLast

How do you get the most recent matching entry in a log array without reversing it?

---

`log.findLast(predicate)` iterates from the end and returns the last element that matches, or `undefined`. `findLastIndex` returns its index, or `-1`.

That avoids `[...log].reverse().find(...)`, which copies the array.

### array-at
- title: Array.prototype.at
- version: ES2022
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/at

How do you read the last element of an array without `arr[arr.length - 1]`?

---

`arr.at(-1)`. `at` takes an integer, and a negative value counts back from the end. Out-of-range indexes return `undefined`.

`arr[-1]` reads a property named `"-1"`, which is `undefined` on normal arrays.

### array-with
- title: Array.prototype.with
- version: ES2023
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/with

How do you change index 2 of an array in React state without mutating it?

---

`arr.with(2, newValue)` returns a new array with that index replaced and leaves `arr` unchanged. Negative indexes count from the end.

Unlike bracket assignment, `with` throws a `RangeError` if the index is out of range instead of growing the array.

### sparse-arrays
- title: Empty slots in sparse arrays
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array

`const a = [1, , 3];` Does `a.forEach` visit index 1? Does `for...of`?

---

Index 1 is an empty slot, not an `undefined` element. Older methods such as `forEach`, `map`, and `filter` skip empty slots. `for...of`, spread, and newer methods such as `at` and `toSorted` treat them as `undefined`.

That inconsistency is why `Array(3).map((_, i) => i)` returns empty slots instead of `[0, 1, 2]`. Use `Array.from({ length: 3 }, ...)`.

### array-length-truncate
- title: Setting length truncates
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/length

What happens to `arr` after `arr.length = 0`? What about `arr.length = 10` on a three-element array?

---

Setting `length` smaller deletes the elements past the new length, so `arr.length = 0` empties the array in place. Every reference to that array sees it empty.

Setting `length` larger adds empty slots, not `undefined` elements. Prefer creating a new array when other code should keep the old contents.

### splice-vs-slice
- title: splice versus slice
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/splice

What is the difference between `arr.slice(1, 3)` and `arr.splice(1, 3)`?

---

`slice(1, 3)` returns a shallow copy of elements from index 1 up to, but not including, 3, and leaves `arr` unchanged. `splice(1, 3)` removes three elements starting at index 1 from `arr` in place and returns the removed elements.

`splice` can also insert. Use `toSpliced` when you need the splice result as a new array without mutation.

### map-parseint
- title: ["1", "2", "3"].map(parseInt)
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map

What does `["1", "2", "3"].map(parseInt)` return, and why?

---

`[1, NaN, NaN]`. `map` calls its callback with the element, the index, and the array. `parseInt` treats the second argument as a radix, so it runs `parseInt("2", 1)` and `parseInt("3", 2)`, which are `NaN`.

Pass a wrapper that only forwards what you mean: `arr.map((s) => parseInt(s, 10))`, or use `arr.map(Number)`.

### array-isarray
- title: Array.isArray
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/isArray

How do you reliably check that a value is an array?

---

`Array.isArray(value)`. `typeof` returns `"object"` for arrays, so it cannot tell them apart from other objects.

`Array.isArray` also works for arrays created in another realm, such as an iframe, where `instanceof Array` returns `false`.

### array-toreversed
- title: toReversed
- version: ES2023
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toReversed

You call `items.reverse()` to display a list in reverse order, and the original list changes too. What should you use?

---

`reverse()` reverses the array in place and returns the same array. `toReversed()` returns a new reversed array and leaves the original unchanged.

It is the copying counterpart of `reverse()`. Empty slots become `undefined` in the copy.

### array-tospliced
- title: toSpliced
- version: ES2023
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSpliced

What does `arr.toSpliced(1, 2)` return, compared with `arr.splice(1, 2)`?

---

`toSpliced(1, 2)` returns a new array with the two elements removed and leaves `arr` unchanged. `splice(1, 2)` mutates `arr` and returns the removed elements.

The return values are opposite in meaning, so a direct swap of `splice` for `toSpliced` needs a review of what the code uses.

### fill-shared-reference
- title: fill with an object shares one reference
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fill

`const grid = Array(3).fill([]); grid[0].push(1);` What is `grid[1]`?

---

`[1]`. `fill` puts the same value in every slot. When the value is an object, every slot references that one object.

Create a new object per slot with `Array.from({ length: 3 }, () => [])`.

### array-destructuring
- title: Destructuring defaults apply only to undefined
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring

In `const { size = 10 } = options;`, what is `size` when `options.size` is `null`?

---

`size` is `null`. A destructuring default is used only when the value is `undefined`, not for `null` or other falsy values.

Destructuring `null` or `undefined` itself throws a `TypeError`, so guard the source, for example `= options ?? {}`.

### destructuring-swap
- title: Swap variables with destructuring
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring

How do you swap the values of `a` and `b` without a temporary variable?

---

`[a, b] = [b, a];`. The right side builds an array of the current values, and array destructuring assigns them back in the new order.

If the previous line has no semicolon, a line starting with `[` can be parsed as part of it. End the previous statement with a semicolon.

### shallow-copy
- title: Spread makes a shallow copy
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Glossary/Shallow_copy

You copy state with `{ ...state }` and then change `copy.user.name`. Why does the original change?

---

Spread, `Object.assign`, `Array.from`, and `slice` make shallow copies. Top-level properties are copied, but nested objects are shared references, so changing `copy.user.name` changes the same `user` object.

Copy each nested level you change, or make a deep copy, where the source and copy are completely independent.

### arraybuffer-resize
- title: Resizable ArrayBuffer
- version: ES2024
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer/resize

How do you create an `ArrayBuffer` that can grow later without allocating a new buffer and copying?

---

Pass `maxByteLength`: `new ArrayBuffer(8, { maxByteLength: 64 })`. Then `buffer.resize(32)` changes its length up to that maximum. `buffer.resizable` tells you whether a buffer supports it.

Resizing beyond `maxByteLength` throws a `RangeError`. Typed arrays created without a fixed length track the buffer's size as it changes.

### arraybuffer-transfer
- title: ArrayBuffer.prototype.transfer
- version: ES2024
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer/transfer

What does `buffer.transfer()` return, and what happens to the original buffer?

---

It returns a new `ArrayBuffer` with the same contents and detaches the original. A detached buffer has `byteLength` 0 and cannot be read or written.

`transfer` can take a new length, and `transferToFixedLength` returns a non-resizable buffer. Use it to hand off ownership of binary data so the old reference cannot be used by mistake.

### atomics-waitasync
- title: Atomics.waitAsync
- version: ES2024
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics/waitAsync

Why can't the browser main thread use `Atomics.wait`, and what does ES2024 provide instead?

---

`Atomics.wait` blocks the thread, which the main thread is not allowed to do. `Atomics.waitAsync` waits on a location in shared memory without blocking and returns an object whose `value` is either a promise or a string result if it finished immediately.

It works only on an `Int32Array` or `BigInt64Array` that views a `SharedArrayBuffer`. Another thread wakes waiters with `Atomics.notify`.

### sharedarraybuffer
- title: SharedArrayBuffer and cross-origin isolation
- version: ES2017
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer

`SharedArrayBuffer` is undefined on your page. What do browsers require, and why use `Atomics` with it?

---

Browsers expose `SharedArrayBuffer` only when the document is cross-origin isolated, which needs the `Cross-Origin-Opener-Policy` and `Cross-Origin-Embedder-Policy` headers. The restriction is a mitigation against Spectre-style attacks.

The same memory can be seen by several workers at once. Plain reads and writes can race, so use `Atomics` operations for synchronized access.

### property-enumeration
- title: keys, getOwnPropertyNames, and ownKeys
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Enumerability_and_ownership_of_properties

Which of `Object.keys`, `Object.getOwnPropertyNames`, `Reflect.ownKeys`, and `for...in` include non-enumerable, symbol, or inherited properties?

---

`Object.keys` returns own enumerable string keys. `Object.getOwnPropertyNames` adds own non-enumerable string keys. `Reflect.ownKeys` returns all own keys, strings and symbols, enumerable or not. `for...in` visits enumerable string keys, own and inherited.

Pick the narrowest one that matches the intent. Serializers and copy helpers usually want own enumerable keys only.

### object-entries
- title: Object.entries
- version: ES2017
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries

How do you loop over an object's keys and values together?

---

`for (const [key, value] of Object.entries(obj))`. `Object.entries` returns an array of `[key, value]` pairs for the object's own enumerable string-keyed properties.

It skips inherited and symbol keys. Pair it with `new Map(Object.entries(obj))` to turn an object into a `Map`.

### object-values
- title: Object.values
- version: ES2017
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/values

How do you sum the values of `{ a: 1, b: 2 }`?

---

`Object.values(obj).reduce((s, v) => s + v, 0)`. `Object.values` returns an array of the object's own enumerable string-keyed property values, in the same order as `Object.keys`.

It does not include inherited properties or symbol-keyed properties.

### getownpropertydescriptors
- title: Copy getters with getOwnPropertyDescriptors
- version: ES2017
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyDescriptors

`Object.assign({}, src)` turns a getter on `src` into a plain value. How do you copy the getter itself?

---

`Object.assign` reads each property, which runs the getter and copies the result. To copy the accessor, copy the descriptors:

```js
const copy = Object.defineProperties({}, Object.getOwnPropertyDescriptors(src));
```

Use `Object.create(Object.getPrototypeOf(src), Object.getOwnPropertyDescriptors(src))` to keep the prototype too. The copy is still shallow.

### object-freeze
- title: Object.freeze is shallow
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze

After `const cfg = Object.freeze({ db: { host: "a" } })`, can you change `cfg.db.host`?

---

Yes. `Object.freeze` prevents adding, removing, or changing the object's own properties, but it is shallow. `cfg.db` still points to an unfrozen object.

Writes to a frozen property are ignored in sloppy mode and throw a `TypeError` in strict mode. Freeze nested objects recursively if the whole tree must be read-only.

### seal-vs-preventextensions
- title: preventExtensions, seal, and freeze
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal

What is the difference between `Object.preventExtensions`, `Object.seal`, and `Object.freeze`?

---

`preventExtensions` stops new properties from being added. `seal` also makes existing properties non-configurable, so they cannot be deleted, but their values can still change. `freeze` also makes data properties read-only.

All three are shallow and cannot be undone. Check the state with `Object.isExtensible`, `Object.isSealed`, and `Object.isFrozen`.

### object-assign
- title: Object.assign
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign

What does `Object.assign(target, a, b)` do when `a` and `b` both have a key `x`? Does it deep merge?

---

It copies own enumerable properties from `a` and then `b` into `target`, so `b.x` wins, and it returns `target`, which is mutated. It reads with getters on the sources and writes with setters on the target.

It does not deep merge: nested objects are copied by reference. Use `Object.assign({}, a, b)` or `{ ...a, ...b }` to avoid mutating `a`.

### defineproperty-defaults
- title: defineProperty defaults are false
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty

After `Object.defineProperty(obj, "id", { value: 1 })`, can you change, delete, or see `id` in `Object.keys`?

---

No to all three. Attributes you omit default to `false`, so `writable`, `enumerable`, and `configurable` are all `false`.

That differs from plain assignment, which creates a writable, enumerable, configurable property. Spell out every attribute you want.

### computed-property-names
- title: Computed property names
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Object_initializer

How do you create an object whose key comes from a variable, in a single literal?

---

Wrap the expression in brackets: `{ [field]: value }`. The expression is evaluated and converted to a property key, a string or a symbol.

It also works for methods and with symbols, such as `[Symbol.iterator]() {}`.

### method-shorthand
- title: Method shorthand is not constructible
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Method_definitions

What is the difference between `{ greet() {} }` and `{ greet: function () {} }`?

---

Both create a method that gets `this` from the call site. The shorthand form can use `super` to reach the object's prototype, and it is not a constructor: `new obj.greet()` throws a `TypeError`.

Use shorthand in object literals and classes. Use a function expression only when you need a constructor.

### json-stringify-omits
- title: What JSON.stringify drops
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify

What is `JSON.stringify({ a: undefined, b: () => 1, c: NaN, d: [undefined] })`?

---

`'{"c":null,"d":[null]}'`. Properties whose values are `undefined`, functions, or symbols are omitted from objects. In arrays, those values become `null`. `NaN` and `Infinity` become `null`.

A `Date` becomes an ISO string through its `toJSON` method, and a BigInt throws a `TypeError`. A round trip through JSON is not a faithful clone.

### json-tojson
- title: toJSON customizes serialization
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify

How do you keep a `password` field out of `JSON.stringify` output for a class?

---

Define a `toJSON()` method. `JSON.stringify` calls it and serializes its return value instead of the object.

The second argument, the replacer, can also filter keys with an array or transform values with a function. `toJSON` keeps the rule with the class.

### json-parse-reviver
- title: JSON.parse reviver
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse

An API returns ISO date strings. How can `JSON.parse` turn them into `Date` objects?

---

Pass a reviver function as the second argument. It is called for each key and value, and its return value replaces the parsed value. Returning `undefined` deletes the property.

Match on the key name, not only on what the string looks like. Invalid JSON throws a `SyntaxError`, so wrap untrusted input in `try/catch`.

### delete-operator
- title: What delete does
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/delete

What does `delete obj.x` return, does it affect the prototype, and does it free memory?

---

`delete` removes an own property and returns `true`, including when the property did not exist. It does not touch the prototype, so an inherited `x` remains visible. Deleting a non-configurable property returns `false`, or throws a `TypeError` in strict mode.

`delete` is not about memory. Memory is freed by garbage collection when nothing references a value.

### in-operator
- title: in checks the prototype chain
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/in

What are `"toString" in {}` and `Object.hasOwn({}, "toString")`?

---

`"toString" in {}` is `true`, because `in` looks up the whole prototype chain. `Object.hasOwn({}, "toString")` is `false`, because it checks only own properties.

`in` returns `true` for a property whose value is `undefined`, unlike `obj.x !== undefined`. Using `in` on a primitive right-hand side throws a `TypeError`.

### object-tostring-type
- title: Object.prototype.toString for type tags
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/toString

What does `Object.prototype.toString.call([])` return, and how can a class change its result?

---

It returns `"[object Array]"`. Built-ins produce tags such as `"[object Date]"` and `"[object Null]"`. For other objects, the tag comes from the `Symbol.toStringTag` property, and defaults to `"Object"`.

Because any class can set `Symbol.toStringTag`, the tag is not a security check. Prefer `Array.isArray` and `instanceof` for type checks.

### symbol-uniqueness
- title: Every Symbol() is unique
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol

Is `Symbol("id") === Symbol("id")`? What is the string argument for?

---

No. Every call to `Symbol()` returns a new, unique value. The string is only a description for debugging and does not affect identity.

Symbols make collision-free property keys, useful when adding metadata to objects you do not own.

### symbol-registry
- title: Symbol.for uses a global registry
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/for

How can two separate modules get the same symbol without importing it from each other?

---

`Symbol.for("app.id")` looks up the key in the global symbol registry and creates the symbol only if it is not there, so every call with that key returns the same symbol. `Symbol.keyFor(sym)` returns the key of a registered symbol.

The registry is shared across the realm, so namespace your keys to avoid collisions.

### symbol-keys-hidden
- title: Symbol keys are skipped by most enumeration
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols

Does a symbol-keyed property show up in `Object.keys`, `for...in`, or `JSON.stringify`? Is it private?

---

It does not appear in any of them. `Object.getOwnPropertySymbols(obj)` returns the symbol keys, and `Reflect.ownKeys` includes them too.

So symbol keys are hidden from casual enumeration but not private. Use `#private` fields when you need real privacy.

### well-known-symbols
- title: Well-known symbols
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol

Name three well-known symbols and the language behavior each one customizes.

---

Well-known symbols are static properties of `Symbol` that the language uses as protocol keys. `Symbol.iterator` makes an object iterable. `Symbol.toPrimitive` controls conversion to a primitive. `Symbol.hasInstance` customizes `instanceof`. `Symbol.toStringTag` sets the `Object.prototype.toString` tag.

They let user objects plug into language features without string-named methods that could collide with ordinary data.

### symbol-tostringtag
- title: Symbol.toStringTag
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toStringTag

How do you make `String(new Queue())` print `[object Queue]` instead of `[object Object]`?

---

Define a `Symbol.toStringTag` getter that returns `"Queue"`. `Object.prototype.toString` reads it to build the tag.

```js
class Queue {
  get [Symbol.toStringTag]() { return "Queue"; }
}
```

It only changes the tag that `Object.prototype.toString` reports.

### symbol-no-new
- title: new Symbol() throws
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/Symbol

What happens with `new Symbol("x")`?

---

It throws a `TypeError`. `Symbol` is not a constructor, because a symbol is a primitive value. Call `Symbol("x")` without `new`.

This prevents creating symbol wrapper objects by accident. `typeof Symbol("x")` is `"symbol"`.

### proxy-basics
- title: What a Proxy is
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy

What are the two arguments of `new Proxy(target, handler)`, and what happens with an empty handler?

---

`target` is the object being wrapped, and `handler` is an object of trap functions that intercept operations such as property reads and writes. With an empty handler, every operation is forwarded to the target unchanged.

Proxies power validation, logging, and reactive state. Work on the proxy, not the target, or the traps do not run.

### proxy-traps
- title: Common Proxy traps
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy

Which traps intercept `obj.x`, `obj.x = 1`, `"x" in obj`, `delete obj.x`, and calling a proxied function?

---

`get`, `set`, `has`, `deleteProperty`, and `apply`. Others include `construct` for `new`, `ownKeys` for key listing, `defineProperty`, and `getOwnPropertyDescriptor`.

A `set` trap must return `true` to report success; returning a falsy value makes the assignment throw a `TypeError` in strict mode.

### proxy-invariants
- title: Proxy invariants
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy/get

Can a `get` trap return a different value for a property that is frozen on the target?

---

No. If the target has a non-writable, non-configurable own data property, the `get` trap must return the same value. Otherwise the proxy throws a `TypeError`.

These invariants keep proxies from lying about facts the language guarantees, such as frozen properties. Each trap has its own list of invariants.

### proxy-revocable
- title: Proxy.revocable
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/revocable

How do you hand out access to an object and cut it off later?

---

`Proxy.revocable(target, handler)` returns `{ proxy, revoke }`. After `revoke()` is called, any operation on the proxy throws a `TypeError`.

Revoking also lets the proxy drop its references to the target and handler. It is useful for granting temporary access to a plugin or third-party code.

### reflect-api
- title: What Reflect is for
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect

What is `Reflect`, and why is it usually used inside Proxy traps?

---

`Reflect` is a namespace object with static methods for interceptable operations, with the same names and arguments as the Proxy traps: `Reflect.get`, `Reflect.set`, `Reflect.has`, and so on. It is not a constructor.

Inside a trap, calling the matching `Reflect` method performs the default behavior, so you can add logic and still forward correctly.

### reflect-receiver
- title: Forward the receiver in a get trap
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect/get

In a Proxy `get` trap, why write `Reflect.get(target, key, receiver)` instead of `target[key]`?

---

The `receiver` argument is the `this` value used if the property is a getter. Passing it through means getters run with the proxy, or an object inheriting from it, as `this`.

With `target[key]`, a getter runs with the raw target as `this`, so property reads inside the getter skip the proxy's traps.

### reflect-ownkeys
- title: Reflect.ownKeys
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect/ownKeys

How do you list every own key of an object, including symbols and non-enumerable keys, in one call?

---

`Reflect.ownKeys(obj)` returns an array of all own property keys, both strings and symbols, regardless of enumerability. It is equivalent to combining `Object.getOwnPropertyNames` and `Object.getOwnPropertySymbols`.

It throws a `TypeError` if the argument is not an object.

### reflect-defineproperty-boolean
- title: Reflect.defineProperty returns a boolean
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect/defineProperty

What is the difference between `Object.defineProperty` and `Reflect.defineProperty` when the definition fails?

---

`Object.defineProperty` throws a `TypeError` on failure and returns the object on success. `Reflect.defineProperty` returns `false` on failure and `true` on success.

The boolean result lets you branch with `if` instead of `try/catch`, and it is the shape a `defineProperty` trap must return.

### proxy-private-fields
- title: Proxies and private fields
- version: ES2022
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy

You wrap a class instance with private fields in a Proxy and call a method that reads `this.#count`. Why does it throw?

---

Private fields are not properties, so proxy traps cannot forward them. The method runs with `this` set to the proxy, and the proxy object does not have `#count`, so the access throws a `TypeError`.

A common workaround is a `get` trap that wraps methods so they are applied with the target as `this` when called through the proxy.

### intl-numberformat
- title: Intl.NumberFormat for currency
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat

How do you format `1234.5` as euros for a German user?

---

```js
new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(1234.5);
```

It produces the locale's grouping, decimal separator, and currency symbol placement. Do not hand-build currency strings with `toFixed` and string concatenation.

### intl-datetimeformat
- title: Intl.DateTimeFormat and time zones
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat

How do you show the same `Date` in Tokyo time for a user whose computer is set to London?

---

Pass the `timeZone` option: `new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Tokyo", dateStyle: "medium", timeStyle: "short" }).format(date)`.

A `Date` is a single instant. Only formatting applies a time zone, and without `timeZone` the formatter uses the runtime's default time zone.

### intl-collator
- title: Intl.Collator for sorting
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator/Collator

How do you sort `["item10", "item2"]` so `item2` comes first?

---

Use a collator with numeric collation: `arr.sort(new Intl.Collator(undefined, { numeric: true }).compare)`. The `numeric` option compares digit runs as numbers, so `2` sorts before `10`.

The `sensitivity` option controls whether case and accents matter, for example `"base"` to treat `a`, `A`, and `á` as equal.

### intl-relativetimeformat
- title: Intl.RelativeTimeFormat
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat

How do you render "yesterday" or "in 3 days" in the user's language?

---

```js
const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
rtf.format(-1, "day"); // "yesterday"
rtf.format(3, "day");  // "in 3 days"
```

`numeric: "auto"` allows words like "yesterday"; the default `"always"` gives "1 day ago". You still compute the difference and choose the unit yourself.

### intl-locale
- title: Intl.Locale
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale

How do you read the language and region out of a tag like `"en-US"` without string splitting?

---

`new Intl.Locale("en-US")` parses a Unicode locale identifier. Its `language` is `"en"` and its `region` is `"US"`. It also exposes options such as `calendar` and `hourCycle`.

`maximize()` fills in the most likely script and region from the existing values. Locale objects can be passed to other `Intl` constructors.

### intl-compact-notation
- title: Compact and unit number formatting
- version: ES2020
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat

How do you display a large number in a short compact form, and `3500` as a volume in liters, with `Intl.NumberFormat`?

---

Use `notation: "compact"` for short forms of large numbers. Use `style: "unit"` with a unit for measurements: `new Intl.NumberFormat("en-US", { style: "unit", unit: "liter" }).format(3500)` gives `"3,500 L"`.

The output follows the locale. Do not build unit labels by string concatenation.

### intl-segmenter
- title: Intl.Segmenter for graphemes and words
- version: ES2022
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter

How do you count user-visible characters in a string with flag emoji, or split Japanese text into words?

---

Use `new Intl.Segmenter(locale, { granularity: "grapheme" })` for user-visible characters, or `"word"` and `"sentence"` for other boundaries. `segment(str)` returns an iterable of segments.

`length` and `[...str]` count code units and code points, which miscount combined emoji. Word segmentation also handles languages that do not separate words with spaces.

### intl-supportedvaluesof
- title: Intl.supportedValuesOf
- version: ES2022
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/supportedValuesOf

How do you fill a time zone dropdown with the zones the runtime actually supports?

---

`Intl.supportedValuesOf("timeZone")` returns a sorted array of supported values. Other keys include `"currency"`, `"calendar"`, `"collation"`, `"numberingSystem"`, and `"unit"`.

An unsupported key throws a `RangeError`. The list depends on the runtime, so do not assume two browsers return the same values.

### datetimeformat-formattoparts
- title: formatToParts for custom date layouts
- version: ES2017
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/formatToParts

You need to style the month differently from the rest of a localized date. How do you get the pieces without parsing the formatted string?

---

`formatter.formatToParts(date)` returns an array of objects with `type` and `value`, such as `{ type: "month", value: "March" }` and `{ type: "literal", value: " " }`.

Map over the parts and wrap the ones you want. Parsing the output of `format` breaks across locales because order and separators change.

### tolocalestring-reuse
- title: Reuse Intl formatters
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toLocaleString

A table renders ten thousand numbers with `n.toLocaleString("en-US", opts)`. How can you make it faster?

---

`toLocaleString` with locale arguments sets up formatting each time it is called. Create one `Intl.NumberFormat` object with the same locale and options and call its `format` method for every number.

The output is the same. The saving comes from not repeating locale lookup and option processing.

### trailing-commas
- title: Trailing commas in parameter lists
- version: ES2017
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Trailing_commas

Is `function f(a, b,) {}` valid, and why would a team want it?

---

Yes. Trailing commas are allowed in function parameter lists and in function calls.

Adding a parameter on a new line then changes one line in the diff instead of two. A trailing comma after a rest parameter is still a syntax error, and JSON does not allow trailing commas.

### hashbang
- title: Hashbang comments
- version: ES2023
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar

What does `#!/usr/bin/env node` at the top of a JavaScript file mean to the language?

---

It is a hashbang comment. The language treats `#!` at the very start of a script or module as a comment that runs to the end of the line.

The operating system uses it to choose the interpreter for an executable file. It is only valid as the first characters of the source; anywhere else it is a syntax error.

### default-parameters
- title: Default parameters apply to undefined
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters

With `function f(x = 5)`, what is `x` for `f()`, `f(undefined)`, and `f(null)`?

---

`5`, `5`, and `null`. A default applies when the argument is missing or `undefined`. `null` is a real value and is passed through.

Defaults are evaluated at call time, so `function f(list = [])` gets a new array on each call. Later parameters can refer to earlier ones.

### rest-parameters
- title: Rest parameters
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters

How do you write a function that takes any number of arguments as a real array?

---

Use a rest parameter: `function sum(...nums) {}`. `nums` is a real `Array` with all remaining arguments, so `map` and `reduce` work.

The rest parameter must be last, and there can be only one. Unlike `arguments`, it works in arrow functions.

### arguments-object
- title: The arguments object
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/arguments

What is `arguments`, and why can't you call `arguments.map`?

---

`arguments` is an array-like object available inside non-arrow functions. It holds all passed arguments and has `length`, but it is not an `Array`, so it has no `map`.

Convert it with `Array.from(arguments)`, or replace it with rest parameters. Arrow functions have no `arguments` of their own.

### switch-strict-match
- title: switch uses strict equality
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/switch

`switch ("1") { case 1: ... }` Does the case match? What happens without `break`?

---

It does not match. `switch` compares with strict equality, so the string `"1"` does not equal the number `1`.

Without `break`, execution falls through into the next case's statements until a `break` or the end of the `switch`.

### date-month-index
- title: Date months are zero-based
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date

What date does `new Date(2024, 1, 15)` create?

---

February 15, 2024. The `monthIndex` argument starts at `0` for January. Days of the month start at `1`.

The same rule applies to `getMonth()` and `setMonth()`. Out-of-range values roll over, so month `12` becomes January of the next year.

### date-only-utc
- title: Date-only strings parse as UTC
- version: ES6
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse

Why does `new Date("2024-03-10")` show March 9 for some users, while `new Date("2024-03-10T00:00")` does not?

---

Date-only ISO strings are treated as UTC. Date-time strings without an offset are treated as local time. A UTC midnight shown in a time zone west of UTC is the previous evening.

Store date-only values as strings, or parse their parts and build the date in the time zone you intend. Non-ISO formats are implementation-specific.

### garbage-collection
- title: Mark-and-sweep garbage collection
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management

How does JavaScript decide that memory can be freed, and why are cycles not a leak?

---

Modern engines use mark-and-sweep: starting from roots such as the global object, they mark every reachable value and free what was not reached. An object is collected when it is unreachable, not when its reference count hits zero.

Two objects that refer only to each other are unreachable and are collected. Leaks come from references you keep by accident, such as globals, caches, timers, and event listeners.

### math-max-empty
- title: Math.max() with no arguments
- version: ES6
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/max

What are `Math.max()`, `Math.max(...[])`, and `Math.max(1, "a")`?

---

`Math.max()` and `Math.max(...[])` return `-Infinity`, the identity value for "largest". `Math.max(1, "a")` is `NaN`, because any argument that converts to `NaN` makes the result `NaN`.

Guard empty arrays before showing a maximum. Spreading a huge array into `Math.max` can exceed argument limits; `reduce` avoids that.

### math-random-not-crypto
- title: Math.random is not for security
- version: ES6
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random

Can you use `Math.random()` to generate a password reset token?

---

No. `Math.random()` returns a pseudo-random number from `0` up to but not including `1`, and it does not provide cryptographically secure random numbers.

Use the Web Crypto API, `crypto.getRandomValues()`, or `crypto.randomUUID()` for tokens and IDs that must not be guessable.
