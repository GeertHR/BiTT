USE [testgjh]
GO
/****** Object:  StoredProcedure [logi].[InsertData]    Script Date: 23-8-2023 14:45:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [logi].[InsertData] @ReportName nvarchar(100), @Domain varchar(20), @PathName nvarchar(500),@ServerName nvarchar(50), @DateCreated DATETIME, @DateModified DATETIME, @ModifiedBy nvarchar(20), @Query nvarchar(max), @DataHash varchar(MAX), @DateExtracted DATETIME, @Object nvarchar(50), @DatalayerID nvarchar(50), @ConnectionID nvarchar(50), @ServerConnection nvarchar(50)
AS
BEGIN
INSERT INTO ##all_data (ReportName, Domain, PathName, ServerName, DateCreated, DateModified, ModifiedBy, Query, DataHash, DateExtracted, Object, DatalayerID, ConnectionID, ServerConnection) VALUES 
(@ReportName,@Domain,@PathName,@ServerName,@DateCreated, @DateModified, @ModifiedBy, @Query, CONVERT(VARCHAR(32), HashBytes('MD5', @DataHash), 2), @DateExtracted, @Object, @DatalayerID, CASE WHEN @ConnectionID IS NULL OR @ConnectionID = '' THEN '-LEEG-' ELSE @ConnectionID END, CASE WHEN @ServerConnection IS NULL OR @ServerConnection = '' THEN '-LEEG-' ELSE @ServerConnection END);






END


GO
