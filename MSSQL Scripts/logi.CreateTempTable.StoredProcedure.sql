USE [testgjh]
GO
/****** Object:  StoredProcedure [logi].[CreateTempTable]    Script Date: 23-8-2023 14:45:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [logi].[CreateTempTable] 
AS
BEGIN

--drop tijdelijke tabellen wanneer aanwezig
DROP TABLE IF EXISTS ##all_data;

--create tabel voor alle gegevens en gefilterde gegevens
CREATE TABLE ##all_data(
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Domain] [nvarchar](20) NULL,
	[ReportName] [nvarchar](100) NULL,
	[ServerName] [nvarchar](50) NULL,
	[PathName] [nvarchar](500) NULL,
	[DateCreated] [datetime] NULL,
	[DateModified] [datetime] NULL,
	[ModifiedBy] [nvarchar](20) NULL,
	[DatalayerID] [nvarchar](50) NULL,
	[ConnectionID] [nvarchar](50) NULL,
	[ServerConnection] [nvarchar](50) NULL,
	[Query] [nvarchar](max) NULL,
	[DataHash] [varchar](32) NULL,
	[Object] [nvarchar](50) NULL,
	[DateExtracted] [datetime] NULL
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

END

GO
