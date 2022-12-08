BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "cache_table" (
	"cache_key"	varchar(255) NOT NULL,
	"value"	text NOT NULL,
	"expires"	datetime NOT NULL,
	PRIMARY KEY("cache_key")
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag">=0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	bigint NOT NULL,
	"action_time"	datetime NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "user_euser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_euser_user_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"euser_id"	bigint NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("euser_id") REFERENCES "user_euser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_euser_groups" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"euser_id"	bigint NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("euser_id") REFERENCES "user_euser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_euser" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"username"	text NOT NULL,
	"account_id"	text NOT NULL,
	"student_id"	text NOT NULL,
	"tenant"	text NOT NULL,
	"school"	text NOT NULL,
	"school_id"	text NOT NULL,
	"middle_name"	text NOT NULL,
	"password_text"	text NOT NULL,
	"refresh_token"	text NOT NULL
);
INSERT INTO "cache_table" VALUES (':1:challenge_auth_code','gAWVDgAAAAAAAACMCjIwMTQxMzQxNjGULg==','9999-12-31 23:59:59');
INSERT INTO "cache_table" VALUES (':1:challenge_auth_code_date','gAWVIAAAAAAAAACMCGRhdGV0aW1llIwEZGF0ZZSTlEMEB+YMCJSFlFKULg==','9999-12-31 23:59:59');
INSERT INTO "django_session" VALUES ('q12yleziolb8ey5am1i7lrh396evfga0','e30:1p0SzD:nMbLrS5Vyh9z80OOQtklYtKc4wFhs7e0zVZ4ikrNdGI','2022-12-14 19:43:15.593790');
INSERT INTO "django_session" VALUES ('alxpztr8pw7019re9aph9cspy203qwtq','e30:1p0T1w:XLzuYq73wD_12CuE5OZ4N2vfHrOfsZ-TlJYdkgAOa_U','2022-12-14 19:46:04.160836');
INSERT INTO "django_session" VALUES ('qt0t7lmeszhuzq4dh882q4i4a8inrrmv','e30:1p0T3n:UNP7STaOGFKbvcQ9AmL3gdFrn65dbhrdU208lakcmlo','2022-12-14 19:47:59.496350');
INSERT INTO "django_session" VALUES ('96duapkbfmfl7qqzgmp9pdqvlcdusa2a','e30:1p0T6a:pDCYT4cbYLGg5F-IBiCVUuZMM9fFDDguMN8cppI0nUk','2022-12-14 19:50:52.041112');
INSERT INTO "django_session" VALUES ('i4ktc16lewizr7a0t3susupmep1o5yma','.eJxVijsKwzAMQO-iuQTZiq04Y6DnMP5IuBQyxMkUeve2kKEd3-eEmI69xaPLFh8VZjAMt1-ZU3nK-i19K8NFfbgvl_-bW-rtcyphJhwVRSdSW30Qi8ohOwmcmcSjp2Cw4ihOreVSMZmJ0Rnh4jy83jPbL6U:1p0TT5:ci_Gkl1sEP93sT7dbCHNcAXKKV2h6wyYxpQ7naTHLz0','2022-12-14 20:14:07.656227');
INSERT INTO "django_session" VALUES ('hx6xh8kgn2v4hkdavgvafyox7iprr5s8','e30:1p2Hdo:3nRlEDBJeILsuwS76kFOHxg22oq7IOpRXkB4bA23fqE','2022-12-19 20:00:40.527048');
INSERT INTO "django_session" VALUES ('74tuu0r64l70kf1bhg10ynw6ovs9asvj','.eJxVyrsKwzAMheF30VyC7fimjoU-h5ElGZdCh7iZSt-9CWRIx_Od_wOF1ncv69ClPASu4OBytkr81Nd-jIWnY43pfjv8L-40-laqaMIgiTPW2nLkxsoc1TPmeSNvo0EXlDDZGISSmury3MS2Znyw8P0BTwEw2g:1p2wPV:TSr9McCaH5p1jEY-ZMxrPPFNdJJ9mhjd4DKad8k6XKs','2022-12-21 15:32:37.566641');
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (21,6,'add_euser','Can add e user');
INSERT INTO "auth_permission" VALUES (22,6,'change_euser','Can change e user');
INSERT INTO "auth_permission" VALUES (23,6,'delete_euser','Can delete e user');
INSERT INTO "auth_permission" VALUES (24,6,'view_euser','Can view e user');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (5,'sessions','session');
INSERT INTO "django_content_type" VALUES (6,'user','euser');
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2022-11-30 18:46:47.757793');
INSERT INTO "django_migrations" VALUES (2,'admin','0001_initial','2022-11-30 18:46:47.771520');
INSERT INTO "django_migrations" VALUES (3,'admin','0002_logentry_remove_auto_add','2022-11-30 18:46:47.785293');
INSERT INTO "django_migrations" VALUES (4,'admin','0003_logentry_add_action_flag_choices','2022-11-30 18:46:47.794599');
INSERT INTO "django_migrations" VALUES (5,'contenttypes','0002_remove_content_type_name','2022-11-30 18:46:47.819287');
INSERT INTO "django_migrations" VALUES (6,'auth','0001_initial','2022-11-30 18:46:47.853100');
INSERT INTO "django_migrations" VALUES (7,'auth','0002_alter_permission_name_max_length','2022-11-30 18:46:47.868809');
INSERT INTO "django_migrations" VALUES (8,'auth','0003_alter_user_email_max_length','2022-11-30 18:46:47.879809');
INSERT INTO "django_migrations" VALUES (9,'auth','0004_alter_user_username_opts','2022-11-30 18:46:47.889499');
INSERT INTO "django_migrations" VALUES (10,'auth','0005_alter_user_last_login_null','2022-11-30 18:46:47.899122');
INSERT INTO "django_migrations" VALUES (11,'auth','0006_require_contenttypes_0002','2022-11-30 18:46:47.902645');
INSERT INTO "django_migrations" VALUES (12,'auth','0007_alter_validators_add_error_messages','2022-11-30 18:46:47.912384');
INSERT INTO "django_migrations" VALUES (13,'auth','0008_alter_user_username_max_length','2022-11-30 18:46:47.922158');
INSERT INTO "django_migrations" VALUES (14,'auth','0009_alter_user_last_name_max_length','2022-11-30 18:46:47.932171');
INSERT INTO "django_migrations" VALUES (15,'auth','0010_alter_group_name_max_length','2022-11-30 18:46:47.948046');
INSERT INTO "django_migrations" VALUES (16,'auth','0011_update_proxy_permissions','2022-11-30 18:46:47.962729');
INSERT INTO "django_migrations" VALUES (17,'auth','0012_alter_user_first_name_max_length','2022-11-30 18:46:47.972681');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2022-11-30 18:46:47.981851');
INSERT INTO "user_euser" VALUES (2,'pbkdf2_sha256$390000$lpL7XbQms1sJKxHHa4vIbB$95zxHwtK6zNlFVqyLtCQezg/PvbwEtXdejTiYIemCzM=','2022-12-07 15:32:37.558130',1,'Sjoerd','Vermeulen','22572@dewillem.nl',1,1,'2022-11-30 18:51:14.846833','22572','17326','24108','dewillem','CSG Willem van Oranje','d81b4ba47a2f49b79d2335eb3ee74426','','Sj03rd@WvO.sv','221208LGrJLVp8nMrUKgeyYKM3Kzg4rBS84-1m0zQ');
INSERT INTO "user_euser" VALUES (28,'pbkdf2_sha256$390000$jq5RUVsDwxItIw25nMc32k$CgYrmTAdK4GB28e67iMpSpJbvXzLrhTXfwHO+ZTvT+E=','2022-12-05 20:02:07.276530',0,'','','',0,1,'2022-12-05 20:02:04.812445','22538','','','dewillem','CSG Willem van Oranje','d81b4ba47a2f49b79d2335eb3ee74426','','goochelen.com','221205mcZffbpQ1AALT_6EZBGFf1igqfmbVwSizLE');
CREATE INDEX IF NOT EXISTS "cache_table_expires" ON "cache_table" (
	"expires"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "user_euser_user_permissions_permission_id_9fb6df8a" ON "user_euser_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "user_euser_user_permissions_euser_id_53a155a7" ON "user_euser_user_permissions" (
	"euser_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "user_euser_user_permissions_euser_id_permission_id_e1798cb4_uniq" ON "user_euser_user_permissions" (
	"euser_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "user_euser_groups_group_id_61afbfd2" ON "user_euser_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "user_euser_groups_euser_id_d499a68c" ON "user_euser_groups" (
	"euser_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "user_euser_groups_euser_id_group_id_fbc8ee3a_uniq" ON "user_euser_groups" (
	"euser_id",
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "user_euser_username_school_29a05377_uniq" ON "user_euser" (
	"username",
	"school"
);
COMMIT;
