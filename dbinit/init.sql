SET FOREIGN_KEY_CHECKS=0;
CREATE DATABASE IF NOT EXISTS SpAppDb DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
-- ----------------------------
-- Table structure for searchrecoder
-- ----------------------------
DROP TABLE IF EXISTS `searchrecoder`;
CREATE TABLE `searchrecoder` (
  `reqid` int(11) NOT NULL auto_increment,
  `reqloc` varchar(255) default NULL,
  `reqkeywds` varchar(255) default NULL,
  `remark` text,
  `recommendsite` varchar(255) default NULL,
  `addTime` datetime default NULL,
  PRIMARY KEY  (`reqid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of searchrecoder
-- ----------------------------
