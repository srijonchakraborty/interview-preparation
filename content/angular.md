# Angular

### typed-forms
- title: Reactive forms became typed in v14
- version: v14
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/typed-forms

Before Angular 14, what type was `form.controls.email.value` on a reactive form? What do you use when a control must never be null?

---

Angular 14 introduced strictly typed reactive forms. `FormControl`, `FormGroup`, and `FormArray` carry the value type, so `value` and `valueChanges` are typed from the control definitions instead of `any`.

A control created with `new FormControl('')` is `string | null`, because `reset()` can clear it. Pass `{ nonNullable: true }` when the control should reset to its initial value instead of `null`. `FormBuilder.nonNullable` does the same for a group. `UntypedFormGroup` and `UntypedFormControl` exist so older code migrates one form at a time. Typed forms did not remove template-driven forms.

### standalone
- title: Standalone components declare their own imports
- version: v15
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/imports

What problem do standalone components solve, and which Angular version made them a stable API?

---

A standalone component, directive, or pipe lists the components and pipes it uses in its own `imports` array. It does not have to be declared in an `NgModule`. Standalone APIs were a developer preview in v14 and became stable in v15.

`NgModule` is still supported. The practical change is that the dependency is visible on the component instead of on a distant module. Bootstrapping a standalone root is `bootstrapApplication(AppComponent)`. A common interview mistake is to say modules were removed. They were not. New trees should prefer standalone components so each file shows what it renders.

### required-inputs
- title: Required inputs fail compilation when a binding is missing
- version: v16
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/inputs

How do you require a component input so a missing binding is a compile error? Why is that different from `input.required()`?

---

Angular 16 added required inputs on the decorator form:

```ts
@Input({ required: true }) title!: string;
```

If a parent template uses the component and does not bind `title`, the compiler reports an error. This is a compile-time check, not a runtime default.

Signal inputs are a later API: `input()` and `input.required()`, tied to the signal reactivity work that became stable in v20. Do not describe `input.required()` as the v16 feature. v16's feature is `@Input({ required: true })`. A required input can still be set to `undefined` if its type includes `undefined`; `required` means the binding is present.

### signals-preview
- title: Signals started as a v16 developer preview
- version: v16
- level: intermediate
- status: verified
- source: https://angular.dev/guide/signals

What did Angular 16 ship for signals, and why was it a mistake to treat that API as a stable contract?

---

Angular 16 introduced `signal()`, `computed()`, and `effect()` as a developer preview. A signal holds a value, readers are tracked, and writers notify only the computations that read it. `computed()` derives a value lazily. `effect()` is for side effects and should not be the default way to render state.

Developer preview means the API can still change. The fundamental primitives, including `signal`, `computed`, `effect`, `linkedSignal`, signal inputs, and signal queries, graduated to stable in v20. In an interview, separate "we tried signals in 16" from "the reactivity model is stable as of v20". Zone.js change detection still existed throughout that preview.

### control-flow
- title: Built-in @if and @for replace the structural directives
- version: v17
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/control-flow

What is wrong with this template in Angular 17 or later, and what replaced `*ngFor`?

```html
<div *ngIf="user">{{ user.name }}</div>
```

---

Nothing is wrong if `CommonModule` or `NgIf` is imported. The current syntax, stable since v17, is built into the template and does not need that import:

```html
@if (user) {
  <p>{{ user.name }}</p>
} @else {
  <p>Signed out</p>
}
@for (item of items; track item.id) {
  <li>{{ item.name }}</li>
}
```

`track` is required on `@for`. Tracking by a stable id avoids recreating DOM nodes when the list changes. `@for` also has an `@empty` block. `*ngIf` and `*ngFor` still run, but new templates should use the built-in control flow. `@if` is template syntax, not a directive you add to `imports`.

### defer
- title: Deferrable views load a component later
- version: v17
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/defer

How do you keep a heavy chart out of the initial bundle until the user scrolls to it?

---

Angular 17 added `@defer`. The deferred template is compiled into a separate chunk and loaded when a trigger fires:

```html
@defer (on viewport) {
  <heavy-chart />
} @placeholder {
  <p>Chart placeholder</p>
} @loading {
  <p>Loading chart</p>
} @error {
  <p>Chart failed to load</p>
}
```

Triggers include `on viewport`, `on idle`, `on interaction`, `on timer`, and `when` a boolean becomes true. `@placeholder` is shown before loading starts. `@loading` is shown while the chunk loads. The heavy component's dependencies stay out of the main bundle only if they are not imported eagerly somewhere else. Defer is about loading, not about whether the component is standalone, but the deferred dependency is imported from the deferred boundary rather than the parent.

### signals-stable
- title: Signal primitives are stable in v20
- version: v20
- level: intermediate
- status: verified
- source: https://angular.dev/roadmap

Which signal APIs did Angular mark stable in v20? What is `linkedSignal` for?

---

Angular's roadmap records that v20 graduated the fundamental reactivity primitives to stable: `signal`, `computed`, `effect`, `linkedSignal`, signal-based queries, and signal inputs. That is the version to cite when an interviewer asks whether signals are production-ready.

`linkedSignal` is a writable signal whose value resets when a source signal changes. Use it for state that is derived from a selection but can be overridden locally, such as the chosen tab defaulting from the current route and then following the user's click. `effect()` remains for side effects such as logging or synchronizing an imperative widget. It is not a second change detector you use to copy one signal into another; that copy belongs in `computed` or `linkedSignal`.

### signal-forms
- title: Signal Forms are stable in v22
- version: v22
- level: experienced
- status: verified
- source: https://angular.dev/events/v22

What did the Angular v22 release stabilize, and what should you say about older forms APIs?

---

The v22 release event says three APIs are now stable: Signal Forms, Asynchronous Signals, and Angular Aria. It calls that set a production-ready reactive foundation.

Memorize those three names and the version. That page does not say `FormGroup` was removed, so do not invent a removal date in the answer.

### zone-versus-signals
- title: Zone.js and signals answer different problems
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals

Why did Angular add signals when Zone.js already re-renders after async work? What does a signal make precise?

---

Zone.js patches async APIs and tells Angular that some work happened. The framework then runs change detection over the component tree, skipping branches that use `OnPush` and have not been marked dirty. It does not know which binding actually changed, so a timer or an HTTP response can dirty a large tree.

A signal records which computations read it. Updating the signal invalidates those computations and the views that read them. That is finer than "something async finished". Signals do not by themselves remove Zone.js from an existing app. In an interview, describe both: Zone.js is a coarse "run change detection" notification, and signals are a dependency-tracked value graph. `OnPush` plus immutable inputs was the older way to limit the tree; signals are the model Angular has standardized.
