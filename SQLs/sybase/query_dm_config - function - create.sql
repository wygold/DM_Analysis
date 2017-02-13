--Remember to create these functions before run the sql in the db
CREATE  FUNCTION FormulaList (@key varchar(30), @TableName integer)
RETURNS varchar(500)
AS
   DECLARE @value varchar(500)
   DECLARE @retun_value varchar(500)
   DECLARE list_curs cursor for
      select M_FORMULA from MUREXDB.DYNDBF1#TRN_DYNO_DBF  where M_CREATION=@key and 1=@TableName
      union all 
      select M_FORMULA from MUREXDB.DYNDBF2#TRN_DYNO_DBF  where M_CREATION=@key and 2=@TableName
      union all 
      select M_FORMULA from MUREXDB.DYNDBF3#TRN_DYNO_DBF  where M_CREATION=@key and 3=@TableName
      union all 
      select M_FORMULA from MUREXDB.DYNDBF4#TRN_DYNO_DBF  where M_CREATION=@key and 4=@TableName
      
    open list_curs

  while (1=1)
  begin
        fetch list_curs into @value
        
        if @@sqlstatus = 2
        begin
              break
        end
        set @retun_value=@retun_value+@value
  end

close list_curs
return @retun_value
GO


CREATE  FUNCTION FldNameList (@key varchar(30), @TableName integer)
RETURNS varchar(500)
AS
   DECLARE @value varchar(500)
   DECLARE @retun_value varchar(500)
   DECLARE list_curs cursor for
      select M_FLDNAME from MUREXDB.DYNDBF1#TRN_DYNC_DBF  where M_VALUE=@key and 1=@TableName
      union all 
      select M_FLDNAME from MUREXDB.DYNDBF2#TRN_DYNC_DBF  where M_VALUE=@key and 2=@TableName
      union all 
      select M_FLDNAME from MUREXDB.DYNDBF3#TRN_DYNC_DBF  where M_VALUE=@key and 3=@TableName
      union all 
      select M_FLDNAME from MUREXDB.DYNDBF4#TRN_DYNC_DBF  where M_VALUE=@key and 4=@TableName
      
    open list_curs
    set @retun_value = ''
  while (1=1)
  begin
        fetch list_curs into @value
        
        if @@sqlstatus = 2
        begin
              break
        end
        
        if @retun_value <> ''
        begin 
            set @retun_value=@retun_value+','+@value
        end 
        else
            begin 
            set @retun_value=@value
        end 

end

close list_curs
return @retun_value
GO


CREATE  FUNCTION IndexList (@key1 numeric(10,0))
RETURNS varchar(500)
AS
   DECLARE @value varchar(500)
   DECLARE @retun_value varchar(500)
   DECLARE list_curs cursor for
                select 
				rtrim(T2.M_LABEL)
                from RPO_DMSETUP_COLUMN_DBF T1 ,RPO_DMSETUP_COLUMN_INDEX_DBF T2
                where T1. M_REFERENCE = T2. M_RPO_DMSETUP_COLUMN_REF and T1.M_RPO_DMSETUP_TABLE_REF=@key1 
                group by T1.M_RPO_DMSETUP_TABLE_REF,T2.M_LABEL 

    open list_curs
    set @retun_value = ''
  while (1=1)
  begin
        fetch list_curs into @value
        
        if @@sqlstatus = 2
        begin
              break
        end
        
        if @retun_value <> ''
        begin 
            set @retun_value=@retun_value+','+@value
        end 
        else
            begin 
            set @retun_value=@value
        end 

end

close list_curs
return @retun_value
GO

CREATE  FUNCTION ExpValList (@key numeric(10,0))
RETURNS varchar(500)
AS
   DECLARE @value varchar(500)
   DECLARE @retun_value varchar(500)
   DECLARE list_curs cursor for
                select M_EXP_VAL from DAPFLT_EXP_DBF where M_FILTER_REF=@key 
    open list_curs
    set @retun_value = ''
  while (1=1)
  begin
        fetch list_curs into @value
        
        if @@sqlstatus = 2
        begin
              break
        end
        
        if @retun_value <> ''
        begin 
            set @retun_value=@retun_value+@value
        end 
        else
            begin 
            set @retun_value=@value
        end 

end

close list_curs
return @retun_value
GO


CREATE  FUNCTION TypoLabelList (@key numeric(10,0))
RETURNS varchar(500)
AS
   DECLARE @value varchar(500)
   DECLARE @retun_value varchar(500)
   DECLARE list_curs cursor for
         select rtrim(TYPO.M_LABEL) from CSF_REQUEST_DBF CREQ,TYPOLOGY_DBF TYPO where CREQ.M_REFERENCE=@key and TYPO.M_REFERENCE=CREQ.M_NODE_REF 
    open list_curs
    set @retun_value = ''
  while (1=1)
  begin
        fetch list_curs into @value
        
        if @@sqlstatus = 2
        begin
              break
        end
        
        if @retun_value <> ''
        begin 
            set @retun_value=@retun_value+','+@value
        end 
        else
            begin 
            set @retun_value=@value
        end 

end

close list_curs
return @retun_value
GO

CREATE  FUNCTION ChValueList (@key numeric(10,0))
RETURNS varchar(500)
AS
   DECLARE @value varchar(500)
   DECLARE @retun_value varchar(500)
   DECLARE list_curs cursor for
         select rtrim(M_CH_VALUE) from DAPFLT_CH_DBF where M_CH_VALUE IS NOT NULL and M_FILTER_REF=@key 
    open list_curs
    set @retun_value = ''
  while (1=1)
  begin
        fetch list_curs into @value
        
        if @@sqlstatus = 2
        begin
              break
        end
        
        if @retun_value <> ''
        begin 
            set @retun_value=@retun_value+','+@value
        end 
        else
            begin 
            set @retun_value=@value
        end 

end

close list_curs
return @retun_value
GO
