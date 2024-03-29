USE [testgjh]
GO
/****** Object:  StoredProcedure [logi].[ExtractDataInit]    Script Date: 23-8-2023 14:45:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [logi].[ExtractDataInit]
AS
BEGIN

TRUNCATE TABLE logi.temp_xml_data;

WITH TABELSCHEMA AS
(SELECT DISTINCT TABLE_NAME FROM [DWH.CDWH_FB].INFORMATION_SCHEMA.COLUMNS)
INSERT INTO logi.xml_data (Domain, ReportName, ServerName, [PathName], DateCreated, DateModified, ModifiedBy, DatalayerID, ConnectionID, ServerConnection, Query, DataHash, Object, DateExtracted, ValidFrom)
SELECT  Domain, ReportName, ServerName, [PathName], DateCreated, DateModified, ModifiedBy, DatalayerID, ConnectionID, ServerConnection, Query, DataHash, Object, DateExtracted, DateExtracted
FROM ##all_data a
JOIN  TABELSCHEMA B ON a.[Object] =  b.TABLE_NAME COLLATE database_default;
END




GO
