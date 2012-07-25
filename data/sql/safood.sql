-- --------------------------------------------------------
-- Host:                         192.168.0.189
-- Server version:               5.1.62-0ubuntu0.11.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2012-07-25 15:53:51
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;

-- Dumping structure for table safood.additive
DROP TABLE IF EXISTS `additive`;
CREATE TABLE IF NOT EXISTS `additive` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(90) DEFAULT NULL,
  `alias` varchar(120) DEFAULT NULL,
  `cns` varchar(60) DEFAULT NULL,
  `ins` varchar(60) DEFAULT NULL,
  `effect` varchar(90) DEFAULT NULL,
  `safe4child` tinyint(1) DEFAULT '0',
  `created` int(11) DEFAULT NULL,
  `status` tinyint(11) DEFAULT '-1',
  `karma` float(11,4) DEFAULT '0.0000',
  `views_count` int(11) unsigned DEFAULT '0',
  `user_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cns` (`cns`),
  KEY `karma` (`karma`),
  KEY `name` (`name`),
  KEY `views_count` (`views_count`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- Dumping data for table safood.additive: ~7 rows (approximately)
/*!40000 ALTER TABLE `additive` DISABLE KEYS */;
REPLACE INTO `additive` (`id`, `name`, `alias`, `cns`, `ins`, `effect`, `safe4child`, `created`, `status`, `karma`, `views_count`, `user_id`) VALUES
	(1, '迷迭香提取物', '测试1', '4.017 ', NULL, '抗氧化剂', 0, 1342737909, 0, 0.0000, 7, 1),
	(2, '测试2', '测试2-其他名称', '20.032  ', '160a', '测试2-抗氧化剂', 0, 1342737919, 0, 0.0000, 11, 1),
	(3, '测试3', '测试3-其他名称', '17.031 ', '500iii', '测试3-抗氧化剂', 1, 1342737931, 0, 0.0000, 5, 1),
	(4, '测试4', '测试4-其他名称', '17.024 ', NULL, '测试4-干燥剂', 0, 1342738151, 0, 0.0000, 5, 2),
	(5, '测试5', '测试5-别名', '12.174 ', NULL, '膨松剂', 0, 1342738812, 0, 0.0000, 1, 2),
	(7, '测试6', '测试6-别名', '12.174 ', NULL, '膨松剂', 0, 1342738812, 0, 0.0000, 0, 2),
	(8, '迷迭香', '测试8', '4.017 ', '227b', '防腐剂', 0, 1343172169, 0, 0.0000, 0, 1);
/*!40000 ALTER TABLE `additive` ENABLE KEYS */;


-- Dumping structure for table safood.additive_detail
DROP TABLE IF EXISTS `additive_detail`;
CREATE TABLE IF NOT EXISTS `additive_detail` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `additive_id` int(11) unsigned DEFAULT NULL,
  `adi` varchar(600) DEFAULT NULL,
  `ld50` varchar(600) DEFAULT NULL,
  `apply_range` varchar(3000) DEFAULT NULL,
  `safe_status` varchar(1200) DEFAULT NULL,
  `using_status` varchar(300) DEFAULT NULL,
  `safe_risk` varchar(300) DEFAULT NULL,
  `safe_rank` smallint(5) unsigned DEFAULT '0',
  `preparation` varchar(900) DEFAULT NULL,
  `preparation_short` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `additive_id` (`additive_id`),
  CONSTRAINT `FK_addi_id` FOREIGN KEY (`additive_id`) REFERENCES `additive` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- Dumping data for table safood.additive_detail: ~5 rows (approximately)
/*!40000 ALTER TABLE `additive_detail` DISABLE KEYS */;
REPLACE INTO `additive_detail` (`id`, `additive_id`, `adi`, `ld50`, `apply_range`, `safe_status`, `using_status`, `safe_risk`, `safe_rank`, `preparation`, `preparation_short`) VALUES
	(1, 1, '0-0.025mg/kg\r\n', '1.6-3.2g/kg 大鼠口服\r\n', '盐及代盐制品 \r\n', '无已知不良反应\r\n', NULL, NULL, 0, NULL, NULL),
	(2, 2, '', '3460mg/kg  口服；1250mg/kg腹腔注射\r\n', '发酵面制品 冷冻米面制品\r\n', '无已知不良反应\r\n', NULL, NULL, 0, '头发中加入盐酸，加热水解6-8h，然后减压蒸馏出盐酸，再加活性炭脱色、过滤，滤液用氨水中和，得L-胱氨酸粗结晶，再用氨水溶解并中和，得L-半胱氨酸粗结晶，再用氨水溶解并中和，经重结晶后，再用盐酸溶液溶解，并进行电解还原，然后经浓缩、冷却、结晶、干燥，即得\r\n', '以头发为原料，加入盐酸，经过一系列的化学反应制成\r\n'),
	(3, 3, '0-1.25mg/kg（以抗坏血酸棕榈酸酯与抗坏血酸硬脂酸酯之和计，单独摄取和共同摄取）\r\n', '14.4g/kg 大鼠，经口。   0.1%-1%饲料慢性试验饲养6个月后，体重增加，血浆、肝、肾、脾、睾丸、心、肺等组织无异常变化\r\n', '调制乳  稀奶油（淡奶油）及其类似品  脂肪，油和乳化脂肪制品（02.01.01.01植物油除外） 氢化植物油  冰淇淋、雪糕类   经表面处理的鲜水果  经表面处理的新鲜蔬菜  豆类制品   可可制品、巧克力和巧克力制品,包括代可可脂巧克力及制品  除胶基糖果以外的其他糖果   面包  糕点  饼干 果蔬汁（肉）饮料（包括发酵型产品等） 植物蛋白饮料  风味饮料（包括果味饮料、乳味、茶味、咖啡味及其他味饮料等）（仅限果味饮料）  固体饮料类（速溶咖啡除外）  速溶咖啡  干酵母  其他（饮料混浊剂） \r\n', '在澳大利亚未取得食品使用许可\r\n', NULL, NULL, 0, '山梨醇与油酸在催化剂下进行酯化反应而得\r\n', ''),
	(4, 4, '不作特殊规定\r\n', '测试4-ld50', '调制乳  稀奶油（淡奶油）及其类似品  脂肪，油和乳化脂肪制品（02.01.01.01植物油除外） 氢化植物油  冰淇淋、雪糕类   经表面处理的鲜水果  经表面处理的新鲜蔬菜  豆类制品   可可制品、巧克力和巧克力制品,包括代可可脂巧克力及制品  除胶基糖果以外的其他糖果   面包  糕点  饼干 果蔬汁（肉）饮料（包括发酵型产品等） 植物蛋白饮料  风味饮料（包括果味饮料、乳味、茶味、咖啡味及其他味饮料等）（仅限果味饮料）  固体饮料类（速溶咖啡除外）  速溶咖啡  干酵母  其他（饮料混浊剂） \r\n', '测试4-安全情况', NULL, NULL, 0, '山梨醇与油酸在催化剂下进行酯化反应而得\r\n', ''),
	(5, 5, '不作特殊规定\r\n', '测试5-ld50', '调制乳  稀奶油（淡奶油）及其类似品  脂肪，油和乳化脂肪制品（02.01.01.01植物油除外） 氢化植物油  冰淇淋、雪糕类   经表面处理的鲜水果  经表面处理的新鲜蔬菜  豆类制品   可可制品、巧克力和巧克力制品,包括代可可脂巧克力及制品  除胶基糖果以外的其他糖果   面包  糕点  饼干 果蔬汁（肉）饮料（包括发酵型产品等） 植物蛋白饮料  风味饮料（包括果味饮料、乳味、茶味、咖啡味及其他味饮料等）（仅限果味饮料）  固体饮料类（速溶咖啡除外）  速溶咖啡  干酵母  其他（饮料混浊剂） \r\n', '测试5-安全情况', NULL, NULL, 0, '测试5-制法', '');
/*!40000 ALTER TABLE `additive_detail` ENABLE KEYS */;


-- Dumping structure for table safood.additive_search
DROP TABLE IF EXISTS `additive_search`;
CREATE TABLE IF NOT EXISTS `additive_search` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `additive_id` int(11) unsigned DEFAULT NULL,
  `search` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `search_times` (`search`),
  KEY `additive_id` (`additive_id`),
  CONSTRAINT `FK_saddi_id` FOREIGN KEY (`additive_id`) REFERENCES `additive` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Dumping data for table safood.additive_search: ~4 rows (approximately)
/*!40000 ALTER TABLE `additive_search` DISABLE KEYS */;
REPLACE INTO `additive_search` (`id`, `additive_id`, `search`) VALUES
	(1, 1, 0),
	(2, 2, 1),
	(3, 3, 2),
	(4, 4, 3);
/*!40000 ALTER TABLE `additive_search` ENABLE KEYS */;


-- Dumping structure for table safood.food
DROP TABLE IF EXISTS `food`;
CREATE TABLE IF NOT EXISTS `food` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `status` tinyint(11) DEFAULT '-1',
  `karma` float(11,4) DEFAULT '0.0000',
  `views_count` int(11) unsigned DEFAULT '0',
  `user_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `karma` (`karma`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- Dumping data for table safood.food: ~17 rows (approximately)
/*!40000 ALTER TABLE `food` DISABLE KEYS */;
REPLACE INTO `food` (`id`, `name`, `created`, `status`, `karma`, `views_count`, `user_id`) VALUES
	(1, '方便面', 1342969289, 0, 0.0000, 8, NULL),
	(2, '火腿肠', 1342969317, 0, 0.0000, 6, NULL),
	(3, '面包', 1342969340, 0, 0.0000, 2, NULL),
	(4, '威化', 1343032498, 0, 0.0000, 1, NULL),
	(5, '泡芙', 1343032529, 0, 0.0000, 1, NULL),
	(6, '桃酥', 1343032529, 0, 0.0000, 2, NULL),
	(7, '曲奇', 1343032529, 0, 0.0000, 1, NULL),
	(8, '锅巴', 1343032529, 0, 0.0000, 1, NULL),
	(9, '薯片', 1343032529, 0, 0.0000, 1, NULL),
	(10, '罐头', 1343032529, 0, 0.0000, 1, NULL),
	(11, '雪碧', 1343032529, 0, 0.0000, 2, NULL),
	(12, '可乐', 1343032529, 0, 0.0000, 1, NULL),
	(13, '王老吉', 1343050729, 0, 0.0000, 1, NULL),
	(14, '粗粮饼干', 1343050729, 0, 0.0000, 1, NULL),
	(15, '农夫果园', 1343050729, 0, 0.0000, 1, NULL),
	(16, '鲜橙多', 1343050819, 0, 0.0000, 1, NULL),
	(17, '冰红茶', 1343050815, 0, 0.0000, 1, NULL);
/*!40000 ALTER TABLE `food` ENABLE KEYS */;


-- Dumping structure for table safood.food_part
DROP TABLE IF EXISTS `food_part`;
CREATE TABLE IF NOT EXISTS `food_part` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `food_id` int(11) unsigned DEFAULT '0',
  `name` varchar(60) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `food_id` (`food_id`),
  KEY `name` (`name`),
  CONSTRAINT `FK_pfood_id` FOREIGN KEY (`food_id`) REFERENCES `food` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Dumping data for table safood.food_part: ~5 rows (approximately)
/*!40000 ALTER TABLE `food_part` DISABLE KEYS */;
REPLACE INTO `food_part` (`id`, `food_id`, `name`) VALUES
	(1, 1, '面饼'),
	(2, 1, '酱包'),
	(3, 1, '粉包'),
	(4, 2, '火腿肠'),
	(5, 3, '面包');
/*!40000 ALTER TABLE `food_part` ENABLE KEYS */;


-- Dumping structure for table safood.food_search
DROP TABLE IF EXISTS `food_search`;
CREATE TABLE IF NOT EXISTS `food_search` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `food_id` int(11) unsigned NOT NULL DEFAULT '0',
  `search` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `search` (`search`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `FK_sfood_id` FOREIGN KEY (`food_id`) REFERENCES `food` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Dumping data for table safood.food_search: ~3 rows (approximately)
/*!40000 ALTER TABLE `food_search` DISABLE KEYS */;
REPLACE INTO `food_search` (`id`, `food_id`, `search`) VALUES
	(1, 1, 1),
	(2, 2, 2),
	(3, 3, 3);
/*!40000 ALTER TABLE `food_search` ENABLE KEYS */;


-- Dumping structure for table safood.ingredient
DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE IF NOT EXISTS `ingredient` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `part_id` int(11) unsigned DEFAULT '0',
  `additive_id` int(11) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `additive_id` (`additive_id`),
  KEY `part_id` (`part_id`),
  CONSTRAINT `FK_iaddi_id` FOREIGN KEY (`additive_id`) REFERENCES `additive` (`id`) ON DELETE SET NULL,
  CONSTRAINT `FK_ifood_id` FOREIGN KEY (`part_id`) REFERENCES `food_part` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

-- Dumping data for table safood.ingredient: ~12 rows (approximately)
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
REPLACE INTO `ingredient` (`id`, `part_id`, `additive_id`) VALUES
	(1, 1, 1),
	(2, 1, 2),
	(3, 1, 3),
	(4, 2, 3),
	(5, 2, 2),
	(6, 3, 5),
	(7, 5, 5),
	(8, 5, 2),
	(9, 4, 2),
	(10, 4, 3),
	(11, 4, 1),
	(12, 4, 7);
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;


-- Dumping structure for table safood.user
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `fullname` varchar(50) DEFAULT NULL,
  `password` varchar(40) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  `avatar_hash` varchar(32) DEFAULT NULL,
  `level` tinyint(3) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Dumping data for table safood.user: ~2 rows (approximately)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
REPLACE INTO `user` (`id`, `email`, `username`, `fullname`, `password`, `created`, `status`, `avatar_hash`, `level`) VALUES
	(1, 'test@safood.com', 'test', 'test safood', '1234', 1342751875, 0, NULL, 0),
	(2, 'test2@safood.com', 'test2', 'test2 safood', '12345', 1342751921, 0, NULL, 0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
