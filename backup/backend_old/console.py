from recommender import ContentRecommender

# Inisialisasi
rec = ContentRecommender()

# Test dengan keyword
results = rec.get_recommendations(
    platform='youtube', 
    keyword='tempe', 
    category='masakan', 
    top_n=5
)

# Cek hasil
print(f"\nTotal results: {len(results)}")

if results:
    print("\nFirst result:")
    print(f"Caption: {results[0]['caption'][:100]}...")
    print(f"Similarity: {results[0]['similarity_score']:.4f}")
    print(f"Likes: {results[0]['likes']}")
    print(f"Views: {results[0]['views']}")
else:
    print("No results found!")


