CREATE TABLE IF NOT EXISTS "MEMBER" (
	"SSN" char(11) NOT NULL,
	"firstname" varchar NOT NULL,
	"lastname" varchar NOT NULL,
	"phoneno" varchar(10),
	"picture" varchar,
	"taxreturn" varchar,
	"address" text,
	PRIMARY KEY ("SSN")
);

CREATE TABLE IF NOT EXISTS "ACCOUNT" (
	"username" varchar NOT NULL,
	"password" varchar NOT NULL,
	"barcode" integer,
	"datecreated" date, 
	"SSN" char(11),
	PRIMARY KEY ("username", "barcode"),
	FOREIGN KEY ("SSN") REFERENCES "MEMBER" ("SSN")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "STUDENT" (
	"studentIDno" char(7) NOT NULL,
	"SSN" char(11) NOT NULL,
	"semester" integer,
	"dptname" varchar,
	PRIMARY KEY ("studentIDno", "SSN"),
	FOREIGN KEY ("SSN") REFERENCES "MEMBER" ("SSN")
             ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("dptname") REFERENCES "DEPARTMENT" ("dptname")
             ON UPDATE CASCADE
             ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "DEPARTMENT" (
	"dptname" varchar,
	PRIMARY KEY ("dptname")
);

CREATE TABLE IF NOT EXISTS "ALLERGEN" (
	"allergenID" integer,
	"allergen" text,
	PRIMARY KEY ("allergenID")
);

CREATE TABLE IF NOT EXISTS "IS_ALLERGIC" (
	"allergenID" integer,
	"SSN" char(11) NOT NULL,
	PRIMARY KEY ("allergenID", "SSN"),
	FOREIGN KEY ("allergenID") REFERENCES "ALLERGEN" ("allergenID")
             ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("SSN") REFERENCES "MEMBER" ("SSN")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "FOOD_ITEM" (
	"itemName" varchar,
	"locationID" integer NOT NULL,
	"itemCode" integer NOT NULL,
	PRIMARY KEY ("itemCode"),
	FOREIGN KEY ("locationID") REFERENCES "LOCATION" ("locationID")
			ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "FOOD_CATEGORY" (
	"categoryName" varchar, 
	PRIMARY KEY ("categoryName")
);

CREATE TABLE IF NOT EXISTS "BELONGS_CAT" (
	"categoryName" varchar,
	"itemCode" integer NOT NULL,
	PRIMARY KEY ("categoryName", "itemCode"),
	FOREIGN KEY ("categoryName") REFERENCES "FOOD_CATEGORY" ("categoryName")
             ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
             ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "INGREDIENTS" (
	"foodIngredient" varchar,
	"itemCode" integer NOT NULL,
	PRIMARY KEY ("foodIngredient", "itemCode"),
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
             ON UPDATE CASCADE
        	 ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "CONTAINS_AL" (
	"allergenID" integer,
	"itemCode" integer NOT NULL,
	PRIMARY KEY ("allergenID", "itemCode"),
	FOREIGN KEY ("allergenID") REFERENCES "ALLERGEN" ("allergenID")
             ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
             ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "SCHEDULE" (
	"scheduleID" integer,
	"locationID" integer NOT NULL,
	PRIMARY KEY ("scheduleID"),
	FOREIGN KEY ("locationID") REFERENCES "ESTIA" ("locationID")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "OFFERS_SCHEDULE" (
	"scheduleID" integer,
	"date" date NOT NULL,
	"meal" varchar NOT NULL,
	PRIMARY KEY ("scheduleID", "date"),
	FOREIGN KEY ("scheduleID") REFERENCES "SCHEDULE" ("scheduleID")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "INCLUDES_FOOD" (
	"scheduleID" integer,
	"itemCode" integer NOT NULL,
	FOREIGN KEY ("scheduleID") REFERENCES "SCHEDULE" ("scheduleID")
             ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
             ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "LOCATION" (
	"locationID" integer,
	PRIMARY KEY ("locationID")
);

CREATE TABLE IF NOT EXISTS "GENERAL" (
	"name" varchar,
	"type" varchar,
	"locationID" integer,
	PRIMARY KEY ("locationID"),
	FOREIGN KEY ("locationID") REFERENCES "LOCATION" ("locationID")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "ESTIA" (
	"campus" varchar,
	"locationID" integer,
	PRIMARY KEY ("locationID"), 
	FOREIGN KEY ("locationID") REFERENCES "LOCATION" ("locationID")
             ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "ENTERS" (
	"date" date,
	"time" datetime,
	"SSN" char(11) NOT NULL,
	"locationID" integer NOT NULL,
	PRIMARY KEY ("SSN", "locationID","date","time"),
	FOREIGN KEY ("SSN") REFERENCES "MEMBER" ("SSN")
             ON UPDATE CASCADE
             ON DELETE SET NULL,
	FOREIGN KEY ("locationID") REFERENCES "ESTIA" ("locationID")
             ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "REVIEWS" (
	"stars" varchar NOT NULL,
	"review" text,
	"SSN" char(11) NOT NULL,
	"itemCode" integer NOT NULL,
	"locationID" integer,
	"date" date,
	PRIMARY KEY ("SSN", "itemCode"), 
	FOREIGN KEY ("SSN") REFERENCES "MEMBER" ("SSN")
             ON UPDATE CASCADE
             ON DELETE SET NULL,
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
             ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("locationID") REFERENCES "LOCATION" ("locationID")
             ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "PURCHASES" (
	"date" date,
	"time" datetime, 
	"paid" float,
	"SSN" char(11) NOT NULL,
	"itemCode" integer NOT NULL,
	"locationID" integer,
	"transNo" varchar NOT NULL,
	PRIMARY KEY ("transNo"),
	FOREIGN KEY ("SSN") REFERENCES "MEMBER" ("SSN")
             ON UPDATE CASCADE
             ON DELETE SET NULL,
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
             ON UPDATE CASCADE
             ON DELETE SET NULL,
	FOREIGN KEY ("locationID") REFERENCES "GENERAL" ("locationID")
             ON UPDATE CASCADE
             ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "OFFERS_ITEM" (
	"locationID" integer,
	"itemCode" integer NOT NULL,
	"startDate" date,
	"endDate" date,
	"price" float,
	"mealtype" varchar,
	PRIMARY KEY ("startDate", "endDate","itemCode")
	FOREIGN KEY ("itemCode") REFERENCES "FOOD_ITEM" ("itemCode")
			 ON UPDATE CASCADE
             ON DELETE RESTRICT,
	FOREIGN KEY ("locationID") REFERENCES "GENERAL" ("locationID")
			 ON UPDATE CASCADE
             ON DELETE RESTRICT
);

CREATE INDEX review_search
ON REVIEWS("itemCode","locationID");

CREATE INDEX account_ssn
ON ACCOUNT("SSN");

CREATE INDEX inc_food
ON INCLUDES_FOOD("scheduleID");

CREATE INDEX fd_item
ON FOOD_ITEM("itemName","locationID");

CREATE INDEX purch_search
ON PURCHASES("itemCode","SSN","date");