
-- SET FOREIGN_KEY_CHECKS = 0;
-- DROP TABLE `Answers`;

-- DROP TABLE `Bookmarks`;

-- DROP TABLE `CalendarEvent`;
-- DROP TABLE `Calendars`;
-- DROP TABLE `Communities`;
-- DROP TABLE `CommunityForums`;
-- DROP TABLE `CommunityMembers`;
-- DROP TABLE `CommunityModerator`;
-- DROP TABLE `Confirmations`;
-- DROP TABLE `cources`;
-- DROP TABLE `cources_lectors`;
-- DROP TABLE `cources_videos`;

-- DROP TABLE `Forum`;


-- DROP TABLE `lectors`;
-- DROP TABLE `lectors_cources`;
-- DROP TABLE `log_href`;
-- DROP TABLE `Messages`;
-- DROP TABLE `MEvents_lectors`;
-- DROP TABLE `News`;
-- DROP TABLE `osfm_users`;
-- DROP TABLE `PhotoGalleries`;
-- DROP TABLE `Photos`;
-- DROP TABLE `Polls`;
-- DROP TABLE `PollVariant`;
-- DROP TABLE `Questions`;
-- DROP TABLE `Services`;
-- DROP TABLE `Tags`;
-- DROP TABLE `TagsLinks`;
-- DROP TABLE `tExtraFields`;
-- DROP TABLE `translation_timer`;

-- DROP TABLE `Users_events`;
-- DROP TABLE `users_registered_on_events`;
-- DROP TABLE `UsersCalendar`;
-- DROP TABLE `UsersPollsAnswers`;
-- DROP TABLE `Videos_lectors`;
-- DROP TABLE `Votes`;
-- SET FOREIGN_KEY_CHECKS = 1;


-- users
-- overall users fields
--  (`is_superuser`,`spec_id`,`experience`,`addspeciality`,`addexperience`,`graduate`,`dissertation`,`title`,`addtitle`,`category_id`,`town`,
--  `phone_number`,`phone_visible`,`email_visible`,`ICQ_Skype`,`social`,`is_staff`,`is_active`,`is_admin`,`awords`,`organization`,`job`,
--  `site`,`school`,`graduate_year`,`faculty`,`cathedra`,`country`,`login`,`pass`,`last_login`,`firstname`,`lastname`,
--  `surname`,`avatar`,`sex`,`birthday`,`email`,`status`,`createdate`,`updatedate`,`lastvisit`,`lastaccess`,`type`,`user_ptr_id`)

-- non-used user fields
--  (`is_superuser`,,`addspeciality`,`addexperience`,`graduate`,`title`,`addtitle`,`category_id`,
--  ,`phone_visible`,`email_visible`,,`social`,`is_staff`,`is_active`,`is_admin`,`awords`,,
--  ,,`faculty`,`cathedra`,,`last_login`,
--  ,`avatar`,`sex`,,`type`)

SET FOREIGN_KEY_CHECKS = 0;

ALTER DATABASE medtusdj_db_migrate CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE `account_additionalimage` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`image` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`user_id` int(11) NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=110 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `account_aword` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`user_id` int(11) NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=166 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `account_category` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=5 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;

CREATE TABLE `account_myuser` (
	`id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`is_superuser` tinyint(1) NOT NULL,
	`spec_id` int(10) DEFAULT NULL,
	`experience` varchar(256) DEFAULT NULL,
	`addspeciality` varchar(256) DEFAULT NULL,
	`addexperience` varchar(256) DEFAULT NULL,
	`graduate_id` int(11),
	`dissertation` varchar(256) DEFAULT NULL,
	`title` varchar(256) DEFAULT NULL,
	`addtitle` varchar(256) DEFAULT NULL,
	`category_id` varchar(256) DEFAULT NULL,
	`town` varchar(256) DEFAULT NULL,
	`phone_number` varchar(256) DEFAULT NULL,
	`phone_visible` varchar(256) DEFAULT NULL,
	`email_visible` varchar(256) DEFAULT NULL,
	`ICQ_Skype` varchar(256) DEFAULT NULL,
	`social` varchar(256) DEFAULT NULL,
	`is_staff` tinyint(1) NOT NULL,
	`is_active` tinyint(1) NOT NULL,
	`is_admin` tinyint(1) NOT NULL,
	`awords_id` int(11) DEFAULT NULL,
	`organization` varchar(256) DEFAULT NULL,
	`job` varchar(256) DEFAULT NULL,
	`site` varchar(256) DEFAULT NULL,
	`school` varchar(256) DEFAULT NULL,
	`graduate_year` varchar(256) DEFAULT NULL,
	`faculty` varchar(256) DEFAULT NULL,
	`cathedra` varchar(256) DEFAULT NULL,
	`country` varchar(256) DEFAULT NULL,
	`login` varchar(50) DEFAULT NULL,
	`pass` varchar(255) DEFAULT NULL,
	`last_login` datetime DEFAULT NULL,
	`firstname` varchar(255) DEFAULT NULL,
	`lastname` varchar(255) DEFAULT NULL,
	`surname` varchar(255) DEFAULT NULL,
	`avatar` varchar(255) DEFAULT NULL,
	`sex` varchar(256) DEFAULT NULL,
	`birthday` date DEFAULT NULL,
	`email` varchar(50) DEFAULT NULL,
	`status` int(10) UNSIGNED DEFAULT 0,
	`createdate` datetime DEFAULT NULL,
	`updatedate` datetime DEFAULT NULL,
	`lastvisit` datetime DEFAULT NULL,
	`lastaccess` datetime DEFAULT NULL,
	`type` int(10) UNSIGNED DEFAULT NULL,
	`user_ptr_id` int(11) NOT NULL DEFAULT 2,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `account_myuser_id_10fc97f0` (`id`,`town`) USING BTREE,
  KEY `account_myuser_id_799923ec` (`id`,`spec_id`) USING BTREE,
  KEY `account_myuser_fd9427e3` (`graduate_id`)) ENGINE=`MyISAM` AUTO_INCREMENT=76361 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `account_myuser` CHANGE COLUMN `town` `town` int(11) DEFAULT NULL, CHANGE COLUMN `country` `country` int(11) DEFAULT NULL;

-- event access
DROP TABLE IF EXISTS `account_eventaccess`;
CREATE TABLE `account_eventaccess` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `event_type` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_eventaccess_event_type_60314d8c` (`event_type`(255),`user_id`),
  KEY `account_eventaccess_event_type_33187f4a` (`event_type`(255),`user_id`,`time`),
  KEY `account_eventaccess_6340c63c` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=241 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `account_myuser_groups` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`myuser_id` int(11) NOT NULL,
	`group_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `myuser_id` USING BTREE (`myuser_id`, `group_id`) comment '',
	INDEX `account_myuser_groups_f1d9e869` USING BTREE (`myuser_id`) comment '',
	INDEX `account_myuser_groups_5f412f9a` USING BTREE (`group_id`) comment '',
	CONSTRAINT `group_id_refs_id_f508e480` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
	CONSTRAINT `myuser_id_refs_id_3bca27d5` FOREIGN KEY (`myuser_id`) REFERENCES `account_myuser___` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;

CREATE TABLE `account_myuser_user_permissions` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`myuser_id` int(11) NOT NULL,
	`permission_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `myuser_id` USING BTREE (`myuser_id`, `permission_id`) comment '',
	INDEX `account_myuser_user_permissions_f1d9e869` USING BTREE (`myuser_id`) comment '',
	INDEX `account_myuser_user_permissions_83d7f98b` USING BTREE (`permission_id`) comment '',
	CONSTRAINT `myuser_id_refs_id_62ed4079` FOREIGN KEY (`myuser_id`) REFERENCES `account_myuser___` (`id`),
	CONSTRAINT `permission_id_refs_id_6c32d930` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;

--DROP TABLE IF EXISTS `account_timer`;
--CREATE TABLE `account_timer` (
--  `id` int(11) NOT NULL AUTO_INCREMENT,
--  `user_id` int(11) NOT NULL,
--  `post_id` int(11) NOT NULL,
--  `time` int(11) NOT NULL,
--  PRIMARY KEY (`id`),
--  KEY `post_id_refs_id_01e2d4ff` (`post_id`),
--  CONSTRAINT `account_timer_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `medtus_translation` (`id`)
--) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

ALTER TABLE `auth_group` CHANGE COLUMN `name` `name` varchar(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `id`;
ALTER TABLE `auth_group` ENGINE=`InnoDB` AUTO_INCREMENT=1 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `auth_group_permissions` DROP FOREIGN KEY `permission_id_refs_id_5886d21f`;
ALTER TABLE `auth_group_permissions` DROP FOREIGN KEY `group_id_refs_id_3cea63fe`;
ALTER TABLE `auth_group_permissions` DROP INDEX `auth_group_permissions_1e014c8f`;
ALTER TABLE `auth_group_permissions` DROP INDEX `auth_group_permissions_425ae3c4`;
ALTER TABLE `auth_group_permissions` ENGINE=`InnoDB` AUTO_INCREMENT=1 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `auth_group_permissions` ADD INDEX `auth_group_permissions_5f412f9a` USING BTREE (`group_id`) comment '';
ALTER TABLE `auth_group_permissions` ADD INDEX `auth_group_permissions_83d7f98b` USING BTREE (`permission_id`) comment '';
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `medtusdj_db_migrate`.`auth_group` (`id`);
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `medtusdj_db_migrate`.`auth_permission` (`id`);
ALTER TABLE `auth_permission` DROP FOREIGN KEY `content_type_id_refs_id_728de91f`;
ALTER TABLE `auth_permission` DROP INDEX `auth_permission_1bb8f392`;
ALTER TABLE `auth_permission` CHANGE COLUMN `name` `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `id`;
ALTER TABLE `auth_permission` CHANGE COLUMN `codename` `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `content_type_id`;
ALTER TABLE `auth_permission` ENGINE=`InnoDB` AUTO_INCREMENT=181 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `auth_permission` ADD INDEX `auth_permission_37ef4eb4` USING BTREE (`content_type_id`) comment '';
ALTER TABLE `auth_permission` ADD CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `medtusdj_db_migrate`.`django_content_type` (`id`);
CREATE TABLE `banners_banner` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`alt` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`text` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`img` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`url` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`sort` smallint(5) UNSIGNED NOT NULL,
	`group_id` int(11) NOT NULL,
	`often` smallint(5) UNSIGNED NOT NULL,
	`html` tinyint(1) NOT NULL,
	`flash` tinyint(1) NOT NULL,
	`public` tinyint(1) NOT NULL,
	`created_at` datetime NOT NULL,
	`updated_at` datetime NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `group_id_refs_id_55e9fa3d` USING BTREE (`group_id`) comment '',
	CONSTRAINT `group_id_refs_id_55e9fa3d` FOREIGN KEY (`group_id`) REFERENCES `banners_bannergroup` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=4 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_banner_urls` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`banner_id` int(11) NOT NULL,
	`url_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `banner_id` USING BTREE (`banner_id`, `url_id`) comment '',
	INDEX `url_id_refs_id_5a648394` USING BTREE (`url_id`) comment '',
	CONSTRAINT `banner_id_refs_id_3e8e05ba` FOREIGN KEY (`banner_id`) REFERENCES `banners_banner` (`id`),
	CONSTRAINT `url_id_refs_id_5a648394` FOREIGN KEY (`url_id`) REFERENCES `banners_url` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=9 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_bannergroup` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`slug` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`width` smallint(5) UNSIGNED NOT NULL,
	`height` smallint(5) UNSIGNED NOT NULL,
	`speed` smallint(5) UNSIGNED NOT NULL,
	`public` tinyint(1) NOT NULL,
	`created_at` datetime NOT NULL,
	`updated_at` datetime NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `slug` USING BTREE (`slug`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=2 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_log` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`banner_id` int(11) NOT NULL,
	`group_id` int(11) NOT NULL,
	`user_id` int(11) DEFAULT NULL,
	`datetime` datetime NOT NULL,
	`ip` char(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`user_agent` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`page` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`key` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`type` smallint(5) UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `banner_id_refs_id_8fd401ac` USING BTREE (`banner_id`) comment '',
	INDEX `group_id_refs_id_b7a5d2d5` USING BTREE (`group_id`) comment '',
	CONSTRAINT `banner_id_refs_id_8fd401ac` FOREIGN KEY (`banner_id`) REFERENCES `banners_banner` (`id`),
	CONSTRAINT `group_id_refs_id_b7a5d2d5` FOREIGN KEY (`group_id`) REFERENCES `banners_bannergroup` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_log_urls` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`log_id` int(11) NOT NULL,
	`url_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `log_id` USING BTREE (`log_id`, `url_id`) comment '',
	INDEX `url_id_refs_id_ce778ffd` USING BTREE (`url_id`) comment '',
	CONSTRAINT `url_id_refs_id_ce778ffd` FOREIGN KEY (`url_id`) REFERENCES `banners_url` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_logstat` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`banner_id` int(11) NOT NULL,
	`group_id` int(11) NOT NULL,
	`date` date NOT NULL,
	`view` int(10) UNSIGNED NOT NULL,
	`click` int(10) UNSIGNED NOT NULL,
	`unique_click` int(10) UNSIGNED DEFAULT NULL,
	`unique_view` int(10) UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `banners_logstat_5f36a279` USING BTREE (`banner_id`) comment '',
	INDEX `banners_logstat_5f412f9a` USING BTREE (`group_id`) comment '',
	CONSTRAINT `banner_id_refs_id_249a2c64` FOREIGN KEY (`banner_id`) REFERENCES `banners_banner` (`id`),
	CONSTRAINT `group_id_refs_id_e87dea6d` FOREIGN KEY (`group_id`) REFERENCES `banners_bannergroup` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_logstat_urls` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`logstat_id` int(11) NOT NULL,
	`url_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `logstat_id` USING BTREE (`logstat_id`, `url_id`) comment '',
	INDEX `banners_logstat_urls_5f4f2613` USING BTREE (`logstat_id`) comment '',
	INDEX `banners_logstat_urls_c379dc61` USING BTREE (`url_id`) comment '',
	CONSTRAINT `logstat_id_refs_id_9cc81e4f` FOREIGN KEY (`logstat_id`) REFERENCES `banners_logstat` (`id`),
	CONSTRAINT `url_id_refs_id_fc92db29` FOREIGN KEY (`url_id`) REFERENCES `banners_url` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `banners_url` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` varchar(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`url` varchar(2048) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`regex` tinyint(1) NOT NULL,
	`public` tinyint(1) NOT NULL,
	`created_at` datetime NOT NULL,
	`updated_at` datetime NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=2 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `circle_circle` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`parent_id` int(11) NOT NULL,
	`friend_id` int(11) NOT NULL,
	`activated` tinyint(1) NOT NULL,
	`createdate` datetime NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=122 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `circle_dialog` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`authA_id` int(11) NOT NULL,
	`authB_id` int(11) NOT NULL,
	`createdate` datetime NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=26 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `circle_record` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`auth_id` int(11) NOT NULL,
	`value` varchar(2048) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
	`dialog_id` int(11) NOT NULL,
	`createdate` datetime NOT NULL,
	`viewed` datetime NOT NULL,
	`moderated` tinyint(1) NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=181 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `Clinicals` ENGINE=`MyISAM` AUTO_INCREMENT=272 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `Comments` ENGINE=`InnoDB` AUTO_INCREMENT=72121 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `Countries` ENGINE=`InnoDB` AUTO_INCREMENT=250 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `django_admin_log` DROP FOREIGN KEY `user_id_refs_id_c8665aa`;
ALTER TABLE `django_admin_log` DROP FOREIGN KEY `content_type_id_refs_id_288599e6`;
ALTER TABLE `django_admin_log` DROP INDEX `django_admin_log_1bb8f392`;
ALTER TABLE `django_admin_log` DROP INDEX `django_admin_log_403f60f`;
ALTER TABLE `django_admin_log` CHANGE COLUMN `object_id` `object_id` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL after `content_type_id`;
ALTER TABLE `django_admin_log` CHANGE COLUMN `object_repr` `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `object_id`;
ALTER TABLE `django_admin_log` CHANGE COLUMN `change_message` `change_message` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `action_flag`;
ALTER TABLE `django_admin_log` ENGINE=`InnoDB` AUTO_INCREMENT=167 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `django_admin_log` ADD INDEX `django_admin_log_6340c63c` USING BTREE (`user_id`) comment '';
ALTER TABLE `django_admin_log` ADD INDEX `django_admin_log_37ef4eb4` USING BTREE (`content_type_id`) comment '';
ALTER TABLE `django_admin_log` ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `medtusdj_db_migrate`.`django_content_type` (`id`);
ALTER TABLE `django_content_type` CHANGE COLUMN `name` `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `id`;
ALTER TABLE `django_content_type` CHANGE COLUMN `app_label` `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `name`;
ALTER TABLE `django_content_type` CHANGE COLUMN `model` `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `app_label`;
ALTER TABLE `django_content_type` ENGINE=`InnoDB` AUTO_INCREMENT=61 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `django_session` DROP INDEX `django_session_3da3d3d8`;
ALTER TABLE `django_session` CHANGE COLUMN `session_key` `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL first;
ALTER TABLE `django_session` CHANGE COLUMN `session_data` `session_data` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL after `session_key`;
ALTER TABLE `django_session` ENGINE=`InnoDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ROW_FORMAT=COMPACT COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `django_session` ADD INDEX `django_session_b7b81f0c` USING BTREE (`expire_date`) comment '';
ALTER TABLE `Groups` ENGINE=`MyISAM` AUTO_INCREMENT=238 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `GroupTypes` ENGINE=`MyISAM` AUTO_INCREMENT=20 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `GroupUsers` ADD COLUMN `activated` tinyint(1) NOT NULL after `user_id`;
ALTER TABLE `GroupUsers` ADD COLUMN `invite_id` int(11) DEFAULT NULL after `activated`;
ALTER TABLE `GroupUsers` ADD INDEX `GroupUsers_fa9e6b40` USING BTREE (`invite_id`) comment '';
CREATE TABLE `library_country` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=4 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `library_graduate` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=4 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
INSERT INTO `library_graduate` VALUES ('2', 'Доктор'), ('1', 'Кандидат');
CREATE TABLE `library_school` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=3 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `library_spec` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=101 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `library_title` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=20 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
INSERT INTO `library_title` VALUES ('20', 'Аспирант'), ('21', 'Ассистент'), ('22', 'Ведущий научный сотрудник'), ('23', 'Главный научный сотрудник'), ('24', 'Докторант'), ('25', 'Доцент'), ('26', 'Младший научный сотрудник'), ('27', 'Научный сотрудник'), ('28', 'Преподаватель'), ('29', 'Профессор'), ('31', 'Стажер'), ('32', 'Старший научный сотрудник'), ('30', 'Старший преподаватель'), ('33', 'Студент');
CREATE TABLE `library_topic` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=10 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `library_town` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`country_id` int(11) NOT NULL,
	`name` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `name` USING BTREE (`name`) comment '',
	INDEX `library_town_d860be3c` USING BTREE (`country_id`) comment '',
	CONSTRAINT `country_id_refs_id_243e7518` FOREIGN KEY (`country_id`) REFERENCES `library_country` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `mce_filebrowser_filebrowserfile` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`file_type` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`uploaded_file` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`create_date` datetime NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=4 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `medtus_like` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`material_id` int(11) DEFAULT NULL,
	`service_id` int(11) DEFAULT NULL,
	`user_id` int(11) NOT NULL,
	`createdate` datetime NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=382 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `medtus_materialphoto` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`service_id` int(11) DEFAULT NULL,
	`object_id` int(11) DEFAULT NULL,
	`picture` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`thumb` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=457 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `medtus_materialvideo` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`service_id` int(11) DEFAULT NULL,
	`object_id` int(11) DEFAULT NULL,
	`data` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`preview` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=123 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `medtus_translation` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` varchar(255) NOT NULL,
	`data` longtext NOT NULL,
	`active` tinyint(1) NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=6 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;

CREATE TABLE `medtus_visited` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `material_id` int(11) DEFAULT NULL,
  `counter` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `medtus_visited_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_1c4b94e1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT;

ALTER TABLE `MEvents` ADD COLUMN `starttime` time DEFAULT NULL after `end`;
ALTER TABLE `MEvents` ADD COLUMN `public_main` tinyint(1) NOT NULL DEFAULT 0 after `show_cmedu`;
ALTER TABLE `MEvents` ADD COLUMN `createdate` datetime DEFAULT NULL after `public_main`;
ALTER TABLE `MEvents` ADD COLUMN `comment_show` tinyint(1) NOT NULL DEFAULT 1 after `comment_cnt`;
ALTER TABLE `MEvents` ENGINE=`MyISAM` AUTO_INCREMENT=1547 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;

-- ----------------------------
--  Table structure for `partners_partner`
-- ----------------------------
DROP TABLE IF EXISTS `partners_partner`;
CREATE TABLE `partners_partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rubric_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `partners_partner_e7022157` (`rubric_id`),
  CONSTRAINT `partners_partner_ibfk_1` FOREIGN KEY (`rubric_id`) REFERENCES `partners_rubric` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
--  Records of `partners_partner`
-- ----------------------------
BEGIN;
INSERT INTO `partners_partner` VALUES ('1', 'partners_images/title-ru_1.jpg', 'Клиническое подразделение РНМОТ', 'http://www.ingorts.ru/index.php/ru', '1'), ('2', 'partners_images/duma-logo-main.jpg', 'Комитет государственной думы по охране здоровья', 'http://www.ohrana-zdorovja.ru/', '2'), ('3', 'partners_images/medways100x100_nm.jpg', '', 'http://www.medways.ru/', '3'), ('4', 'partners_images/logo-remedium.gif', '', 'http://www.remedium.ru/', '3'), ('5', 'partners_images/sochi0214_2.jpg', '', 'http://www.yandex.ru/', '2'), ('6', 'partners_images/lekarXXI200.jpg', '', 'http://www.yandex.ru/', '2'), ('7', 'partners_images/VIII_big.jpg', '', 'http://www.yandex.ru/', '2'), ('8', 'partners_images/3_89f9a308010a3adbb09cd48149981ffa.jpg', '', 'http://www.yandex.ru/', '2'), ('9', 'partners_images/banner_Fest.gif', '', 'http://www.yandex.ru/', '2'), ('10', 'partners_images/lor2014.gif', '', 'http://www.yandex.ru/', '2'), ('12', 'partners_images/logo-1.png', 'ФГБУ \"НАУЧНЫЙ ЦЕНТР АКУШЕРСТВА, ГИНЕКОЛОГИИ И ПЕРИНАТОЛОГИИ имени академика В.И. Кулакова Минздрава России', 'http://www.ncagip.ru/', '1'), ('13', 'partners_images/nczd_logo.jpg', 'Федеральное государственное  бюджетное научное учреждение \"Научный центр здоровья детей\"', 'http://www.nczd.ru/', '1'), ('14', 'partners_images/25-27.02.12.jpg', 'Союз педиатров России', 'http://www.pediatr-russia.ru/', '1'), ('15', 'partners_images/71364.jpg', 'Ассоциация междисциплинарной медицины', 'http://intermeda.ru/', '1'), ('16', 'partners_images/1322484388_associaciya-rossiyskih-farmacevticheskih-proizvoditeley-arfp.jpg', 'Ассоциация Российских Фармацевтических Производителей', 'http://www.arfp.ru/', '1'), ('17', 'partners_images/234028-s.jpg', 'Национальное общество по атеротромбозу', 'http://www.noat.ru/', '1'), ('18', 'partners_images/logo-big.jpg', 'Национальное научное общество КАРДИОВАСКУЛЯРНАЯ ПРОФИЛАКТИКА И РЕАБИЛИТАЦИЯ', 'http://www.cardioprevent.ru/', '1'), ('19', 'partners_images/logo_rosokr.png', 'росокр', 'http://www.rosokr.ru/', '1'), ('20', 'partners_images/logo.jpg', 'Клуб аритмологов', 'http://club-aritmolog.ru/', '1'), ('21', 'partners_images/logo-2.png', 'Научное общество гастроэнтерологов  России (НОГР)', 'http://tsrv.biz/', '1'), ('22', 'partners_images/307749_html_m7b95d3a4.jpg', 'РМОАГ', 'http://www.gipertonik.ru/', '1'), ('23', 'partners_images/press_r_545C3B11-8265-4181-AC23-3D38F034A3E4.jpg', 'РАСПМ', 'http://www.raspm.ru/', '1'), ('25', 'partners_images/logo_raop_1_1.jpg', 'Российская ассоциация по остеопорозу', 'http://www.osteoporoz.ru/', '1'), ('26', 'partners_images/92994_240x240.jpg', 'Союз противораковых организаций России', 'http://netoncology.ru/', '1'), ('27', 'partners_images/logo-1.jpg', 'Российское общество онкоурологов', 'http://www.roou.ru/', '1'), ('28', 'partners_images/ed0853f8eeffcc7a89917d9ef8f2efc4.jpg', 'рарч', 'http://www.rahr.ru/', '1'), ('30', 'partners_images/ossn.png', 'оссн', 'http://ossn.ru/', '1'), ('31', 'partners_images/rodvk.png', 'РОДВК', 'http://www.rodv.ru/', '1'), ('32', 'partners_images/nadk.gif', 'Национальный альянс дерматологов и косметологов', 'http://www.nadc.ru/', '1'), ('33', 'partners_images/avop.png', 'Ассоциация врачей общей практики', 'http://familymedicine.ru/', '1'), ('34', 'partners_images/bakuleva.png', 'Научный центр сердечно-сосудистой хирургии им. А.Н. Бакулева', 'http://www.bakulev.ru/', '1'), ('35', 'partners_images/roib.jpg', 'РОИБ', 'http://www.painrussia.ru/', '1'), ('37', 'partners_images/fsrk.png', 'Фонд содействия развитию кардиологии', 'http://www.painrussia.ru/', '1'), ('38', 'partners_images/rou.jpg', 'роу', 'http://ooorou.ru/', '1');
COMMIT;

-- ----------------------------
--  Table structure for `partners_rubric`
-- ----------------------------
DROP TABLE IF EXISTS `partners_rubric`;
CREATE TABLE `partners_rubric` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
--  Records of `partners_rubric`
-- ----------------------------
BEGIN;
INSERT INTO `partners_rubric` VALUES ('1', 'Медицинские ассоциации и сообщества'), ('2', 'Государственные учреждения'), ('3', 'Издательства и медицинские СМИ');
COMMIT;

ALTER TABLE `PGalleries` ENGINE=`MyISAM` AUTO_INCREMENT=115 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `PGPhotos` ENGINE=`MyISAM` AUTO_INCREMENT=810 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `post_post` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`content` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`topic_id` int(11) NOT NULL,
	`spec_id` int(11) NOT NULL,
	`title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`created` time NOT NULL,
	`changed` time NOT NULL,
	`publisher_id` int(11) NOT NULL,
	`viewed` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `post_post_76f18ad3` USING BTREE (`topic_id`) comment '',
	INDEX `post_post_421877ba` USING BTREE (`spec_id`) comment '',
	INDEX `post_post_81b79144` USING BTREE (`publisher_id`) comment '',
	CONSTRAINT `spec_id_refs_id_4608fa1a` FOREIGN KEY (`spec_id`) REFERENCES `library_spec` (`id`),
	CONSTRAINT `topic_id_refs_id_cf547e66` FOREIGN KEY (`topic_id`) REFERENCES `library_topic` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=5 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `post_postphoto` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`post_id` int(11) NOT NULL,
	`picture` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`thumb` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `post_postphoto_87a49a9a` USING BTREE (`post_id`) comment '',
	CONSTRAINT `post_id_refs_id_aead6737` FOREIGN KEY (`post_id`) REFERENCES `post_post` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `post_postvideo` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`post_id` int(11) NOT NULL,
	`data` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`preview` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `post_postvideo_87a49a9a` USING BTREE (`post_id`) comment '',
	CONSTRAINT `post_id_refs_id_e53f19c2` FOREIGN KEY (`post_id`) REFERENCES `post_post` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=1 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `PostLinks` DROP PRIMARY KEY;
ALTER TABLE `PostLinks` ADD PRIMARY KEY(`service_id`,`object_id`,`post_id`);
ALTER TABLE `Posts` ADD COLUMN `publicmain` tinyint(1) NOT NULL DEFAULT 0 after `format`;
ALTER TABLE `Posts` ADD COLUMN `code` text CHARACTER SET utf8 NOT NULL after `publicmain`;
ALTER TABLE `Posts` ADD COLUMN `image` varchar(255) CHARACTER SET utf8 NOT NULL after `code`;
ALTER TABLE `Posts` ADD COLUMN `comment_show` tinyint(1) NOT NULL DEFAULT 1 after `image`;
ALTER TABLE `Posts` ADD COLUMN `begindate` datetime NOT NULL after `comment_show`;
ALTER TABLE `Posts` ENGINE=`MyISAM` AUTO_INCREMENT=11003 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `Records` CHANGE COLUMN `spec_id` `spec_id` int(10) UNSIGNED DEFAULT NULL after `id`;
ALTER TABLE `Records` ENGINE=`MyISAM` AUTO_INCREMENT=30 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `Settings` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`online` tinyint(1) DEFAULT NULL,
	`translation_id` int(11) DEFAULT NULL,
    `agreement` longtext COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `Settings_92be99ab` USING BTREE (`translation_id`) comment '',
	CONSTRAINT `translation_id_refs_id_076e4838` FOREIGN KEY (`translation_id`) REFERENCES `medtus_translation` (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=4 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `south_migrationhistory` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`app_name` varchar(255) NOT NULL,
	`migration` varchar(255) NOT NULL,
	`applied` datetime NOT NULL,
	PRIMARY KEY (`id`)) ENGINE=`InnoDB` AUTO_INCREMENT=16 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `statistics` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`material_id` int(11) NOT NULL,
	`service_id` int(11) NOT NULL,
	`likes` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`viewings` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE `material` USING BTREE (`material_id`, `service_id`) comment '') ENGINE=`InnoDB` AUTO_INCREMENT=1256 COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
CREATE TABLE `thumbnail_kvstore` (
	`key` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`value` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	PRIMARY KEY (`key`)) ENGINE=`InnoDB` COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;
ALTER TABLE `Towns` ADD INDEX `Towns_9acd27ed` USING BTREE (`checked`) comment '';
ALTER TABLE `Towns` ADD INDEX `Towns_55a4ce96` USING BTREE (`region`) comment '';
ALTER TABLE `Towns` ADD INDEX `Towns_a65e5e94` USING BTREE (`country_id`) comment '';
ALTER TABLE `Towns` ADD INDEX `Towns_4da47e07` USING BTREE (`name`) comment '';
ALTER TABLE `Towns` ADD INDEX `Towns_country_id_6dbd696b` USING BTREE (`country_id`, `name`) comment '';

ALTER TABLE `Videos` ADD COLUMN `public_main` tinyint(1) NOT NULL DEFAULT 0 after `show_cmedu`;
ALTER TABLE `Videos` ADD COLUMN `comment_show` tinyint(1) NOT NULL DEFAULT 1 after `comment_cnt`;
ALTER TABLE `Videos` ENGINE=`MyISAM` AUTO_INCREMENT=1034 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ROW_FORMAT=DYNAMIC COMMENT='' CHECKSUM=0 DELAY_KEY_WRITE=0;

ALTER TABLE `oExtraFields` ADD INDEX `objet_id__name` (`object_id`, `name`) comment '';
ALTER TABLE `sExtraFields` ADD INDEX `objet_id__name` (`object_id`, `name`) comment '';
ALTER TABLE `iExtraFields` ADD INDEX `objet_id__name` (`object_id`, `name`) comment '';
ALTER TABLE `dExtraFields` ADD INDEX `objet_id__name` (`object_id`, `name`) comment '';

TRUNCATE `account_myuser`;
TRUNCATE `circle_circle`;
TRUNCATE `circle_dialog`;
TRUNCATE `circle_record`;

INSERT IGNORE INTO `account_myuser`
	 (`id`, `avatar`, `createdate`, `email`, `firstname`,  `lastname`,  `lastaccess`,
	  `lastvisit`,  `login`, `pass`, `spec_id`,   `status`,  `surname`, `updatedate`,`user_ptr_id`,
	  `organization`,`job`,`site`,`phone_number`,`ICQ_Skype`,`experience`, `school`, `town`, `dissertation`,
	  `country`, `graduate_year`, `birthday`, `is_staff`,`is_active`,`is_admin`, `graduate_id`,
	  `category_id`
	)
SELECT u.id, u.avatar, u.createdate, u.email, u.firstname, u.lastname, u.lastaccess, 
	   u.lastvisit, u.login, u.pass, u.spec_id, u.`status`, u.surname, u.updatedate, u.user_ptr_id,
	   o.`value`, o1.`value`, o2.`value`, s1.`value`, s2.`value`, s3.`value`, s4.`value`, IF(i0.`value` = 0, NULL, i0.`value`), s6.`value`,
	   IF(i1.`value` = 0, NULL, i1.`value`), i2.`value`, d1.`value`, 0, 1, 0, IF(i3.`value` = 0, NULL, i3.`value`),
	   1
FROM Users u
left join oExtraFields o ON o.object_id = u.id and o.`name` = 'job_comp'
left join oExtraFields o1 ON o1.object_id = u.id and o1.`name` = 'job_title'
left join oExtraFields o2 ON o2.object_id = u.id and o2.`name` = 'job_site'

left join sExtraFields s1 ON s1.object_id = u.id and s1.name = 'phone'
left join sExtraFields s2 ON s2.object_id = u.id and s2.name = 'icq'
left join sExtraFields s3 ON s3.object_id = u.id and s3.name = 'experience'
left join sExtraFields s4 ON s4.object_id = u.id and s4.name = 'vuz'
-- left join sExtraFields s5 ON s5.object_id = u.id and s5.name = 'city'
-- left join Towns t ON s5.`value` = t.`name`
left join sExtraFields s6 ON s6.object_id = u.id and s6.name = 'diser_theme'

left join iExtraFields i0 ON i0.object_id = u.id and i0.name = 'town'
left join iExtraFields i1 ON i1.object_id = u.id and i1.name = 'country'
left join iExtraFields i2 ON i2.object_id = u.id and i2.name = 'vuz_finish_year'
left join iExtraFields i3 ON i3.object_id = u.id and i3.name = 'grade'

left join dExtraFields d1 ON d1.object_id = u.id and d1.name = 'birthday'
;


UPDATE account_myuser u
left join iExtraFields i0 ON i0.object_id = u.id and i0.name = 'town'
left join iExtraFields i1 ON i1.object_id = u.id and i1.name = 'country'
SET u.town = i0.`value`, u.country = i1.`value`;

INSERT IGNORE INTO library_school(`name`)
SELECT s1.`value` FROM sExtraFields s1
WHERE s1.`name` = 'vuz'
GROUP BY s1.`value`;
-- select * from Users where login = 'intentia@mail.ru';
-- select * from account_myuser where email = 'intentia@mail.ru';
-- select * from medtusdj_db.account_myuser where email = 'intentia@mail.ru';
-- select distinct(name) from dExtraFields;
-- select * from iExtraFields where name = 'grade';

-- friends
INSERT INTO circle_circle(`activated`, `createdate`, `parent_id`, `friend_id`)
SELECT 1, f.createdate, f.from_id, f.to_id FROM Frends f
;

INSERT INTO `account_aword` VALUES ('92', 'достижения есть', '24851'), ('153', 'достижение всей жизни №1', '40896'), ('162', 'супер доктор', '70976'), ('163', '  ', '70976'), ('164', '   ', '70976'), ('165', 'супер медсестра', '70976');
INSERT INTO `account_category` VALUES ('1', 'Нет категории'), ('2', 'Высшая категория'), ('3', 'Первая категория'), ('4', 'Вторая категория');

update `account_myuser` set `is_admin`='1', `is_staff` = '1', `is_active` = '1', `is_superuser` = '1' 
where `email` IN (
'zds_1@mail.ru',
'medtusovka.movies@mail.ru',
'aryabov2004@inbox.ru',
'ryabovm_08@mail.ru',
'mike.sutulov@gmail.com',
'vrvm.promo@gmail.com',
'vrvm.kam@inbox.ru',
'vrvm.event@inbox.ru',
'aryabov2004@list.ru'
);

update `django_site` set `name`='vrvm.ru', `domain`='vrvm.ru' where `id`='1';

ALTER TABLE `django_admin_log` DROP FOREIGN KEY `content_type_id_refs_id_93d2d1f8`;
DROP TABLE django_content_type;
ALTER TABLE `django_admin_log` ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

DROP TABLE auth_permission;
CREATE TABLE django_content_type LIKE medtusdj_db.django_content_type;
CREATE TABLE auth_permission LIKE medtusdj_db.auth_permission;
INSERT INTO django_content_type SELECT * FROM medtusdj_db.django_content_type;
INSERT INTO auth_permission SELECT * FROM medtusdj_db.auth_permission;

-- Messages 
ALTER TABLE `circle_dialog` ADD UNIQUE `dialog unique` (`authA_id`, `authB_id`) comment '';

INSERT IGNORE INTO circle_dialog(AuthA_id, AuthB_id, createdate)
SELECT IF(m.from_user_id < m.to_user_id, m.from_user_id, m.to_user_id),
	IF(m.to_user_id > m.from_user_id,m.to_user_id,m.from_user_id), 
m.createdate FROM Messages as m
GROUP BY m.from_user_id, m.to_user_id
order by m.id ASC
;

INSERT INTO circle_record(auth_id, createdate, dialog_id, `value`, viewed) 
SELECT m.from_user_id, m.createdate, IFNULL(d.id, d1.id), m.content, IF(m.isread = 1, m.createdate, NULL) FROM Messages m
left join circle_dialog d ON m.from_user_id = d.authA_id AND m.to_user_id = d.authB_id
left join circle_dialog d1 ON m.from_user_id = d1.authB_id AND m.to_user_id = d1.authA_id
;

DROP TABLE IF EXISTS `account_passtoken`;
CREATE TABLE `account_passtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `user_id` int(10) NOT NULL,
  `token` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `medtus_translation`;
CREATE TABLE `medtus_translation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `medtus_feedback`;
CREATE TABLE `medtus_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `topic` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `contact` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `answered` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

UPDATE Videos v
SET v.image = CONCAT('/media/old_video_img/',v.image);

SET FOREIGN_KEY_CHECKS = 1;