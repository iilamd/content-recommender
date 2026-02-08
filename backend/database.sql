-- 1. Setup Database
CREATE DATABASE IF NOT EXISTS content_recommender;
USE content_recommender;

-- 2. Matikan pengecekan key sementara untuk setup bersih
SET FOREIGN_KEY_CHECKS = 0;

-- --------------------------------------------------------
-- Struktur Tabel `users`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Struktur Tabel `contents`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `contents` (
  `id` VARCHAR(25) NOT NULL,
  `platform` VARCHAR(20) NOT NULL,
  `category` VARCHAR(50) NOT NULL,
  `caption` TEXT DEFAULT NULL,
  `hashtag` TEXT DEFAULT NULL,
  `url` VARCHAR(500) DEFAULT NULL,
  `text_for_tfidf` TEXT DEFAULT NULL,
  `likes` INT(11) DEFAULT 0,
  `views` INT(11) DEFAULT 0,
  `comments` INT(11) DEFAULT 0,
  `engagement_rate` FLOAT DEFAULT 0,
  `is_popular` TINYINT(1) DEFAULT 0,
  `shares` INT(11) DEFAULT 0,
  `saves` INT(11) DEFAULT 0,
  `created_at` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Struktur Tabel `favorites`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `favorites` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `content_id` VARCHAR(25) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_favorite` (`user_id`, `content_id`),
  CONSTRAINT `fk_fav_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_fav_content` FOREIGN KEY (`content_id`) REFERENCES `contents` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Struktur Tabel `activity_logs`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `activity_logs` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `action` VARCHAR(50) NOT NULL,
  `platform` VARCHAR(20) DEFAULT NULL,
  `keyword` VARCHAR(255) DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_log_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 3. Aktifkan kembali pengecekan key
SET FOREIGN_KEY_CHECKS = 1;