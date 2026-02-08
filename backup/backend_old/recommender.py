import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import Database

class ContentRecommender:
    def __init__(self):
        """
        Inisialisasi TF-IDF Vectorizer
        TIDAK ada preprocessing tambahan karena data sudah bersih dari Google Colab
        """
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            lowercase=True
        )
    
    def get_recommendations(self, platform, keyword, category=None, top_n=6, use_popularity=True):
        """
        Dapatkan rekomendasi konten berdasarkan TF-IDF dan Cosine Similarity
        
        Parameters:
        -----------
        platform : str
            Platform yang dipilih ('youtube', 'tiktok', 'instagram')
        keyword : str
            Kata kunci pencarian dari user
        category : str, optional
            Kategori konten ('masakan', 'it', atau None untuk semua)
        top_n : int
            Jumlah rekomendasi yang akan ditampilkan (default: 6)
        use_popularity : bool
            Apakah boost konten populer atau tidak (default: True)
        
        Returns:
        --------
        list
            List of dict berisi rekomendasi konten
        """
        
        # === 1. AMBIL DATA DARI DATABASE ===
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query dengan filter kategori optional
        if category:
            query = """
                SELECT id, platform, category, caption, hashtag, url, text_for_tfidf,
                       likes, views, comments, engagement_rate, is_popular
                FROM contents 
                WHERE platform = %s AND category = %s
            """
            cursor.execute(query, (platform, category))
        else:
            query = """
                SELECT id, platform, category, caption, hashtag, url, text_for_tfidf,
                       likes, views, comments, engagement_rate, is_popular
                FROM contents 
                WHERE platform = %s
            """
            cursor.execute(query, (platform,))
        
        contents = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Jika tidak ada data
        if not contents:
            print(f"No data found for platform: {platform}, category: {category}")
            return []
        
        # === 2. BUAT DATAFRAME ===
        df = pd.DataFrame(contents)
        print(f"Total data loaded: {len(df)}")
        
        # === 3. FILTER DATA YANG text_for_tfidf TIDAK KOSONG ===
        # Ini PENTING karena TF-IDF tidak bisa bekerja dengan text kosong
        df = df[
            df['text_for_tfidf'].notna() &  # Bukan NULL
            (df['text_for_tfidf'].astype(str).str.strip() != '')  # Bukan string kosong
        ]
        
        print(f"Data with valid text_for_tfidf: {len(df)}")
        
        # Jika setelah filter tidak ada data valid
        if len(df) == 0:
            print("No valid data with text_for_tfidf")
            return []
        
        # === 4. PERSIAPAN TEXT UNTUK TF-IDF ===
        # Gunakan text_for_tfidf yang sudah diproses dari Google Colab
        # TIDAK perlu preprocessing ulang!
        all_texts = df['text_for_tfidf'].tolist()
        
        # Preprocessing keyword user (MINIMAL: hanya lowercase dan strip)
        keyword_processed = str(keyword).lower().strip()
        print(f"Keyword processed: {keyword_processed}")
        
        # === 5. TF-IDF VECTORIZATION ===
        # Tambahkan keyword ke corpus
        all_texts_with_keyword = all_texts + [keyword_processed]
        
        try:
            # TF-IDF Vectorization
            tfidf_matrix = self.vectorizer.fit_transform(all_texts_with_keyword)
            print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
        except Exception as e:
            print(f"Error in TF-IDF: {e}")
            return []
        
        # === 6. COSINE SIMILARITY ===
        # Vector terakhir = keyword user
        keyword_vector = tfidf_matrix[-1]
        
        # Semua vector konten
        content_vectors = tfidf_matrix[:-1]
        
        # Hitung similarity
        similarities = cosine_similarity(keyword_vector, content_vectors)[0]
        
        # Tambahkan similarity score ke DataFrame
        df['similarity_score'] = similarities
        
        # === 7. BOOST KONTEN POPULER (Optional) ===
        if use_popularity:
            # Handle engagement_rate yang mungkin NULL
            df['engagement_rate_safe'] = df['engagement_rate'].fillna(0)
            
            # Boost score dengan engagement rate (max 10% boost)
            df['final_score'] = df['similarity_score'] * (1 + df['engagement_rate_safe'] * 0.1)
        else:
            df['final_score'] = df['similarity_score']
        
        # === 8. SORT DAN AMBIL TOP N ===
        df = df.sort_values('final_score', ascending=False)
        
        # Ambil top N
        top_recommendations = df.head(top_n)
        
        print(f"Top recommendations count: {len(top_recommendations)}")
        
        # === 9. FORMAT OUTPUT ===
        result = []
        for _, row in top_recommendations.iterrows():
            # Handle NULL di caption/hashtag
            caption_display = row['caption'] if pd.notna(row['caption']) and str(row['caption']).strip() else 'No caption available'
            hashtag_display = row['hashtag'] if pd.notna(row['hashtag']) and str(row['hashtag']).strip() else ''
            url_display = row['url'] if pd.notna(row['url']) and str(row['url']).strip() else '#'
            
            item = {
                'id': str(row['id']),
                'platform': row['platform'],
                'category': row['category'],
                
                # Text fields dengan handle NULL
                'caption': caption_display,
                'hashtags': hashtag_display,
                'video_url': url_display,
                
                # Similarity score
                'similarity_score': float(row['similarity_score']),
                
                # Numeric fields dengan handle NULL
                'likes': int(row['likes']) if pd.notna(row['likes']) else 0,
                'views': int(row['views']) if pd.notna(row['views']) else 0,
                'comments': int(row['comments']) if pd.notna(row['comments']) else 0,
                'engagement_rate': float(row['engagement_rate']) if pd.notna(row['engagement_rate']) else 0.0,
                'is_popular': bool(row['is_popular']) if pd.notna(row['is_popular']) else False
            }
            
            result.append(item)
        
        # Print top 3 untuk debugging
        print("\nTop 3 recommendations:")
        for i, item in enumerate(result[:3], 1):
            print(f"{i}. {item['caption'][:50]}... (score: {item['similarity_score']:.4f})")
        
        return result