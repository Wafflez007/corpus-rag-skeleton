# Quick Reference: Mystical Effects for Ouija Board Theme

## 🎯 At a Glance

This is a quick reference for developers working with the Ouija Board theme's custom mystical effects.

---

## 🚫 DO NOT REMOVE

The following CSS sections are **essential** and cannot be replicated with Tailwind/DaisyUI:

### 1. Blood Drip Animations
```css
.theme-dark-gothic .blood-drip-container { ... }
@keyframes blood-gooey-fall { ... }
```
**Why:** Requires SVG gooey filter and complex pseudo-element physics

### 2. Mystical Fog Overlay
```css
.theme-dark-gothic::before { ... }
@keyframes mystical-fog { ... }
```
**Why:** Multi-layer radial gradients with fixed positioning

### 3. Floating Particles
```css
.theme-dark-gothic::after { ... }
@keyframes floating-particles { ... }
```
**Why:** Animated background-position with multiple particles

### 4. Custom Planchette Cursor
```css
.theme-dark-gothic, .theme-dark-gothic * {
    cursor: url("data:image/svg+xml...") ...;
}
```
**Why:** Inline SVG data URI with custom hotspot

### 5. Title Pulse Animation
```css
.theme-dark-gothic h1 { animation: title-pulse ... }
@keyframes title-pulse { ... }
```
**Why:** Animated multi-layer text-shadow

### 6. Button Glow Animation
```css
.theme-dark-gothic .btn-primary { animation: button-glow ... }
@keyframes button-glow { ... }
```
**Why:** Pulsing inset and outset box-shadows

---

## ✅ Safe to Modify with Tailwind

These can be replaced or enhanced with Tailwind utilities:

- Layout (grid, flex) - Use Tailwind grid/flex classes
- Spacing (padding, margin) - Use Tailwind spacing utilities
- Colors (background, text) - Use Tailwind color utilities
- Basic borders - Use Tailwind border utilities
- Simple shadows - Use Tailwind shadow utilities

---

## 🔍 How to Identify Custom Effects

Look for this marker in the CSS:
```css
/* ⚠️ CUSTOM MYSTICAL EFFECT - CANNOT BE REPLICATED WITH TAILWIND/DAISYUI */
```

---

## 📦 Required HTML Elements

### Blood Drips
```html
<div class="side-decoration left-decoration">
    <div class="blood-drip-container">
        <div class="blood-drip"></div>
        <div class="blood-drip"></div>
        <div class="blood-drip"></div>
        <div class="blood-drip"></div>
        <div class="blood-drip"></div>
    </div>
</div>
```

### SVG Gooey Filter
```html
<svg style="position:absolute;width:0;height:0">
    <defs>
        <filter id="blood-goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9" result="goo" />
            <feComposite in="SourceGraphic" in2="goo" operator="atop"/>
        </filter>
    </defs>
</svg>
```

---

## 🎨 CSS Variables Used

```css
--primary: #8b0000;      /* Deep Blood Red */
--secondary: #2b0505;    /* Dried Blood */
--accent: #ff3f3f;       /* Bright Red Glow */
--bg-main: #050505;      /* Void Black */
--bg-card: #110a0a;      /* Dark Card */
--text-main: #d4d4d4;    /* Ghostly White */
--border: #3a1a1a;       /* Dark Border */
```

---

## 🧪 Testing

Run these tests to verify effects are preserved:
```bash
python -m pytest tests/test_mystical_effects_preserved.py -v
```

---

## 📚 Full Documentation

For complete details, see:
- `MYSTICAL_EFFECTS_PRESERVED.md` - Comprehensive documentation
- `TASK_10_COMPLETION_SUMMARY.md` - Implementation summary

---

## ⚡ Quick Checklist

Before committing CSS changes:

- [ ] All `⚠️ CUSTOM MYSTICAL EFFECT` sections intact?
- [ ] Blood drip animations still working?
- [ ] Mystical fog overlay visible?
- [ ] Custom cursor appearing?
- [ ] Title pulsing with glow?
- [ ] Tests passing? (`pytest tests/test_mystical_effects_preserved.py`)

---

## 🆘 Troubleshooting

### Blood drips not animating
- Check SVG filter `#blood-goo` exists in HTML
- Verify `.blood-drip-container` has `filter: url('#blood-goo')`

### Fog/particles not visible
- Check `::before` and `::after` pseudo-elements
- Verify z-index layering (should be 0)

### Cursor not showing
- Check SVG data URI is properly encoded
- Verify cursor fallback is present

### Animations too fast/slow
- Check `prefers-reduced-motion` setting
- Verify animation-duration values

---

**Last Updated:** December 2, 2025  
**Maintained by:** Tailwind/DaisyUI Integration Team
