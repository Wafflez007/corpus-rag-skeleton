# Tailwind CSS + DaisyUI Migration Guide

This guide documents the migration from custom CSS to Tailwind CSS + DaisyUI, providing patterns and best practices for future development.

## Table of Contents

1. [Overview](#overview)
2. [Architecture Changes](#architecture-changes)
3. [Component Migration Patterns](#component-migration-patterns)
4. [Theme Configuration](#theme-configuration)
5. [Responsive Design](#responsive-design)
6. [Custom Effects Preservation](#custom-effects-preservation)
7. [Testing Strategy](#testing-strategy)
8. [Common Pitfalls](#common-pitfalls)
9. [Future Enhancements](#future-enhancements)

## Overview

### Why Migrate?

**Before Migration:**
- ~1800 lines of custom CSS
- Manual responsive breakpoints
- Inconsistent component styling
- Difficult to maintain and extend

**After Migration:**
- ~500 lines of custom CSS (theme-specific effects only)
- Tailwind utility classes for layout/spacing
- DaisyUI components for consistency
- Easy theme customization
- Mobile-first responsive design

### Migration Strategy

1. **CDN-based approach** - No build tools required
2. **Progressive migration** - Launcher → Legal Eagle → Ouija Board
3. **Hybrid approach** - Tailwind/DaisyUI for standard components, custom CSS for unique effects
4. **Functionality preservation** - All features work identically post-migration

## Architecture Changes

### File Structure

```
skeleton_core/
├── templates/
│   └── index.html          # Now includes Tailwind + DaisyUI CDN links
└── static/
    ├── styles.css          # Reduced from 1800 to ~500 lines
    ├── app.js              # Unchanged
    └── sounds/             # Unchanged
```

### HTML Template Changes

**Added to `<head>`:**
```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- DaisyUI -->
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.4.19/dist/full.min.css" rel="stylesheet" />

<!-- Inline Tailwind Config -->
<script>
  tailwind.config = {
    daisyui: {
      themes: [
        {
          "legal-eagle": { /* theme colors */ },
          "ouija-board": { /* theme colors */ }
        }
      ]
    }
  }
</script>
```

**Applied theme:**
```html
<html lang="en" data-theme="{{ 'legal-eagle' if 'Legal' in app_name else 'ouija-board' }}">
```

## Component Migration Patterns

### Buttons

**Before (Custom CSS):**
```html
<button class="btn-primary">UPLOAD</button>

<style>
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  /* ... more styles */
}
</style>
```

**After (DaisyUI):**
```html
<button class="btn btn-primary min-h-[44px]">UPLOAD</button>
```

### Cards

**Before (Custom CSS):**
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
</div>

<style>
.card {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  /* ... more styles */
}
</style>
```

**After (DaisyUI):**
```html
<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Title</h2>
    <p>Content</p>
  </div>
</div>
```

### Inputs

**Before (Custom CSS):**
```html
<input type="text" class="input-field" placeholder="Enter text...">

<style>
.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  /* ... more styles */
}
</style>
```

**After (DaisyUI):**
```html
<input type="text" class="input input-bordered w-full min-h-[44px]" placeholder="Enter text...">
```

### Chat Messages

**Before (Custom CSS):**
```html
<div class="message user-message">
  <div class="message-content">User text</div>
</div>

<style>
.user-message {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}
.message-content {
  background: var(--primary);
  color: white;
  padding: 12px 16px;
  border-radius: 18px;
  /* ... more styles */
}
</style>
```

**After (DaisyUI):**
```html
<div class="chat chat-end">
  <div class="chat-bubble chat-bubble-primary">User text</div>
</div>
```

### Layout Grids

**Before (Custom CSS):**
```html
<div class="three-column-layout">
  <div class="column">Column 1</div>
  <div class="column">Column 2</div>
  <div class="column">Column 3</div>
</div>

<style>
.three-column-layout {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
@media (max-width: 768px) {
  .three-column-layout {
    grid-template-columns: 1fr;
  }
}
</style>
```

**After (Tailwind):**
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### Progress Bars

**Before (Custom CSS):**
```html
<div class="progress-container">
  <div class="progress-bar" style="width: 70%"></div>
</div>

<style>
.progress-container {
  width: 100%;
  height: 8px;
  background: var(--bg-secondary);
  border-radius: 4px;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s ease;
}
</style>
```

**After (DaisyUI):**
```html
<progress class="progress progress-primary" value="70" max="100"></progress>
```

## Theme Configuration

### DaisyUI Theme Structure

Each app mode defines a complete color palette:

```javascript
tailwind.config = {
  daisyui: {
    themes: [
      {
        "theme-name": {
          // Main colors
          "primary": "#color",       // Primary actions (buttons, links)
          "secondary": "#color",     // Secondary elements
          "accent": "#color",        // Accent/highlight color
          "neutral": "#color",       // Neutral text color
          
          // Background colors
          "base-100": "#color",      // Main background
          "base-200": "#color",      // Card/section background
          "base-300": "#color",      // Border/divider color
          
          // Semantic colors
          "info": "#color",          // Info messages
          "success": "#color",       // Success messages
          "warning": "#color",       // Warning messages
          "error": "#color"          // Error messages
        }
      }
    ]
  }
}
```

### Legal Eagle Theme

Professional blue corporate aesthetic:

```javascript
"legal-eagle": {
  "primary": "#0f172a",      // Deep slate navy
  "secondary": "#334155",    // Steel grey
  "accent": "#ca8a04",       // Muted gold
  "neutral": "#1e293b",      // Dark slate
  "base-100": "#f8fafc",     // Light grey background
  "base-200": "#f1f5f9",     // Card background
  "base-300": "#e2e8f0",     // Border color
  "info": "#3b82f6",         // Blue
  "success": "#10b981",      // Green
  "warning": "#f59e0b",      // Amber
  "error": "#ef4444"         // Red
}
```

**Design Principles:**
- Sharp corners (minimal border-radius)
- Professional shadows
- High contrast for readability
- Legal pad aesthetic for AI messages

### Ouija Board Theme

Dark gothic mystical aesthetic:

```javascript
"ouija-board": {
  "primary": "#8b0000",      // Deep blood red
  "secondary": "#2b0505",    // Dried blood
  "accent": "#ff3f3f",       // Bright red glow
  "neutral": "#d4d4d4",      // Ghostly white
  "base-100": "#050505",     // Void black
  "base-200": "#110a0a",     // Dark card
  "base-300": "#3a1a1a",     // Dark border
  "info": "#8b0000",         // Red
  "success": "#8b0000",      // Red
  "warning": "#ff3f3f",      // Bright red
  "error": "#ff3f3f"         // Bright red
}
```

**Design Principles:**
- Dark backgrounds with high contrast text
- Red accent colors for mystical feel
- Glow effects on interactive elements
- Atmospheric gradients and shadows

### Creating New Themes

1. **Define color palette** in inline config
2. **Choose semantic colors** (info, success, warning, error)
3. **Test contrast ratios** - Aim for WCAG AA (4.5:1 for text)
4. **Apply theme** via `data-theme` attribute
5. **Test on multiple devices** for consistency

## Responsive Design

### Mobile-First Approach

Tailwind uses mobile-first breakpoints - styles apply to mobile by default, then override for larger screens:

```html
<!-- Stack on mobile, row on desktop -->
<div class="flex flex-col lg:flex-row">
  <div>Left</div>
  <div>Right</div>
</div>
```

### Breakpoint Reference

| Breakpoint | Min Width | Typical Device |
|------------|-----------|----------------|
| (default)  | 0px       | Mobile phones  |
| `sm:`      | 640px     | Large phones   |
| `md:`      | 768px     | Tablets        |
| `lg:`      | 1024px    | Desktops       |
| `xl:`      | 1280px    | Large desktops |
| `2xl:`     | 1536px    | Extra large    |

### Common Responsive Patterns

**Grid Columns:**
```html
<!-- 1 column mobile, 2 tablet, 3 desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

**Flex Direction:**
```html
<!-- Vertical mobile, horizontal desktop -->
<div class="flex flex-col lg:flex-row gap-4">
```

**Text Size:**
```html
<!-- Smaller on mobile, larger on desktop -->
<h1 class="text-2xl lg:text-4xl">Title</h1>
```

**Spacing:**
```html
<!-- Less padding on mobile, more on desktop -->
<div class="p-4 lg:p-8">Content</div>
```

**Visibility:**
```html
<!-- Hide on mobile, show on desktop -->
<div class="hidden lg:block">Desktop only</div>

<!-- Show on mobile, hide on desktop -->
<div class="block lg:hidden">Mobile only</div>
```

### Touch Target Sizes

All interactive elements must meet 44x44px minimum:

```html
<button class="btn btn-primary min-h-[44px] min-w-[44px]">Click</button>
<input class="input input-bordered min-h-[44px]">
<a href="#" class="btn min-h-[44px] min-w-[44px]">Link</a>
```

## Custom Effects Preservation

### What to Keep in Custom CSS

Some effects cannot be replicated with Tailwind/DaisyUI and should remain in custom CSS:

1. **Complex animations** (blood drips, fog effects)
2. **Custom cursors** (planchette cursor)
3. **Unique visual effects** (title pulse, mystical glow)
4. **Theme-specific decorations** (legal pad lines, gothic borders)

### Ouija Board Custom Effects

**Blood Drip Animation:**
```css
.blood-drip {
  position: absolute;
  width: 2px;
  background: linear-gradient(to bottom, #8b0000, transparent);
  animation: drip 3s ease-in infinite;
}

@keyframes drip {
  0% { height: 0; opacity: 1; }
  50% { height: 100px; opacity: 0.8; }
  100% { height: 150px; opacity: 0; }
}
```

**Mystical Fog:**
```css
.mystical-fog {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(139, 0, 0, 0.1), transparent);
  pointer-events: none;
  animation: fog-pulse 8s ease-in-out infinite;
}

@keyframes fog-pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}
```

**Planchette Cursor:**
```css
.planchette-cursor {
  cursor: url('data:image/svg+xml;utf8,<svg>...</svg>'), auto;
}
```

### When to Use Custom CSS vs. Tailwind

**Use Tailwind for:**
- Layout (flex, grid, spacing)
- Colors (text, background, border)
- Typography (font size, weight, line height)
- Standard animations (fade, slide, scale)
- Responsive design (breakpoints)

**Use Custom CSS for:**
- Complex keyframe animations
- Custom cursors
- Pseudo-element decorations
- Theme-specific visual effects
- Anything that requires multiple CSS properties working together

## Testing Strategy

### Unit Tests

Test specific component rendering:

```python
def test_button_has_daisyui_classes():
    """Verify buttons use DaisyUI classes"""
    html = render_template('index.html', app_name='Legal Eagle')
    assert 'btn btn-primary' in html
    assert 'min-h-[44px]' in html  # Touch target size
```

### Property-Based Tests

Test universal properties across all inputs:

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_all_buttons_meet_touch_target_size(button_text):
    """Property: All buttons must be at least 44x44px"""
    html = render_button(button_text)
    assert 'min-h-[44px]' in html
    assert 'min-w-[44px]' in html or 'w-full' in html
```

### Visual Regression Testing

Compare screenshots before/after migration:

```python
def test_visual_regression():
    """Compare screenshots of migrated components"""
    before = screenshot('before_migration.png')
    after = screenshot('after_migration.png')
    diff = compare_images(before, after)
    assert diff < 0.05  # Less than 5% difference
```

### Accessibility Testing

Verify WCAG compliance:

```python
def test_color_contrast():
    """Verify color contrast meets WCAG AA (4.5:1)"""
    theme = get_theme_colors('legal-eagle')
    contrast = calculate_contrast(theme['primary'], theme['base-100'])
    assert contrast >= 4.5
```

## Common Pitfalls

### 1. Forgetting Mobile-First

❌ **Wrong:**
```html
<div class="lg:flex-row flex-col">  <!-- Desktop first -->
```

✅ **Correct:**
```html
<div class="flex-col lg:flex-row">  <!-- Mobile first -->
```

### 2. Not Using DaisyUI Components

❌ **Wrong:**
```html
<button class="bg-primary text-white px-4 py-2 rounded">Click</button>
```

✅ **Correct:**
```html
<button class="btn btn-primary">Click</button>
```

### 3. Mixing Custom CSS with Tailwind

❌ **Wrong:**
```html
<div class="flex gap-4 custom-spacing">  <!-- Conflicting styles -->
```

✅ **Correct:**
```html
<div class="flex gap-4">  <!-- Use Tailwind only -->
```

### 4. Forgetting Touch Target Sizes

❌ **Wrong:**
```html
<button class="btn btn-sm">Small button</button>  <!-- Too small for mobile -->
```

✅ **Correct:**
```html
<button class="btn btn-primary min-h-[44px]">Button</button>
```

### 5. Not Testing Responsive Breakpoints

Always test on multiple device sizes:
- Mobile (375px)
- Tablet (768px)
- Desktop (1024px)
- Large desktop (1440px)

### 6. Overriding DaisyUI Styles

❌ **Wrong:**
```css
.btn-primary {
  background: red !important;  /* Breaks theme system */
}
```

✅ **Correct:**
```javascript
// Update theme configuration instead
"primary": "#ff0000"
```

## Future Enhancements

### 1. Build Process Migration

**Current:** CDN-based (no build tools)
**Future:** Build process with PurgeCSS

**Benefits:**
- Smaller CSS file size (~10KB vs. 3MB)
- Faster page loads
- Custom Tailwind plugins

**Migration Steps:**
1. Install Tailwind CLI: `npm install -D tailwindcss`
2. Create `tailwind.config.js`
3. Set up build script in `package.json`
4. Configure PurgeCSS for production
5. Update deployment process

### 2. Component Library

Create reusable component library:

```python
# components.py
def render_button(text, variant='primary', size='md'):
    return f'<button class="btn btn-{variant} btn-{size}">{text}</button>'

def render_card(title, content):
    return f'''
    <div class="card bg-base-200 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">{title}</h2>
        <p>{content}</p>
      </div>
    </div>
    '''
```

### 3. Dark Mode Toggle

Add system-wide dark mode:

```javascript
// Toggle between light and dark themes
function toggleDarkMode() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme.includes('dark') ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}
```

### 4. Custom Tailwind Plugins

Create plugins for repeated patterns:

```javascript
// tailwind.config.js
module.exports = {
  plugins: [
    function({ addComponents }) {
      addComponents({
        '.mystical-glow': {
          boxShadow: '0 0 20px rgba(255, 63, 63, 0.5)',
          animation: 'glow 2s ease-in-out infinite'
        }
      })
    }
  ]
}
```

### 5. Design Tokens

Extract theme values to shared configuration:

```javascript
// design-tokens.js
export const colors = {
  legalEagle: {
    primary: '#0f172a',
    secondary: '#334155',
    // ...
  },
  ouijaBoard: {
    primary: '#8b0000',
    secondary: '#2b0505',
    // ...
  }
}
```

## Conclusion

The migration to Tailwind CSS + DaisyUI provides:
- **80% reduction** in custom CSS (1800 → 500 lines)
- **Consistent components** across the application
- **Easy theme customization** per app personality
- **Mobile-first responsive design** out of the box
- **Improved maintainability** for future development

All functionality has been preserved, and the application now has a modern, scalable styling architecture.

For questions or issues, refer to:
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [DaisyUI Documentation](https://daisyui.com/)
- Project steering files in `.kiro/steering/`
