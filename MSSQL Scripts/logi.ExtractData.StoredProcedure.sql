USE [testgjh]
GO
/****** Object:  StoredProcedure [logi].[ExtractData]    Script Date: 23-8-2023 14:45:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [logi].[ExtractData]
AS
BEGIN
TRUNCATE TABLE logi.temp_xml_data;

--vergelijk schema met cdwh
WITH TABELSCHEMA AS
(SELECT DISTINCT TABLE_NAME FROM [DWH.CDWH_FB].INFORMATION_SCHEMA.COLUMNS)
INSERT INTO logi.temp_xml_data (Domain, ReportName, ServerName, [PathName], DateCreated, DateModified, ModifiedBy, DatalayerID, ConnectionID, ServerConnection, Query, DataHash, Object, DateExtracted)
SELECT  Domain, ReportName, ServerName, [PathName], DateCreated, DateModified, ModifiedBy, DatalayerID, ConnectionID, ServerConnection, Query, DataHash, Object, DateExtracted
FROM ##all_data a
JOIN  TABELSCHEMA B ON a.[Object] =  b.TABLE_NAME COLLATE database_default;

--verwijderde rijen uit logi.xml_data
UPDATE xml
SET ValidTo = GETDATE()
FROM logi.xml_data xml
LEFT JOIN logi.temp_xml_data temp
ON xml.Domain = temp.Domain
    AND xml.ReportName = temp.ReportName
    AND xml.ServerName = temp.ServerName
    AND xml.PathName = temp.PathName
    AND xml.DataHash = temp.DataHash
WHERE temp.Domain IS NULL
    AND xml.ValidTo IS NULL;



--nieuwe rijen
INSERT INTO logi.xml_data (Domain, ReportName, ServerName, [PathName], DateCreated, DateModified, ModifiedBy, DatalayerID, ConnectionID, ServerConnection, Query, DataHash, Object, DateExtracted, ValidFrom)
SELECT new.Domain, new.ReportName, new.ServerName, new.[PathName], new.DateCreated, new.DateModified, new.ModifiedBy, new.DatalayerID, new.ConnectionID, new.ServerConnection, new.Query, new.DataHash, new.Object, new.DateExtracted, new.DateExtracted
FROM logi.temp_xml_data new
LEFT JOIN logi.xml_data old
	ON old.Domain = new.Domain 
	AND old.ReportName = new.ReportName 
	AND old.ServerName = new.ServerName 
	AND old.[PathName] = new.[PathName] 
	AND old.DatalayerID = new.DatalayerID 
	AND old.ConnectionID = new.ConnectionID
	AND old.ServerConnection = new.ServerConnection
WHERE old.Domain IS NULL;

--aangepaste hash waarden
INSERT INTO logi.xml_data (Domain, ReportName, ServerName, [PathName], DateCreated, DateModified, ModifiedBy, DatalayerID, ConnectionID, ServerConnection, Query, DataHash, [Object], DateExtracted, ValidFrom)
SELECT new.Domain, new.ReportName, new.ServerName, new.[PathName], new.DateCreated, new.DateModified, new.ModifiedBy, new.DatalayerID, new.ConnectionID, new.ServerConnection, new.Query, new.DataHash, new.[Object], new.DateExtracted, new.DateExtracted
FROM logi.temp_xml_data new
LEFT JOIN logi.xml_data old
ON new.Domain = old.Domain
  AND new.ReportName = old.ReportName
  AND new.ServerName = old.ServerName
  AND new.[PathName] = old.[PathName]
  AND old.DatalayerID = new.DatalayerID 
  AND old.ConnectionID = new.ConnectionID
  AND old.ServerConnection = new.ServerConnection
  AND old.DataHash = new.DataHash
WHERE old.Domain IS NULL;

UPDATE xml
SET ValidTo = GETDATE()
FROM logi.xml_data xml
LEFT JOIN logi.temp_xml_data temp
ON xml.Domain = temp.Domain
  AND xml.ReportName = temp.ReportName
  AND xml.ServerName = temp.ServerName
  AND xml.PathName = temp.PathName
  AND xml.DatalayerID = temp.DatalayerID 
  AND xml.ConnectionID = temp.ConnectionID
  AND xml.ServerConnection = temp.ServerConnection
  AND xml.DataHash = temp.DataHash
WHERE temp.Domain IS NULL
    AND xml.ValidTo IS NULL;

END




GO
