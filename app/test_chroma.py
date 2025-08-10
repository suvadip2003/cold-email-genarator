import chromadb
import traceback

print("--- 1. Starting ChromaDB test ---")

try:
    print("--- 2. Attempting to create PersistentClient... ---")
    
    # This is the line we suspect is causing the silent crash.
    client = chromadb.PersistentClient(path="vectorstore")
    
    print("--- 3. PersistentClient created successfully! ---")
    
    collection = client.get_or_create_collection(name="test_collection")
    print("--- 4. Collection accessed successfully! ---")

    print("\n✅ SUCCESS: ChromaDB is working correctly.")

except Exception as e:
    print(f"\n❌ AN ERROR OCCURRED: {e}")
    traceback.print_exc()

# This will keep the window open so we can see the output.
input("\nTest finished. Press Enter to exit...")