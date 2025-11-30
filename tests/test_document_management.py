"""Quick test for document management features"""
import os
from dotenv import load_dotenv
from skeleton_core.vector_store import VectorStore

# Load environment
load_dotenv()

# Initialize vector store
vs = VectorStore()

print("Testing Document Management Features")
print("=" * 50)

# Test 1: List documents
print("\n1. Listing documents...")
docs = vs.list_documents()
print(f"   Found {len(docs)} documents:")
for doc in docs:
    print(f"   - {doc['source']}: {doc['pages']} pages, {doc['chunks']} chunks")

# Test 2: Search with filter (if documents exist)
if docs:
    print("\n2. Testing filtered search...")
    test_source = docs[0]['source']
    print(f"   Searching only in: {test_source}")
    results = vs.search("test query", n_results=3, filter_sources=[test_source])
    print(f"   Found {len(results)} results")
    
    print("\n3. Testing unfiltered search...")
    results_all = vs.search("test query", n_results=3)
    print(f"   Found {len(results_all)} results")
else:
    print("\n   No documents to test search with")

print("\n✓ All tests completed!")
