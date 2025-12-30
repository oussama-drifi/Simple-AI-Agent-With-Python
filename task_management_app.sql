-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:8080
-- Généré le : mer. 24 déc. 2025 à 23:56
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `task_management_app`
--

-- --------------------------------------------------------

--
-- Structure de la table `sub_tasks`
--

CREATE TABLE `sub_tasks` (
  `sub_task_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `deadline` datetime NOT NULL,
  `creation_date` datetime DEFAULT current_timestamp(),
  `is_done` tinyint(1) DEFAULT 0,
  `task_id` int(11) NOT NULL,
  `updated_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `sub_tasks`
--

INSERT INTO `sub_tasks` (`sub_task_id`, `title`, `description`, `deadline`, `creation_date`, `is_done`, `task_id`, `updated_date`, `deleted_at`) VALUES
(1, 'Design prompt flow', 'Chat UX', '2025-12-17 18:57:03', '2025-12-16 18:57:03', 0, 5, NULL, NULL),
(2, 'Implement intent parser', 'NL → SQL', '2025-12-18 18:57:03', '2025-12-16 18:57:03', NULL, 5, NULL, NULL),
(3, 'Write README', 'Main readme', '2025-12-18 18:57:03', '2025-12-12 18:57:03', 1, 6, '2025-12-14 18:57:03', NULL),
(4, 'Add examples', 'Usage examples', '2025-12-18 18:57:03', '2025-12-12 18:57:03', 0, 6, NULL, NULL),
(5, 'Fix login bug', 'Auth issue', '2025-12-15 18:57:03', '2025-12-10 18:57:03', 0, 7, NULL, NULL),
(6, 'Late patch', 'Hotfix', '2025-12-21 00:00:00', '2025-12-10 00:00:00', NULL, 7, NULL, NULL),
(7, 'Cleanup files', 'Remove legacy code', '2025-11-26 18:57:03', '2025-11-06 18:57:03', 1, 9, '2025-11-16 18:57:03', NULL),
(8, 'Draft slides', 'Initial slides', '2025-12-14 18:57:03', '2025-12-11 18:57:03', 0, 11, NULL, '2025-12-15 18:57:03'),
(9, 'Rehearse demo', 'Practice run', '2025-12-17 18:57:03', '2025-12-16 18:57:03', NULL, 11, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `tasks`
--

CREATE TABLE `tasks` (
  `task_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `creation_date` datetime DEFAULT current_timestamp(),
  `category` varchar(100) DEFAULT 'other',
  `priority` enum('low','medium','high') DEFAULT 'medium',
  `status` enum('todo','in progress','canceled','completed') DEFAULT 'todo',
  `updated_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `tasks`
--

INSERT INTO `tasks` (`task_id`, `title`, `description`, `deadline`, `creation_date`, `category`, `priority`, `status`, `updated_date`, `deleted_at`) VALUES
(5, 'Finish AI Agent', 'Core logic for AI agent', '2025-12-17 00:00:00', '2025-12-16 18:43:36', 'Development', 'high', 'in progress', '2025-12-24 20:28:23', NULL),
(6, 'Write Documentation', 'API documentation for endpoints', '2025-12-19 18:43:36', '2025-12-11 18:43:36', 'Docs', 'medium', '', '2025-12-15 18:43:36', NULL),
(7, 'Fix Bugs', 'Critical bug fixes for modifications', '2025-12-14 18:43:36', '2025-12-06 18:43:36', 'Maintenance', 'high', '', NULL, NULL),
(8, 'Brainstorm Features', 'Future ideas', NULL, '2025-12-16 18:43:36', 'Planning', 'low', 'todo', NULL, NULL),
(9, 'Old Prototype', 'Deprecated version', '2025-11-16 18:43:36', '2025-10-17 18:43:36', 'Archive', 'low', '', '2025-11-26 18:43:36', '2025-12-06 18:43:36'),
(10, 'Refactor Code', 'Cleanup messy code', '2025-12-21 18:43:36', '2025-12-09 18:43:36', 'Development', 'medium', '', NULL, NULL),
(11, 'Prepare Demo', 'Client demo preparation', '2025-12-15 18:43:36', '2025-12-12 18:43:36', 'Presentation', 'high', 'in progress', '2025-12-16 18:43:36', NULL);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `sub_tasks`
--
ALTER TABLE `sub_tasks`
  ADD PRIMARY KEY (`sub_task_id`),
  ADD KEY `task_id` (`task_id`),
  ADD KEY `idx_is_done` (`is_done`);

--
-- Index pour la table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`task_id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_deadline` (`deadline`),
  ADD KEY `idx_priority` (`priority`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `sub_tasks`
--
ALTER TABLE `sub_tasks`
  MODIFY `sub_task_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `task_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `sub_tasks`
--
ALTER TABLE `sub_tasks`
  ADD CONSTRAINT `sub_tasks_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`task_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
