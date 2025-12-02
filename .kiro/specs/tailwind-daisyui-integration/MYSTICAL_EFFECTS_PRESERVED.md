# Preserved Custom Mystical Effects for Ouija Board Theme

This document identifies all custom CSS effects for the Ouija Board theme that **cannot be replicated** with Tailwind CSS or DaisyUI and must be preserved in the custom CSS file.

## ✅ Preserved Effects

### 1. Blood Drip Animations
**Location:** `skeleton_core/static/styles.css` - Lines ~1600-1750

**Description:** Realistic blood drip animation using SVG gooey filter effect with liquid physics simulation.

**Key Features:**
- Gooey filter creates liquid merging effect
- Multiple blood drips with staggered timing
- Gravity-based acceleration animation
- Bulb and droplet shapes using pseudo-elements
- Responsive to `prefers-reduced-motion`

**CSS Classes:**
- `.theme-dark-gothic .blood-drip-container`
- `.theme-dark-gothic .blood-drip-container .blood-drip`
- `.theme-dark-gothic .blood-drip-container .blood-drip::before`
- `.theme-dark-gothic .blood-drip-container .blood-drip::after`

**Animation:**
- `@keyframes blood-gooey-fall` - 7-9 second fall with height stretching

**Why it can't be replicated:**
- Requires SVG filter (`url('#blood-goo')`)
- Complex pseudo-element positioning
- Dynamic height changes during animation
- Gooey liquid physics effect

---

### 2. Mystical Fog Effects
**Location:** `skeleton_core/static/styles.css` - Lines ~1050-1070

**Description:** Animated fog overlay using multiple radial gradients that create atmospheric depth.

**Key Features:**
- Fixed position overlay covering entire viewport
- Multiple radial gradients at different positions
- Subtle color variations (blood red to bright red)
- Non-interactive (pointer-events: none)

**CSS Classes:**
- `.theme-dark-gothic::before` - Fog overlay

**Animation:**
- `@keyframes mystical-fog` - Subtle movement and opacity changes

**Why it can't be replicated:**
- Uses `::before` pseudo-element for layering
- Multiple complex radial gradients
- Fixed positioning with z-index management
- Requires precise gradient positioning

---

### 3. Floating Particles Effect
**Location:** `skeleton_core/static/styles.css` - Lines ~1072-1090

**Description:** Animated particle system using radial gradients to simulate floating mystical particles.

**Key Features:**
- 6 different particle positions
- Animated background position for movement
- Varying opacity for depth effect
- 25-second infinite animation loop

**CSS Classes:**
- `.theme-dark-gothic::after` - Particles overlay

**Animation:**
- `@keyframes floating-particles` - Background position and opacity animation

**Why it can't be replicated:**
- Uses `::after` pseudo-element for layering
- Multiple radial gradients with precise positioning
- Animated background-position property
- Complex timing and opacity variations

---

### 4. Custom Planchette Cursor
**Location:** `skeleton_core/static/styles.css` - Lines ~1040-1055

**Description:** Custom SVG cursor shaped like a Ouija board planchette with mystical eye.

**Key Features:**
- SVG data URI embedded in CSS
- Different cursor states (default, pointer, text)
- Planchette shape with circular eye
- Blood red color scheme

**CSS Classes:**
- `.theme-dark-gothic, .theme-dark-gothic *` - Default cursor
- `.theme-dark-gothic button, .theme-dark-gothic a` - Pointer cursor
- `.theme-dark-gothic input, .theme-dark-gothic textarea` - Text cursor

**Why it can't be replicated:**
- Requires inline SVG data URI
- Custom cursor hotspot positioning
- Different cursor variants for different elements
- Complex SVG path definitions

---

### 5. Title Pulse Animation
**Location:** `skeleton_core/static/styles.css` - Lines ~1095-1105

**Description:** Pulsing glow effect on h1 titles with animated text-shadow and scale.

**Key Features:**
- Animated text-shadow with multiple layers
- Color transition from blood red to bright red
- Subtle scale transform (1.0 to 1.02)
- 4-second infinite loop
- Uses Creepster font

**CSS Classes:**
- `.theme-dark-gothic .spooky-title`
- `.theme-dark-gothic h1`

**Animation:**
- `@keyframes title-pulse` - Text-shadow, opacity, and scale animation

**Why it can't be replicated:**
- Multiple layered text-shadows
- Animated text-shadow color changes
- Combined with transform scale
- Requires custom keyframe animation

---

### 6. Button Glow Animation
**Location:** `skeleton_core/static/styles.css` - Lines ~1107-1120

**Description:** Pulsing glow effect on buttons with animated box-shadow.

**Key Features:**
- Animated box-shadow with inset and outset shadows
- Color transition from blood red to bright red
- 3-second infinite loop
- Enhanced on hover

**CSS Classes:**
- `.theme-dark-gothic .btn-primary`
- `.theme-dark-gothic button`

**Animation:**
- `@keyframes button-glow` - Box-shadow animation

**Why it can't be replicated:**
- Multiple layered box-shadows (inset and outset)
- Animated shadow color and spread
- Requires custom keyframe animation
- Complex shadow combinations

---

### 7. Blood Splatter Decorations
**Location:** `skeleton_core/static/styles.css` - Lines ~1755-1800

**Description:** Animated blood splatter effects using pseudo-elements with radial gradients.

**Key Features:**
- Irregular splatter shapes using border-radius
- Blur filter for realistic effect
- Animated appearance and disappearance
- Multiple splatter sizes

**CSS Classes:**
- `.theme-dark-gothic .blood-splatter`
- `.theme-dark-gothic .blood-splatter::before`
- `.theme-dark-gothic .blood-splatter::after`

**Animation:**
- `@keyframes splatter-appear` - Opacity, scale, and rotation animation

**Why it can't be replicated:**
- Pseudo-elements with complex shapes
- Irregular border-radius values
- Blur filter effects
- Animated transform with rotation

---

### 8. Mystical Card Glow
**Location:** `skeleton_core/static/styles.css` - Lines ~1122-1135

**Description:** Cards with mystical glow, dot pattern background, and blood splatter effects.

**Key Features:**
- Multiple box-shadows (outset and inset)
- SVG dot pattern background
- Blood splatter pseudo-elements
- Border glow effect

**CSS Classes:**
- `.theme-dark-gothic .card`
- `.theme-dark-gothic .ouija-border`
- `.theme-dark-gothic .ouija-border::before`
- `.theme-dark-gothic .ouija-border::after`

**Why it can't be replicated:**
- Multiple layered shadows
- SVG pattern background
- Pseudo-elements for blood splatters
- Complex radial gradients for splatters

---

## 🔧 Integration with Tailwind/DaisyUI

These custom effects work **alongside** Tailwind CSS and DaisyUI by:

1. **Specificity:** All effects use `.theme-dark-gothic` prefix, ensuring they only apply to Ouija Board theme
2. **Layering:** Effects use pseudo-elements (::before, ::after) that don't interfere with Tailwind classes
3. **Z-index Management:** Proper z-index values ensure effects layer correctly with Tailwind components
4. **CSS Variables:** Effects use CSS custom properties that can be overridden if needed
5. **Reduced Motion:** All animations respect `prefers-reduced-motion` media query

## 📝 Maintenance Notes

- **Do not remove** any CSS marked with `⚠️ CUSTOM MYSTICAL EFFECT` comments
- These effects are essential to the Ouija Board personality and cannot be achieved with utility classes
- When updating Tailwind/DaisyUI, ensure these custom effects remain functional
- Test all mystical effects after any CSS changes to ensure they still work correctly

## 🎨 Effect Dependencies

### Required HTML Elements:
- Blood drips require: `<div class="blood-drip-container">` with child `<div class="blood-drip">` elements
- Blood splatters require: Elements with `.blood-splatter` class

### Required SVG Filters:
- Blood drip gooey effect requires: SVG filter with id `blood-goo` in HTML

### Required Fonts:
- Creepster font for headings (loaded via Google Fonts or similar)
- Georgia serif for body text

## ✅ Validation Checklist

When testing the Ouija Board theme, verify:

- [ ] Blood drips animate smoothly from top to bottom
- [ ] Mystical fog overlay is visible and subtle
- [ ] Floating particles move across the screen
- [ ] Custom planchette cursor appears on all elements
- [ ] Title pulses with glowing effect
- [ ] Buttons have pulsing glow animation
- [ ] Cards have mystical shadows and dot patterns
- [ ] All effects respect `prefers-reduced-motion` setting
- [ ] Effects work alongside Tailwind/DaisyUI components
- [ ] No visual conflicts with DaisyUI styling

## 📊 Performance Considerations

- All animations use GPU-accelerated properties (transform, opacity)
- CSS containment applied where appropriate
- Animations pause when `prefers-reduced-motion` is enabled
- Pseudo-elements used efficiently to minimize DOM nodes
- Background patterns use optimized SVG data URIs

---

**Last Updated:** December 2, 2025  
**Spec:** tailwind-daisyui-integration  
**Task:** 10. Preserve custom mystical effects for Ouija Board
