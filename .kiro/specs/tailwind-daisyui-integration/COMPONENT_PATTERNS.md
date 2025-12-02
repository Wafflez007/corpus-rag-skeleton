# Tailwind CSS + DaisyUI Component Patterns

Quick reference guide for common UI patterns in Project Corpus.

## Table of Contents

1. [Buttons](#buttons)
2. [Cards](#cards)
3. [Forms](#forms)
4. [Chat Interface](#chat-interface)
5. [Progress & Loading](#progress--loading)
6. [Alerts & Feedback](#alerts--feedback)
7. [Layout Patterns](#layout-patterns)
8. [Responsive Utilities](#responsive-utilities)
9. [Accessibility](#accessibility)

## Buttons

### Primary Button
```html
<button class="btn btn-primary min-h-[44px]">
  UPLOAD
</button>
```

### Accent Button
```html
<button class="btn btn-accent min-h-[44px]">
  🔮 Summon Spirits
</button>
```

### Button with Icon
```html
<button class="btn btn-primary min-h-[44px]">
  <span>📂</span>
  Choose File
</button>
```

### Full Width Button
```html
<button class="btn btn-primary w-full min-h-[44px]">
  SEND MESSAGE
</button>
```

### Disabled Button
```html
<button class="btn btn-primary min-h-[44px]" disabled>
  Processing...
</button>
```

### Button Group
```html
<div class="flex gap-3">
  <button class="btn btn-primary flex-1 min-h-[44px]">Save</button>
  <button class="btn btn-secondary flex-1 min-h-[44px]">Cancel</button>
</div>
```

## Cards

### Basic Card
```html
<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card content goes here</p>
  </div>
</div>
```

### Card with Icon Header
```html
<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">
      <span class="text-2xl">📂</span>
      Upload Documents
    </h2>
    <p>Select files to upload</p>
  </div>
</div>
```

### Card with Actions
```html
<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Confirm Action</h2>
    <p>Are you sure you want to proceed?</p>
    <div class="card-actions justify-end mt-4">
      <button class="btn btn-secondary min-h-[44px]">Cancel</button>
      <button class="btn btn-primary min-h-[44px]">Confirm</button>
    </div>
  </div>
</div>
```

### Scrollable Card
```html
<div class="card bg-base-200 shadow-xl h-full">
  <div class="card-body">
    <h2 class="card-title">Document Library</h2>
    <div class="overflow-y-auto max-h-[500px] space-y-2">
      <!-- Scrollable content -->
    </div>
  </div>
</div>
```

## Forms

### Text Input
```html
<input 
  type="text" 
  class="input input-bordered w-full min-h-[44px]" 
  placeholder="Enter your query..."
/>
```

### File Input
```html
<input 
  type="file" 
  class="file-input file-input-bordered w-full min-h-[44px]"
  accept=".txt,.pdf"
/>
```

### Textarea
```html
<textarea 
  class="textarea textarea-bordered w-full min-h-[100px]" 
  rows="4"
  placeholder="Enter message..."
></textarea>
```

### Checkbox
```html
<label class="flex items-center gap-2 cursor-pointer min-h-[44px]">
  <input type="checkbox" class="checkbox checkbox-primary" />
  <span>Select document</span>
</label>
```

### Select All Checkbox
```html
<label class="flex items-center gap-2 cursor-pointer min-h-[44px] font-semibold">
  <input 
    type="checkbox" 
    class="checkbox checkbox-primary" 
    id="select-all"
  />
  <span>Select All</span>
</label>
```

### Form with Validation
```html
<form class="space-y-4">
  <div>
    <label class="label">
      <span class="label-text">Email</span>
    </label>
    <input 
      type="email" 
      class="input input-bordered w-full min-h-[44px]" 
      required
    />
  </div>
  
  <div>
    <label class="label">
      <span class="label-text">Message</span>
    </label>
    <textarea 
      class="textarea textarea-bordered w-full" 
      rows="4"
      required
    ></textarea>
  </div>
  
  <button type="submit" class="btn btn-primary w-full min-h-[44px]">
    Submit
  </button>
</form>
```

## Chat Interface

### User Message (Right)
```html
<div class="chat chat-end">
  <div class="chat-bubble chat-bubble-primary">
    What is the main topic of the document?
  </div>
</div>
```

### AI Message (Left)
```html
<div class="chat chat-start">
  <div class="chat-bubble">
    The document discusses legal contracts and agreements.
  </div>
</div>
```

### Message with Timestamp
```html
<div class="chat chat-end">
  <div class="chat-header mb-1">
    <time class="text-xs opacity-50">12:45 PM</time>
  </div>
  <div class="chat-bubble chat-bubble-primary">
    User message
  </div>
</div>
```

### Message with Source Citation
```html
<div class="chat chat-start">
  <div class="chat-bubble">
    <p>The contract specifies a 30-day notice period.</p>
    <div class="text-xs opacity-70 mt-2">
      📄 Source: contract.pdf (Page 3)
    </div>
  </div>
</div>
```

### Chat Container
```html
<div class="card bg-base-200 shadow-xl h-full">
  <div class="card-body">
    <h2 class="card-title">💬 Chat</h2>
    
    <!-- Messages container -->
    <div class="overflow-y-auto h-[500px] space-y-4" id="chat-messages">
      <!-- Chat messages go here -->
    </div>
    
    <!-- Input area -->
    <div class="flex gap-3 mt-4">
      <input 
        type="text" 
        class="input input-bordered flex-1 min-h-[44px]" 
        placeholder="Type your message..."
      />
      <button class="btn btn-primary min-h-[44px] min-w-[44px]">
        SEND
      </button>
    </div>
  </div>
</div>
```

## Progress & Loading

### Progress Bar
```html
<progress 
  class="progress progress-primary w-full" 
  value="70" 
  max="100"
></progress>
```

### Indeterminate Progress
```html
<progress class="progress progress-primary w-full"></progress>
```

### Loading Spinner
```html
<span class="loading loading-spinner loading-lg"></span>
```

### Loading Spinner with Text
```html
<div class="flex items-center gap-3">
  <span class="loading loading-spinner loading-md"></span>
  <span>Processing...</span>
</div>
```

### Progress with Stages
```html
<div class="space-y-2">
  <div class="flex justify-between text-sm">
    <span>Uploading document...</span>
    <span>70%</span>
  </div>
  <progress class="progress progress-primary w-full" value="70" max="100"></progress>
  <div class="text-xs opacity-70">
    Stage: Vectorizing pages
  </div>
</div>
```

## Alerts & Feedback

### Error Alert
```html
<div class="alert alert-error">
  <span>⚠️ File upload failed. Please try again.</span>
</div>
```

### Success Alert
```html
<div class="alert alert-success">
  <span>✅ Document uploaded successfully!</span>
</div>
```

### Info Alert
```html
<div class="alert alert-info">
  <span>ℹ️ Processing may take a few moments.</span>
</div>
```

### Warning Alert
```html
<div class="alert alert-warning">
  <span>⚠️ File size is large. Upload may take longer.</span>
</div>
```

### Dismissible Alert
```html
<div class="alert alert-error">
  <span>⚠️ An error occurred.</span>
  <button class="btn btn-sm btn-ghost min-h-[44px]" onclick="this.parentElement.remove()">
    ✕
  </button>
</div>
```

### Alert with Actions
```html
<div class="alert alert-warning">
  <div class="flex-1">
    <span>⚠️ Unsaved changes detected.</span>
  </div>
  <div class="flex gap-2">
    <button class="btn btn-sm btn-ghost min-h-[44px]">Discard</button>
    <button class="btn btn-sm btn-primary min-h-[44px]">Save</button>
  </div>
</div>
```

## Layout Patterns

### Two Column Layout
```html
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
  <div>Left column</div>
  <div>Right column</div>
</div>
```

### Three Column Layout
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### Sidebar Layout
```html
<div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
  <!-- Sidebar (1/4 width on desktop) -->
  <div class="lg:col-span-1">
    <div class="card bg-base-200 shadow-xl">
      <div class="card-body">Sidebar</div>
    </div>
  </div>
  
  <!-- Main content (3/4 width on desktop) -->
  <div class="lg:col-span-3">
    <div class="card bg-base-200 shadow-xl">
      <div class="card-body">Main content</div>
    </div>
  </div>
</div>
```

### Centered Container
```html
<div class="container mx-auto px-4 max-w-4xl">
  <div class="card bg-base-200 shadow-xl">
    <div class="card-body">Centered content</div>
  </div>
</div>
```

### Full Height Layout
```html
<div class="min-h-screen flex flex-col">
  <!-- Header -->
  <header class="p-4 bg-base-200">
    <h1 class="text-2xl font-bold">Header</h1>
  </header>
  
  <!-- Main content (grows to fill space) -->
  <main class="flex-1 p-4">
    Content
  </main>
  
  <!-- Footer -->
  <footer class="p-4 bg-base-200">
    Footer
  </footer>
</div>
```

### Split Screen
```html
<div class="min-h-screen flex flex-col md:flex-row">
  <div class="flex-1 bg-primary p-8">
    Left side
  </div>
  <div class="flex-1 bg-secondary p-8">
    Right side
  </div>
</div>
```

## Responsive Utilities

### Show/Hide by Breakpoint
```html
<!-- Show only on mobile -->
<div class="block lg:hidden">Mobile only</div>

<!-- Show only on desktop -->
<div class="hidden lg:block">Desktop only</div>

<!-- Show on tablet and up -->
<div class="hidden md:block">Tablet and desktop</div>
```

### Responsive Text Size
```html
<h1 class="text-2xl md:text-3xl lg:text-4xl">
  Responsive heading
</h1>
```

### Responsive Spacing
```html
<div class="p-4 md:p-6 lg:p-8">
  Responsive padding
</div>

<div class="space-y-4 lg:space-y-6">
  Responsive vertical spacing
</div>
```

### Responsive Flex Direction
```html
<!-- Stack on mobile, row on desktop -->
<div class="flex flex-col lg:flex-row gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Responsive Grid Columns
```html
<!-- 1 column mobile, 2 tablet, 3 desktop, 4 large desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>
```

## Accessibility

### Touch Target Sizes
All interactive elements must be at least 44x44px:

```html
<button class="btn btn-primary min-h-[44px] min-w-[44px]">Click</button>
<input class="input input-bordered min-h-[44px]">
<a href="#" class="btn min-h-[44px] min-w-[44px]">Link</a>
```

### ARIA Labels
```html
<button class="btn btn-primary min-h-[44px]" aria-label="Upload document">
  📂
</button>

<input 
  type="text" 
  class="input input-bordered min-h-[44px]"
  aria-label="Search documents"
  placeholder="Search..."
/>
```

### Focus Indicators
DaisyUI provides built-in focus indicators. Ensure they're visible:

```html
<!-- Focus ring is automatic on DaisyUI components -->
<button class="btn btn-primary min-h-[44px]">
  Accessible button
</button>
```

### Keyboard Navigation
```html
<!-- Ensure proper tab order -->
<div class="space-y-4">
  <input type="text" class="input input-bordered min-h-[44px]" tabindex="1">
  <input type="text" class="input input-bordered min-h-[44px]" tabindex="2">
  <button class="btn btn-primary min-h-[44px]" tabindex="3">Submit</button>
</div>
```

### Screen Reader Text
```html
<button class="btn btn-primary min-h-[44px]">
  <span aria-hidden="true">🗑️</span>
  <span class="sr-only">Delete document</span>
</button>
```

### Color Contrast
Ensure text meets WCAG AA standards (4.5:1 ratio):

```html
<!-- Good contrast -->
<div class="bg-base-100 text-base-content p-4">
  High contrast text
</div>

<!-- Check contrast for custom colors -->
<div class="bg-primary text-primary-content p-4">
  Primary colored section
</div>
```

## Quick Tips

### Spacing Scale
- `gap-1` = 0.25rem (4px)
- `gap-2` = 0.5rem (8px)
- `gap-3` = 0.75rem (12px)
- `gap-4` = 1rem (16px)
- `gap-6` = 1.5rem (24px)
- `gap-8` = 2rem (32px)

### Common Combinations
```html
<!-- Card with full-width button -->
<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Title</h2>
    <p>Content</p>
    <button class="btn btn-primary w-full min-h-[44px] mt-4">Action</button>
  </div>
</div>

<!-- Input with button -->
<div class="flex gap-3">
  <input class="input input-bordered flex-1 min-h-[44px]" placeholder="Search...">
  <button class="btn btn-primary min-h-[44px]">Search</button>
</div>

<!-- Scrollable list -->
<div class="overflow-y-auto max-h-[400px] space-y-2">
  <div class="p-3 bg-base-200 rounded">Item 1</div>
  <div class="p-3 bg-base-200 rounded">Item 2</div>
  <div class="p-3 bg-base-200 rounded">Item 3</div>
</div>
```

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [DaisyUI Components](https://daisyui.com/components/)
- [DaisyUI Themes](https://daisyui.com/docs/themes/)
- [Tailwind Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)
