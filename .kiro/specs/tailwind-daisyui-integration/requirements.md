# Requirements Document

## Introduction

This specification defines the requirements for integrating Tailwind CSS and DaisyUI into Project Corpus to modernize the UI design system. The goal is to replace the current custom CSS approach with a utility-first framework while preserving the distinct personalities and themes of the Legal Eagle and Ouija Board applications, as well as improving the launcher interface.

## Glossary

- **Tailwind CSS**: A utility-first CSS framework that provides low-level utility classes for building custom designs
- **DaisyUI**: A component library built on top of Tailwind CSS that provides pre-styled, themeable components
- **Launcher**: The multi-app launcher script (`launcher.py`) that allows users to select and start different app modes
- **Legal Eagle**: The professional legal assistant application mode with blue corporate aesthetic
- **Ouija Board**: The mystical/gothic application mode with dark atmospheric aesthetic
- **Theme System**: The configuration-based approach to customizing UI appearance per application mode
- **Skeleton Core**: The reusable RAG core logic in `skeleton_core/` that serves all application modes

## Requirements

### Requirement 1

**User Story:** As a developer, I want to integrate Tailwind CSS and DaisyUI into the project, so that I can leverage modern utility-first styling and pre-built components.

#### Acceptance Criteria

1. WHEN the project is set up THEN the system SHALL include Tailwind CSS via CDN or build process
2. WHEN the project is set up THEN the system SHALL include DaisyUI as a Tailwind plugin
3. WHEN pages load THEN the system SHALL apply Tailwind's base styles and utilities
4. WHEN DaisyUI components are used THEN the system SHALL render them with proper styling
5. WHEN the application runs THEN the system SHALL maintain compatibility with existing Flask/Jinja2 templates

### Requirement 2

**User Story:** As a user of the Legal Eagle app, I want the interface to maintain its professional legal aesthetic using Tailwind and DaisyUI, so that the experience remains consistent with the legal assistant personality.

#### Acceptance Criteria

1. WHEN the Legal Eagle app loads THEN the system SHALL apply a blue corporate color scheme using DaisyUI theme configuration
2. WHEN displaying text THEN the system SHALL use professional sans-serif fonts (IBM Plex Sans or similar)
3. WHEN rendering UI components THEN the system SHALL use sharp, professional styling (minimal border radius, clean lines)
4. WHEN displaying AI messages THEN the system SHALL style them with legal pad aesthetic using Tailwind utilities
5. WHEN rendering buttons and cards THEN the system SHALL apply professional shadows and spacing using Tailwind classes

### Requirement 3

**User Story:** As a user of the Ouija Board app, I want the interface to maintain its dark gothic aesthetic using Tailwind and DaisyUI, so that the mystical experience is preserved.

#### Acceptance Criteria

1. WHEN the Ouija Board app loads THEN the system SHALL apply a dark gothic color scheme using DaisyUI theme configuration
2. WHEN displaying headings THEN the system SHALL use gothic/mystical fonts (Creepster or similar via custom font integration)
3. WHEN rendering UI elements THEN the system SHALL apply dark backgrounds with mystical accents (purples, deep reds)
4. WHEN displaying interactive elements THEN the system SHALL include subtle glow effects using Tailwind utilities
5. WHEN the page is visible THEN the system SHALL display atmospheric visual effects (gradients, shadows, patterns)

### Requirement 4

**User Story:** As a user of the launcher, I want an improved interface built with Tailwind and DaisyUI, so that I can easily select and start different application modes.

#### Acceptance Criteria

1. WHEN the launcher runs THEN the system SHALL display a clean, modern interface using DaisyUI components
2. WHEN viewing app options THEN the system SHALL present them as cards with clear visual hierarchy using Tailwind utilities
3. WHEN hovering over app options THEN the system SHALL provide visual feedback using Tailwind hover states
4. WHEN selecting an app THEN the system SHALL provide clear confirmation and launch feedback
5. WHEN the launcher displays THEN the system SHALL be responsive across different screen sizes using Tailwind responsive utilities

### Requirement 5

**User Story:** As a developer, I want to configure DaisyUI themes per application mode, so that each app can have its distinct visual identity while using the same component library.

#### Acceptance Criteria

1. WHEN configuring themes THEN the system SHALL support multiple DaisyUI theme definitions in the configuration
2. WHEN an app loads THEN the system SHALL apply the correct theme based on the app's configuration
3. WHEN switching between apps THEN the system SHALL maintain theme isolation (each app uses its own theme)
4. WHEN customizing themes THEN the system SHALL allow color palette overrides via DaisyUI theme configuration
5. WHEN themes are applied THEN the system SHALL ensure all DaisyUI components respect the theme settings

### Requirement 6

**User Story:** As a developer, I want to migrate existing custom CSS components to Tailwind utilities and DaisyUI components, so that the codebase is more maintainable and consistent.

#### Acceptance Criteria

1. WHEN migrating layouts THEN the system SHALL replace custom CSS grid/flexbox with Tailwind utility classes
2. WHEN migrating buttons THEN the system SHALL use DaisyUI button components with appropriate variants
3. WHEN migrating form inputs THEN the system SHALL use DaisyUI input and textarea components
4. WHEN migrating cards THEN the system SHALL use DaisyUI card components with custom content
5. WHEN migrating modals and alerts THEN the system SHALL use DaisyUI modal and alert components

### Requirement 7

**User Story:** As a developer, I want to preserve existing functionality during the migration, so that no features are lost when adopting Tailwind and DaisyUI.

#### Acceptance Criteria

1. WHEN the migration is complete THEN the system SHALL maintain all file upload functionality
2. WHEN the migration is complete THEN the system SHALL maintain all chat functionality
3. WHEN the migration is complete THEN the system SHALL maintain all document management functionality
4. WHEN the migration is complete THEN the system SHALL maintain all error handling and feedback mechanisms
5. WHEN the migration is complete THEN the system SHALL maintain all accessibility features (ARIA labels, keyboard navigation)

### Requirement 8

**User Story:** As a user, I want the application to remain responsive on mobile devices after the Tailwind migration, so that I can use it on any device.

#### Acceptance Criteria

1. WHEN viewing on mobile devices THEN the system SHALL apply mobile-first responsive design using Tailwind breakpoints
2. WHEN interacting on touch devices THEN the system SHALL ensure touch targets meet minimum size requirements (44x44px)
3. WHEN viewing the chat interface on mobile THEN the system SHALL optimize layout for small screens using Tailwind responsive utilities
4. WHEN uploading files on mobile THEN the system SHALL provide appropriate mobile-friendly UI
5. WHEN viewing on tablets THEN the system SHALL adapt layout using Tailwind's medium breakpoint utilities

### Requirement 9

**User Story:** As a developer, I want to maintain custom animations and transitions using Tailwind's animation utilities, so that the user experience remains polished.

#### Acceptance Criteria

1. WHEN messages appear THEN the system SHALL animate them using Tailwind animation utilities or custom animations
2. WHEN buttons are hovered THEN the system SHALL apply smooth transitions using Tailwind transition utilities
3. WHEN loading indicators display THEN the system SHALL use Tailwind animation utilities for spinning or pulsing effects
4. WHEN errors appear THEN the system SHALL animate them in using Tailwind animation utilities
5. WHEN users prefer reduced motion THEN the system SHALL respect the prefers-reduced-motion setting

### Requirement 10

**User Story:** As a developer, I want clear documentation on the Tailwind and DaisyUI integration, so that future developers can maintain and extend the system.

#### Acceptance Criteria

1. WHEN reviewing the codebase THEN the system SHALL include comments explaining theme configuration
2. WHEN reviewing the codebase THEN the system SHALL include documentation on custom Tailwind utilities
3. WHEN reviewing the codebase THEN the system SHALL include examples of DaisyUI component usage
4. WHEN onboarding new developers THEN the system SHALL provide README updates explaining the Tailwind/DaisyUI setup
5. WHEN extending the system THEN the system SHALL provide guidelines for adding new themes or app modes
