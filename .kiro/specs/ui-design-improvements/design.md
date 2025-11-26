# Design Document: UI Design Improvements

## Overview

This design document outlines comprehensive improvements to the user interface and user experience for both Legal Eagle and Ouija Board applications. The improvements focus on visual polish, responsive design, accessibility, and enhanced user feedback while maintaining the distinct thematic identities of each application mode.

The design leverages the existing skeleton-core architecture and CSS variable-based theming system, extending it with new components, improved interactions, and better responsive behavior. All improvements will be implemented in a way that maintains the separation between core functionality and theme-specific customizations.

## Architecture

### Component Structure

The UI improvements will be organized into the following layers:

1. **Base Layer (skeleton_core/static/styles.css)**
   - Core CSS reset and normalization
   - Shared component styles using CSS variables
   - Responsive breakpoints and media queries
   - Animation keyframes and transitions
   - Accessibility utilities

2. **Theme Layer (CSS variable definitions)**
   - Legal Eagle theme variables (theme-blue-corporate)
   - Ouija Board theme variables (theme-dark-gothic)
   - Theme-specific overrides and extensions

3. **Component Layer (HTML + JavaScript)**
   - Upload interface with progress feedback
   - Chat interface with message rendering
   - Loading states and indicators
   - Error handling and display

### Responsive Design Strategy

The application will use a mobile-first approach with the following breakpoints:

- **Mobile**: < 768px (single column, stacked layout)
- **Tablet**: 768px - 1024px (optimized spacing, larger touch targets)
- **Desktop**: > 1024px (full layout with optimal spacing)

### Theme System Architecture

The theme system uses CSS custom properties (variables) for all themeable values:

```css
.theme-{name} {
  --primary: <color>;
  --secondary: <color>;
  --accent: <color>;
  --bg-main: <color>;
  --bg-card: <color>;
  --bg-input: <color>;
  --text-main: <color>;
  --text-dim: <color>;
  --border: <color>;
  
  /* Typography */
  --font-heading: <font-family>;
  --font-body: <font-family>;
  --font-mono: <font-family>;
  
  /* Spacing */
  --spacing-xs: <size>;
  --spacing-sm: <size>;
  --spacing-md: <size>;
  --spacing-lg: <size>;
  --spacing-xl: <size>;
  
  /* Borders */
  --radius-sm: <size>;
  --radius-md: <size>;
  --radius-lg: <size>;
}
```

## Components and Interfaces

### 1. Upload Component

**Purpose**: Handle file selection, validation, upload, and progress feedback

**HTML Structure**:
```html
<div id="upload-section">
  <input type="file" id="fileInput" accept=".txt,.pdf" />
  <button onclick="uploadFile()">UPLOAD</button>
  <div id="upload-feedback">
    <div id="upload-progress">
      <div id="progress-bar"></div>
      <span id="progress-text">0%</span>
    </div>
    <p id="upload-status"></p>
  </div>
</div>
```

**JavaScript Interface**:
```javascript
async function uploadFile() {
  // Validate file
  // Show progress
  // Upload with progress updates
  // Display success/error
}

function validateFile(file) {
  // Check file type
  // Check file size
  // Return validation result
}

function updateProgress(percent) {
  // Update progress bar width
  // Update progress text
}
```

### 2. Chat Component

**Purpose**: Display conversation history and handle message input/submission

**HTML Structure**:
```html
<div id="chat-section">
  <div id="chat-history">
    <!-- Messages appended here -->
  </div>
  <div id="chat-input-container">
    <input type="text" id="queryInput" />
    <button onclick="sendQuery()">SEND</button>
  </div>
  <div id="chat-loading" class="hidden">
    <!-- Loading indicator -->
  </div>
</div>
```

**JavaScript Interface**:
```javascript
async function sendQuery() {
  // Get input value
  // Add user message to history
  // Show loading indicator
  // Send request
  // Add AI response to history
  // Hide loading indicator
  // Scroll to bottom
}

function addMessage(text, type) {
  // Create message element
  // Apply appropriate styling
  // Append to chat history
  // Trigger scroll
}

function scrollToBottom() {
  // Smooth scroll to latest message
}
```

### 3. Loading Indicators

**Purpose**: Provide visual feedback during async operations

**Types**:
- Progress bar (for uploads with known progress)
- Spinner (for indeterminate operations)
- Typing indicator (for AI response generation)
- Pulse animation (for background operations)

**Implementation**:
```javascript
function showLoading(type, container) {
  // Create loading element
  // Apply animation
  // Insert into container
}

function hideLoading(container) {
  // Remove loading element
  // Clean up
}
```

### 4. Error Display Component

**Purpose**: Show user-friendly error messages with recovery options

**HTML Structure**:
```html
<div class="error-message" role="alert">
  <span class="error-icon">⚠️</span>
  <div class="error-content">
    <p class="error-title">Error Title</p>
    <p class="error-description">Error description</p>
  </div>
  <button class="error-dismiss">Dismiss</button>
</div>
```

**JavaScript Interface**:
```javascript
function showError(title, description, container) {
  // Create error element
  // Add dismiss handler
  // Insert into container
  // Auto-dismiss after timeout
}
```

## Data Models

### Message Object

```javascript
{
  id: string,           // Unique message identifier
  type: 'user' | 'ai',  // Message sender type
  text: string,         // Message content
  timestamp: Date,      // When message was created
  status: 'sending' | 'sent' | 'error'  // Message status
}
```

### Upload State

```javascript
{
  file: File,           // File object being uploaded
  progress: number,     // Upload progress (0-100)
  status: 'validating' | 'uploading' | 'processing' | 'complete' | 'error',
  error: string | null, // Error message if failed
  result: {             // Result after successful upload
    filename: string,
    pages: number,
    chunks: number
  }
}
```

### Theme Configuration

```javascript
{
  name: string,         // Theme identifier
  displayName: string,  // Human-readable name
  cssClass: string,     // CSS class to apply
  variables: {          // CSS variable values
    primary: string,
    secondary: string,
    // ... other variables
  }
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all testable acceptance criteria, several properties can be consolidated:

- Properties 5.1-5.5 all relate to upload feedback and can be tested through the upload state management
- Properties 6.1-6.3 and 6.5 all relate to chat interaction and can be tested through message handling
- Properties 7.1, 7.4, 7.5 relate to accessibility and can be tested through DOM inspection
- Properties 8.1, 8.2, 8.5 relate to loading states and can be tested through async operation handling
- Properties 9.1, 9.2, 9.5 relate to message rendering and can be tested through message display logic

The following properties represent the unique, non-redundant correctness requirements:

Property 1: Touch target minimum size
*For any* interactive element in the interface, the computed size (including padding) should be at least 44x44 pixels to ensure touch accessibility
**Validates: Requirements 4.2**

Property 2: File validation before upload
*For any* file selected for upload, the system should validate file type and size before initiating the upload process, rejecting invalid files with appropriate error messages
**Validates: Requirements 5.4**

Property 3: Upload progress feedback
*For any* file upload operation, the system should display progress updates showing percentage completion from 0% to 100%
**Validates: Requirements 5.1**

Property 4: Upload success feedback
*For any* successfully completed upload, the system should display a message containing both the document name and the page count
**Validates: Requirements 5.2**

Property 5: Upload error feedback
*For any* failed upload operation, the system should display an error message that includes information about why the upload failed
**Validates: Requirements 5.3**

Property 6: Sequential upload processing
*For any* sequence of multiple upload requests, the system should process them one at a time in the order received, with status updates for each
**Validates: Requirements 5.5**

Property 7: Immediate user message display
*For any* user message submission, the message should appear in the chat history immediately upon calling the send function
**Validates: Requirements 6.1**

Property 8: Loading indicator during AI response
*For any* chat query being processed, a loading indicator should be visible in the chat area until the response is received
**Validates: Requirements 6.2**

Property 9: Auto-scroll to latest message
*For any* new message added to the chat history, the chat container should automatically scroll to display the newest message
**Validates: Requirements 6.3**

Property 10: Enter key submission
*For any* Enter keypress event in the chat input field, the system should trigger the query submission function
**Validates: Requirements 6.5**

Property 11: ARIA labels on interactive elements
*For any* interactive element (button, input, link) in the interface, the element should have either an aria-label attribute or accessible text content
**Validates: Requirements 7.1**

Property 12: Color contrast compliance
*For any* text element and its background color combination, the contrast ratio should meet or exceed 4.5:1 for normal text and 3:1 for large text
**Validates: Requirements 7.4**

Property 13: Alt text for meaningful images
*For any* image or icon that conveys meaning (not purely decorative), the element should have an alt attribute or aria-label providing a text alternative
**Validates: Requirements 7.5**

Property 14: Loading indicator during upload
*For any* file upload in progress, a progress bar element should be visible with percentage text updated as upload progresses
**Validates: Requirements 8.1**

Property 15: Loading indicator during query
*For any* chat query being processed, a loading element should be present in the chat area until the query completes
**Validates: Requirements 8.2**

Property 16: Error display with information
*For any* error that occurs during processing, the system should display an error message element containing information about the error
**Validates: Requirements 8.5**

Property 17: Distinct message styling
*For any* pair of user message and AI message elements, they should have different CSS classes applied to distinguish them visually
**Validates: Requirements 9.1**

Property 18: AI message visual indicators
*For any* AI message displayed, the message element should contain an icon or avatar element to identify it as an AI response
**Validates: Requirements 9.2**

Property 19: Timestamp display when relevant
*For any* message where timing information is relevant, the message element should include a timestamp element
**Validates: Requirements 9.5**

Property 20: CSS variable fallbacks
*For any* CSS custom property usage, the var() function should include a fallback value to handle cases where the variable is undefined
**Validates: Requirements 10.5**

## Error Handling

### File Upload Errors

**Error Types**:
1. Invalid file type (not .txt or .pdf)
2. File too large (exceeds size limit)
3. Network error during upload
4. Server processing error
5. Empty file

**Handling Strategy**:
- Validate file type and size client-side before upload
- Display specific error messages for each error type
- Provide recovery actions (e.g., "Try a different file")
- Log errors for debugging
- Reset upload UI to allow retry

**Example Error Messages**:
- Legal Eagle: "File type not supported. Please upload a .txt or .pdf document."
- Ouija Board: "The spirits reject this offering. Only .txt or .pdf scrolls are accepted."

### Chat Query Errors

**Error Types**:
1. Empty query submitted
2. Network error during request
3. AI service error (rate limit, safety filter, etc.)
4. No documents uploaded yet
5. Timeout waiting for response

**Handling Strategy**:
- Validate query is non-empty before sending
- Display user-friendly error messages
- Distinguish between temporary and permanent errors
- Provide retry option for temporary errors
- Suggest actions for permanent errors (e.g., upload a document first)

**Example Error Messages**:
- Legal Eagle: "No case files have been uploaded. Please upload a document before submitting queries."
- Ouija Board: "The void is empty. Offer a document to the spirits before seeking answers."

### Network Errors

**Handling Strategy**:
- Detect offline state and notify user
- Implement retry logic with exponential backoff
- Cache failed requests for retry when online
- Display connection status indicator
- Provide manual retry button

### Accessibility Errors

**Handling Strategy**:
- Ensure error messages are announced to screen readers using ARIA live regions
- Provide keyboard-accessible dismiss buttons
- Use appropriate ARIA roles (role="alert" for errors)
- Maintain focus management when errors appear

## Testing Strategy

### Unit Testing

The UI improvements will include unit tests for:

1. **File Validation Logic**
   - Test valid file types (.txt, .pdf) are accepted
   - Test invalid file types are rejected
   - Test file size limits are enforced
   - Test empty files are rejected

2. **Message Rendering**
   - Test user messages render with correct styling
   - Test AI messages render with correct styling
   - Test messages include required elements (text, timestamp, icon)
   - Test long messages wrap correctly

3. **Error Message Generation**
   - Test error messages include required information
   - Test error messages are theme-appropriate
   - Test error messages have dismiss functionality

4. **Utility Functions**
   - Test color contrast calculation
   - Test scroll position calculation
   - Test progress percentage calculation

### Property-Based Testing

Property-based tests will be implemented using **Hypothesis** (Python) for backend validation and **fast-check** (JavaScript) for frontend validation.

Each property-based test will:
- Run a minimum of 100 iterations with randomly generated inputs
- Include a comment explicitly referencing the correctness property from this design document
- Use the format: `# Feature: ui-design-improvements, Property {number}: {property_text}`

**Property Test Examples**:

1. **Touch Target Size Property**
   - Generate random interactive elements with various padding/size combinations
   - Verify all elements meet 44x44px minimum
   - Test with different viewport sizes

2. **File Validation Property**
   - Generate random file objects with various types and sizes
   - Verify validation correctly accepts/rejects based on rules
   - Test edge cases (exactly at size limit, empty files, etc.)

3. **Upload Progress Property**
   - Generate random upload scenarios with different file sizes
   - Verify progress updates from 0% to 100%
   - Verify progress is monotonically increasing

4. **Message Display Property**
   - Generate random message content (various lengths, special characters)
   - Verify messages always render with correct structure
   - Verify user/AI messages have distinct classes

5. **Color Contrast Property**
   - Generate random color combinations
   - Calculate contrast ratios
   - Verify all text/background combinations meet WCAG AA standards

6. **ARIA Label Property**
   - Generate random interactive elements
   - Verify all have accessible names (aria-label or text content)
   - Test with various element types (button, input, link, etc.)

### Integration Testing

Integration tests will verify:

1. **Upload Flow**
   - Select file → validate → upload → display success
   - Test with both .txt and .pdf files
   - Test error scenarios

2. **Chat Flow**
   - Upload document → send query → receive response → display
   - Test with various query types
   - Test error scenarios

3. **Theme Switching**
   - Verify theme CSS classes apply correctly
   - Verify all theme variables are defined
   - Verify theme-specific overrides work

4. **Responsive Behavior**
   - Test layout at different viewport sizes
   - Verify breakpoints trigger correctly
   - Verify touch targets on mobile

### Accessibility Testing

Accessibility will be validated through:

1. **Automated Testing**
   - Use axe-core or similar tool to scan for WCAG violations
   - Test keyboard navigation
   - Test screen reader compatibility

2. **Manual Testing**
   - Navigate entire interface with keyboard only
   - Test with screen reader (NVDA/JAWS/VoiceOver)
   - Verify focus indicators are visible
   - Test with high contrast mode

3. **Contrast Testing**
   - Verify all text meets WCAG AA contrast requirements (4.5:1 for normal, 3:1 for large)
   - Test with color blindness simulators
   - Verify information isn't conveyed by color alone

### Visual Regression Testing

To ensure design consistency:

1. **Screenshot Comparison**
   - Capture screenshots of key UI states
   - Compare against baseline images
   - Flag visual differences for review

2. **Theme Consistency**
   - Verify both themes render correctly
   - Test all UI states (default, hover, focus, active, disabled)
   - Verify animations and transitions

## Implementation Notes

### CSS Organization

The CSS will be organized into logical sections:

1. **CSS Variables** - Theme definitions
2. **Reset & Base** - Normalization and defaults
3. **Layout** - Grid, flexbox, spacing utilities
4. **Components** - Reusable component styles
5. **Utilities** - Helper classes
6. **Animations** - Keyframes and transitions
7. **Responsive** - Media queries
8. **Theme Overrides** - Theme-specific customizations

### JavaScript Organization

The JavaScript will be modular:

1. **upload.js** - File upload handling
2. **chat.js** - Chat interface logic
3. **ui.js** - UI utilities (loading, errors, etc.)
4. **validation.js** - Input validation
5. **accessibility.js** - A11y helpers

### Performance Considerations

1. **CSS Performance**
   - Use CSS containment for chat messages
   - Minimize repaints with transform/opacity animations
   - Use will-change sparingly for animated elements

2. **JavaScript Performance**
   - Debounce scroll events
   - Use requestAnimationFrame for animations
   - Lazy load chat messages if history grows large
   - Throttle progress updates

3. **Asset Optimization**
   - Minimize CSS and JavaScript
   - Use system fonts where possible
   - Optimize any custom fonts with font-display: swap

### Browser Compatibility

Target browsers:
- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile Safari (iOS 13+)
- Chrome Mobile (Android 8+)

Fallbacks for:
- CSS Grid → Flexbox
- CSS Custom Properties → Sass variables (build time)
- Modern JavaScript → Babel transpilation if needed

### Accessibility Standards

Compliance targets:
- WCAG 2.1 Level AA
- Section 508
- ARIA 1.2 best practices

Key requirements:
- Keyboard navigation for all interactive elements
- Screen reader support with proper ARIA labels
- Sufficient color contrast (4.5:1 minimum)
- Focus indicators on all focusable elements
- No keyboard traps
- Meaningful tab order
- Skip links for navigation

### Theme Extension Guidelines

To add a new theme:

1. Create a new CSS class `.theme-{name}`
2. Define all required CSS variables
3. Add theme-specific overrides if needed
4. Create a config.py with theme reference
5. Test all UI states with new theme
6. Verify accessibility compliance
7. Document theme in README

Required CSS variables for any theme:
- Color palette (primary, secondary, accent, backgrounds, text, borders)
- Typography (font families for heading, body, mono)
- Spacing scale (xs, sm, md, lg, xl)
- Border radii (sm, md, lg)
- Shadows (optional, can use defaults)

### Mobile-Specific Considerations

1. **Touch Interactions**
   - Minimum 44x44px touch targets
   - Adequate spacing between interactive elements
   - No hover-dependent functionality

2. **Virtual Keyboard**
   - Adjust viewport when keyboard appears
   - Ensure input fields scroll into view
   - Provide "done" button for keyboard dismissal

3. **Performance**
   - Minimize animations on low-end devices
   - Reduce bundle size for faster loading
   - Use passive event listeners for scroll

4. **Gestures**
   - Support swipe to dismiss errors
   - Pull to refresh (if applicable)
   - Pinch to zoom on images (if applicable)

### Legal Eagle Specific Design Details

**Color Palette**:
- Primary: #0f172a (Deep Slate Navy)
- Secondary: #334155 (Steel Grey)
- Accent: #ca8a04 (Muted Gold)
- Background: #f8fafc (Very Light Grey)
- Card: #ffffff (White)
- Text: #1e293b (Dark Slate)

**Typography**:
- Headings: IBM Plex Sans (sans-serif, professional)
- Body: IBM Plex Sans
- AI Responses: Georgia (serif, document-like)
- Code/Input: Courier New (monospace, typewriter-like)

**Visual Elements**:
- Sharp corners (4px border-radius)
- Subtle shadows for depth
- Grid pattern background on cards
- Left border accent on AI messages (legal pad style)
- Uppercase button text
- Professional icons (briefcase, gavel, document)

### Ouija Board Specific Design Details

**Color Palette**:
- Primary: #8b0000 (Deep Blood Red)
- Secondary: #2b0505 (Dried Blood)
- Accent: #ff3f3f (Bright Red Glow)
- Background: #050505 (Void Black)
- Card: #110a0a (Dark Card)
- Text: #d4d4d4 (Ghostly White)

**Typography**:
- Headings: Creepster (gothic, mystical)
- Body: Georgia (serif, old-world)
- Monospace: Courier New

**Visual Elements**:
- Rounded corners for organic feel
- Glowing shadows and animations
- Radial gradient backgrounds
- Pulsing animations on key elements
- Crosshair cursor
- Mystical icons (crystal ball, skull, candle)
- Dot pattern background texture

**Animations**:
- Title pulse (4s cycle)
- Glow effects on hover
- Fade-in for messages
- Flicker effects (subtle)
