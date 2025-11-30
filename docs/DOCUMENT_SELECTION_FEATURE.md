# Document Selection Feature

## What Was Added

Users can now **select which uploaded documents to query** instead of re-uploading files every time.

## New Features

### 1. Document Library UI
- Shows all uploaded documents with page/chunk counts
- Checkboxes to select which documents to search
- "Select All" toggle for convenience
- Delete button (🗑️) to remove unwanted documents
- Refresh button to reload the list

### 2. Backend Endpoints

**GET /documents**
- Lists all uploaded documents with metadata
- Returns: `{documents: [{source, pages, chunks}, ...]}`

**DELETE /documents/<source>**
- Removes a document and all its chunks
- Returns: `{success: true, deleted_chunks: N}`

### 3. Filtered Search
- Chat queries now only search **selected documents**
- If all documents selected = searches everything (no filter)
- If some selected = only searches those specific files

## How It Works

1. **Upload** - Documents persist in ChromaDB (`./chroma_db`)
2. **Library loads** - On page load, shows all uploaded files
3. **User selects** - Check/uncheck documents to include
4. **Chat filters** - Queries only search selected documents
5. **Delete option** - Remove documents you no longer need

## Code Changes

### Backend (`skeleton_core/`)
- `vector_store.py`: Added `list_documents()`, `delete_document()`, `filter_sources` param to `search()`
- `app.py`: Added `/documents` GET/DELETE routes, modified `/chat` to accept `sources` filter

### Frontend (`skeleton_core/static/`)
- `app.js`: Added document management functions (refresh, delete, toggle, filter)
- `styles.css`: Added document library styling
- `index.html`: Added document library section with checkboxes

## Theme Support

Both personalities supported:
- **Legal Eagle**: "Document Library" with professional styling
- **Ghost/Ouija**: "Summoned Texts" with spooky language

## Usage

1. Upload documents as usual
2. Documents appear in the library automatically
3. Uncheck documents you don't want to query
4. Ask questions - only selected documents are searched
5. Delete documents using the 🗑️ button when done
