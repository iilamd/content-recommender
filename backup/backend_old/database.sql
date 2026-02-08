CREATE DATABASE IF NOT EXISTS content_recommender;
USE content_recommender;

-- Tabel Users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Content (Data konten untuk rekomendasi)
CREATE TABLE contents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    theme VARCHAR(255) NOT NULL,
    caption TEXT NOT NULL,
    hashtags TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_platform (platform)
);

-- Tabel Favorites
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES contents(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, content_id)
);

-- Tabel Activity Log
CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    platform VARCHAR(20),
    keyword VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample data untuk Instagram
INSERT INTO contents (platform, title, theme, caption, hashtags) VALUES
('instagram', '10 Tips Fotografi untuk Pemula', 'Fotografi', 'Yuk belajar fotografi! 📸 Swipe untuk tips yang mudah dipraktikkan langsung. Dijamin feed Instagram kamu makin keren! ✨', '#FotografiPemula #TipsFotografi #InstagramTips #ContentCreator #PhotographyTips #BelajarFotografi #InstaDaily #CreativeContent'),
('instagram', 'Resep Smoothie Bowl Viral', 'Makanan Sehat', 'Smoothie bowl cantik yang lagi viral! 🍓🥥 Gampang banget bikinnya dan super sehat. Save resepnya ya! 💚', '#SmoothieBowl #HealthyFood #ResepSehat #Foodstagram #ViralRecipe #HealthyLifestyle #FoodContent #InstaFood'),
('instagram', 'Workout Rumahan 15 Menit', 'Fitness', 'Nggak ada waktu ke gym? Ini dia workout 15 menit yang bisa dilakukan di rumah! 💪 No equipment needed. Yuk mulai sekarang!', '#WorkoutRumahan #FitnessIndonesia #HomeWorkout #SehatBersama #OlahragaDirumah #FitnessMotivation #HealthyLiving #WorkoutTips'),
('instagram', 'Tutorial Makeup Natural untuk Sehari-hari', 'Kecantikan', 'Makeup natural yang cocok untuk daily look! Simpel, cepat, dan hasilnya glowing. Tutorial lengkap ada di carousel ini! 💄✨', '#MakeupTutorial #MakeupNatural #BeautyTips #MakeupIndonesia #DailyMakeup #GlowingSkin #BeautyContent #MakeupIdeas');

-- Insert sample data untuk TikTok
INSERT INTO contents (platform, title, theme, caption, hashtags) VALUES
('tiktok', 'Transisi Outfit Keren', 'Fashion', 'Transition outfit hari ini! Kalian suka yang mana? 👗✨ #OOTD', '#TransisiOutfit #OOTD #FashionTikTok #OutfitIdeas #StyleInspiration #TikTokFashion #FYP #Viral #TrendingNow'),
('tiktok', 'Life Hack Dapur yang Jarang Diketahui', 'Tips & Trik', 'Mind blown! 🤯 Kenapa baru tau sekarang sih? Coba deh praktikkin di rumah!', '#LifeHack #DapurTips #TipsAndTricks #Viral #FYP #TikTokTips #KitchenHacks #ViralTikTok #MustTry'),
('tiktok', 'Dance Challenge Terbaru', 'Hiburan', 'Ikutan dance challenge yang lagi viral! Kalian udah coba belum? Tag temen kalian! 💃🕺', '#DanceChallenge #TikTokDance #Viral #FYP #DanceTrend #ChallengeAccepted #TrendingDance #ViralChallenge #DanceVideo'),
('tiktok', 'Cara Belajar Efektif untuk Ujian', 'Edukasi', 'Tips belajar efektif yang terbukti ampuh! Dijamin nilai kamu naik 📚✨ Part 1 dari 3', '#TipsBelajar #BelajarEfektif #StudyTips #Edukasi #Mahasiswa #Pelajar #FYP #EducationTikTok #StudyMotivation');

-- Insert sample data untuk YouTube
INSERT INTO contents (platform, title, theme, caption, hashtags) VALUES
('youtube', 'Cara Edit Video Cinematic Pakai HP', 'Tutorial Editing', 'Tutorial lengkap edit video cinematic hanya pakai smartphone! Aplikasi gratis yang powerful banget. Perfect untuk content creator pemula. Jangan lupa subscribe dan nyalakan notifikasi! 🎬', '#EditVideoHP #TutorialEdit #CinematicVideo #ContentCreator #VideoEditing #YouTubeTutorial #MobileEditing #FreeTutorial'),
('youtube', 'Review Gadget Terbaru 2025', 'Teknologi', 'Unboxing dan review gadget terbaru yang wajib kamu tahu! Specs lengkap, performa, dan apakah worth it untuk dibeli? Full review ada di video ini! 📱', '#ReviewGadget #Unboxing #TechReview #GadgetTerbaru #Technology #YouTubeIndonesia #TechChannel #GadgetReview'),
('youtube', 'Vlog Jalan-Jalan ke Destinasi Tersembunyi', 'Travel', 'Eksplorasi tempat wisata hidden gem yang belum banyak orang tahu! Pemandangan indah, biaya terjangkau, dan pengalaman yang nggak terlupakan. Simak sampai habis ya! 🗺️', '#TravelVlog #HiddenGem #WisataIndonesia #Traveling #VlogIndonesia #ExploreIndonesia #TravelTips #YouTubeTravel'),
('youtube', 'Cara Memasak Rendang Autentik', 'Kuliner', 'Tutorial memasak rendang dengan resep turun temurun! Bumbu lengkap dan cara masak yang benar agar daging empuk dan bumbu meresap sempurna. Dijamin enak! 🍛', '#ResepRendang #MasakanIndonesia #TutorialMasak #Kuliner #IndonesianFood #CookingChannel #TraditionalFood #ResepMasakan');