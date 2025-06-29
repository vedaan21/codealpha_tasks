-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 06, 2025 at 06:16 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `file_duplicate`
--

-- --------------------------------------------------------

--
-- Table structure for table `fd_admin`
--

CREATE TABLE `fd_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fd_admin`
--

INSERT INTO `fd_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `fd_selected`
--

CREATE TABLE `fd_selected` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `file_path` varchar(100) NOT NULL,
  `filetype` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `hash_val` varchar(100) NOT NULL,
  `duplicate_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fd_selected`
--

INSERT INTO `fd_selected` (`id`, `uname`, `file_path`, `filetype`, `status`, `hash_val`, `duplicate_id`) VALUES
(1, 'guru', 'D:\\a\\cert5.jpg', 'file', 0, 'e2736c0ef9ffb095931f05cb3bdc965626723a07560cf297ca290a215d491bfd', 0),
(2, 'guru', 'D:\\a\\cert6.jpg', 'file', 0, '35e8fec411be2deef0891405ac02d290ee039db0f38ba75a2e5019e74b7ffc12', 0),
(3, 'guru', 'D:\\a\\mylist.txt', 'file', 0, '2b01565e7b2885e7b2e2a9597dca450d4cf832448efd46ac611d9f132a0cce72', 0),
(5, 'guru', 'D:\\a1\\data1.txt', 'file', 0, 'a85c36f2a2ab85f1ac23c92b3701395d85e84abbfc64d43b5431209e8982d337', 0),
(7, 'guru', 'D:\\b\\Agroculture.pptx', 'file', 0, '2852c4531ede6e0012a9d5e960facd9be50c847b1215eb0a4f629c6070361520', 0),
(8, 'guru', 'D:\\b\\det.txt', 'file', 0, 'c9f2974ecab37b9bfefbd7a51a088eb5783318fc33f8181c112fe67da0adeb8d', 0),
(11, 'guru', 'D:\\c\\test22.html', 'file', 0, '6bad5da5850a45d5ef9a64946de0c35229a1b89f48d01ed86b5697337081da01', 0),
(12, 'guru', 'D:\\c\\test33.html', 'file', 0, '4e8183dc34152fb3e45ea909c86535bfa1edaba2f0622d71a6772e96e9a238f5', 0);

-- --------------------------------------------------------

--
-- Table structure for table `fd_user`
--

CREATE TABLE `fd_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fd_user`
--

INSERT INTO `fd_user` (`id`, `name`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Guru', 8855662452, 'guru@gmail.com', 'guru', '123456');
