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

### component-anatomy
- title: A component is a class, template, and selector
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components

What three things does every Angular component need?

---

Every component needs a TypeScript class for behavior, an HTML template that controls what renders, and a CSS selector that says how the component is used in HTML. You attach Angular metadata with the `@Component` decorator.

Interviewers use this to see whether you describe a component as a view plus a class, or only as a TypeScript file. The decorator object is the metadata: `selector`, `template`, and the other properties the guide covers.

### component-styles-inline
- title: Component styles can live on the decorator
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components

Where can a component's CSS live, and what does it affect by default?

---

A component may set `styles` or `styleUrl` on `@Component`. `templateUrl` and `styleUrl` are relative to the directory that contains the component. You can mix inline and external files per component.

By default those styles affect only elements defined in that component's template. Saying "component CSS is always global" misses the encapsulation default the anatomy guide states.

### component-imports
- title: Templates only see imported components
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components

How does a standalone component use another component, directive, or pipe?

---

Add that dependency to the `imports` array of the `@Component` decorator. By default, Angular components are standalone, so another component can import the class directly.

Components created earlier may set `standalone: false`. For those, you import the `NgModule` that declares them. Before Angular 19.0.0 the `standalone` option defaults to `false`, so do not assume every existing file is standalone just because new ones are.

### host-element-and-view
- title: Host element versus component view
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components

What is a component's host element, and what is its view?

---

Angular creates one component instance for every element that matches the selector. That matching DOM element is the host element. The DOM produced from the component's template is the view, and it renders inside the host.

The app is a tree of components. That tree is the mental model for dependency injection and child queries, so "the component is just the class" leaves out where the template actually lands.

### selector-compile-time
- title: Selectors are matched at compile time
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/selectors

If you add a component's tag with a DOM API after startup, does Angular create that component?

---

Angular matches component selectors statically at compile time. Changing the DOM at run time, with Angular bindings or with DOM APIs, does not change which components are rendered.

An element can match exactly one component selector. If several component selectors match the same element, Angular reports an error. Selectors are case-sensitive.

### selector-types
- title: Which CSS selectors a component may use
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/selectors

Which selector shapes can a component use?

---

Angular supports type selectors such as `profile-photo`, attribute selectors such as `[dropzone]` or `[type="reset"]`, and class selectors such as `.menu-item`. For attribute values, only the equals operator is supported.

Combinators, namespaces, and pseudo-classes other than `:not` are not supported. You can concatenate selectors, as in `button[type="reset"]`, or list several with commas. Angular creates a component for each element that matches any selector in that list.

### custom-element-name
- title: Custom component tags need a hyphen
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/selectors

Why do Angular custom element selectors include a hyphen?

---

Most components should use a custom element name, and custom element names include a hyphen as the HTML specification describes. By default Angular reports an error for a custom tag that matches no available component, which catches mistyped names.

The CLI prefix is `app-` by default. Angular reserves the `ng` prefix for framework APIs. Do not use `ng` as the prefix for your own components.

### attribute-selector-trap
- title: A missed attribute selector fails quietly
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/selectors

Why is an attribute selector easier to forget to import than a custom element?

---

Use an attribute selector when the component should sit on a native element, such as `button[yt-upload]`, so consumers keep the element's built-in APIs, including ARIA attributes. Attribute selectors should be lowercase dash-case.

Angular does not report an error for a custom attribute that matches no component. If the consumer forgets the import, the component simply does not render. A custom element name fails more loudly.

### emulated-encapsulation
- title: Emulated styles stay in the template
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/styling

What is the default view encapsulation mode?

---

The default is `ViewEncapsulation.Emulated`. Angular gives each component a unique HTML attribute, adds it to elements in the template, and rewrites the component's CSS selectors to include that attribute, so styles do not leak out.

Global styles defined outside the component can still affect elements inside an emulated component. The other modes are `ShadowDom`, `ExperimentalIsolatedShadowDom`, and `None`.

### host-pseudo-class
- title: Style the host without Shadow DOM
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/styling

How do you style a component's host element under emulated encapsulation?

---

Emulated mode supports the `:host` pseudo-class, and the compiler also supports `:host-context()` even though that pseudo-class is deprecated in modern browsers. Angular rewrites these to attributes, so runtime behavior does not follow the native pseudo-class rules.

Emulated mode does not support other Shadow DOM pseudo-classes such as `::shadow` or `::part`. `:host` is the supported way to target the host without turning on real Shadow DOM.

### ng-deep-discouraged
- title: ng-deep punches through encapsulation
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/styling

What does `::ng-deep` do, and should new code use it?

---

When a selector contains `::ng-deep`, Angular stops applying view-encapsulation boundaries after that point. The part of the selector after `::ng-deep` can match elements outside the component template, which makes the rule behave like a global style.

The Angular team strongly discourages new use of `::ng-deep`. It remains only for backwards compatibility. Where you place `::ng-deep` changes which side of the selector must still come from the component's own template.

### shadow-dom-encapsulation
- title: Shadow DOM encapsulation changes more than CSS
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/components/styling

What else changes when you set `ViewEncapsulation.ShadowDom`?

---

`ShadowDom` attaches a shadow root to the host and renders the template and styles into that shadow tree. Styles inside the shadow tree cannot affect elements outside it. `ExperimentalIsolatedShadowDom` also keeps global styles from affecting elements in the shadow tree.

The styling guide warns that a shadow tree also affects event propagation, interaction with the form API, and how developer tools show elements. `ViewEncapsulation.None` disables encapsulation so the component's styles behave as global styles.

### external-styles-skip-encapsulation
- title: External stylesheets skip emulated scoping
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/styling

Why might a stylesheet linked from a template ignore emulated encapsulation?

---

A `style` element in the template is scoped by the component's encapsulation mode, and Angular does not support bindings inside style elements. Component styles are emitted with the component's JavaScript, so they load even when the component is lazy-loaded.

A template `link` to a CSS file, and an `@import` in CSS, are treated as external styles. External styles are not affected by emulated view encapsulation. That is the trap when a "component stylesheet" still leaks.

### css-variable-namespacing
- title: CSS variables can be namespaced per app
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/components/styling

How do you stop two apps on one page from sharing `--primary-color`?

---

Custom properties inherit down the DOM. `provideCssVarNamespacing` prefixes compiled component custom properties with the application's `APP_ID` and an underscore, so `--primary-color` becomes something like `--my-app_primary-color`. The default `APP_ID` is `ng`, so each app on the page needs its own id.

Angular does not rewrite static `style` attributes, object or string style bindings, names inside a binding value, or `Renderer2.setStyle`. A `--global--` prefix opts a name out and is stripped back to a normal custom property.

### signal-input
- title: Declare an input with the input function
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/inputs

How do you declare a signal input and read it?

---

Call `input` in a component or directive property initializer, for example `value = input(0)`. The template binds with the same square-bracket syntax as a decorator input. `input` returns an `InputSignal`, and you read it by calling it.

Signal inputs are read-only. TypeScript infers the type from a default value. `input()` with no default is `undefined` until a parent sets it. The decorator form `@Input()` remains fully supported.

### inputs-are-static
- title: Inputs are fixed at compile time
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/inputs

Can a component add a new input while it is running?

---

Angular records inputs statically at compile time. Inputs cannot be added or removed at run time. Input names are case-sensitive, and a subclass inherits inputs from the class it extends.

You can call `input` only in component and directive property initializers. The compiler gives that call special meaning, so it is not a normal function you call later from a method.

### input-required-signal
- title: input.required checks the binding at build time
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/inputs

What does `input.required` guarantee?

---

`input.required()` declares an input that must be set when the component is used in a template. If a required input is missing, Angular reports an error at build time. The returned `InputSignal` does not automatically include `undefined`.

This is the signal form of required inputs. The decorator form `@Input({ required: true })` is a separate, still-supported API on the same page. Do not treat the two call styles as the same feature version.

### input-transform
- title: Transforms rewrite an input as it is set
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/inputs

What does an input `transform` function change?

---

A `transform` runs when Angular sets the input and replaces the stored value with the function's result. The parameter type of the transform is what the template is allowed to bind. The `InputSignal` type is the return type, so a number can go in and a string can come out.

The function must be statically analyzable at build time and should be pure. `booleanAttribute` treats the presence of the attribute as true, but the literal string `"false"` as false. `numberAttribute` parses a number and produces `NaN` when parsing fails.

### input-alias
- title: An input alias is only the template name
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/inputs

If an input is aliased to `sliderValue`, what name do you use in TypeScript?

---

The `alias` option changes the name used in templates, as in `input(0, { alias: 'sliderValue' })` bound with `[sliderValue]`. The class property name stays the same in TypeScript.

The inputs guide says to avoid aliases in general. They are for renaming while keeping the old template name, or for avoiding a collision with a native DOM property. Do not prefix input names the way you prefix selectors.

### model-input
- title: A model input writes back to the parent
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/inputs

When should a component use `model` instead of `input`?

---

`model` is an input the component can write with `set` or `update`. A two-way binding such as `[(value)]="volume"` propagates that write to the parent. Bind the signal instance, not the result of calling it, when the parent value is a signal. A plain property can be bound the same way.

Declaring `checked = model(false)` also creates an output named `checkedChange`. Model inputs can be required or aliased, but they do not support input transforms. Use them when the component's job is to edit a value, such as a custom form control.

### decorator-input-setter
- title: Decorator inputs can be setters
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/inputs

Can an `@Input` be a getter and setter, and what is the risk?

---

A decorator-based input may be a property with a getter and setter, or only a public setter. Prefer an input transform when you only need to adapt the value. Signal inputs are the recommended API for new work, and `@Input` remains supported.

Angular may call an input setter more than once. A setter that does expensive work, such as DOM updates, can hurt performance. You can also list inherited inputs in the `inputs` array of `@Component`, including an alias after a colon.

### output-function
- title: Custom events come from output
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/outputs

How does a component raise a custom event?

---

Assign a property with `output()`, which returns an `OutputEmitterRef`. Call `emit` to raise the event, with or without a payload. The parent listens with parentheses and reads the payload from `$event`.

Angular custom events do not bubble up the DOM. Output names are case-sensitive, subclasses inherit outputs, and `output` may be called only in a component or directive property initializer. The `@Output()` plus `EventEmitter` form remains fully supported.

### output-naming
- title: Name outputs like events, not handlers
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/outputs

What naming rules does the outputs guide give?

---

Use camelCase, and do not prefix the name with "on". Avoid names that collide with events on DOM elements such as `HTMLElement`. Do not add a selector-style prefix, because one element hosts only one component.

An alias, `output({ alias: 'valueChanged' })` or `@Output('valueChanged')`, changes only the template name. The class property name is unchanged. You can also list inherited outputs in the `outputs` metadata, with an alias after a colon.

### output-subscription-cleanup
- title: Output subscriptions are cleaned up
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/outputs

If you subscribe to an output from a dynamically created component, who unsubscribes?

---

`OutputRef.subscribe` lets you listen from code, which is how you handle outputs on a `ComponentRef` created dynamically. Angular automatically cleans up those subscriptions when it destroys the component.

`subscribe` also returns an `OutputRefSubscription` whose `unsubscribe` method you can call yourself. The trap is treating a component output like a DOM event that bubbles to an ancestor listener. It does not bubble.

### lifecycle-order-init
- title: ngOnChanges runs before ngOnInit
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/lifecycle

When do `ngOnChanges` and `ngOnInit` run?

---

`ngOnInit` runs once, after Angular has set the initial input values, and before the component's own template is initialized. `ngOnChanges` runs after inputs change, also before the template is checked, and the first `ngOnChanges` runs before `ngOnInit`.

`ngOnChanges` receives a `SimpleChanges` record. Each `SimpleChange` has `previousValue`, `currentValue`, and `firstChange`. If an input has an alias, the record key is still the TypeScript property name.

### destroy-ref
- title: DestroyRef registers cleanup without ngOnDestroy
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/lifecycle

How do you run cleanup when a component is destroyed without putting everything in `ngOnDestroy`?

---

`ngOnDestroy` runs once just before destruction, for example when `@if` hides the component or the user navigates away. You can instead inject `DestroyRef` and call `onDestroy` with a callback. That callback can be passed to other code that must clean up with the component.

`DestroyRef.destroyed` tells you the instance is already gone. Checking it avoids work after destruction, including the `NG0911` error for a view that has already been destroyed.

### ng-do-check-cost
- title: ngDoCheck runs on every check
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/lifecycle

Why does the lifecycle guide tell you to avoid `ngDoCheck`?

---

`ngDoCheck` runs before every time Angular checks that component's template. It is the hook for detecting state changes outside normal change detection. During initialization, the first `ngDoCheck` runs after `ngOnInit`.

The method runs very frequently and can hurt performance. The guide says to avoid it unless you have no alternative. Angular walks the tree from top to bottom and visits each component once per traversal, so do not make further state changes in the middle of that pass.

### after-content-and-view
- title: Content hooks and view hooks are different
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/lifecycle

What is the difference between content lifecycle hooks and view lifecycle hooks?

---

`ngAfterContentInit` runs once after nested content is initialized, and `ngAfterContentChecked` runs every time that content is checked. `ngAfterViewInit` and `ngAfterViewChecked` are the same idea for children in the component's own template. Use them to read content queries or view queries.

Changing state in any of those four hooks produces an `ExpressionChangedAfterItHasBeenCheckedError`. The checked hooks also run very often, so the guide says to avoid them when you can.

### render-callbacks
- title: afterNextRender is an app-wide hook
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/components/lifecycle

How do `afterNextRender` and `afterEveryRender` differ from `ngAfterViewInit`?

---

They are functions, not class methods, and they run after Angular has rendered all components on the page into the DOM. They must be called in an injection context, typically the constructor. They are not tied to one component instance.

They do not run during server-side rendering or build-time prerendering. Optional phases run in this order: `earlyRead`, `write`, `mixedReadWrite`, then `read`. Split writes and reads so layout work does not thrash. The lifecycle interfaces drop the `ng` prefix, so `ngOnInit` implements `OnInit`.

### lifecycle-hook-order
- title: Directive and component hooks are unordered
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/components/lifecycle

If a directive and a component share an element, whose `ngOnInit` runs first?

---

The framework does not guarantee the order of a given lifecycle hook between the component and the directives on the same element, whether the directives come from the template or from `hostDirectives`.

Never depend on an order you happened to observe. The lifecycle guide says that order may change in a later version of Angular.

### ng-content-placeholder
- title: ng-content marks a projection slot
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/content-projection

What does `ng-content` do?

---

`ng-content` is a placeholder, not a component and not a DOM element. Children of the host element are projected at that placeholder. The component's content is those projected children. The view is the elements written in the component's own template.

The compiler processes every `ng-content` at build time. You cannot insert, remove, or modify it at run time, and you cannot put directives, styles, or arbitrary attributes on it.

### conditional-ng-content
- title: Hiding ng-content still creates the content
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/content-projection

What goes wrong if you wrap `ng-content` in `@if`?

---

You should not conditionally include `ng-content` with `@if`, `@for`, or `@switch`. Angular always instantiates and creates DOM nodes for content rendered to an `ng-content` placeholder, even when that placeholder is hidden.

The slot is not a normal element you can show and hide. For conditional rendering of component content, the guide points you to template fragments instead of hiding the placeholder.

### ng-content-select
- title: select routes projected children
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/content-projection

How do you project a title and a body into different places?

---

Put a `select` attribute on `ng-content`. The placeholder supports the same CSS selectors as component selectors. A placeholder without `select` captures every child that did not match a selected slot.

If there is no unselected placeholder, children that match nothing are not rendered. Fallback content is the child content you put inside the `ng-content` element itself, and it shows when no matching child was projected.

### ng-project-as
- title: ngProjectAs changes the match, not the element
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/content-projection

How can an `h3` be projected into a slot that selects `card-title`?

---

`ngProjectAs` sets the CSS selector Angular compares against `ng-content` `select`, instead of using the element's own identity. The attribute accepts only static values. It cannot be bound to a dynamic expression.

The element still renders as itself. The attribute only changes which slot it matches. That is the tool when the projected tag is not the tag the slot asks for.

### projected-content-ownership
- title: Projected content belongs to the parent
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/components/content-projection

If a child uses `OnPush`, does that skip change detection for content projected into it?

---

Projected content is rendered inside the receiving component, but the parent that declared it still owns it. Change detection checks that content when the parent runs. `OnPush` on the receiver can skip the receiver's own template and still not skip the projected content.

Dependency injection for projected content comes from the parent's injector, not from the receiver's `viewProviders`. Library components that find children with `ContentChildren` and wire keyboard or ARIA behavior may break if you project those children in from another view.

### template-is-compiled
- title: Templates are HTML plus Angular syntax
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates

What does Angular do with a template before it reaches the browser?

---

A template is HTML plus Angular syntax for bindings, events, variables, and built-in template functions. Angular compiles it to JavaScript so it can keep the page updated as data changes and apply rendering optimizations.

Template comments are not included in the rendered output. Component and directive elements may be self-closed. Angular ignores and collapses unnecessary whitespace and may insert comment nodes as placeholders for dynamic content.

### template-at-and-script
- title: The @ character and script tags are special
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates

Why can a literal `@` in a template be a problem?

---

`@` starts dynamic template syntax such as control flow. To show a literal `@`, escape it as an HTML entity. Attributes that contain `[]` or `()` are bindings and event listeners, not ordinary HTML attributes.

Angular does not support a `script` element in templates. The templates guide sends you to the security page for that restriction. Most other HTML syntax is valid template syntax.

### text-interpolation
- title: Interpolation prints an expression as text
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/binding

What do double curly braces do in a template?

---

`{{ theme }}` is text interpolation. Angular evaluates the expression and keeps the text updated. You can use it anywhere you would write text in HTML. Every value is converted to a string, and objects and arrays use their `toString` method.

Bindings that change over time should read signals. Angular tracks signals read in the template and updates the page when those values change. A plain field read in interpolation does not necessarily update when that field changes.

### property-versus-attribute
- title: Property bindings and attribute bindings differ
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/binding

When do you use `[disabled]` versus `[attr.role]`?

---

Square brackets bind a DOM property, a component input, or a directive input. `[disabled]` sets the property on the element's DOM object whenever the expression changes. The same syntax sets an input on a component.

`attr.` sets an HTML attribute that has no corresponding DOM property, such as many SVG attributes, by calling `setAttribute`. If the bound value is `null`, Angular removes the attribute. Interpolation inside an attribute value is treated as a property binding.

### class-and-style-bindings
- title: Class and style bindings need a new reference
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/binding

Why does mutating a class object fail to update the DOM?

---

`[class.expanded]` adds or removes that class based on truthiness. `[class]` accepts a space-separated string, a string array, or a record of class names to booleans. `[style.display]` sets one CSS property, `[style.height.px]` adds a unit, and `[style]` accepts a declaration string or an object.

When `[class]` is an array or object, or `[style]` is an object, Angular compares the old and new values with `===`. Mutating the same object does not apply. Create a new array or object. Static classes, `[class]`, and `[class.name]` are combined, and Angular does not guarantee class order.

### aria-attribute-binding
- title: String ARIA bindings remove null
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/binding

How does Angular bind `[aria-label]`?

---

Angular can bind string values to ARIA attributes. It writes the string onto the attribute and removes the attribute when the bound value is `null`.

Some ARIA features are DOM properties or directive inputs that expect structured values such as element references. Those use ordinary property bindings. The binding guide points to the accessibility guide for those cases.

### event-listener-syntax
- title: Parentheses listen for events
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/event-listeners

How do you listen for a click or a key in a template?

---

Put the event name in parentheses and a statement that runs when the event fires, such as `(keyup)="updateField()"`. The statement can be any native event, including `click`, `keydown`, and `mouseover`. Every listener receives `$event` as the event object.

`(keyup.enter)` filters to that key. Extra modifiers are `alt`, `control`, `meta`, and `shift`. By default the binding uses the event's `key` value. A `code` suffix uses the physical `code` value, which stays stable when Alt changes the character a key produces.

### prevent-default-in-templates
- title: A false event statement calls preventDefault
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/event-listeners

What happens if a template event handler evaluates to false?

---

If the handler should replace the browser's default action, call `preventDefault` on the event. If the handler statement evaluates to `false`, Angular also calls `preventDefault`, the same idea as a native handler attribute.

Prefer the explicit `preventDefault` call so the intent is obvious. Global targets `window`, `document`, and `body` can prefix an event in `host` metadata, such as `(window:click)`. Custom event names can be added by an `EventManagerPlugin` registered on `EVENT_MANAGER_PLUGINS` with `multi: true`.

### expression-limits
- title: Template expressions are not full JavaScript
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/expression-syntax

Which JavaScript features are missing from a template expression?

---

Expressions support strings, booleans, numbers, objects, arrays, `null`, regular expressions, and template strings. `BigInt` literals are not supported. The only globals are `undefined` and `$any`. `new`, bitwise operators, destructuring, and the comma operator are unsupported. Declarations such as `let`, `const`, functions, classes, and arrow functions with block bodies are unsupported.

Assignment and increment operators are valid only in event listener statements, unless they sit inside an arrow function. Event statements do not support pipes. Arrow functions in expressions must have an expression body. Pipes cannot be used inside an arrow function, but an arrow function can be passed to a pipe.

### optional-chaining-v22
- title: Optional chaining matches JavaScript in v22
- version: v22
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/expression-syntax

What did Angular 22 change about `?.` in templates?

---

Before Angular 22, optional chaining in a template returned `null` when the left side was `null` or `undefined`. Since Angular 22 it matches JavaScript and returns `undefined`.

The v22 migration wrapped existing expressions in `$safeNavigationMigration` so they keep the old null-returning behavior. That name is a compiler instruction, not a function you can call from TypeScript. The guide says to stop relying on the null-versus-undefined difference so the wrapper can be removed.

### template-this
- title: Template expressions imply this
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/expression-syntax

How does a template refer to a field on the component class?

---

Expressions run in the component class plus template variables, locals, and the supported globals. A reference to a class member implies `this`. You do not write `this` for a normal field read.

If a template variable has the same name as a class member, the variable shadows the member. Write `this.` when you need the class member, including when an `@let` declaration is meant to shadow a member for signal narrowing.

### at-let
- title: @let names a template expression
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/variables

What is `@let` for, and can you assign to it later?

---

`@let` declares one local variable from a template expression. Angular keeps that variable updated as the expression changes. Each `@let` declares exactly one name, and the declaration ends with a semicolon.

Unlike JavaScript `let`, you cannot reassign it. An event handler that writes to the `@let` name does not work. The variable is not hoisted. It is visible in the current view and descendant views, and not in parent or sibling views.

### template-reference-variables
- title: A hash marks a template reference
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/variables

What does `#taskInput` on an element refer to?

---

A template reference variable refers to a DOM element, a component or directive instance, or a `TemplateRef` from `ng-template`. On a component, the variable is the component instance. On `ng-template`, it is the `TemplateRef`. On any other displayed element, it is the `HTMLElement`.

To point the variable at a directive, the directive needs `exportAs`, and the variable is written as `#firstZone="dropZone"`. A directive without `exportAs` cannot be referenced that way. `@if`, `@for`, structural directives, and `ng-template` create a nested scope, so a variable declared inside is not visible outside.

### at-if-blocks
- title: @if can name its condition result
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/control-flow

How do you show one block or another without a structural directive?

---

`@if` shows its content when the condition is truthy. You can add any number of `@else if` blocks and one `@else` block. The condition result can be saved with `as`, as in `@if (user.profile.settings.startDate; as startDate)`.

Built-in control flow is template syntax. The control flow guide is the place that defines `@if`, `@for`, and `@switch`. A long condition is easier to read when the `as` clause names it once inside the block.

### at-for-track
- title: track tells @for which DOM to keep
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/control-flow

Why does `@for` take a `track` expression?

---

`@for` repeats its block for any iterable, with extra optimizations for arrays. The `track` expression ties each item to DOM nodes so Angular can do the smallest DOM update when the collection changes. Prefer a stable unique property such as `id`.

`$index` is appropriate for a static collection that never changes. Tracking the item itself uses `===` and can make updates much slower. Unlike `*ngFor`, `@for` reuses the view when the tracked property changes but the object reference stays the same, and it updates bindings instead of recreating the element. `@for` does not support `break` or `continue`.

### at-for-locals-and-empty
- title: @for exposes index variables and @empty
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/control-flow

Which implicit variables exist inside `@for`, and when does `@empty` show?

---

Inside `@for` you always have `$count`, `$index`, `$first`, `$last`, `$even`, and `$odd`. A `let` segment can alias them, which matters when an inner `@for` would otherwise hide the outer names.

`@empty` is optional and sits immediately after the loop body. Its content renders when the collection has no items. That replaces the extra `@if` people used to wrap around an empty list.

### at-switch
- title: @switch compares with triple equals
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/control-flow

How does `@switch` choose a branch?

---

`@switch` compares the condition to each `@case` with `===`. There is no fallthrough, so you do not write `break`. Consecutive `@case` lines can share one block. `@default` runs when nothing matches. If nothing matches and there is no `@default`, nothing is shown.

`@default never` asks the template type checker to prove a union is exhaustive, but that narrowing works on variables, not on a function call or a signal read. Assign the signal to `@let` first. For a nested union, pass the object to `never`, as in `@default never(state)`.

### defer-what-is-split
- title: @defer splits standalone dependencies
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/defer

Which dependencies inside `@defer` actually leave the main bundle?

---

`@defer` puts components, directives, pipes, and their component CSS into a separate file loaded when a trigger fires. A dependency is deferred only if it is standalone and is not referenced outside the `@defer` block in the same file, including `ViewChild` queries.

Non-standalone dependencies are still eager. Transitive dependencies may be declared in an `NgModule` and can still participate in deferred loading. The compiler emits a dynamic import for each deferred dependency and does not guarantee import order. The main block renders after those imports resolve.

### defer-blocks-and-triggers
- title: Placeholder, loading, and error are eager
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/defer

What is the difference between `@placeholder`, `@loading`, and `@error`?

---

The default trigger is `on idle`, based on `requestIdleCallback`. `@placeholder` shows before the trigger and is optional. `@loading` replaces it while dependencies load. `@error` shows if loading fails. Dependencies of all three sub-blocks are eagerly loaded.

`@placeholder` accepts `minimum`. `@loading` accepts `after` and `minimum`, in milliseconds or seconds. `on` triggers include `idle`, `viewport`, `interaction`, `hover`, `immediate`, and `timer`. Several `on` triggers separated by semicolons are OR conditions. `when` loads once the expression is truthy and does not go back to the placeholder if it becomes falsy again.

### defer-prefetch-and-pitfalls
- title: Prefetch loads code before the block renders
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/templates/defer

What does `prefetch` do, and what defeats a lazy `@defer` chunk?

---

A `prefetch` trigger, written after a semicolon, downloads the deferred JavaScript before the main trigger renders the block. For example, `on interaction; prefetch on idle` fetches on idle and renders on interaction.

Importing the deferred component through a barrel file can keep it in the main bundle. Nested `@defer` blocks should use different triggers so they do not load together. Deferring something already in the initial viewport can increase cumulative layout shift. With HMR, defer chunks are fetched eagerly unless you serve with `--no-hmr`.

### defer-ssr-and-tests
- title: SSR shows the defer placeholder
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/templates/defer

What does `@defer` render on the server, and how do you step through it in a test?

---

On the server, for SSR or static generation, a defer block renders its `@placeholder`, or nothing if there is no placeholder, and triggers do not run. The client hydrates that placeholder and then activates triggers. Rendering the main content on the server requires incremental hydration and `hydrate` triggers.

In tests, defer blocks play through normally unless you set `TestBed` `deferBlockBehavior` to `DeferBlockBehavior.Manual`. `getDeferBlocks()` returns fixtures you can `render` with `DeferBlockState.Loading` or `DeferBlockState.Complete`. Only standalone dependencies can be deferred. `NgModule`-based ones stay in the eager bundle.

### directive-kinds
- title: Components are a kind of directive
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/directives

What are the three kinds of directives?

---

A directive adds behavior to an existing element or component. Angular describes three kinds: components, which have their own template; attribute directives, which change appearance or behavior; and structural directives, which add and remove DOM.

Use a directive for reusable behavior such as a tooltip or a hover style, or to extend a component you do not own. If you need your own markup, use a component. The `host` object can listen to events and bind host styles without a separate template.

### attribute-directive
- title: An attribute directive matches an attribute
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/directives/attribute-directives

How do you write and apply an attribute directive?

---

An attribute directive is a class with `@Directive` and an attribute selector such as `[appHighlight]`. Apply it by adding that attribute to an element. Angular creates one directive instance for that element. Directives do not support namespaces.

For a one-off class, style, property, or event, use template bindings instead of a directive. `ng generate directive` scaffolds the class and a test. Host events go in the `host` metadata. `ElementRef.nativeElement` is the imperative handle on the host element.

### directive-input-and-non-bindable
- title: One binding can both apply and configure a directive
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/directives/attribute-directives

How can one attribute both attach a directive and pass it a value?

---

Give the directive an `input` whose name matches the selector. `[appHighlight]="color"` then applies the directive and sets the value. Other inputs, such as `defaultColor`, can be set on the same element. A static string does not need square brackets.

`ngNonBindable` stops interpolation, directives, and bindings for the element's children, but directives on the same element as `ngNonBindable` still run. Putting it on a parent disables property and event bindings for the descendants.

### structural-directive-asterisk
- title: The asterisk wraps an element in ng-template
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/directives/structural-directives

What does the asterisk in front of a structural directive mean?

---

A structural directive is applied to `ng-template` and decides whether to render that template. For everyday conditions and loops, the guide says to use `@if`, `@for`, and `@switch`. Write a structural directive for reusable rendering those blocks do not cover.

The asterisk is shorthand. Angular turns `*select` into an `ng-template` that hosts the directive around the element. Only one structural directive is allowed per element in that shorthand, because there is only one `ng-template` to unwrap. Use extra `ng-template` or `ng-container` layers when you need more than one.

### structural-directive-context
- title: Embedded views get a context object
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/directives/structural-directives

What two services does a structural directive inject to render its template?

---

`TemplateRef` is the content of the `ng-template`. `ViewContainerRef` is where the directive can create an embedded view. `createEmbeddedView` takes the template and a context object. A value stored as `$implicit` is what a bare `let data` receives.

In microsyntax, a key such as `from` is prefixed with the directive selector and turned into an input name, so `from` becomes `selectFrom`. `ngTemplateGuard_` can narrow an input inside the template, including the literal `'binding'` for a truthiness guard. `ngTemplateContextGuard` types the context object. An `ng-template` with no structural directive does not render.

### dependency-injection-basics
- title: DI supplies dependencies from outside
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/di

What problem does Angular dependency injection solve?

---

Dependency injection supplies a class with the objects it needs instead of constructing them inside the class. A dependency can be any value, function, or service the class does not create itself. You provide values, and you inject them.

Components and directives participate automatically. The overview lists the practical wins as easier refactoring, reuse across the app, and tests that can substitute a test double for a real implementation.

### what-is-a-service
- title: @Service means a root singleton
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/di

What does the `@Service` decorator do?

---

A service is a class you inject so components can share data access, state, auth, logging, or other logic. `@Service` makes that class available as a singleton for the whole application. The guide calls that the recommended approach for most services.

`@Service` is shorthand for `@Injectable({ providedIn: 'root' })`. You read a service with `inject()`, in a field initializer or in the constructor of a component, directive, or service. A route guard function is also a valid place to call `inject`.

### service-versus-injectable
- title: @Service does not support constructor injection
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/creating-and-using-services

When should you keep `@Injectable` instead of `@Service`?

---

`ng generate service` creates a service file. `@Service` implies a root singleton, supports `inject()`, supports a `factory` option, and is tree-shakable when nothing uses it. It does not support constructor-parameter injection, `useClass`, `useValue`, `useExisting`, `useFactory`, or non-root scopes such as `providedIn: 'platform'`.

The `factory` function runs in an injection context and replaces those `use*` options. Set `autoProvided: false` when you want to put the class in a `providers` array yourself, for a route or a component. A root service overridden on a component is destroyed with that component.

### injection-context
- title: inject only works in an injection context
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/di/dependency-injection-context

Where is it legal to call `inject`?

---

An injection context exists while Angular constructs a class it instantiated, such as an `@Injectable` or `@Component`, in field initializers of those classes, in a `useFactory` or `InjectionToken` factory, and in a stack frame that is already running in an injection context. Router guards are one of those frames, so a `CanActivateFn` may call `inject`.

Outside that context Angular throws `NG0203`. `runInInjectionContext` runs a function in a context when you already hold an injector such as the `EnvironmentInjector`. `assertInInjectionContext` throws a clearer error when a helper is called too late, for example from a click handler.

### injector-hierarchies
- title: Environment and element injectors are separate trees
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/di/hierarchical-dependency-injection

Which injectors does Angular search when a component asks for a service?

---

Angular has an `EnvironmentInjector` hierarchy, configured with `@Service` or the `providers` of `ApplicationConfig`, and an `ElementInjector` hierarchy created for each DOM element. An element injector is empty unless the component or directive sets `providers`. `NgModule` apps also have a `ModuleInjector` built from `providers` and imported modules.

Resolution tries the current element injector, then parent element injectors. If none has the token, Angular starts again at the originating element and walks the environment injector hierarchy. The first provider it finds wins. If the walk reaches `NullInjector` and the dependency is not optional, you get an error.

### resolution-modifiers
- title: optional, self, skipSelf, and host
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/hierarchical-dependency-injection

What do the `inject` options `optional`, `self`, `skipSelf`, and `host` change?

---

`optional: true` resolves a missing token as `null` instead of throwing. `self: true` looks only at the current element injector. `skipSelf: true` starts at the parent element injector, ignoring providers on the current element. `host: true` stops the walk at the host component even if a parent also provides the token.

You can combine modifiers except `host` with `self`, and `skipSelf` with `self`. Constructor injection uses `@Optional()`, `@Self()`, `@SkipSelf()`, and `@Host()` for the same ideas. Components and directives on the same element share one injector.

### providers-versus-view-providers
- title: viewProviders are invisible to projected content
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/hierarchical-dependency-injection

Why can projected content miss a service listed in `viewProviders`?

---

`providers` and `viewProviders` both configure the component's element injector. `viewProviders` are visible only inside the component's own view. Content projected with `ng-content` cannot see them.

Angular resolves injection where the content was declared, not where it is rendered. Projected content still walks up from the parent template, so it can see a root service while missing the host's view provider. To give projected content that view-level service, accept an `ng-template` and render it with an injector that can see the service, rather than using `ng-content`.

### platform-and-root-override
- title: Bootstrap providers override root services
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/hierarchical-dependency-injection

If a service is `providedIn: 'root'` and also listed in `ApplicationConfig`, which one is used?

---

`bootstrapApplication` creates the root environment injector as a child of the platform injector. The platform injector holds platform-wide dependencies, and above that is `NullInjector`. A provider in the `ApplicationConfig` passed to `bootstrapApplication` overrides a provider configured for `root` on `@Injectable`.

That is how you replace a default such as `LocationStrategy` without editing the service. For `NgModule` apps, app-wide providers belong on the `AppModule` `providers` array. `@Service` is preferred to a manual root provider when you want unused services to be tree-shaken.

### injection-token
- title: Tokens identify values by object identity
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

Why do you use an `InjectionToken` instead of a TypeScript interface?

---

An `InjectionToken` is the DI key for a non-class value such as a config object, a function, or a primitive. The string you pass is only a debug description. Angular identifies the token by object reference, not by that string.

A TypeScript interface disappears at runtime, so it cannot be a provider key or an `inject` argument. A token with a `factory` is `providedIn: 'root'` by default, the factory may call `inject`, and the token is tree-shakable if nothing injects it.

### provider-recipes
- title: useClass, useValue, useFactory, and useExisting
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

What is the difference between `useClass` and `useExisting`?

---

`providers: [LocalService]` is shorthand for `{ provide: LocalService, useClass: LocalService }`. `useClass` creates an instance of a class, `useValue` supplies a fixed value, and `useFactory` calls a function. `useExisting` is an alias to a provider that already exists, so both tokens return the same instance.

`useClass` does not alias. It constructs a separate instance. `multi: true` lets several providers contribute to one token, which is how interceptor lists are built. A service with no `providedIn` must be listed in some `providers` array or it cannot be injected.

### signal-read-and-write
- title: You read a signal by calling it
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/signals

How do you create, read, and update a writable signal?

---

`signal(initial)` returns a `WritableSignal`. Calling it reads the value and lets Angular track the read. `set` replaces the value. `update` computes the next value from the previous one. `asReadonly()` returns a read-only view that still reflects writes to the original signal.

That read-only view does not stop deep mutation of an object stored inside the signal. By default, equality is `Object.is`. You can pass an `equal` function to `signal` or `computed`. `isSignal` and `isWritableSignal` distinguish signals from plain values and read-only signals from writable ones.

### computed-signals
- title: computed is lazy, cached, and dynamic
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/signals

When does a `computed` recompute?

---

`computed` derives a read-only signal from other signals. The derivation does not run until the first read, and the result is cached until a dependency changes. You cannot `set` a computed signal.

Only signals actually read during that run are dependencies. A branch that does not read a signal does not subscribe to it, and a later run can drop a dependency it no longer reads. That is why an expensive filter belongs in `computed` rather than in every event handler.

### reactive-context
- title: Signal reads are tracked only synchronously
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals

Why does a signal read after `await` inside an `effect` not become a dependency?

---

A reactive context is active while running an `effect` or `afterRenderEffect`, evaluating `computed`, `linkedSignal`, or a resource `params` function, and rendering a template including host bindings. The reactive context lasts only for the synchronous part of that work.

Reads after an asynchronous boundary are not tracked. Read the signal before `await`, including by passing it as an argument that is evaluated immediately. `untracked` reads a signal without recording a dependency. `assertNotInReactiveContext` fails when code that must not be reactive is called from a reactive context.

### onpush-and-signals
- title: A signal read marks an OnPush view
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/signals

What happens when an `OnPush` template reads a signal?

---

Angular tracks that signal as a dependency of the component. When the signal changes, Angular marks the component so it is updated the next time change detection runs. The signals guide points to the skipping-subtrees guide for the rest of the `OnPush` rules.

`effect` and `afterRenderEffect` are for synchronizing non-reactive APIs, not for deriving state that `computed` or `linkedSignal` can express. Async data belongs in a resource, because `signal`, `computed`, and `input` are synchronous.

### linked-signal
- title: linkedSignal resets when its source changes
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/signals/linked-signal

What does `linkedSignal` do that `signal` does not?

---

`linkedSignal` is writable state tied to other signals. You pass a computation, as with `computed`. Whenever that computation's value changes, the linked signal is set to the new result, so a selection cannot point at an option that no longer exists.

You can still `set` it locally until the source changes again. The object form separates `source` and `computation`. The computation receives the new source value and `previous.source` plus `previous.value`. Using `previous` requires explicit generic type arguments. An `equal` function tells downstream consumers whether the result changed.

### linked-signal-set
- title: A linkedSignal can write back to its source
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals/linked-signal

How can setting a linked signal update a different source signal?

---

Pass a `set` function in the options. It receives the new value and a `rawSet` function. `rawSet` updates the linked signal's internal state directly and can skip an expensive computation when you already know the result.

The usual pattern writes the change back into the source of truth, such as converting Fahrenheit into a Celsius signal, or immutably updating one field of an object held in a parent signal. The linked signal then reads the source again and stays consistent with it.

### resource-loader
- title: resource turns async work into signals
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/signals/resource

What do `params` and `loader` mean on `resource`?

---

Signal APIs such as `signal`, `computed`, and `input` are synchronous. `resource` wraps async work so you can read the result as a signal. `params` is a reactive computation. Whenever signals it reads change, the loader runs again with that value. If `params` returns `undefined`, the loader does not run and the status is `idle`.

The loader receives `params`, `previous`, and an `abortSignal`. A new params value aborts an in-flight load. `reload()` runs the loader again. `stream` is for a source that keeps producing values, such as a socket. `loader` is for one-shot work such as an HTTP fetch. `httpResource` performs that fetch through `HttpClient`, including interceptors.

### resource-status
- title: resource value throws when status is error
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals/resource

How do you read a resource without throwing?

---

`value` is the latest result, or `undefined` unless you set `defaultValue`. Reading `value()` throws when `status` is `error`. `hasValue` is the type guard that means a value is present and that reading it will not throw. `isLoading` is whether the loader is running. `error` is the latest error, or `undefined`.

Statuses are `idle`, `error`, `loading`, `reloading`, `resolved`, and `local`. `loading` means params changed. `reloading` means `reload()` and keeps the previous value. `local` means the value was set with `set` or `update`. An `id` stores the resolved value in `TransferState` for hydration, but the guide says not to use that for user-specific data if the HTML can be shared.

### resource-chain
- title: chain propagates resource status
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals/resource

When should a second resource call `chain` on the first?

---

`chain` in a `params` function reads another resource and copies its status. Idle, loading, reloading, and error on the upstream resource put the downstream resource in that same status, and the loader does not run. During reloading, `chain` does not return the previous value. On `resolved` or `local`, it returns the current value.

Returning `undefined` params makes the resource `idle`, which hides a real loading or error state. Pass the chained value itself as params. An object like `{ companyId: undefined }` is still defined, so the loader would run. Use `computed` when you only need a synchronous derivation. `resourceFromSnapshots` is experimental.

### zoneless-why
- title: Zone.js schedules checks it cannot prove
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/zoneless

Why does the zoneless guide say Zone.js checks more often than it needs to?

---

Zone.js treats DOM events and async tasks as signs that state might have changed, then synchronizes the application by running change detection. It does not know whether state actually changed, so that work happens more often than necessary.

The same guide lists the cost as payload and startup time, harder stack traces, and patches that do not cover every browser API. `async` and `await` cannot be patched effectively and must be downleveled. Some libraries are incompatible with those patches.

### zoneless-v20
- title: v20 turns zoneless on explicitly
- version: v20
- level: intermediate
- status: verified
- source: https://angular.dev/guide/zoneless

How do you enable zoneless change detection in an Angular v20 app?

---

The zoneless guide says zoneless is the default in Angular v21 and later, and that you should make sure `provideZoneChangeDetection` is not overriding that default. In Angular v20, enable it by adding `provideZonelessChangeDetection()` to the providers passed to `bootstrapApplication`, or to an `NgModule` `providers` array.

A zoneless build should also drop `zone.js` and `zone.js/testing` from the `polyfills` of the build and test targets, or from `polyfills.ts`, and can uninstall the `zone.js` package. Leaving the polyfill in place keeps the library you meant to remove.

### zoneless-notifications
- title: Zoneless views update only when notified
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/zoneless

What actually schedules a zoneless view to refresh?

---

Angular refreshes a view when it is notified by `ChangeDetectorRef.markForCheck` (which `AsyncPipe` calls), `ComponentRef.setInput`, an update to a signal read in the template, a bound host or template listener, or attaching a view that one of those already marked dirty.

`OnPush` is the recommended way to force components onto those notifications, but it is not required if the component notifies Angular itself. A library host that creates user components with `ViewContainerRef.createComponent` cannot use `OnPush` when those children still rely on Zone.js. Content projection is not that kind of host.

### zoneless-zone-apis
- title: Some NgZone APIs never fire when zoneless
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/zoneless

Which `NgZone` APIs break after you enable zoneless change detection?

---

`NgZone.onMicrotaskEmpty`, `onUnstable`, and `onStable` never emit in a zoneless application. `NgZone.isStable` is always `true`. Replace a "wait until stable" check with `afterNextRender` or `afterEveryRender`, or with a direct DOM API such as `MutationObserver`.

`NgZone.run` and `NgZone.runOutsideAngular` can stay. Removing them can regress libraries that still run in zoned apps. SSR without Zone.js must register async work with `PendingTasks`, or with `pendingUntilEvent` from `rxjs-interop`, or serialization will not wait. Router navigations and incomplete `HttpClient` requests already use that service.

### reactive-forms-zoneless
- title: setValue does not schedule zoneless change detection
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/zoneless

Why can a reactive form look stale in a zoneless template?

---

`setValue`, `patchValue`, `FormArray.push`, and similar APIs update form state and emit form observables. They do not automatically schedule component change detection.

If the template reads that form state, connect the observable to a notification such as `ChangeDetectorRef.markForCheck()`, or expose the data through signals the template reads. `TestBed` is zoneless by default even when `zone.js` is loaded. Prefer `await fixture.whenStable()` over `fixture.detectChanges()` when you want the test to follow production scheduling.

### forms-two-styles
- title: Reactive and template-driven forms differ in data flow
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms

When should you pick reactive forms instead of template-driven forms?

---

Both styles capture input, validate it, and track changes. Reactive forms create the model in the class, keep it immutable, update synchronously, and validate with functions. Template-driven forms create the model with directives, mutate it, update asynchronously, and validate with directives.

The forms guide says to use reactive forms when forms are central or the app is already reactive, because they scale, reuse, and test with less change-detection setup. Template-driven forms fit a simple form whose logic stays in the template. Both are built on `FormControl`, `FormGroup`, `FormArray`, and `ControlValueAccessor`.

### reactive-source-of-truth
- title: The FormControl is the reactive source of truth
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms

In a reactive form, where does the value live?

---

You construct the `FormControl` in the class and bind it with `[formControl]` from `ReactiveFormsModule`. The control, not the input element, is the source of truth for value and status. View-to-model and model-to-view updates are synchronous and do not depend on rendering.

A template-driven input uses `[(ngModel)]` from `FormsModule`. `NgModel` creates the `FormControl` for you, and the template is the source of truth. Model-to-view updates are asynchronous: `ngOnChanges` queues a task that sets the control on a later turn, and `NgModel` triggers another change-detection pass to avoid `ExpressionChangedAfterItHasBeenChecked` errors.

### form-control-value
- title: value is a snapshot, valueChanges is the stream
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

How do you read a reactive control's current value?

---

`value` is a snapshot of the current value. `valueChanges` is the observable you subscribe to in the class, or read in the template with `AsyncPipe`. `setValue` replaces the control's value and checks that the provided value matches the control's structure.

On a group or array, `setValue` must match the whole structure. `patchValue` updates only the properties you pass and fails silently when the shape is wrong. `setValue` is the strict check that catches nesting mistakes. `FormGroup` is a fixed set of named controls. `FormArray` is a numerically indexed list you can grow and shrink.

### form-builder
- title: FormBuilder factories controls, groups, and arrays
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

What does `FormBuilder` save you from writing?

---

`FormBuilder` is an injectable service with `control`, `group`, and `array`. Inject it with `inject(FormBuilder)` and call `group` to build nested groups without constructing every `FormControl` by hand. `ReactiveFormsModule` still has to be imported.

`AbstractControl` is the base of `FormControl`, `FormGroup`, and `FormArray`. `FormRecord` tracks a collection of `FormControl` instances that share one value type. `FormControlName` binds a named control inside a group. `FormControlDirective` binds a standalone control. `FormArrayName` binds a nested array, and `FormArrayDirective` binds a standalone array.

### form-events-stream
- title: events unifies value, status, and submit
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

What does the `events` observable on a form control include?

---

`AbstractControl.events` emits `ValueChangeEvent`, `StatusChangeEvent`, `PristineChangeEvent`, `TouchedChangeEvent`, `FormResetEvent`, and `FormSubmittedEvent`. Status values include `VALID`, `INVALID`, `PENDING`, and `DISABLED`. Each event has a `source` control.

A value event fires right after that control updates, which can be before the parent group's `value` has updated. Subscribe to the parent when you need the parent value. `emitEvent: false` suppresses `valueChanges` and `statusChanges`. `onlySelf: true` stops the update from notifying parents. The default for both is the opposite.

### form-touched-dirty
- title: Touched and dirty are separate flags
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

What is the difference between touched and dirty?

---

Angular marks a control touched on focus and blur that do not change the value, and dirty when the value changes. `markAsTouched` and `markAsDirty` propagate to parents by default. `markAsUntouched` and `markAsPristine` cascade to children and then recalculate parents.

`markAllAsTouched` is how you reveal every validation error on submit. `markAllAsDirty` marks the control and its descendants. `patchValue` with `emitEvent: false` does not by itself mark the form dirty, so call `markAsDirty` when a programmatic edit should count as a user change.

### form-type-guards
- title: Narrow AbstractControl before using subgroup APIs
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

How do you know an `AbstractControl` is a `FormArray` inside a validator?

---

`isFormControl`, `isFormGroup`, `isFormRecord`, and `isFormArray` are type guards. When they return true, TypeScript narrows the control so you can use that subtype's API.

Custom validators receive `AbstractControl`. Returning `null` when the guard fails means "this validator does not apply", which is different from returning a validation error. That keeps a group validator from calling array-only APIs on the wrong control.

### template-validators
- title: Template validators are HTML attributes
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/form-validation

How do you validate a template-driven input?

---

Add the same attributes you would use for native HTML validation, such as `required` and `minlength`. Angular matches them to validator functions. On every value change the control becomes `INVALID` with an error list, or `VALID` when the result is `null`.

Export the directive with `#name="ngModel"` and read `invalid`, `dirty`, `touched`, and `hasError`. Show messages only when the control is invalid and either dirty or touched. A value change marks it dirty. Blur marks it touched. That avoids errors before the user has edited the field.

### reactive-validators
- title: Reactive validators are functions on the control
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/form-validation

Where do reactive form validators live?

---

Synchronous validators are functions that take a control and return errors or `null`. Pass one function, or an array of them, as the second argument to `FormControl`. Async validators return a Promise or Observable and are the third argument. Async validators run only after every sync validator passes, and each must complete before errors are set.

Built-in checks such as `Validators.required` and `Validators.minLength` mirror the template attributes. A `required` attribute can stay on the input for accessibility even though the class validators already enforce it. `get` on the parent finds a named child control.

### custom-validator-shape
- title: A validator returns null or an error map
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/form-validation

What should a custom `ValidatorFn` return?

---

A factory such as `forbiddenNameValidator` takes the configuration and returns a function of `AbstractControl`. That function returns `null` when the value is valid, or a `ValidationErrors` object whose key is the error name and whose value is extra data for the message.

For a template-driven custom validator, wrap the function in a directive that provides `NG_VALIDATORS` with `multi: true` and `useExisting`. `useClass` would construct a different instance and drop the bound inputs. Cross-field checks belong on a common ancestor, usually the `FormGroup`, because sibling controls cannot see each other.

### async-validators
- title: Async validators enter the pending state
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/form-validation

When does a control become `pending`?

---

Async validators run only after synchronous validation succeeds. The control stays `pending` until the Promise or Observable completes. The Observable must complete. Operators such as `first`, `last`, `take`, or `takeUntil` make an infinite stream finite. The last emitted value is the validation result.

Template-driven async validators provide `NG_ASYNC_VALIDATORS`. By default every validator runs on each change, which is expensive for HTTP checks. Set `updateOn` to `blur` or `submit` on `ngModelOptions` or on the `FormControl` options. After `addValidators`, `setValidators`, or `clearValidators`, call `updateValueAndValidity` or the status stays stale.

### form-status-classes
- title: Angular mirrors control state onto CSS classes
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/form-validation

Which CSS classes does Angular add to a form control?

---

The control element receives `ng-valid`, `ng-invalid`, `ng-pending`, `ng-pristine`, `ng-dirty`, `ng-untouched`, and `ng-touched`. The enclosing form element also receives `ng-submitted`.

You style from those classes instead of copying state into your own class bindings. By default Angular puts `novalidate` on the form and uses its own validator directives. `ngNativeValidate` turns native HTML validation back on.

### http-client-role
- title: HttpClient is the framework HTTP API
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/http

What does Angular give you for talking to a backend?

---

`HttpClient`, from `@angular/common/http`, is the client API for HTTP. The overview lists typed response values, error handling, request and response interception, and testing utilities as the main features.

The making-requests guide says to put that client behind an injectable service rather than calling it from every component. The service returns the `Observable`, and the template can subscribe with the `async` pipe.

### http-provide
- title: provideHttpClient configures the client
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/http/setup

How do you make `HttpClient` injectable?

---

The setup guide says `HttpClient` is available for injection by default in Angular v21 and later. `provideHttpClient` configures features in `ApplicationConfig` or in an `NgModule` `providers` array. Inject the client with `inject(HttpClient)`.

The default backend is `fetch`. `withXhr()` switches to `XMLHttpRequest`, which you need for upload progress. The guide says not to use `withXhr` for server rendering: XHR on the server is deprecated and intended to be removed in Angular 23, and the server XHR library can mishandle redirects. `withInterceptors` registers function interceptors. `withInterceptorsFromDi` enables the older class interceptors.

### http-parent-and-jsonp
- title: Child HttpClient does not use parent interceptors by default
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/setup

What does `withRequestsMadeViaParent` change?

---

`provideHttpClient` in a child injector replaces any `HttpClient` configuration from the parent. `withRequestsMadeViaParent` runs this injector's interceptors and then forwards the request to the parent `HttpClient`. There must already be an `HttpClient` above this injector, or using the option fails at runtime.

`withJsonpSupport`, `HttpClientJsonpModule`, and `HttpClient.jsonp` are deprecated because JSONP can cause cross-site scripting. Prefer CORS. `HttpClientModule` is also deprecated. Its equivalent is `provideHttpClient(withInterceptorsFromDi(), withXhr())`. Importing `HttpClientModule` in several injectors makes interceptor order poorly defined.

### http-cold-observable
- title: Each HttpClient subscription sends a request
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

Does calling `http.get` send the request immediately?

---

`HttpClient` methods return cold observables. Nothing is sent until something subscribes, and every subscription sends its own request. A generic such as `get<Config>` is a type assertion. `HttpClient` does not check that the JSON matches that type. Omit the generic and the body type is `Object`. The guide suggests `unknown` when the shape is uncertain.

Unsubscribing aborts an in-progress request, which is why the `async` pipe cancels work when the user navigates away and why `switchMap` drops a stale request. The observable usually completes after the response, though an interceptor can change that. Still unsubscribe in a component so a late callback does not touch a destroyed view.

### http-response-types
- title: responseType selects the body kind
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

How do you download text or bytes instead of JSON?

---

The default `responseType` is `'json'`. `'text'` returns a string, `'arraybuffer'` returns an `ArrayBuffer`, and `'blob'` returns a `Blob`. The option must be a literal type. If you pass options from a variable, write `as const` so TypeScript keeps the literal.

`post` takes a body before the options. Strings are sent as text, plain objects and arrays as JSON, `FormData` as multipart, and `HttpParams` or `URLSearchParams` as URL-encoded form data. You must subscribe to a mutation observable or the request never fires.

### http-params-headers
- title: HttpParams and HttpHeaders are immutable
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

What happens if you call `set` on an existing `HttpParams`?

---

`params` accepts a plain object or an `HttpParams` instance. `headers` accepts a plain object or `HttpHeaders`. Both classes are immutable. `set` and `append` return a new instance and leave the old one unchanged.

`HttpParams` uses `HttpUrlEncodingCodec` unless you pass a custom `HttpParameterCodec`. `observe: 'response'` emits the full response so you can read status and headers. `observe: 'events'` emits the lifecycle stream. Like `responseType`, `observe` must be a literal type. Download progress requires `reportDownloadProgress: true`.

### http-progress-and-errors
- title: Upload progress needs XHR, and status 0 is not HTTP
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/making-requests

Why does `reportUploadProgress` throw on the default client?

---

Progress events are off by default. The fetch backend does not support upload progress and throws if you set `reportUploadProgress`. Configure `provideHttpClient(withXhr())` when you need those events. Event types include `Sent`, `UploadProgress`, `ResponseHeader`, `DownloadProgress`, `Response`, and `User` for an interceptor's custom event.

Failures arrive as `HttpErrorResponse` on the observable error channel. Network and timeout errors use status `0`. A timeout's `error` is a `DOMException` named `TimeoutError`. The `timeout` option covers only the backend request, not time spent in interceptors. `catchError` can turn the error into a UI value, and `retry` resubscribes.

### http-integrity
- title: integrity checks the body before size limits
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/making-requests

What does the request `integrity` option guarantee?

---

`integrity` requires the response body to match the hash you provide. A mismatch fails as a network error. The making-requests guide recommends it for critical resources loaded from outside your origin.

During SSR, the fetch implementation reads the entire body to verify `integrity` before it returns, because the Fetch standard requires that. Angular applies `maxResponseBodySize` only after fetch returns, so that limit does not cap the bytes buffered during the integrity check.

### http-interceptors
- title: Functional interceptors run in listed order
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/interceptors

How do you add an auth header to every request?

---

A functional interceptor receives the `HttpRequest` and `next`. It returns an observable of `HttpEvent`. Register it with `provideHttpClient(withInterceptors([...]))`. Interceptors run in the order listed, and each can change the request or the response stream before calling `next`.

Most request and response fields are immutable, so you `clone` the request to change headers. The body is not protected from deep mutation. The interceptor runs in an injection context, so `inject(AuthService)` works. Skipping `next` lets you return a synthetic `HttpResponse`, for example from a cache.

### http-context
- title: HttpContext is metadata for interceptors
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/interceptors

How do you tell one interceptor to skip caching without sending a header to the server?

---

`HttpContext` is a typed map on the request, keyed by `HttpContextToken`. The token's factory supplies the default. Set it in the request options with `context: new HttpContext().set(CACHING_ENABLED, false)`. The interceptor reads `req.context.get`.

Unlike the rest of `HttpRequest`, the context object is mutable. A retry sees mutations an earlier pass stored there. Class-based interceptors implement `HttpInterceptor` and are enabled with `withInterceptorsFromDi()` plus a `multi: true` provider on `HTTP_INTERCEPTORS`. Their order follows provider registration and is hard to predict in a deep injector tree. The guide recommends functional interceptors.

### routes-and-provide-router
- title: provideRouter registers the route table
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/define-routes

How does a URL become a component?

---

A route object pairs a `path` with a `component` or other configuration. A `Routes` array is usually `src/app/app.routes.ts` in a CLI app. `provideRouter(routes)` adds the router when you bootstrap without relying on the CLI's defaults.

The router is the client-side piece that swaps content after the first `index.html` load, without a full page request. The routing overview splits that into routes, outlets, and links, and also lists nested routes, params, guards, and resolvers.

### route-matching-order
- title: The first matching route wins
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/define-routes

Why must `users/new` be listed before `users/:id`?

---

Angular stops at the first route whose `path` matches. More specific paths have to come before less specific ones. A static `users/new` listed after `users/:id` never runs, because `:id` already matched `new`.

A parameter starts with `:`. Names must start with a letter and may contain letters, digits, underscores, and hyphens. Parameters are not query-string values. `**` is the wildcard, usually last, and is the usual 404 route. `redirectTo` sends the user to another URL instead of creating a component.

### route-title-and-data
- title: The router can set the document title
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/define-routes

How do you set the page title for a route?

---

The `title` property can be a string. Angular updates the document title when the route activates. `title` can also be a `ResolveFn`. A custom `TitleStrategy` provided on the `TitleStrategy` token replaces `DefaultTitleStrategy` when every page needs the same suffix or breadcrumb format. `buildTitle` reads the route title, and `Title` from `@angular/platform-browser` writes the document.

`data` holds static metadata such as an analytics id. Dynamic needs use route resources or resolvers. Child routes go in `children`, and the parent template needs its own `router-outlet` or the child has nowhere to render. A route `providers` array is visible only to that route and its children.

### lazy-routes
- title: loadComponent splits a route out of the main bundle
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/loading-strategies

What is the difference between `component` and `loadComponent`?

---

`component` eagerly includes that component in the same JavaScript bundle as the route config. `loadComponent` and `loadChildren` take a function that returns a promise, usually a dynamic `import()`. A default export can be returned directly. The router requests that chunk only when the route is matched.

The router runs those loader functions in the route's injection context, so `inject` can read route, parent, or global providers and choose which file to import. The loading guide recommends eager routes for the primary landing page and lazy routes for the rest, and warns that nested lazy loads add later requests.

### route-input-binding
- title: withComponentInputBinding copies route state into inputs
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/common-router-tasks

How can a routed component read `:id` as an input?

---

Pass `withComponentInputBinding()` to `provideRouter`, or use `bindToComponentInputs` with `RouterModule.forRoot`. The router then assigns route data onto inputs of the same name. If nothing matches, the input becomes `undefined`, so optional inputs should include `undefined` in their type. A transform or a `linkedSignal` can supply a default.

When keys collide, priority is route resources, then `data` and resolvers, then path and matrix parameters, then query parameters. `queryParams: false` skips query binding. `unmatchedInputBehavior: 'undefinedIfStale'` avoids clearing inputs that were never supplied, except matrix parameters, which still clear when removed. Child routes inherit parent params and data unless you set `paramsInheritanceStrategy` to `'emptyOnly'`.

### router-link
- title: RouterLink navigates without a full reload
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/navigate-to-routes

How do you link to another route in a template?

---

Import `RouterLink` and put `routerLink` on an anchor. A string without a leading slash is relative to the current URL. A leading slash is absolute from the app root. An array is the form to use when a segment is dynamic, such as `['user', currentUserId]`.

`href` alone performs a normal browser navigation. `RouterLink` is what stays inside the single-page router. The `browserUrl` input can show a different address than the route that actually activates. The common tasks guide also describes the link parameters array: path segments, required parameters, and an object of optional matrix parameters.

### router-navigate
- title: navigate and navigateByUrl are different shapes
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/navigate-to-routes

When do you call `navigate` instead of `navigateByUrl`?

---

Inject `Router` and call `navigate` with a commands array when you are building a path from segments, query params, or matrix params. `relativeTo` plus `ActivatedRoute` resolves that array from the current route. `..` segments must all sit in the first command string. A leading slash on the first command makes the navigation absolute and ignores `relativeTo`.

`navigateByUrl` takes one URL string and is the absolute form for a full path, query string, and fragment. `replaceUrl: true` replaces the current history entry. `browserUrl` changes only what the address bar shows, not which route is matched.

### location-strategy
- title: PathLocationStrategy is the default URL style
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/common-router-tasks

What is the difference between path URLs and hash URLs?

---

`PathLocationStrategy` is the default HTML5 `pushState` style, so a crisis center lives at a path such as `/crisis-center`. `RouterModule.forRoot` selects that strategy. `HashLocationStrategy` puts the route after a hash so older browsers do not request a new page from the server.

You opt into the hash style by overriding the `LocationStrategy` provider while bootstrapping. The hierarchical injector guide shows the same idea as `{ provide: LocationStrategy, useClass: HashLocationStrategy }` in application providers.

### can-activate-guard
- title: canActivate can cancel or redirect
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/api/router/CanActivateFn

What can a `canActivate` guard return?

---

A `CanActivateFn` receives the `ActivatedRouteSnapshot` and `RouterStateSnapshot` and returns `MaybeAsync<GuardResult>`. You place the function on the route's `canActivate` array. It may call `inject` because guards run in an injection context.

If every guard returns `true`, navigation continues. If any returns `false`, navigation is cancelled. If any returns a `UrlTree`, the current navigation is cancelled and a new one starts toward that tree. That is the redirect path, not a second boolean.

### can-deactivate-guard
- title: canDeactivate sees the component instance
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/api/router/CanDeactivateFn

When does `canDeactivate` run, and what is its first argument?

---

`canDeactivate` runs when the user is leaving the route. The function receives the component instance, the current route snapshot, the current router state, and the next router state.

The results mean the same thing as `canActivate`: all `true` continues, any `false` cancels, and a `UrlTree` starts a new navigation. The API example checks a `hasUnsavedChanges` flag on the component and returns the opposite, so a dirty screen blocks the transition.

### can-match-guard
- title: canMatch skips a route instead of cancelling navigation
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/api/router/CanMatchFn

How is `canMatch` different from `canActivate`?

---

A `CanMatchFn` receives the `Route`, the `UrlSegment` list, and a partial match snapshot. It is listed on `canMatch`. If every guard returns `true`, the router may use that route. If any returns `false`, that route is skipped and other route configs are tried.

`canActivate` cancels the navigation when it returns `false`. `canMatch` only removes one candidate from matching. Use it when two routes share a shape and permission decides which configuration applies, not when you want to stop the user entirely.

### to-signal
- title: toSignal subscribes for you
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/ecosystem/rxjs-interop

How do you expose an observable as a signal?

---

`toSignal` from `@angular/core/rxjs-interop` subscribes immediately, like the `async` pipe, and unsubscribes when the creating component or service is destroyed. It must run in an injection context unless you pass an injector. Do not call it once per read. Reuse the signal.

If you omit `initialValue`, the signal is `undefined` until the first emission. The page compares that with the `async` pipe returning `null`. `requireSync: true` demands a synchronous first value, such as a `BehaviorSubject`, and then no initial value is required. `manualCleanup` opts out of automatic unsubscribe. `equal` suppresses updates when consecutive values compare the same.

### to-signal-errors
- title: A toSignal error surfaces when you read it
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/ecosystem/rxjs-interop

What happens if the observable passed to `toSignal` errors or completes?

---

If the observable errors, that error is thrown when the signal is read. If the observable completes, the signal keeps returning the last value it emitted.

`toObservable` goes the other direction. It watches the signal with an effect and emits into a `ReplaySubject`. The first value may be synchronous on subscription, and later values are asynchronous. Several `set` calls in one turn collapse to the last value, because signals do not notify synchronously. `rxResource` uses a `stream` function that returns an observable instead of a `loader`. That observable must emit a value or an error before it completes.

### async-pipe
- title: The async pipe subscribes and marks the view
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/api/common/AsyncPipe

What does the `async` pipe do with an observable or a promise?

---

`AsyncPipe` subscribes to an `Observable` or `Promise` and returns the latest emitted value. A new emission marks the component to be checked. When the component is destroyed, the pipe unsubscribes. If the expression's reference changes, it unsubscribes from the old source and subscribes to the new one.

`transform` returns `null` when the input is `null` or `undefined`. The pipe is exported by `CommonModule`, and a standalone component can import `AsyncPipe` directly. It is the template equivalent of remembering to unsubscribe.

### date-pipe-purity
- title: DatePipe ignores in-place Date mutation
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/api/common/DatePipe

Why does editing a `Date` object not refresh a `date` pipe?

---

`DatePipe` formats a `Date`, a number of milliseconds since the UTC epoch, or an ISO string. Usage is `date:format:timezone:locale`. It runs only for a pure change: a new primitive, or a new object reference. Mutating a `Date` does not count. Create a new `Date` when the displayed value should change.

If `format` is omitted, the pipe reads `DATE_PIPE_DEFAULT_OPTIONS` and otherwise uses `mediumDate`. The timezone argument overrides that token, and otherwise the local timezone is used. `locale` defaults to `LOCALE_ID`, which is `en-US`. Only `en-US` locale data ships with Angular. Other languages need their locale data imported. `DatePipe` is exported by `CommonModule`.

### test-runner-defaults
- title: ng test runs Vitest in jsdom
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/testing

What does `ng test` run in a new CLI project?

---

New CLI projects test with Vitest. Vitest runs unit tests in Node, and `jsdom` simulates the DOM. `happy-dom` is the other supported DOM library. `ng test` builds in watch mode and reruns when files change. The default include globs are `**/*.spec.ts` and `**/*.test.ts`.

Karma is still supported, and the testing guide points migrations at a separate Karma-to-Vitest page. `--coverage` writes a report under `coverage/`. In CI, a `CI=true` environment runs a single non-interactive pass. Otherwise pass `--no-watch` and `--no-progress`. `providersFile` can export default test providers such as `provideHttpClientTesting`.

### testbed-create-component
- title: createComponent freezes the TestBed
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/testing/components-basics

What does `TestBed.createComponent` return, and what can you no longer change?

---

`createComponent` builds the component, inserts a host element in the test DOM, and returns a `ComponentFixture`. Calling it freezes the current `TestBed` definition. Later `configureTestingModule` or `override` calls throw. The component class alone misses template bindings, so DOM tests exist to check that the class and template work together.

`fixture.componentInstance` is the class. `fixture.nativeElement` is the host, typed as `any` because the platform might not be a browser. `await fixture.whenStable()` waits for the initial render. `TestBed.compileComponents` is required only when the tested components use `@defer`. `DebugElement.query(By.css(...))` from `@angular/platform-browser` is the platform-neutral query. `querySelector` is fine when you know you are in a browser.

### testing-services
- title: TestBed.inject builds the service under test
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/testing/services

How do you unit test a service without rendering a component?

---

Services hold logic that should be tested apart from any template. `TestBed.inject` returns the service. The testing guide's example calls it in `beforeEach` so each test gets a fresh instance and does not leak state. A `@Service` class is available to that injector without an extra provider entry.

By default dependencies are real. Replace a slow or unstable one with `{ provide: Token, useValue: stub }`. A Vitest `vi.fn()` stub can both return a fixed value and assert the arguments it was called with. Clear the mock in `afterEach` so later tests do not see earlier calls. HTTP-specific fakes are documented in the HTTP testing guide, not in this page.

### zoneless-testbed
- title: TestBed is zoneless unless you opt into Zone
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/zoneless

How do you force a unit test to use Zone-based change detection?

---

`TestBed` uses zoneless change detection by default even if `zone.js` is in the test polyfills. Add `provideZoneChangeDetection()` to the testing providers when a test must run zoned. `provideZonelessChangeDetection()` is optional when you only want to be explicit.

`fixture.detectChanges()` forces a pass that production might not have scheduled. Updating a template value without a signal or `markForCheck` throws `ExpressionChangedAfterItHasBeenCheckedError`. `fixture.changeDetectorRef` belongs to the host view, so its `markForCheck` does not refresh an `OnPush` component's template. `provideCheckNoChangesConfig` is in developer preview and can periodically throw that same error when a binding changed without a notification.

### styles-travel-with-component
- title: Component CSS is part of the JavaScript output
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/styling

Where do component styles go in the build?

---

When Angular compiles a component, its styles are emitted with that component's JavaScript. Rendering the component includes those styles, including when the component is lazy-loaded.

The trap is treating component CSS as a separate global file the router might forget. The styling guide says the styles participate in the JavaScript module system, so the component and its CSS arrive together.

### css-preprocessors
- title: Component styles can come from Sass, Less, or Stylus
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/styling

Does a component style have to be plain CSS?

---

Angular works with any tool that outputs CSS, including Sass, Less, and Stylus. The component still receives CSS after that tool runs.

Encapsulation applies to the CSS Angular associates with the component. The preprocessor does not change the rule that emulated styles are scoped to the template.

### input-name-collisions
- title: Do not name an input after a DOM property
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/inputs

How should you choose an input name?

---

Avoid names that collide with properties on DOM elements such as `HTMLElement`. A collision makes it unclear whether the binding belongs to the component or the element. Do not prefix input names the way you prefix selectors. One element hosts one component, so a custom property is assumed to belong to that component.

The same page says aliases are the escape hatch when you must rename a property or avoid a native name. The alias changes the template name only.

### emit-event-data
- title: emit sends the payload the parent reads as $event
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/outputs

What does the parent receive when an output calls `emit`?

---

`emit` can send a primitive or an object. In the parent template, `$event` is that payload, and the handler method receives it as a normal argument.

The output name in the template is the property name unless you set an alias. The class still calls `emit` on the property, not on the alias.

### constructor-creates-instance
- title: The constructor runs when Angular creates the component
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/lifecycle

Is the constructor an Angular lifecycle hook?

---

The lifecycle guide lists `constructor` in the creation phase as the standard JavaScript constructor. It runs when Angular instantiates the component. The change-detection hooks, such as `ngOnInit` and `ngOnChanges`, run later while Angular walks the tree.

People put input-dependent work in the constructor. Initial inputs are ready at `ngOnInit`, which runs once after those inputs are set and before the component's own template is initialized.

### slot-fallback-content
- title: ng-content can show fallback children
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/components/content-projection

What appears if nobody projects a matching child?

---

Fallback content is markup you place inside the `ng-content` element. Angular shows it when the host has no matching projected child for that placeholder.

A selected slot and an unselected slot can each have their own fallback. If you omit an unselected `ng-content`, children that match no `select` are not rendered at all.

### for-accepts-iterables
- title: @for repeats any iterable
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/control-flow

What kinds of collections can `@for` walk?

---

`@for` repeats its block for any JavaScript iterable. Angular adds extra performance optimizations when the value is an array.

The block still needs a `track` expression so DOM nodes stay tied to items. There is no `break` or `continue`. Use `@empty` when the collection has no items.

### bare-ng-template
- title: ng-template does not render by itself
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/directives/structural-directives

What happens if you wrap elements in `ng-template` and add no structural directive?

---

`ng-template` defines a template that does not render anything by default. Without a structural directive, the elements inside are not shown.

A structural directive injects `TemplateRef` and decides when to create an embedded view. The asterisk form is only shorthand for putting that directive on an `ng-template` around the element.

### root-service-benefits
- title: A root service is one shared tree-shakable instance
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/di/creating-and-using-services

What do you get when a service is provided at the root?

---

The creating-services guide says a globally provided service gives three things: one shared instance for the application, availability without a manual provider registration, and tree-shaking so an unused service can be dropped from the production bundle.

`@Service` is the shorthand that provides the class at the root. `@Injectable` does not do that unless you set `providedIn: 'root'`. Inject the service with `inject()` in a component or in another service.

### one-control-form-control
- title: FormControl tracks a single field
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

What does one `FormControl` represent?

---

`FormControl` manages the value and validity of one control, corresponding to one HTML control such as an input. `AbstractControl` is the base class it shares with `FormGroup` and `FormArray`.

Read the current value from `value`, or listen to `valueChanges`. `setValue` replaces that value. On a single control the example sets a string. On a group, the same method must match the group's structure.

### group-versus-array
- title: FormGroup is fixed, FormArray grows
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

When do you use `FormGroup` instead of `FormArray`?

---

`FormGroup` tracks a fixed set of named controls and can nest other groups. The top-level form in a component is a `FormGroup`. `FormArray` tracks a numerically indexed list of controls, and you add or remove controls at run time.

`FormRecord` is the other collection type in the API summary: a set of `FormControl` instances that share the same value type. `FormBuilder.group`, `control`, and `array` are the factory methods for these instances.

### import-reactive-forms
- title: Reactive bindings need ReactiveFormsModule
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/reactive-forms

Why does `[formControl]` fail until you import something?

---

The reactive forms guide imports `ReactiveFormsModule` from `@angular/forms` on the component that binds `[formControl]`, `formGroup`, or `formControlName`. The directives that sync a class model to the DOM live in that module.

`FormControlDirective` syncs a standalone `FormControl`. `FormControlName` syncs a named control inside a group. `FormGroupDirective` and `FormGroupName` sync groups. `FormArrayName` syncs a nested array, and `FormArrayDirective` syncs a standalone array.

### import-forms-module
- title: ngModel comes from FormsModule
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms

Which import makes `[(ngModel)]` work?

---

The template-driven example imports `FormsModule` and binds `[(ngModel)]`. `NgModel` creates and manages the `FormControl`. The template is the source of truth.

Reactive forms import `ReactiveFormsModule` instead and construct the control in the class. Mixing up the two imports is why a template compiles with the directive missing or the wrong binding syntax.

### control-value-accessor
- title: ControlValueAccessor connects DOM and FormControl
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms

What sits between a `FormControl` and a native input?

---

Both form styles are built on `FormControl`, `FormGroup`, `FormArray`, and `ControlValueAccessor`. The accessor is the bridge between a `FormControl` and a built-in DOM element.

In the reactive data-flow description, the accessor listens for the input event and relays the value to the control, and it writes programmatic `setValue` updates back onto the element. Template-driven flow also goes through an accessor, then through `NgModel.viewToModelUpdate()`.

### http-get-arguments
- title: HttpClient.get takes a URL and options
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/http/making-requests

What arguments does `HttpClient.get` take?

---

`get` takes the endpoint URL and an optional options object. A generic argument such as `get<Config>` asserts the JSON type. If you omit it, the body is typed as `Object`. The client does not verify that the payload matches the generic.

`post` is the same idea with a body argument before the options. Strings are sent as text, and plain objects, arrays, numbers, and booleans are sent as JSON.

### subscribe-to-send
- title: A request is not sent until something subscribes
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/http/making-requests

You called `http.post` and the server saw nothing. What was missing?

---

`HttpClient` returns a cold observable. The request is dispatched only when that observable is subscribed, and each subscription sends its own request. The making-requests guide says to subscribe to mutation observables or the request never fires.

Unsubscribing aborts a request that is still in progress. After a normal response, the observable usually completes. The guide still recommends cleaning up a component subscription so a callback does not run against a destroyed view.

### route-parameter-syntax
- title: A colon marks a route parameter
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/define-routes

How do you say that `/user/leeroy` and `/user/jenkins` use the same component?

---

Put a colon in the path, as in `user/:id`. Both URLs render that route's component, and the component reads `id`. A parameter name must start with a letter and may contain letters, digits, underscores, and hyphens. You can declare more than one parameter in one path.

Parameters are not query-string values. The define-routes guide points to the reading-route-state guide for how to read them. Static segments and dynamic segments are matched in array order, first match wins.

### wildcard-route-last
- title: A double asterisk is the fallback route
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/common-router-tasks

How do you show a 404 page?

---

Add a route whose `path` is `**` and whose `component` is the not-found page. The router selects it when the URL matches nothing earlier in the list.

Put that route last. The define-routes guide uses the same wildcard and says Angular stops at the first match, so an early `**` would swallow every URL.

### nested-router-outlet
- title: Child routes render in the parent's outlet
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/define-routes

Where does a child route's component appear?

---

Child routes live in the parent's `children` array. The parent component includes its own `router-outlet`. Navigating between child URLs updates that nested outlet.

The routing overview describes outlets as the placeholders that render the active route. Without an outlet in the parent, the child configuration has nowhere to show its component.

### absolute-link-slash
- title: A leading slash makes a RouterLink absolute
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/navigate-to-routes

On `/settings`, where does `routerLink="notifications"` go?

---

A `routerLink` without a leading slash is relative to the current URL, so that link goes to `/settings/notifications`. A leading slash starts from the root, so `routerLink="/settings/notifications"` is the absolute form of the same path.

A string is the usual relative form. Use an array when a segment is a variable, such as `['user', currentUserId]`. Import `RouterLink` on the component that uses it.

### navigate-with-query-params
- title: navigate can set query parameters
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing/navigate-to-routes

How do you go to `/search?category=books&sort=price` from code?

---

Inject `Router` and call `navigate` with a commands array and a `queryParams` object. The same method accepts a matrix-parameter object as a command, such as `['/products', { featured: true }]`.

`navigateByUrl` is the other method: it takes one URL string, including query and fragment, rather than an array of commands. Use `navigate` when you are assembling the path from pieces.

### import-the-async-pipe
- title: Standalone templates import AsyncPipe
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/api/common/AsyncPipe

How do you use the `async` pipe in a standalone component?

---

Import `AsyncPipe` from `@angular/common` in the component `imports` array. The pipe is also exported by `CommonModule`. The template syntax is `value | async`.

The pipe subscribes to an `Observable` or a `Promise`, returns the latest value, and marks the view for check on each emission. It unsubscribes when the component is destroyed. Passing `null` or `undefined` yields `null`.

### date-pipe-default
- title: DatePipe defaults to mediumDate
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/api/common/DatePipe

What format does `{{ today | date }}` use?

---

The pipe usage is `date:format:timezone:locale`. When `format` is omitted and `DATE_PIPE_DEFAULT_OPTIONS` does not set `dateFormat`, the format is `mediumDate`. A missing timezone uses the local system timezone unless that token sets one. A missing locale uses `LOCALE_ID`, which is `en-US` by default.

The value may be a `Date`, a number of milliseconds since the UTC epoch, or an ISO string. `null` or `undefined` produces `null`. `DatePipe` is exported by `CommonModule`.

### ng-test-reruns
- title: ng test watches files
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/testing

What does `ng test` do after the first run?

---

`ng test` builds the app in watch mode and launches Vitest. Saving a file runs the tests again. New CLI projects include Vitest and `jsdom`. Vitest executes in Node, and `jsdom` simulates the DOM. `happy-dom` is the other supported DOM library.

When `CI` is set, `ng test` runs once, without watch mode. You can force that with `--no-watch` and `--no-progress`. `--coverage` writes a report in the `coverage` directory.

### cli-writes-a-spec
- title: Generating a component also generates a spec
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/testing/components-basics

What test file does `ng generate component` create?

---

The CLI creates an initial spec beside the component. The basics guide shows `TestBed.createComponent`, `fixture.componentInstance`, and `await fixture.whenStable()` inside `beforeEach`, plus a test that the instance is truthy.

That test only proves Angular can construct the component. The guide says a real component test also has to look at the DOM, because the class alone cannot tell you that a binding or a click handler is wired.

### fixture-text-content
- title: Read the rendered host from the fixture
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/testing/components-basics

How do you assert the text a component rendered?

---

`ComponentFixture.nativeElement` is the host element. The guide reads `textContent` and also uses `querySelector` when the test runs in a browser. `await fixture.whenStable()` in `beforeEach` waits for the first render so the later tests can stay synchronous.

`nativeElement` is typed as `any` because a non-browser platform may not provide a full `HTMLElement`. `fixture.debugElement.nativeElement` is the same element reached through Angular's `DebugElement` wrapper.

### defer-shows-nothing-first
- title: A defer block is blank until it triggers
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/defer

What does the user see before an `@defer` block loads?

---

By default a defer block renders nothing before it is triggered, and the default trigger is browser idle. Add `@placeholder` to show something earlier. `@loading` replaces the placeholder while the chunk loads. `@error` shows if the load fails.

The main block's dependencies can be deferred. The placeholder, loading, and error blocks are eagerly loaded, so keep them small. `@placeholder` can take a `minimum` time so a fast response does not flicker.

### provider-class-shorthand
- title: A class in providers means useClass
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

What does `providers: [LocalService]` expand to?

---

It is shorthand for `{ provide: LocalService, useClass: LocalService }`. The class is both the key and the implementation. `useValue` supplies a ready-made value, `useFactory` calls a function, and `useExisting` aliases a token that is already provided.

A class with no `providedIn` and no `@Service` root provider must appear in some `providers` array. Otherwise there is nothing to inject.

### valid-status-is-null
- title: A valid control has no error object
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/forms/form-validation

What does Angular store when a control passes validation?

---

On each value change, validation either produces an error list and the status `INVALID`, or `null` and the status `VALID`. Template-driven fields use the same attribute names as native validation, and Angular maps those attributes to validator functions.

Export `ngModel` to a template variable to read `invalid`, `dirty`, `touched`, and `hasError`. The guide says to show messages only when the control is invalid and either dirty or touched, so the user does not see errors before they edit.

### cli-includes-router
- title: The CLI includes the Angular router
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/routing

Do you add a third-party router to a new Angular app?

---

`@angular/router` is the official router and a core part of the framework. The routing overview says it is included by default in projects the Angular CLI creates.

A single-page app loads `index.html` once. After that the router chooses content from the URL without a full page reload. Routes, outlets, and links are the three pieces the overview names.

### host-metadata-bindings
- title: A directive can bind its host from metadata
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/directives

How does a directive listen to the element it is attached to?

---

The `host` object on `@Directive` maps host events to statements and host bindings to expressions. The overview's highlight directive sets a signal on `mouseenter` and `mouseleave` and binds `background-color` to that signal.

Apply the directive by putting its attribute selector on an element. Every matching element gets the same behavior. If you need your own markup, the guide says to use a component instead.

### pipe-operator
- title: The pipe character is template syntax
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/guide/templates/expression-syntax

Where can you use a pipe in a template?

---

The expression guide lists the pipe operator, written as `total | currency`, as template syntax on top of the JavaScript operators it supports. Event listener statements do not support pipes.

Pipes also cannot appear inside an arrow function. You can pass an arrow function as an argument to a pipe. Assignment operators belong in event statements, not in a binding, unless they are inside an arrow function.

### date-format-presets
- title: DatePipe has named formats
- version: Core
- level: beginner
- status: verified
- source: https://angular.dev/api/common/DatePipe

What does the `medium` date format mean?

---

`DatePipe` accepts predefined names. `mediumDate` is `MMM d, y`. `short`, `medium`, `long`, and `full` add time, and the matching `Time` names format only the time. The API page gives `en-US` examples for each name.

A custom format string uses symbols such as `y`, `M`, and `d`. Quoted text in the format is literal, as in the example that inserts the word "at". Only `en-US` locale data is included until you import more.

### ngclass-for-mutation
- title: Class bindings do not see in-place edits
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/binding

When does the binding guide tell you to use `ngClass`?

---

`[class]` on an array or object updates only when the reference changes under `===`. A single `[class.name]` key cannot be a space-separated list of classes. Mutating the same object leaves the binding unchanged.

The binding guide says to use the `ngClass` directive when you need space-separated names in one key or when you mutate the object. Otherwise create a new array or object. Angular also does not promise any order among the classes it writes.

### style-specificity-limit
- title: Encapsulated styles do not always win
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/components/styling

Does emulated encapsulation guarantee your component CSS beats global CSS?

---

In `Emulated` and `ShadowDom` modes, Angular does not fully guarantee that component styles override styles from outside. The styling guide assumes the outside styles have the same specificity when they collide.

`None` turns the component's styles into global styles. External styles loaded through a template `link` or a CSS `@import` are not emulated at all. Global styles can also affect the inside of an emulated component.

### query-by-template-variable
- title: ViewChild can find a template variable
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/variables

How do you query one specific input from the component class?

---

Declare a template reference variable on the element, such as `#description`. `ViewChild('description')` then queries that variable. The variables guide shows the result typed as `ElementRef` or `undefined`.

The same hash on a component refers to the component instance, and on `ng-template` it refers to a `TemplateRef`. A variable declared inside `@if` or `@for` is not visible outside that nested scope.

### at-let-one-binding
- title: Each @let declares one name
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/variables

Can one `@let` line declare two variables?

---

No. Each `@let` declares exactly one variable, then `=`, then an Angular expression, then a semicolon. The expression may span lines. You cannot separate two names with a comma.

The declaration is not hoisted and cannot be reassigned. It is visible in the current view and in descendant views, including views created by `@if`, `@for`, `@defer`, and structural directives. Sibling and parent views cannot read it.

### viewport-needs-one-root
- title: A viewport placeholder needs one root
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/defer

What does `@defer (on viewport)` watch?

---

By default it watches the placeholder entering the viewport, using the Intersection Observer API. A placeholder used that way must have a single root element. You can instead pass a template reference variable, including inside an options object with `rootMargin` and `threshold`. The options object does not accept `root`.

`on interaction` watches `click` or `keydown` on the placeholder or on a passed reference, and that placeholder must also have one root. `on hover` uses `mouseover` and `focusin` the same way.

### interaction-versus-hover
- title: immediate and timer fire without a gesture
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/templates/defer

Which `@defer` triggers do not wait for the user?

---

`on idle` is the default and can take a timeout passed to `requestIdleCallback`, as in `on idle(500)`. `on immediate` loads as soon as non-deferred content has finished rendering. `on timer` takes a duration in `ms` or `s`. `when` loads once a boolean expression becomes truthy and does not revert if it becomes falsy.

`prefetch` uses the same trigger vocabulary after a semicolon, but it only fetches the JavaScript. The main trigger still decides when the block renders.

### update-on-option
- title: updateOn delays validation
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms/form-validation

How do you stop an async validator from running on every keystroke?

---

The default `updateOn` value is `change`, so validators run after every value change. Set it to `blur` or `submit`. In a template, that is `ngModelOptions`. On a reactive control, it is an option on the `FormControl`.

Async validators already wait until synchronous validators pass, and the control is `pending` until the async result completes. Delaying `updateOn` avoids an HTTP call per character. After you `setValidators` or `clearValidators`, call `updateValueAndValidity` or the status is not recomputed.

### testing-form-data-flow
- title: Template-driven form tests wait for a turn
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/forms

Why does the template-driven form test call `whenStable`?

---

Reactive form updates are synchronous. The forms guide's reactive test sets the input value, dispatches an `input` event, and reads `favoriteColorControl.value` in the same test. The model-to-view test calls `setValue` and reads the input immediately.

Template-driven model updates are asynchronous. Those tests `await fixture.whenStable()` after the event, or after setting the component value, before they assert. The guide says template-driven tests depend on understanding change detection. Reactive tests can query status without rendering when they only touch the control.

### http-cache-modes
- title: The cache option talks to the browser HTTP cache
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

What do `force-cache`, `no-cache`, and `only-if-cached` mean on `HttpClient`?

---

These `cache` values are fetch-backend options. `force-cache` uses a cached response regardless of freshness. `no-cache` always uses the network. `only-if-cached` uses the cache and fails when the response is not cached.

The making-requests guide says the advanced fetch options apply when `HttpClient` uses the fetch backend, which is the default. They are request options beside `headers` and `params`, not interceptor features.

### request-priority
- title: priority hints which request matters
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

What values can the HTTP `priority` option take?

---

`high`, `low`, and `auto`. `auto` is the default and lets the browser decide. The guide says to use `high` for requests that affect Largest Contentful Paint and `low` for work that does not affect the initial experience.

This is a fetch-backend option on the request. It does not change the URL or headers by itself. It tells the browser the relative importance of the load.

### credential-modes
- title: withCredentials overrides credentials
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

When does `HttpClient` send cookies on a cross-origin request?

---

`credentials: 'same-origin'` is the default and sends credentials only to the same origin. `'omit'` never sends them. `'include'` sends them on cross-origin requests too. `withCredentials: true` forces `'include'` and wins if both options are set.

The guide says the `credentials` option does not strip `Cookie` or `Authorization` headers you set yourself. During SSR on Node, `'include'` does not automatically forward cookies from the incoming browser request.

### redirect-modes
- title: redirect follow is the default
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

How do you stop `HttpClient` from following a redirect?

---

The fetch-backend `redirect` option is `'follow'` by default, `'error'` to fail the request, or `'manual'` to return the redirect response so you can handle it. The guide suggests `manual` when the redirect needs custom logic.

On the fetch backend, a response event can also expose `redirected`, which the interceptors guide says means the response came from a redirect. That flag matches the Fetch specification. It is not the same as the `redirect` request option.

### read-http-events
- title: observe events is the full HTTP lifecycle
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/http/making-requests

What does `observe: 'events'` give you that `observe: 'response'` does not?

---

The default observable emits the body. `observe: 'response'` emits the full response, including status and headers. `observe: 'events'` emits the sequence of `HttpEvent` values: sent, upload progress, response header, download progress, the final response, and a user event from an interceptor.

Upload progress is off unless you set `reportUploadProgress`, and the fetch backend throws if you ask for it. Download progress needs `reportDownloadProgress`. Both `observe` values must be literal types, so a helper that returns a plain `string` needs `as const`.

### route-scoped-providers
- title: Route providers stay inside that route
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/define-routes

Who can inject a service provided on a route?

---

A route's `providers` array is available to that route's content and its child routes. The define-routes example puts `AdminService` and a token on the `admin` path so sibling routes outside that section cannot inject them.

The defining-providers guide lists the same three places to register a provider: application bootstrap, a component or directive element, and a route. Component providers are the choice when each component tree needs its own instance.

### matrix-parameter-object
- title: An object in a link is a matrix parameter
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/common-router-tasks

What does `{foo: 'foo'}` mean inside a `routerLink` array?

---

The link parameters array holds the path, required parameters, and optional parameters. An object in that array is a matrix parameter tied to a URL segment, not a query string. The common-tasks example uses `['/crisis-center', {foo: 'foo'}]`.

`navigate` uses the same object form for matrix parameters and a separate `queryParams` option for the query string. A child link appends segments after the parent path. The resulting URL follows the order of the array.

### replace-url-option
- title: replaceUrl rewrites the current history entry
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/routing/navigate-to-routes

How do you navigate without pushing a new history entry?

---

`router.navigateByUrl` accepts `{ replaceUrl: true }` to replace the current URL in history. The method itself takes a full URL string, so query, fragment, and matrix parameters are written in that string.

`browserUrl` is a different option. Navigation still matches the URL you passed to `navigateByUrl`, but the address bar shows `browserUrl`. `RouterLink` has the same `browserUrl` input. A leading slash in `navigate` ignores `relativeTo`.

### factory-deps
- title: useFactory lists dependencies in deps
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

How does a `useFactory` provider receive other services?

---

`useFactory` is a function that returns the value to inject. List the tokens that function needs in `deps`, in argument order. The defining-providers example builds a `LoggerService` from an `APP_CONFIG` token that way.

`useClass` still constructs a new instance of a class. `useExisting` does not. It aliases an existing token so both keys return one instance. A bootstrap provider is the right place for `provideRouter` or `provideHttpClient`, because those have configuration and side effects. A `providedIn: 'root'` service is the tree-shakable alternative when you do not need that configuration.

### bootstrap-provider-cost
- title: A bootstrap provider is always bundled
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

What is the cost of putting a provider in `bootstrapApplication`?

---

An application-level provider is one shared instance available everywhere, which is what you want for logging, configuration, and other global values. The defining-providers guide also says that provider is always included in the JavaScript bundle, even if nothing injects it.

`providedIn: 'root'` or `@Service` can be tree-shaken when unused. Choose bootstrap when the provider has side effects, needs configuration such as routes, or is a `provideSomething` function. Choose a component `providers` array when each component should get its own instance.

### run-tests-in-browser
- title: ng test can launch a real browser
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/guide/testing

How do you run Angular unit tests in Chromium instead of jsdom?

---

The default is Node plus `jsdom`. For a real browser, install a browser provider and set `browsers` in `angular.json` or pass `--browsers`. The testing guide's Playwright example is `ng test --browsers=chromium`, and `chromiumHeadless` forces headless mode. If `CI` is set, headless mode is used unless you override it.

`runnerConfig` points at a custom Vitest config. The CLI overrides `test.projects` and `test.include`, and the Angular team does not support the contents of that file or third-party plugins. `ng generate config vitest` writes a starting config.

### require-sync-option
- title: requireSync demands a value immediately
- version: Core
- level: intermediate
- status: verified
- source: https://angular.dev/ecosystem/rxjs-interop

When would you set `requireSync` on `toSignal`?

---

Signals always have a current value. An observable might not. `initialValue` covers the gap until the first emission. If you omit it, the signal is `undefined` until then. `requireSync: true` requires the observable to emit synchronously on subscription, which a `BehaviorSubject` does, and then you do not pass an initial value.

`toSignal` subscribes immediately and, by default, unsubscribes when its creator is destroyed. It needs an injection context unless you pass an injector. Reuse one signal. Calling `toSignal` again subscribes again.

### ssr-cors-mode
- title: same-origin mode is not a server allowlist
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/making-requests

Does `mode: 'same-origin'` protect a request during server rendering?

---

In the browser, `same-origin` fails cross-origin requests, `cors` allows CORS requests and is the default, and `no-cors` allows simple cross-origin requests whose response is opaque. The making-requests guide says to use `same-origin` for sensitive browser requests.

During SSR on Node, `HttpClient` uses Undici. Undici does not enforce browser CORS checks, so `mode: 'same-origin'` does not restrict those server-side requests. The guide says to validate user-influenced URLs against an allowlist.

### ssr-credential-cookies
- title: SSR does not copy the browser cookie jar
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/making-requests

Will `credentials: 'include'` forward the user's cookies from an SSR request?

---

No. The making-requests guide says that during SSR on Node, `credentials: 'include'` does not automatically forward cookies from the incoming browser request. Explicit `Cookie` or `Authorization` headers you add are not removed by the `credentials` option.

Undici also permits some headers that browsers forbid. The guide says to forward credential headers only to trusted origins. `withCredentials: true` still forces `credentials: 'include'` when both are set.

### fetch-response-type
- title: responseType tells you how CORS classified the body
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/interceptors

What does `responseType` mean on an HTTP response event?

---

When `HttpClient` uses the fetch backend, a response event has `responseType`. The interceptors guide lists `'basic'` for a same-origin response, `'cors'` when CORS headers allow access, `'opaque'` when the cross-origin response has no CORS and headers or body may be limited, `'opaqueredirect'` for a redirected no-cors response, and `'error'` for a network error.

That field follows the Fetch specification. It is not the request `responseType` option that chooses JSON, text, or bytes. An interceptor can branch on it when debugging CORS. The same page says functional interceptors are preferred because DI-based interceptor order follows provider registration and is hard to predict.

### keepalive-requests
- title: keepalive lets a request outlive the page
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/http/making-requests

What is the `keepalive` option on an `HttpClient` request?

---

On the fetch backend, `keepalive: true` allows the request to continue after the page that started it goes away. The making-requests guide points at analytics or logging calls that should finish even if the user navigates away.

It is a request option next to `cache`, `priority`, `mode`, `redirect`, and `credentials`. Those options are available because the default backend is `fetch`. Upload progress is the feature that still requires `withXhr()`, and that backend does not use these fetch options.

### optional-factory-deps
- title: Factory deps can be optional
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

How do you mark one `useFactory` dependency as optional?

---

`deps` lists tokens in parameter order. An optional dependency is wrapped, as in `deps: [RequiredService, [new Optional(), OptionalService]]`. The factory argument for that token may be missing, and the example substitutes a default service.

This is constructor-style `deps`, not `inject()` inside the factory. `@Service` factories are a different API: they run in an injection context and call `inject`. A `multi: true` provider does not replace earlier values. Injecting that token returns an array of every contributed instance.

### resource-abort-signal
- title: A resource aborts the previous load
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals/resource

What happens if resource params change while a load is in flight?

---

The resource aborts the outstanding load. The loader's `abortSignal` is the handle to pass to APIs that understand it, such as `fetch`. If `params` returns `undefined`, the loader does not run and the status becomes `idle`.

`reload()` runs the loader again and the status is `reloading`, which keeps the previous value. A params change uses `loading`. `stream` is for a source that keeps emitting. `loader` is for one request. `httpResource` sends that request through `HttpClient` and its interceptors.

### module-injector-lazy
- title: A lazy NgModule gets its own injector
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/hierarchical-dependency-injection

How does a lazy-loaded `NgModule` get providers?

---

In an `NgModule` app, the `ModuleInjector` is the flattened set of `providers` reachable through `NgModule.imports`. Lazy-loading another `NgModule` creates a child `ModuleInjector`.

If an element injector does not have the token, an `NgModule` app continues the search in that module injector hierarchy. Standalone apps configure the environment injector with `@Service` or `ApplicationConfig.providers` instead. A provider on `ApplicationConfig` overrides one registered for `root`.

### multi-token-array
- title: multi true collects every provider
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/di/defining-dependency-providers

What do you get if you inject a `multi: true` token?

---

Each provider with `multi: true` adds a value instead of replacing the previous one. Injecting the token returns an array of those instances. The defining-providers guide uses that shape for a list of interceptors.

Without `multi`, a second provider for the same token replaces the earlier one at that injector. `useExisting` is not multi. It is an alias, so two tokens share one instance. `useClass` would construct another instance.

### pending-tasks
- title: PendingTasks keeps SSR from serializing early
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/zoneless

How does a zoneless server render know the page is not ready?

---

Without Zone.js, async work must be registered with `PendingTasks`. `run` wraps an async function. `add` returns a cleanup you call in `finally`. Serialization waits until pending tasks are gone. `pendingUntilEvent` in `rxjs-interop` keeps the app unstable until an observable emits, completes, errors, or is unsubscribed.

The framework already tracks an in-flight router navigation and an incomplete `HttpClient` request this way. `NgZone.onStable` will not tell you, because those observables never emit in a zoneless app and `isStable` stays `true`.

### custom-idle-service
- title: You can replace the defer idle scheduler
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/templates/defer

How do you change when `on idle` considers the browser idle?

---

Provide an `IdleService` implementation with `provideIdleServiceWith` in the application providers. The defer guide's example implements `requestOnIdle` and `cancelOnIdle` and can delegate to `requestIdleCallback`.

`on idle` is still the default trigger, and `on idle(500)` still passes a timeout. The custom service changes how that callback is scheduled. It does not change `when`, `timer`, or `viewport`.

### defer-live-region
- title: Screen readers may miss a defer swap
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/templates/defer

How does the defer guide suggest announcing a late-loaded block?

---

A screen reader focused on a deferred section reads the placeholder or loading text first and may not announce the swap when the real content arrives. The guide wraps the `@defer` block in an element with `aria-live="polite"` and `aria-atomic="true"` so the placeholder, loading, content, and error transitions are announced.

That is separate from the loading performance advice: do not defer something already in the initial viewport if the swap would increase cumulative layout shift, and give nested defer blocks different triggers so they do not fetch at once.

### signal-custom-equality
- title: Signals compare with Object.is unless you say otherwise
- version: Core
- level: experienced
- status: verified
- source: https://angular.dev/guide/signals

When does `set` not notify readers?

---

The default equality is `Object.is`. A new object or array notifies even when the contents look the same. Pass `equal` to `signal` or `computed` to compare by value. The signals guide's example uses a deep compare so setting another `['test']` array does not update.

`asReadonly()` blocks `set` and `update` on the public signal, but it does not freeze the object inside. Mutating that object still will not notify, because the signal never saw a `set`. `computed` stays lazy: it recalculates on read after a real dependency change, and only the signals read on that run stay dependencies.
