-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2020 at 08:11 PM
-- Server version: 5.7.24
-- PHP Version: 7.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pajtonsajt`
--

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

DROP TABLE IF EXISTS `korisnici`;
CREATE TABLE IF NOT EXISTS `korisnici` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `lozinka` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `ime`, `prezime`, `email`, `lozinka`) VALUES
(4, 'Stefan', 'Nikolic', 'stefanikolic018@gmail.com', 'pbkdf2:sha256:150000$orDVefEZ$6ce26eb684a30e9659bda220198542fe290d3b086170d3bfaf68b973eb4f40ba'),
(6, 'Nikola', 'Dimitrijevic', 'nidza.dim@gmail.com', 'pbkdf2:sha256:150000$9i5T0Dr3$0da7237b596baeb4d122f682330eb3ec56c5c84582736eaf2a5b26a6724761f0');

-- --------------------------------------------------------

--
-- Table structure for table `ocene`
--

DROP TABLE IF EXISTS `ocene`;
CREATE TABLE IF NOT EXISTS `ocene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `predmet_id` int(11) NOT NULL,
  `ocena` decimal(6,2) NOT NULL,
  `datum` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `foreign` (`predmet_id`),
  KEY `foreign_1` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ocene`
--

INSERT INTO `ocene` (`id`, `student_id`, `predmet_id`, `ocena`, `datum`) VALUES
(1, 1, 3, '10.00', '2020-01-31'),
(2, 1, 4, '8.00', '2020-01-31'),
(4, 1, 6, '9.00', '2020-01-31');

-- --------------------------------------------------------

--
-- Table structure for table `predmeti`
--

DROP TABLE IF EXISTS `predmeti`;
CREATE TABLE IF NOT EXISTS `predmeti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sifra` varchar(30) NOT NULL,
  `naziv` varchar(50) NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `espb` int(11) NOT NULL,
  `obavezni_izborni` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `predmeti`
--

INSERT INTO `predmeti` (`id`, `sifra`, `naziv`, `godina_studija`, `espb`, `obavezni_izborni`) VALUES
(2, 'RM5', 'Racunarske Mreze', 2, 6, 'Obavezni'),
(3, 'WP4', 'Web programiranje', 3, 6, 'Obavezni'),
(4, 'AM3', 'Arhitektura mikrokontrolera', 3, 6, 'Obavezni'),
(5, 'TE2', 'Tehnicki engleski 2', 3, 5, 'Izborni'),
(6, 'KSS1', 'Klijent server sistemi', 3, 6, 'Obavezni');

-- --------------------------------------------------------

--
-- Table structure for table `studenti`
--

DROP TABLE IF EXISTS `studenti`;
CREATE TABLE IF NOT EXISTS `studenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(20) NOT NULL,
  `ime_roditelja` varchar(20) NOT NULL,
  `prezime` varchar(20) NOT NULL,
  `broj_indeksa` varchar(10) NOT NULL,
  `godina_studija` int(11) NOT NULL,
  `jmbg` int(11) NOT NULL,
  `datum_rodjenja` varchar(10) NOT NULL,
  `espb` int(11) NOT NULL,
  `prosek_ocena` decimal(11,2) NOT NULL,
  `broj_telefona` int(11) NOT NULL,
  `email` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `studenti`
--

INSERT INTO `studenti` (`id`, `ime`, `ime_roditelja`, `prezime`, `broj_indeksa`, `godina_studija`, `jmbg`, `datum_rodjenja`, `espb`, `prosek_ocena`, `broj_telefona`, `email`) VALUES
(1, 'Stefan', 'Srboljub', 'Nikolic', 'REr 45/17', 3, 31039981, '1998-03-31', 18, '9.00', 611555036, 'stefanikolic018@gmail.com');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ocene`
--
ALTER TABLE `ocene`
  ADD CONSTRAINT `foreign` FOREIGN KEY (`predmet_id`) REFERENCES `predmeti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `foreign_1` FOREIGN KEY (`student_id`) REFERENCES `studenti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
