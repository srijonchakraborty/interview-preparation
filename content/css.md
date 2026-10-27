# CSS

### specificity
- title: Specificity is a tuple, not a score you add up
- version: Fundamentals
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity

Two rules match the same element. One is `.nav a`, the other is `a`. Which declaration wins, and how do you compare them?

---

Compare specificity as a tuple, left to right: inline style, then IDs, then classes / attributes / pseudo-classes, then elements / pseudo-elements. `.nav a` is one class and one element, so it beats a bare `a`.

Equal tuples fall through to source order. `!important` and cascade layers are separate cascade steps, not extra specificity points. `:where()` adds none. `:is()` takes the most specific selector in its list. A universal selector adds none.

### box-model
- title: content-box versus border-box
- version: Fundamentals
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing

You set `width: 200px` and `padding: 20px` on a div. How wide is the border box under the default `box-sizing`, and what does `border-box` change?

---

The initial value is `content-box`. `width` and `height` size the content box only, so padding and border are added outside that width. With 20px padding on both sides and no border, the border box is 240px.

`box-sizing: border-box` makes `width` include padding and border. Margin stays outside the border box in both modes. A global `border-box` reset is common, but it does not remove margin or change the cascade.

### margin-collapse
- title: When vertical margins collapse
- version: Fundamentals
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model/Mastering_margin_collapsing

Two block siblings have `margin-bottom: 30px` and `margin-top: 20px`. What is the space between them, and which layouts do not collapse margins?

---

Adjoining vertical margins collapse into one margin. The space is the larger of the two, 30px, not 50px. If one margin is negative, the result is the algebraic sum of the most positive and the most negative. Horizontal margins never collapse.

Parent and first or last child can collapse too, when nothing separates them: no padding, border, or block formatting context on the parent. Margins of flex items, grid items, and floats do not collapse with each other. Overflow other than `visible` on the parent also stops parent-child collapse.

### stacking-context
- title: z-index only compares inside a stacking context
- version: Fundamentals
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context

A child has `z-index: 9999`, but it still paints under a sibling of its parent. The parent is `position: relative` with `z-index: 1` and `opacity: 0.99`. Why?

---

`z-index` competes only inside the same stacking context. A new context isolates its descendants. The whole parent context is then ordered against the parent's siblings. A descendant cannot climb out and beat an element in a higher context, no matter how large its `z-index` is.

A context is created by a positioned element whose `z-index` is not `auto`, and also by `opacity` less than 1, `transform`, `filter`, `will-change`, and `isolation: isolate`, among others. `opacity: 0.99` is enough even when the position and z-index would not be.

### flex-versus-grid
- title: Flexbox lays out one axis, grid lays out two
- version: Layout
- level: beginner
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox

When do you choose flexbox, and when do you choose grid? What is wrong with saying "flex is one-dimensional so it cannot wrap"?

---

Flexbox is a one-dimensional layout model. Items are laid out along the main axis, then wrapping starts another line. The lines do not form a strict two-dimensional grid: items do not have to line up in both axes the way grid cells do.

Grid is two-dimensional. Rows and columns are defined together, so it fits page regions, forms, and anything that must align in both directions. Use flex for a toolbar, a row of actions, or distributing space inside a component. Use grid when horizontal and vertical placement are both part of the design. Wrapping a flex container does not turn it into grid.

### position-sticky
- title: Why position sticky sometimes never sticks
- version: Layout
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/position

`position: sticky; top: 0` is set on a header inside a card, but the header scrolls away. What is sticky positioning actually relative to?

---

A sticky box is laid out like `relative` until it crosses the sticky threshold, then it is treated as fixed inside its scrollport. It never escapes its containing block. `top`, `right`, `bottom`, or `left` must set the inset, or there is no threshold to cross.

Any ancestor that is a scroll container can become the sticky element's scrollport. `overflow: hidden`, `auto`, or `scroll` on an ancestor is the usual reason a sticky header appears broken. The element also stops sticking at the end of its containing block, so a short parent gives it nowhere to travel.

### cascade-layers
- title: Cascade layers order whole stylesheets
- version: Modern
- level: experienced
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer

You import a component library and your class selector loses to the library's element selector. How do `@layer` declarations change the result without raising specificity?

---

Unlayered styles beat layered styles. Inside layers, later layers win over earlier layers. Declare the order up front with `@layer reset, library, app;`. Specificity still matters inside a single layer, but a low-specificity rule in a later layer beats a high-specificity rule in an earlier layer.

That is the point for interview work: layers control the cascade before specificity. Use them to keep third-party CSS from fighting your app, instead of adding IDs or `!important`. `!important` reverses layer order, so it is still a poor escape hatch.

### is-versus-where
- title: :is() keeps specificity, :where() zeroes it
- version: Modern
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/:where

What is the specificity of `:is(.nav, #main) a` versus `:where(.nav, #main) a`? Why do both selectors forgive a broken selector in the list?

---

`:is()` takes the specificity of its most specific argument. Here that is the ID, so the selector is as specific as `#main a`. `:where()` always has zero specificity, so `:where(.nav, #main) a` has the specificity of `a` only.

Both use a forgiving selector list: an unknown or unsupported selector inside the list is dropped, and the rest still match. In `:not()` and a normal comma list, one invalid selector invalidates the whole rule. Use `:where()` for defaults you want later styles to override easily.

### has-selector
- title: :has() matches an element by what is inside it
- version: Modern
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/:has

How do you style a card only when it contains an image, without adding a class in JavaScript?

---

`:has()` is the relational pseudo-class. `article:has(img)` matches an article that has an image descendant. `article:has(> img)` limits that to a direct child. You can combine it with other selectors, including `:not(:has(...))`.

The subject is the element the pseudo-class is attached to, not the image. It is for state that is already in the DOM, such as an empty slot or a checked descendant. Do not treat it as a license to encode the whole app in selectors. It is Baseline across current major browsers; say so, and do not claim it is unsupported in evergreen Chrome, Edge, Firefox, or Safari.

### container-queries
- title: Container queries style a component by its container
- version: Modern
- level: intermediate
- status: verified
- source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries

A card component is narrow in a sidebar and wide in the main column. Why is a viewport media query the wrong tool, and what do you set on the parent?

---

A viewport query only knows the window. The same component can be wide on a small page or narrow on a large page. A container query keys off a containment context:

```css
.slot { container-type: inline-size; }
@container (min-width: 30rem) {
  .card { display: grid; }
}
```

`inline-size` is the usual choice because `size` containment also blocks the container from being sized by its contents, which can collapse height. Name the container with `container-name` when queries should not see every ancestor. Container queries do not replace media queries; they answer a different question.
