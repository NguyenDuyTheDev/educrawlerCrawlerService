CREATE TABLE IF NOT EXISTS public."Article"
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( CYCLE INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Domain" text COLLATE pg_catalog."default",
    "Url" text COLLATE pg_catalog."default",
    "FileName" text COLLATE pg_catalog."default",
    "Content" text COLLATE pg_catalog."default",
    "LastUpdate" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "CrawlStatus" text COLLATE pg_catalog."default",
    "Note" text COLLATE pg_catalog."default",
    "SpiderId" integer,
    "Title" text COLLATE pg_catalog."default",
    "FirstCrawlDate" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Article_pkey" PRIMARY KEY ("Id")
);

CREATE TABLE IF NOT EXISTS public."Spider"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Url" text COLLATE pg_catalog."default",
    "Status" text COLLATE pg_catalog."default" DEFAULT 'Available'::text,
    "CrawlStatus" text COLLATE pg_catalog."default" DEFAULT 'Not Running'::text,
    "LastRunDate" timestamp without time zone,
    "LastEndDate" timestamp without time zone,
    "RunTime" integer DEFAULT 0,
    "isBlocked" boolean DEFAULT false,
    "Delay" integer DEFAULT 2,
    "GraphDeep" integer DEFAULT 3,
    "MaxThread" integer DEFAULT 8,
    "CreatedByID" integer,
    "JobId" text COLLATE pg_catalog."default" DEFAULT ''::text,
    "IsAcademic" boolean DEFAULT false,
    CONSTRAINT "Spider_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."User"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Username" text COLLATE pg_catalog."default" NOT NULL,
    "Password" text COLLATE pg_catalog."default" NOT NULL,
    "OnlineStatus" boolean DEFAULT false,
    "LastAccess" timestamp without time zone,
    "AccountStatus" text COLLATE pg_catalog."default" DEFAULT 'Good'::text,
    "FullName" text COLLATE pg_catalog."default",
    "Phone" text COLLATE pg_catalog."default",
    "Mail" text COLLATE pg_catalog."default",
    "Role" text COLLATE pg_catalog."default" DEFAULT 'User'::text,
    "SystemLanguage" text COLLATE pg_catalog."default" DEFAULT 'Vietnamese'::text,
    "SystemMode" text COLLATE pg_catalog."default" DEFAULT 'Light'::text,
    CONSTRAINT "User_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."SpiderKeyword"
(
    "KeywordID" integer NOT NULL,
    "SpiderID" integer NOT NULL,
    CONSTRAINT "SpiderKeyword_pkey" PRIMARY KEY ("KeywordID", "SpiderID")
);

CREATE TABLE IF NOT EXISTS public."Keyword"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( CYCLE INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Name" character varying(30) COLLATE pg_catalog."default" NOT NULL,
    "TotalArticles" integer DEFAULT 0,
    "TotalWords" integer DEFAULT 0,
    CONSTRAINT "Keyword_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."ArticleKeyword"
(
    "KeywordID" integer NOT NULL,
    "ArticleID" integer NOT NULL,
    "TotalWords" integer DEFAULT 0,
    CONSTRAINT "ArticleKeyword_pkey" PRIMARY KEY ("KeywordID", "ArticleID")
);

CREATE TABLE IF NOT EXISTS public."PostprocessingArticleKeyword"
(
    "KeywordID" integer NOT NULL,
    "PostprocessingArticleID" integer NOT NULL,
    "TotalWords" integer DEFAULT 0,
    CONSTRAINT "PostprocessingArticleKeyword_pkey" PRIMARY KEY ("KeywordID", "PostprocessingArticleID")
);

CREATE TABLE IF NOT EXISTS public."PostprocessingArticle"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Title" text COLLATE pg_catalog."default",
    "Domain" text COLLATE pg_catalog."default",
    "Url" text COLLATE pg_catalog."default",
    "Content" text COLLATE pg_catalog."default",
    "LastUpdate" timestamp without time zone,
    CONSTRAINT "PostprocessingArticle_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."PostprocessingArticleFile"
(
    "PostprocessingArticleID" integer NOT NULL,
    "FileID" integer NOT NULL,
    CONSTRAINT "PostprocessingArticleFile_pkey" PRIMARY KEY ("PostprocessingArticleID", "FileID")
);

CREATE TABLE IF NOT EXISTS public."File"
(
    "ID" integer NOT NULL,
    "Name" text COLLATE pg_catalog."default",
    "Location" text COLLATE pg_catalog."default",
    "Type" text COLLATE pg_catalog."default",
    "Source" text COLLATE pg_catalog."default",
    CONSTRAINT "File_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."ArticleFile"
(
    "ArticleID" integer NOT NULL,
    "FileID" integer NOT NULL,
    CONSTRAINT "ArticleFile_pkey" PRIMARY KEY ("FileID", "ArticleID")
);

CREATE TABLE IF NOT EXISTS public."SpiderSupportedFileType"
(
    "SpiderID" integer NOT NULL,
    "FileTypeID" integer NOT NULL,
    CONSTRAINT "SpiderSupportedFileType_pkey" PRIMARY KEY ("SpiderID", "FileTypeID")
);

CREATE TABLE IF NOT EXISTS public."SupportedFileType"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Type" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "SupportedFileType_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."WebpageSpider"
(
    "ID" integer NOT NULL,
    CONSTRAINT "WebpageSpider_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."WebpageSpiderCrawlRules"
(
    "SpiderID" integer NOT NULL,
    "CrawlRulesID" integer NOT NULL,
    CONSTRAINT "WebpageSpiderCrawlRules_pkey" PRIMARY KEY ("SpiderID", "CrawlRulesID")
);

CREATE TABLE IF NOT EXISTS public."CrawlRules"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Tag" text COLLATE pg_catalog."default",
    "HTMLClassName" text COLLATE pg_catalog."default",
    "HTMLIDName" text COLLATE pg_catalog."default",
    "ChildCrawlRuleID" integer,
    CONSTRAINT "CrawlRules_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."SubfolderCrawlRules"
(
    "SubfolderID" integer NOT NULL,
    "CrawlRuleID" integer NOT NULL,
    "SpiderID" integer NOT NULL,
    CONSTRAINT "SubfolderCrawlRules_pkey" PRIMARY KEY ("SubfolderID", "CrawlRuleID")
);

CREATE TABLE IF NOT EXISTS public."WebsiteSpider"
(
    "ID" integer NOT NULL,
    "TotalPage" integer DEFAULT 0,
    "CrawlSuccess" integer DEFAULT 0,
    "CrawlFail" integer DEFAULT 0,
    CONSTRAINT "WebsiteSpider_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."Subfolder"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( CYCLE INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "SpiderID" integer NOT NULL,
    CONSTRAINT "Subfolder_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."SubfolderSearchRules"
(
    "SubfolderID" integer NOT NULL,
    "SearchRuleID" integer NOT NULL,
    "SpiderID" integer NOT NULL,
    CONSTRAINT "SubfolderSearchRules_pkey" PRIMARY KEY ("SubfolderID", "SearchRuleID")
);

CREATE TABLE IF NOT EXISTS public."CrawlHistory"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Url" text COLLATE pg_catalog."default",
    "CrawlStatus" text COLLATE pg_catalog."default" DEFAULT 'Good'::text,
    "RunDate" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "EndDate" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "RunTime" integer DEFAULT 0,
    "IsBlocked" boolean DEFAULT false,
    "SpiderID" integer,
    CONSTRAINT "CrawlHistory_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."WebsiteSpiderHistory"
(
    "ID" integer NOT NULL,
    "TotalPage" integer DEFAULT 0,
    "CrawlSuccess" integer DEFAULT 0,
    "CrawlFail" integer DEFAULT 0,
    CONSTRAINT "WebsiteSpiderHistory_pkey" PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Article"
    ADD CONSTRAINT "Article_SpiderId_fkey" FOREIGN KEY ("SpiderId")
    REFERENCES public."Spider" ("ID") MATCH SIMPLE
    ON UPDATE SET NULL
    ON DELETE SET NULL;


ALTER TABLE IF EXISTS public."Spider"
    ADD CONSTRAINT "Spider_CreatedByID_fkey" FOREIGN KEY ("CreatedByID")
    REFERENCES public."User" ("ID") MATCH SIMPLE
    ON UPDATE SET NULL
    ON DELETE SET NULL;


ALTER TABLE IF EXISTS public."SpiderKeyword"
    ADD CONSTRAINT "SpiderKeyword_KeywordID_fkey" FOREIGN KEY ("KeywordID")
    REFERENCES public."Keyword" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."SpiderKeyword"
    ADD CONSTRAINT "SpiderKeyword_SpiderID_fkey" FOREIGN KEY ("SpiderID")
    REFERENCES public."Spider" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."ArticleKeyword"
    ADD CONSTRAINT "ArticleKeyword_ArticleID_fkey" FOREIGN KEY ("ArticleID")
    REFERENCES public."Article" ("Id") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."ArticleKeyword"
    ADD CONSTRAINT "ArticleKeyword_KeywordID_fkey" FOREIGN KEY ("KeywordID")
    REFERENCES public."Keyword" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."PostprocessingArticleKeyword"
    ADD CONSTRAINT "PostprocessingArticleKeyword_KeywordID_fkey" FOREIGN KEY ("KeywordID")
    REFERENCES public."Keyword" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."PostprocessingArticleKeyword"
    ADD CONSTRAINT "PostprocessingArticleKeyword_PostprocessingArticleID_fkey" FOREIGN KEY ("PostprocessingArticleID")
    REFERENCES public."PostprocessingArticle" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."PostprocessingArticleFile"
    ADD CONSTRAINT "PostprocessingArticleFile_FileID_fkey" FOREIGN KEY ("FileID")
    REFERENCES public."File" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."PostprocessingArticleFile"
    ADD CONSTRAINT "PostprocessingArticleFile_PostprocessingArticleID_fkey" FOREIGN KEY ("PostprocessingArticleID")
    REFERENCES public."PostprocessingArticle" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."ArticleFile"
    ADD CONSTRAINT "ArticleFile_ArticleID_fkey" FOREIGN KEY ("ArticleID")
    REFERENCES public."Article" ("Id") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."ArticleFile"
    ADD CONSTRAINT "ArticleFile_FileID_fkey" FOREIGN KEY ("FileID")
    REFERENCES public."File" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."SpiderSupportedFileType"
    ADD CONSTRAINT "FileTypeIDpk" FOREIGN KEY ("FileTypeID")
    REFERENCES public."SupportedFileType" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."SpiderSupportedFileType"
    ADD CONSTRAINT "SpiderIDpk" FOREIGN KEY ("SpiderID")
    REFERENCES public."Spider" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."WebpageSpider"
    ADD CONSTRAINT "IDfk" FOREIGN KEY ("ID")
    REFERENCES public."Spider" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS "WebpageSpider_pkey"
    ON public."WebpageSpider"("ID");


ALTER TABLE IF EXISTS public."WebpageSpiderCrawlRules"
    ADD CONSTRAINT "CrawlRulesID_fk" FOREIGN KEY ("CrawlRulesID")
    REFERENCES public."CrawlRules" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."WebpageSpiderCrawlRules"
    ADD CONSTRAINT "SpiderID_fk" FOREIGN KEY ("SpiderID")
    REFERENCES public."WebpageSpider" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."CrawlRules"
    ADD CONSTRAINT "CrawlRules_ChildCrawlRuleID_fkey" FOREIGN KEY ("ChildCrawlRuleID")
    REFERENCES public."CrawlRules" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."SubfolderCrawlRules"
    ADD CONSTRAINT "SubfolderCrawlRules_CrawlRuleID_fkey" FOREIGN KEY ("CrawlRuleID")
    REFERENCES public."CrawlRules" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."SubfolderCrawlRules"
    ADD CONSTRAINT "SubfolderCrawlRules_SpiderID_fkey" FOREIGN KEY ("SpiderID")
    REFERENCES public."WebsiteSpider" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."SubfolderCrawlRules"
    ADD CONSTRAINT "SubfolderCrawlRules_SubfolderID_fkey" FOREIGN KEY ("SubfolderID")
    REFERENCES public."Subfolder" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."WebsiteSpider"
    ADD CONSTRAINT "IDfk" FOREIGN KEY ("ID")
    REFERENCES public."Spider" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS "WebsiteSpider_pkey"
    ON public."WebsiteSpider"("ID");


ALTER TABLE IF EXISTS public."Subfolder"
    ADD CONSTRAINT "Subfolder_SpiderID_fkey" FOREIGN KEY ("SpiderID")
    REFERENCES public."WebsiteSpider" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."SubfolderSearchRules"
    ADD CONSTRAINT "SubfolderSearchRules_SearchRuleID_fkey" FOREIGN KEY ("SearchRuleID")
    REFERENCES public."CrawlRules" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."SubfolderSearchRules"
    ADD CONSTRAINT "SubfolderSearchRules_SpiderID_fkey" FOREIGN KEY ("SpiderID")
    REFERENCES public."WebsiteSpider" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."SubfolderSearchRules"
    ADD CONSTRAINT "SubfolderSearchRules_SubfolderID_fkey" FOREIGN KEY ("SubfolderID")
    REFERENCES public."Subfolder" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."CrawlHistory"
    ADD CONSTRAINT "CrawlHistory_SpiderID_fkey" FOREIGN KEY ("SpiderID")
    REFERENCES public."Spider" ("ID") MATCH SIMPLE
    ON UPDATE SET NULL
    ON DELETE SET NULL;


ALTER TABLE IF EXISTS public."WebsiteSpiderHistory"
    ADD CONSTRAINT "WebsiteSpiderHistory_ID_fkey" FOREIGN KEY ("ID")
    REFERENCES public."CrawlHistory" ("ID") MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS "WebsiteSpiderHistory_pkey"
    ON public."WebsiteSpiderHistory"("ID");