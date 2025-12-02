# Design Document: Tailwind CSS + DaisyUI Integration

## Overview

This design outlines the integration of Tailwind CSS and DaisyUI into Project Corpus to modernize the UI architecture while preserving the distinct personalities of the Legal Eagle and Ouija Board applications. The approach uses Tailwind's utility-first methodology combined with DaisyUI's component library to create a maintainable, themeable, and responsive design system.

### Key Design Decisions

1. **CDN-based Integration**: Use Tailwind CSS and DaisyUI via CDN for simplicity and rapid deployment, avoiding build tooling complexity
2. **Theme Configuration**: Leverage DaisyUI's theme system to define custom themes for each app mode
3. **Hybrid Approach**: Maintain minimal custom CSS for unique effects (blood drips, mystical fog) while migrating standard components to Tailwind/DaisyUI
4. **Progressive Migration**: Migrate components incrementally, starting with the launcher, then Legal Eagle, then Ouija Board
5. **Preserve Functionality**: Ensure all existing features (upload, chat, document management) remain fully functional

## Architecture

### Integration Strategy

```
┌─────────────────────────────────────────────────────────┐
│                    HTML Templates                        │
│  (index.html, launcher landing page)                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├─► Tailwind CSS (CDN)
                 │   └─► Utility classes for layout, spacing, colors
                 │
                 ├─► DaisyUI (CDN)
                 │   └─► Pre-built components (buttons, cards, inputs)
                 │
                 └─► Custom CSS (styles.css - minimal)
                     └─► Theme-specific effects (animations, cursors)
```

### File Structure Changes

```
skeleton_core/
├── templates/
│   └── index.html (updated with Tailwind + DaisyUI)
├── static/
│   ├── styles.css (reduced to theme-specific effects only)
│   └── app.js (unchanged)

launcher.py (updated landing page with Tailwind + DaisyUI)

app_legal/
└── config.py (add DaisyUI theme configuration)

app_ghost/
└── config.py (add DaisyUI theme configuration)
```

## Components and Interfaces

### 1. CDN Integration

**Implementation**: Add Tailwind CSS and DaisyUI via CDN in HTML `<head>` sections

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- DaisyUI -->
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.4.19/dist/full.min.css" rel="stylesheet" type="text/css" />
```

**Tailwind Configuration**: Use inline configuration for custom theme values

```html
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          'legal-navy': '#0f172a',
          'legal-gold': '#ca8a04',
          'ghost-dark': '#050505',
          'ghost-glow': '#ff3f3f'
        }
      }
    }
  }
</script>
```

### 2. DaisyUI Theme Configuration

**Legal Eagle Theme** (Professional Blue):
```javascript
{
  "legal-eagle": {
    "primary": "#0f172a",      // Deep slate navy
    "secondary": "#334155",    // Steel grey
    "accent": "#ca8a04",       // Muted gold
    "neutral": "#1e293b",      // Dark slate
    "base-100": "#f8fafc",     // Light grey background
    "base-200": "#f1f5f9",     // Input background
    "base-300": "#e2e8f0",     // Border color
    "info": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444"
  }
}
```

**Ouija Board Theme** (Dark Gothic):
```javascript
{
  "ouija-board": {
    "primary": "#8b0000",      // Deep blood red
    "secondary": "#2b0505",    // Dried blood
    "accent": "#ff3f3f",       // Bright red glow
    "neutral": "#d4d4d4",      // Ghostly white
    "base-100": "#050505",     // Void black
    "base-200": "#110a0a",     // Dark card
    "base-300": "#3a1a1a",     // Dark border
    "info": "#8b0000",
    "success": "#8b0000",
    "warning": "#ff3f3f",
    "error": "#ff3f3f"
  }
}
```

### 3. Component Migration Map

| Current Component | Tailwind/DaisyUI Replacement | Notes |
|-------------------|------------------------------|-------|
| `.btn-primary` | `btn btn-primary` | DaisyUI button with theme colors |
| `.card` | `card bg-base-200 shadow-xl` | DaisyUI card component |
| `.input-field` | `input input-bordered` | DaisyUI input component |
| `.chat-message` | `chat chat-start/chat-end` | DaisyUI chat bubble component |
| `.loading-spinner` | `loading loading-spinner` | DaisyUI loading component |
| `.progress-bar` | `progress progress-primary` | DaisyUI progress component |
| `.error-message` | `alert alert-error` | DaisyUI alert component |
| Grid layouts | `grid grid-cols-*` | Tailwind grid utilities |
| Flexbox layouts | `flex flex-col/flex-row` | Tailwind flex utilities |

### 4. Launcher Page Redesign

**Layout**: Modern split-screen with Tailwind utilities

```html
<div class="min-h-screen flex flex-col md:flex-row">
  <!-- Legal Eagle Side -->
  <div class="flex-1 bg-legal-navy hover:flex-[2] transition-all duration-500">
    <div class="card bg-base-100 shadow-2xl">
      <div class="card-body items-center text-center">
        <h2 class="card-title text-4xl">⚖️ Legal Eagle</h2>
        <p>Professional Document Analysis</p>
        <div class="card-actions">
          <a href="/legal/" class="btn btn-primary">Access Counsel</a>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Ouija Board Side -->
  <div class="flex-1 bg-ghost-dark hover:flex-[2] transition-all duration-500">
    <div class="card bg-base-100 shadow-2xl">
      <div class="card-body items-center text-center">
        <h2 class="card-title text-4xl">🔮 Ouija Board</h2>
        <p>Mystical Document Communion</p>
        <div class="card-actions">
          <a href="/ghost/" class="btn btn-accent">Summon Spirits</a>
        </div>
      </div>
    </div>
  </div>
</div>
```

### 5. Main Application Interface

**Upload Section**:
```html
<div class="card bg-base-200 shadow-xl mb-6">
  <div class="card-body">
    <h2 class="card-title">
      <span class="text-2xl">📂</span>
      Case File Ingestion
    </h2>
    <div class="flex flex-col md:flex-row gap-3">
      <input type="file" class="file-input file-input-bordered flex-1" />
      <button class="btn btn-primary">UPLOAD</button>
    </div>
    <progress class="progress progress-primary hidden" value="0" max="100"></progress>
  </div>
</div>
```

**Chat Interface**:
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <!-- Document Library -->
  <div class="lg:col-span-1">
    <div class="card bg-base-200 shadow-xl h-full">
      <div class="card-body">
        <h2 class="card-title">📚 Library</h2>
        <div class="overflow-y-auto max-h-[500px] space-y-2">
          <!-- Document items -->
        </div>
      </div>
    </div>
  </div>
  
  <!-- Chat Section -->
  <div class="lg:col-span-2">
    <div class="card bg-base-200 shadow-xl h-full">
      <div class="card-body">
        <h2 class="card-title">💬 Counsel Inquiry</h2>
        <div class="overflow-y-auto h-[500px] space-y-4">
          <!-- Chat messages using DaisyUI chat component -->
          <div class="chat chat-end">
            <div class="chat-bubble chat-bubble-primary">User message</div>
          </div>
          <div class="chat chat-start">
            <div class="chat-bubble">AI response</div>
          </div>
        </div>
        <div class="flex gap-3 mt-4">
          <input type="text" class="input input-bordered flex-1" placeholder="Enter your query..." />
          <button class="btn btn-primary">SEND</button>
        </div>
      </div>
    </div>
  </div>
</div>
```

## Data Models

No changes to data models. The integration is purely presentational and does not affect:
- Vector store operations
- Document chunking
- Embedding generation
- Chat functionality
- Backend API routes

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

Before defining properties, let's analyze the testable acceptance criteria from the requirements:

**1.1** - Tailwind CSS inclusion: Testable as example (verify CDN link exists)
**1.2** - DaisyUI inclusion: Testable as example (verify DaisyUI link exists)
**1.3** - Tailwind base styles: Testable as property (all pages should have Tailwind classes)
**1.4** - DaisyUI components: Testable as property (components render with DaisyUI classes)
**1.5** - Flask/Jinja2 compatibility: Testable as property (templates render without errors)

**2.1** - Legal Eagle color scheme: Testable as property (theme colors match specification)
**2.2** - Professional fonts: Testable as example (font-family includes specified fonts)
**2.3** - Sharp styling: Testable as property (border-radius values are minimal)
**2.4** - Legal pad aesthetic: Testable as example (AI messages have specific styling)
**2.5** - Professional shadows: Testable as property (shadow utilities are applied)

**3.1** - Ouija Board color scheme: Testable as property (theme colors match specification)
**3.2** - Gothic fonts: Testable as example (headings use Creepster font)
**3.3** - Dark backgrounds: Testable as property (background colors are dark)
**3.4** - Glow effects: Testable as property (elements have glow classes)
**3.5** - Atmospheric effects: Testable as example (specific visual effects present)

**4.1** - Launcher interface: Testable as property (DaisyUI components used)
**4.2** - Card presentation: Testable as property (cards have proper hierarchy)
**4.3** - Hover feedback: Testable as property (hover states defined)
**4.4** - Launch confirmation: Testable as property (links navigate correctly)
**4.5** - Responsive design: Testable as property (responsive classes applied)

**5.1-5.5** - Theme configuration: Testable as properties (themes apply correctly per app)

**6.1-6.5** - Component migration: Testable as properties (old classes replaced with new)

**7.1-7.5** - Functionality preservation: Testable as properties (features still work)

**8.1-8.5** - Responsive design: Testable as properties (breakpoints work correctly)

**9.1-9.5** - Animations: Testable as properties (animations use Tailwind utilities)

**10.1-10.5** - Documentation: Not testable (documentation quality is subjective)

**Redundancy Analysis**:
- Properties 1.3 and 1.4 can be combined into "Tailwind/DaisyUI classes are present"
- Properties 2.1 and 3.1 can be combined into "Theme colors match specification for all themes"
- Properties 6.1-6.5 can be combined into "Component migration is complete"
- Properties 7.1-7.5 can be combined into "All functionality is preserved"

### Correctness Properties

Property 1: CDN resources are included
*For any* page in the application, the HTML should include both Tailwind CSS and DaisyUI CDN links in the head section
**Validates: Requirements 1.1, 1.2**

Property 2: Tailwind and DaisyUI classes are applied
*For any* component in the application, it should use Tailwind utility classes or DaisyUI component classes instead of custom CSS classes
**Validates: Requirements 1.3, 1.4, 6.1, 6.2, 6.3, 6.4, 6.5**

Property 3: Theme colors match specification
*For any* application mode (Legal Eagle or Ouija Board), the applied DaisyUI theme colors should match the color specifications defined in the design document
**Validates: Requirements 2.1, 3.1, 5.2**

Property 4: Templates render without errors
*For any* page template, rendering with Flask/Jinja2 should complete successfully without template errors
**Validates: Requirements 1.5**

Property 5: Professional styling for Legal Eagle
*For any* element in the Legal Eagle app, border-radius values should be minimal (≤ 8px) and shadows should use professional shadow utilities
**Validates: Requirements 2.3, 2.5**

Property 6: Gothic styling for Ouija Board
*For any* background element in the Ouija Board app, the background color should be dark (luminance < 0.2)
**Validates: Requirements 3.3**

Property 7: Responsive classes are applied
*For any* layout component, it should include Tailwind responsive utility classes (sm:, md:, lg:, xl:) for different breakpoints
**Validates: Requirements 4.5, 8.1, 8.2, 8.3, 8.4, 8.5**

Property 8: Touch targets meet minimum size
*For any* interactive element (button, input, link), the minimum height and width should be at least 44px on mobile devices
**Validates: Requirements 8.2**

Property 9: All functionality is preserved
*For any* user action (upload file, send chat, delete document), the functionality should work identically to the pre-migration implementation
**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**

Property 10: Animations use Tailwind utilities
*For any* animated element, the animation should use Tailwind animation utilities (animate-*, transition-*) or respect prefers-reduced-motion
**Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

Property 11: Launcher uses DaisyUI components
*For any* section of the launcher page, it should use DaisyUI card, button, or other component classes
**Validates: Requirements 4.1, 4.2**

Property 12: Hover states are defined
*For any* interactive element, it should have Tailwind hover state classes (hover:*) defined
**Validates: Requirements 4.3**

Property 13: Theme isolation is maintained
*For any* application mode, changing the theme should not affect other application modes running simultaneously
**Validates: Requirements 5.3**

## Error Handling

### Migration Errors

1. **CDN Loading Failures**
   - Fallback: Include local copies of Tailwind/DaisyUI as backup
   - Detection: Check if Tailwind classes are applied on page load
   - Recovery: Display error message and load fallback CSS

2. **Theme Configuration Errors**
   - Validation: Verify theme colors are valid hex/rgb values
   - Fallback: Use default DaisyUI theme if custom theme fails
   - Logging: Log theme configuration errors to console

3. **Component Migration Issues**
   - Testing: Verify each migrated component renders correctly
   - Rollback: Keep old CSS classes as fallback during migration
   - Validation: Use visual regression testing to catch styling issues

4. **Responsive Breakpoint Issues**
   - Testing: Test on multiple device sizes (mobile, tablet, desktop)
   - Fallback: Ensure mobile-first approach works without breakpoints
   - Validation: Use browser dev tools to test responsive behavior

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **CDN Link Verification**
   - Test that Tailwind CSS CDN link is present in HTML
   - Test that DaisyUI CDN link is present in HTML
   - Test that custom Tailwind config is defined

2. **Theme Configuration**
   - Test Legal Eagle theme has correct primary color (#0f172a)
   - Test Ouija Board theme has correct primary color (#8b0000)
   - Test theme switching works between apps

3. **Component Rendering**
   - Test button renders with `btn btn-primary` classes
   - Test card renders with `card bg-base-200` classes
   - Test input renders with `input input-bordered` classes
   - Test chat bubbles render with `chat chat-start/chat-end` classes

4. **Responsive Behavior**
   - Test grid layout uses `grid-cols-1 lg:grid-cols-3`
   - Test mobile layout stacks vertically
   - Test touch targets are at least 44px on mobile

5. **Functionality Preservation**
   - Test file upload still works after migration
   - Test chat sending still works after migration
   - Test document deletion still works after migration

### Property-Based Testing

Property-based tests will verify universal properties across all inputs using **Hypothesis** (Python's property-based testing library):

1. **Property Test: Tailwind Classes Present**
   - Generate random page templates
   - Verify all contain Tailwind utility classes
   - Verify no old custom CSS classes remain

2. **Property Test: Theme Colors Match**
   - Generate random theme configurations
   - Verify all colors are valid and match specifications
   - Verify theme isolation between apps

3. **Property Test: Responsive Classes Applied**
   - Generate random layout components
   - Verify all have responsive breakpoint classes
   - Verify mobile-first approach is used

4. **Property Test: Touch Targets Meet Minimum**
   - Generate random interactive elements
   - Measure computed height and width
   - Verify all meet 44px minimum on mobile

5. **Property Test: Functionality Preserved**
   - Generate random user actions
   - Execute actions before and after migration
   - Verify results are identical

### Testing Configuration

- **Property-based tests**: Run 100 iterations minimum per property
- **Test framework**: Pytest with Hypothesis plugin
- **Coverage target**: 90% code coverage for migrated components
- **Visual regression**: Use Playwright for screenshot comparisons
- **Accessibility testing**: Use axe-core for WCAG compliance

### Test Tagging

Each property-based test will be tagged with a comment referencing the design document:

```python
def test_tailwind_classes_present():
    """
    **Feature: tailwind-daisyui-integration, Property 2: Tailwind and DaisyUI classes are applied**
    """
    # Test implementation
```

## Implementation Phases

### Phase 1: Launcher Migration
1. Update launcher.py landing page HTML
2. Add Tailwind CSS and DaisyUI CDN links
3. Replace custom CSS with Tailwind utilities
4. Implement DaisyUI card and button components
5. Test responsive behavior
6. Verify hover states and transitions

### Phase 2: Legal Eagle Migration
1. Update index.html template
2. Add Tailwind/DaisyUI CDN links
3. Configure Legal Eagle DaisyUI theme
4. Migrate upload section to DaisyUI components
5. Migrate chat interface to DaisyUI chat components
6. Migrate document library to DaisyUI components
7. Test all functionality
8. Verify professional aesthetic is maintained

### Phase 3: Ouija Board Migration
1. Update index.html template (if separate)
2. Configure Ouija Board DaisyUI theme
3. Migrate components to DaisyUI
4. Preserve custom mystical effects (fog, blood drips)
5. Test all functionality
6. Verify gothic aesthetic is maintained

### Phase 4: Custom Effects Preservation
1. Identify effects that cannot be replicated with Tailwind/DaisyUI
2. Keep minimal custom CSS for:
   - Blood drip animations (Ouija Board)
   - Mystical fog effects (Ouija Board)
   - Custom cursors (both themes)
   - Unique animations (title pulse, button glow)
3. Ensure custom CSS works alongside Tailwind

### Phase 5: Testing and Validation
1. Run all unit tests
2. Run all property-based tests
3. Perform visual regression testing
4. Test on multiple devices and browsers
5. Verify accessibility compliance
6. Performance testing (page load times)

### Phase 6: Documentation
1. Update README with Tailwind/DaisyUI setup
2. Document theme configuration process
3. Add examples of common component patterns
4. Create migration guide for future developers
5. Update steering documents with new architecture

## Performance Considerations

1. **CDN Loading**: Tailwind CSS (~3MB) and DaisyUI (~100KB) will be loaded from CDN
   - Benefit: Browser caching across sites
   - Trade-off: Initial load time vs. build complexity

2. **CSS Purging**: Not implemented in CDN version
   - Future optimization: Switch to build process with PurgeCSS
   - Current approach: Accept larger CSS file for simplicity

3. **Custom CSS Reduction**: Reduce styles.css from ~1800 lines to ~500 lines
   - Remove: Layout, spacing, color utilities (replaced by Tailwind)
   - Keep: Theme-specific animations and effects

4. **Animation Performance**: Use Tailwind's optimized animations
   - Leverage GPU acceleration (transform, opacity)
   - Respect prefers-reduced-motion

## Accessibility Considerations

1. **Color Contrast**: Verify all theme colors meet WCAG AA standards
   - Legal Eagle: Navy (#0f172a) on light grey (#f8fafc) = 14.5:1 ✓
   - Ouija Board: White (#d4d4d4) on black (#050505) = 18.2:1 ✓

2. **Focus Indicators**: Use DaisyUI's built-in focus styles
   - Visible focus rings on all interactive elements
   - High contrast focus indicators

3. **Touch Targets**: Enforce 44px minimum using Tailwind classes
   - `min-h-[44px] min-w-[44px]` on all buttons and inputs

4. **Semantic HTML**: Maintain proper HTML structure
   - Use DaisyUI components which include proper ARIA attributes
   - Preserve existing ARIA labels and roles

5. **Screen Reader Support**: Ensure compatibility
   - Test with NVDA and JAWS
   - Verify DaisyUI components are screen reader friendly

## Browser Compatibility

- **Modern Browsers**: Full support (Chrome, Firefox, Safari, Edge)
- **Tailwind CSS**: Supports all modern browsers with CSS Grid and Flexbox
- **DaisyUI**: Built on Tailwind, same compatibility
- **Fallback**: Graceful degradation for older browsers (IE11 not supported)

## Deployment Considerations

1. **No Build Step Required**: CDN-based approach works immediately
2. **Environment Variables**: No changes to existing .env configuration
3. **Static Assets**: Minimal changes to static file serving
4. **Caching**: Leverage CDN caching for Tailwind/DaisyUI
5. **Rollback Plan**: Keep old styles.css as backup during migration

## Future Enhancements

1. **Build Process**: Migrate from CDN to build process with PurgeCSS
2. **Custom Plugins**: Create Tailwind plugins for repeated patterns
3. **Design Tokens**: Extract theme values to shared configuration
4. **Component Library**: Build reusable component library on top of DaisyUI
5. **Dark Mode**: Implement system-wide dark mode toggle using DaisyUI themes
