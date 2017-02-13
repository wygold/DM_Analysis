select 
isnull(PS.PS_NAME, ' ') as PS_NAME,' | ',
isnull(convert(VARCHAR(10),PS_STEP),' ') as PS_STEP,' | ',
isnull(TBL.BATCH_NAME,' ') as BATCH_NAME ,' | ',
isnull(BAT1.EXECUTION_TIME, ' ') as LAST_EXECUTION_TIME,' | ',
isnull(convert(VARCHAR(10),BAT1.EXECUTION_DATE), ' ') as LAST_EXECUTION_DATE,' | ',
isnull(BAT1.BAT_USER, ' ') as USER_EXECUTED,' | ',
isnull(TBL.COMPUTING_DATES,' ') as GFILTER_DATES,' | ',
isnull(TBL.FILTER,' ') as "GLOBAL_FILTER",' | ',
isnull(TBL.FILTER_EXP1,' ') as "GLOBAL_FILTER_EXP1",' | ',
isnull(TBL.FILTER_EXP2,' ') as "GLOBAL_FILTER_EXP2" ,' | ',
isnull(TBL.HISTORISATION, ' ') as "HISTORISATION",' | ',
isnull(TBL.M_SERIALIZED,' ') as "COMPUTED BY SEVERAL BATCHES",' | ',
isnull(convert(VARCHAR(10),TBL.SCANNER_ENGINES), ' ') as "SCANNER_ENGINES",' | ',
isnull(TBL.DATA_TYPE,' ') as DATA_TYPE,' | ',
isnull(TBL.LABEL_OF_DATA,' ') as LABEL_OF_DATA,' | ',
isnull(TBL.FEEDER,' ') as "SINGLE OBJECTS",' | ',
isnull(BAT2.EXECUTION_TIME,' ') as LAST_EXECUTION_TIME_SOBJ,' | ',
isnull(convert(VARCHAR(10),BAT2.EXECUTION_DATE), ' ') as LAST_EXECUTION_DATE2,' | ',
isnull(BAT2.BAT_USER, ' ') as USER_EXECUTED2,' | ',
isnull(DN.INDEXES,' ') as "INDEXES",' | ',
isnull(DM_SQL1,' ') as "SQL QUERY1",' | ',
isnull(DM_SQL2,' ') as "SQL QUERY2",' | ',
isnull(DM_SQL3,' ') as "SQL QUERY3",' | ',
isnull(TBL.M_UNIT,' ') as "OBJECT_TYPES",' | ',
DN.DM_TABLE_NAME,' | ',
DN.FLDSCNT,' | ',
isnull(DN.DYN_TBL_NAME,' ') as "DYNAMIC_TABLE",' | ',
case when isnull(M_TYPE,4)=0 then 'Murex'
when isnull(M_TYPE,4)=1 then 'Murex Additional'
when isnull(M_TYPE,4)=2 then 'User'
when isnull(M_TYPE,4)=3 then 'User Additional'
else ''
end as "DYNAMIC_TABLE_CATEGORY",' | ',
case when 	ISNULL(convert(VARCHAR(10),DN.TYPE,3),'1') ='1'	then	'SQL'
when	DN.TYPE = 	0	then	DN.CLSTYPE
when	DN.TYPE = 	1	then	'Accounting'
when	DN.TYPE = 	2	then	'Copy Creation'
when	DN.TYPE = 	6	then	'Accounting (Reporting)'
when	DN.TYPE = 	3	then	'External'
when	DN.TYPE = 	4	then	'Payments'
when	DN.TYPE = 	5	then	'Definition report'
when	DN.TYPE = 	6	then	'Accounting report'
when	DN.TYPE = 	7	then	'Cash balances'
when	DN.TYPE = 	8	then	'Simulation'
when	DN.TYPE = 	9	then	'PL VAR'
when	DN.TYPE = 	11	then	'Data Dictionary (Market Data Loader)'
when	DN.TYPE = 	16	then	'Deliverable Cash'
when	DN.TYPE = 	17	then	'Deliverable nostro cash'
when	DN.TYPE = 	19	then	'Trade version audit'
when	DN.TYPE = 	20	then	'Navigation templates'
when	DN.TYPE = 	31	then	'Liquidation Positions'
when	DN.TYPE = 	32	then	'Classification tree'
when	DN.TYPE = 	46	then	'Corporate actions static data'
when	DN.TYPE = 	47	then	'Hedge'
when	DN.TYPE = 	50	then	'MLC'
when	DN.TYPE = 	21	then	 'Collateral'
when	DN.TYPE = 	41	then	 'MRA'
when	DN.TYPE = 	55	then	 'Interest'
when	DN.TYPE = 	34	then	 'VAR data source'
when	M_CLASS_TYPE = 	34	 then 	 'VAR'
when	M_CLASS_TYPE = 	51	 then 	 'Collateral Exchange'
when	M_CLASS_TYPE = 	55	 then 	 'Collateral Interest'
else	isnull(convert(VARCHAR(10),DN.TYPE,3),' ') end as DYN_TYPE,	 ' | ',
isnull(convert(VARCHAR(10),DN.FIELDS_COUNT,3),' ') as DYN_FIELDS_COUNT,' | ',
isnull(convert(VARCHAR(10),DN.TOTAL_HFIELDS_COUNT,3),' ') as TOTAL_HORIZONTAL_FIELDS,' | ',
isnull(convert(VARCHAR(10),DN.HFIELDS_DBFCOUNT,3),' ') as DB_HORIZONTAL_FIELDS,' | ',
DN.DISABLECOMPUTE_FLAG,' | ',
DN.DYNBUILT,' | ',
isnull(rtrim(
case when 	M_DT_TYPE0	 = 	0	then	'NS'
when	M_DT_TYPE0	 = 	1	then	'Contextual Today'
when	M_DT_TYPE0	 = 	2	then	'Contextual Yesterday'
when	M_DT_TYPE0	 = 	7	then	' User Defined Date'
when	M_DT_TYPE0	 = 	19	then	 'Date Shifter'
when	M_DT_TYPE0	 = 	23	then	 'Reporting Date'
when	M_DT_TYPE0	 = 	24	then	 'Reporting Shifter Date' 
else	convert(varchar(20), M_DT_TYPE0,3) end),'   ')||' '||M_DT_SHIFT0 as "DYN_FILTER_DATE0", ' | ',
isnull(rtrim(
case when 	M_DT_TYPE1	 = 	0	then	'NS'
when	M_DT_TYPE1	 = 	1	then	'Contextual Today'
when	M_DT_TYPE1	 = 	2	then	'Contextual Yesterday'
when	M_DT_TYPE1	 = 	7	then	' User Defined Date'
when	M_DT_TYPE1	 = 	19	then	 'Date Shifter'
when	M_DT_TYPE1	 = 	23	then	 'Reporting Date'
when	M_DT_TYPE1	 = 	24	then	 'Reporting Shifter Date' 
else	convert(varchar(20), M_DT_TYPE1,3) end),'   ')||' '||M_DT_SHIFT1 as "DYN_FILTER_DATE1",' | ',
isnull(rtrim(
case when 	M_DT_TYPE2	 = 	0	then	'NS'
when	M_DT_TYPE2	 = 	1	then	'Contextual Today'
when	M_DT_TYPE2	 = 	2	then	'Contextual Yesterday'
when	M_DT_TYPE2	 = 	7	then	' User Defined Date'
when	M_DT_TYPE2	 = 	19	then	 'Date Shifter'
when	M_DT_TYPE2	 = 	23	then	 'Reporting Date'
when	M_DT_TYPE2	 = 	24	then	 'Reporting Shifter Date' 
else	convert(varchar(20), M_DT_TYPE2,3) end),'   ')||' '||M_DT_SHIFT2 as "DYN_FILTER_DATE2" ,' | ',
isnull(DYN_FILTER4,' ') as DYN_PREFILTER1, ' | ',
isnull(DYN_FILTER1,' ') as DYN_PREFILTER2, ' | ',
isnull(DYN_FILTER2,' ') as DYN_PREFILTER3, ' | ',
isnull(TYPOLOGY_FILTER,' ') as DYN_TYPOLOGY, ' | ',
isnull(DYN_FILTER3,' ') as DYN_POSTFILTER, ' | ',
isnull(VIEWER_NAME,' ') as VIEWER_NAME, ' | ',
TBL.FEEDER_DESC as FEEDER_DESC, ' | ',
TBL.BATCH_DESC as BATCH_DESC, ' | ',
TBL.M_FILTER_LABEL, ' | ',
PS_BATCH_FDR_ENTITY, ' | ',
TBL.SCANNER_ENGINE_SIZE AS SCANNER_ENGINE_SIZE, ' | ',
TBL.SCANNER_ENGINE_TYPE AS SCANNER_ENGINE_TYPE, ' | ', 
TBL.SCANNER_ENGINE_NAME AS SCANNER_ENGINE_NAME, ' | ',
TBL.SCANNER_ENGINES_RETRY_TIME AS SCANNER_ENGINES_RETRY_TIME, ' | ',
TBL.SCANNER_RETRIES_THRESHOLD AS SCANNER_RETRIES_THRESHOLD
from
/*This Query lists the Datamart tables, underlying Dynamic tables (with types and filters), SQL, Indexes*/
(
        select 
        rtrim(A.M_LABEL) as "DM_TABLE_NAME", 
        DYN.M_TYPE, DYN.M_DYN_TABLE as "DYN_TBL_NAME", 
        DYN.M_CLASS_TYPE as "TYPE", 
        DYN.M_CLASS as "CLSTYPE", 
        DYN.M_VIEW as "VIEWER_NAME",
        B.COLUMNS_COUNT as "FLDSCNT", 
        str_replace(M_FLDNAME,CHAR(10),' ') as "DYN_FILTER4",
        str_replace(M_FORMULA1,CHAR(10),' ') as "DYN_FILTER1",
        str_replace(M_FORMULA2,CHAR(10),' ') as "DYN_FILTER2", 
        str_replace(M_FORMULA3,CHAR(10),' ') as "DYN_FILTER3",
        FIELDS_COUNT,
        DYNHF.TOTAL_HFIELDS as "TOTAL_HFIELDS_COUNT", 
        DYNHF1.OCCURANCE as "HFIELDS_DBFCOUNT",
        DMSQL.DM_SQL1,
        DMSQL.DM_SQL2,
        DMSQL.DM_SQL3 ,
        TYPO.TYPOLOGY_FILTER,
        DM_IND.INDEXES,
        M_DT_TYPE0, 
        M_DT_TYPE1,
        M_DT_TYPE2,
        M_DT_SHIFT0,
        M_DT_SHIFT1,
        M_DT_SHIFT2,
		case when	M_F_SELPFL	=	0	then 'Detailed DBF'
             when	M_F_SELPFL	=	1 then	'Consolidated DBF'
             when	M_F_SELPFL	=	2	then 'Stored Results'
             else	isnull(convert(VARCHAR(10),M_F_SELPFL),' ') end  as "DYNBUILT",
        case when M_F_CMPNO = 0 then 'N'
             when M_F_CMPNO = 1 then 'Y'
             else isnull(convert(VARCHAR(10),M_F_CMPNO), ' ') end as "DISABLECOMPUTE_FLAG"
        from  RPO_DMSETUP_TABLE_DBF A 
        inner join
        /*Lists the number of columns or fields in each Datamart table*/
        (
            select 
            M_RPO_DMSETUP_TABLE_REF ,
            count(*) "COLUMNS_COUNT" 
            from RPO_DMSETUP_COLUMN_DBF 
            group by M_RPO_DMSETUP_TABLE_REF
        ) B on A.M_REFERENCE=B.M_RPO_DMSETUP_TABLE_REF
        left outer join
        /*Retrives the Query of the SQL based Datamart Table*/
        (
            select 
            M_REFERENCE,
            rtrim(upper(str_replace(str_replace(str_replace(substring(convert(binary(16384),M_REQUEST),1,2000), CHAR(9), ' '), CHAR(10), ' '), CHAR(13), ' ')))||
            rtrim(upper(str_replace(str_replace(str_replace(substring(convert(binary(16384),M_REQUEST),2001,2000), CHAR(9), ' '), CHAR(10), ' '), CHAR(13), ' '))) as DM_SQL1,
            rtrim(upper(str_replace(str_replace(str_replace(substring(convert(binary(16384),M_REQUEST),4001,2000), CHAR(9), ' '), CHAR(10), ' '), CHAR(13), ' ')))||
            rtrim(upper(str_replace(str_replace(str_replace(substring(convert(binary(16384),M_REQUEST),6001,2000), CHAR(9), ' '), CHAR(10), ' '), CHAR(13), ' '))) as DM_SQL2,
            rtrim(upper(str_replace(str_replace(str_replace(substring(convert(binary(16384),M_REQUEST),8001,2000), CHAR(9), ' '), CHAR(10), ' '), CHAR(13), ' '))) as DM_SQL3 
            from RPO_DMSETUP_SQL_TABLE_DBF
        ) DMSQL on A.M_REFERENCE=DMSQL.M_REFERENCE
        left outer join
        /*Lists the underlying dynamic table , type Datamart table*/
        (
            select 
            M_DYN_TABLE,
            M_REFERENCE,
            D1.M_CLASS_TYPE,
            D1.M_CLASS,
            D1.M_TYPO_REF,
            M_DT_TYPE0, 
            M_DT_TYPE1,
            M_DT_TYPE2,
            M_DT_SHIFT0,
            M_DT_SHIFT1,
            M_DT_SHIFT2, 
            DYNFLD.FIELDS_COUNT,
			M_F_SELPFL,
            M_F_CMPNO,			
            D1.M_TYPE,
            M_VIEW
            from RPO_DMSETUP_DYN_TABLE_DBF C1 inner join
            (
                select 
				M_CREATION,
				M_CLASS_TYPE,
				M_CLASS,
				M_TYPO_REF,
				M_DT_TYPE0, 
				M_DT_TYPE1,
				M_DT_TYPE2,
				M_DT_SHIFT0,
				M_DT_SHIFT1,
				M_DT_SHIFT2,
				M_F_SELPFL,
                M_F_CMPNO,
                M_VIEW,
                0 as M_TYPE
				from DYNDBF1#TRN_DYND_DBF 
				union  
				select 
				M_CREATION,
				M_CLASS_TYPE,
				M_CLASS,
				M_TYPO_REF,
				M_DT_TYPE0,
				M_DT_TYPE1,
				M_DT_TYPE2,
				M_DT_SHIFT0,
				M_DT_SHIFT1,
				M_DT_SHIFT2,
				M_F_SELPFL,
                M_F_CMPNO,
                M_VIEW,
                2 as M_TYPE  
				from DYNDBF2#TRN_DYND_DBF 
                union  
                select 
				M_CREATION,
				M_CLASS_TYPE,
				M_CLASS,
				M_TYPO_REF,
				M_DT_TYPE0, 
				M_DT_TYPE1,
				M_DT_TYPE2,
				M_DT_SHIFT0,
				M_DT_SHIFT1,
				M_DT_SHIFT2,
				M_F_SELPFL,
                M_F_CMPNO,
                M_VIEW,
                1 as M_TYPE  
				from DYNDBF3#TRN_DYND_DBF 
                union 
                select 
				M_CREATION,
				M_CLASS_TYPE,
				M_CLASS,
				M_TYPO_REF,
				M_DT_TYPE0, 
				M_DT_TYPE1,
				M_DT_TYPE2,
				M_DT_SHIFT0,
				M_DT_SHIFT1,
				M_DT_SHIFT2,
				M_F_SELPFL,
                M_F_CMPNO,
                M_VIEW,
                3 AS M_TYPE
				from DYNDBF4#TRN_DYND_DBF
            ) D1 on C1.M_DYN_TABLE = D1.M_CREATION 
                AND C1.M_DYN_TABLE_DIR_TYPE = D1.M_TYPE --group by M_DYN_TABLE
            inner join 
                (
                select 
                M_CREATION, 
                count(*) as "FIELDS_COUNT",
                0 as M_TYPE
                from DYNDBF1#TRN_DYNF_DBF 
                group by  M_CREATION 
                union
                select 
                M_CREATION, 
                count(*) as "FIELDS_COUNT",
                2 as M_TYPE 
                from DYNDBF2#TRN_DYNF_DBF 
                group by  M_CREATION 
                union
                select 
                M_CREATION, 
                count(*) as "FIELDS_COUNT" ,
                1 as M_TYPE
                from DYNDBF3#TRN_DYNF_DBF 
                group by  M_CREATION 
                union
                select 
                M_CREATION, 
                count(*) as "FIELDS_COUNT",
                3 as M_TYPE 
                from DYNDBF4#TRN_DYNF_DBF 
                group by  M_CREATION 
            )DYNFLD
            on D1.M_CREATION= DYNFLD.M_CREATION
            AND D1.M_TYPE = DYNFLD.M_TYPE
        )DYN on B.M_RPO_DMSETUP_TABLE_REF=DYN.M_REFERENCE
        left outer join
        /*Lists the filter conditions and expressions for each dynamic table */
        (
            select 
			M_CREATION "DYN_TBL_NAME", 
            0 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 1) as M_FORMULA1 
			from   DYNDBF1#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
            MUREXDB.FormulaList(M_CREATION, 2) as M_FORMULA1
			from   DYNDBF2#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            1 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 3) as M_FORMULA1 
			from   DYNDBF3#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            3 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 4) as M_FORMULA1 
			from   DYNDBF4#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
        )DYNE0 on DYN.M_DYN_TABLE=DYNE0.DYN_TBL_NAME
            AND DYN.M_TYPE=DYNE0.M_TYPE
        left outer join
        (
            select M_CREATION "DYN_TBL_NAME",
            0 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 1) as M_FORMULA2 
			from   DYNDBF1#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 2) as M_FORMULA2 
			from   DYNDBF2#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
            union
            select M_CREATION "DYN_TBL_NAME", 
            1 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 3) as M_FORMULA2 
			from   DYNDBF3#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            3 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 4) as M_FORMULA2 
			from   DYNDBF4#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
        )DYNE1 on DYN.M_DYN_TABLE= DYNE1.DYN_TBL_NAME
        AND DYN.M_TYPE=DYNE1.M_TYPE
        left outer join
        (
            select 
			M_CREATION "DYN_TBL_NAME",
            0 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 1) as M_FORMULA3 
			from   DYNDBF1#TRN_DYNO_DBF  
			where M_USAGE =2 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 2) as M_FORMULA3 
			from   DYNDBF2#TRN_DYNO_DBF  
			where M_USAGE =2 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME", 
            1 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 3) as M_FORMULA3 
			from   DYNDBF3#TRN_DYNO_DBF 
			where M_USAGE =2 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME", 
            3 as M_TYPE,
			MUREXDB.FormulaList(M_CREATION, 4) as M_FORMULA3 
			from   DYNDBF4#TRN_DYNO_DBF  
			where M_USAGE =2 
			group by M_CREATION
        )DYNE2 on DYN.M_DYN_TABLE= DYNE2.DYN_TBL_NAME
        AND DYN.M_TYPE=DYNE2.M_TYPE
        left outer join
        ( 
            select 
			M_VALUE "DYN_TBL_NAME",
            0 as M_TYPE,
			MUREXDB.FldNameList(M_VALUE, 1)  as M_FLDNAME 
			from   DYNDBF1#TRN_DYNC_DBF   
			group by M_VALUE
            union
            select 
			M_VALUE "DYN_TBL_NAME",
            2 as M_TYPE,
			MUREXDB.FldNameList(M_VALUE, 2) as M_FLDNAME 
			from   DYNDBF2#TRN_DYNC_DBF   
			group by M_VALUE
            union
            select 
			M_VALUE "DYN_TBL_NAME",
            1 as M_TYPE,
			MUREXDB.FldNameList(M_VALUE, 3) as M_FLDNAME 
			from   DYNDBF3#TRN_DYNC_DBF   
			group by M_VALUE
            union
            select 
			M_VALUE "DYN_TBL_NAME",
            3 as M_TYPE,
			MUREXDB.FldNameList(M_VALUE, 4) as M_FLDNAME 
			from   DYNDBF4#TRN_DYNC_DBF   
			group by M_VALUE
        )DYNF on DYN.M_DYN_TABLE= DYNF.DYN_TBL_NAME
        AND DYN.M_TYPE=DYNF.M_TYPE
        left outer join
        (
            select 
			CREQ.M_REFERENCE, 
			MUREXDB.TypoLabelList(CREQ.M_REFERENCE) as "TYPOLOGY_FILTER" 
			from CSF_REQUEST_DBF CREQ,TYPOLOGY_DBF TYPO  
            where TYPO.M_REFERENCE=CREQ.M_NODE_REF 
			group by CREQ.M_REFERENCE
        ) TYPO on DYN.M_TYPO_REF=TYPO.M_REFERENCE
        left outer join
        /*Lists the number of horizontal fields for each dynamic table */
        (
            select 
			M_CREATION "DYN_TBL_NAME",
            0 as M_TYPE,
			count(*) "TOTAL_HFIELDS"
            from DYNDBF1#TRN_DYNU_DBF 
			group by M_CREATION
            union all
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
			count(*) "TOTAL_HFIELDS"
            from DYNDBF2#TRN_DYNU_DBF 
			group by M_CREATION
            union all
            select 
			M_CREATION "DYN_TBL_NAME",
            1 as M_TYPE,
			count(*) "TOTAL_HFIELDS"
            from DYNDBF3#TRN_DYNU_DBF 
			group by M_CREATION
            union all
            select 
			M_CREATION "DYN_TBL_NAME",
            3 as M_TYPE,
			count(*) "TOTAL_HFIELDS"
            from DYNDBF4#TRN_DYNU_DBF 
			group by M_CREATION
        ) DYNHF on DYN.M_DYN_TABLE = DYNHF.DYN_TBL_NAME
            AND DYN.M_TYPE=DYNHF.M_TYPE
        left outer join
        /*Lists the number of instances of DB related parser functions (*TBLFIELD ,*TABLE) used in horizontal fields for each dynamic table */
        (
            select M_CREATION "DYN_TBL_NAME",
            M_TYPE,
			(SUM(OCCURANCE)+SUM(OCCURANCE1)) "OCCURANCE" 
			from
            (
                select 
				M_CREATION,
                0 as M_TYPE,
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TBLFIELD','')))/8 "OCCURANCE",
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TABLE(','')))/6 "OCCURANCE1"
                from DYNDBF1#TRN_DYNU_DBF 
                union ALL
                select 
				M_CREATION,
                2 as M_TYPE,
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TBLFIELD','')))/8 "OCCURANCE",
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TABLE(','')))/6 "OCCURANCE1"
                from DYNDBF2#TRN_DYNU_DBF 
                union ALL
                select 
				M_CREATION,
                1 as M_TYPE,
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TBLFIELD','')))/8 "OCCURANCE",
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TABLE(','')))/6 "OCCURANCE1"
                from DYNDBF3#TRN_DYNU_DBF 
                union ALL
                select 
				M_CREATION,
                3 as M_TYPE,
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TBLFIELD','')))/8 "OCCURANCE",
				(len(M_DUP_DEF0)-len(str_replace(M_DUP_DEF0,'TABLE(','')))/6 "OCCURANCE1"
                from DYNDBF4#TRN_DYNU_DBF 
            ) AAA group by M_CREATION,M_TYPE
        ) DYNHF1 on DYN.M_DYN_TABLE=DYNHF1.DYN_TBL_NAME 
         AND DYN.M_TYPE=DYNHF1.M_TYPE

        left outer join
        /*Lists the names and columns of the indexes defined on the Datamart tables from Murex*/
        (
            select 
			M_RPO_DMSETUP_TABLE_REF,
			MUREXDB.IndexList(M_RPO_DMSETUP_TABLE_REF) "INDEXES"
            from  RPO_DMSETUP_COLUMN_DBF T1 ,RPO_DMSETUP_COLUMN_INDEX_DBF T2 
            where T1. M_REFERENCE = T2. M_RPO_DMSETUP_COLUMN_REF  
            group by M_RPO_DMSETUP_TABLE_REF
        ) DM_IND on A.M_REFERENCE= DM_IND.M_RPO_DMSETUP_TABLE_REF

        where A.M_TYPE in (0,4) 
       -- and A.M_MUREX=0 
       ) DN 

        left outer join
        /* Query to fetch the list of  Batches with the underlying single objects along with the Global Filter conditions used in case of Batches 
        Since there is an outer join this also lists the single objects that are not attached to any Batches may be used for Intraday Reports */
        (
            select
            rtrim(A.M_LABEL) as "BATCH_NAME",
            rtrim(A.M_DESC) as "BATCH_DESC",
            case when (BT.M_EXECTX) = 5 then 'FEEDERS'
                 when (BT.M_EXECTX) = 7 then 'EXTRACTIONS'
                 when (BT.M_EXECTX) = 8 then 'PROCEDURES' end  as "M_UNIT",
            A.M_TAGDATA as "LABEL_OF_DATA", 
            A.M_DATACOMP,
            case when A.M_DATASHARED ='Y' then 'DATA PUBLISHED'
                 when  A.M_DATASHARED ='N' then 'PRIVATE'
                 else A.M_DATASHARED end as "DATA_TYPE",
            A.M_SERIALIZED,
            case when A.M_SCNTMPL = 0 then 'N' else 'Y' end as M_SCNTMPL,
            isnull(SCR.M_TEMPLATE,'') as SCANNER_ENGINE_NAME,
            isnull(SCR.M_PROCESS_NB, 0) as SCANNER_ENGINES,
            case when isnull(SCR.M_BATCH_SIZE,-1) = -1 then 0 
                 when isnull(SCR.M_BATCH_SIZE,-1)=2000000000  then 0  
                 when isnull(SCR.M_BATCH_SIZE,-1)=0 then M_THRESHOLD
                 else M_BATCH_SIZE end as SCANNER_ENGINE_SIZE,
            case when isnull(SCR.M_BATCH_SIZE,-1) = -1 then ''
                 when isnull(SCR.M_BATCH_SIZE,-1) = 0 then 'By Threshold'
                 when isnull(SCR.M_BATCH_SIZE,-1) = 2000000000 then 'By positions in one batch' 
                 else 'By Size' end as SCANNER_ENGINE_TYPE,
            case when isnull(SCR.M_RETRIES_BATCH_SIZE,-1) = -1 then 0
                 when isnull(SCR.M_RETRIES_BATCH_SIZE,-1) =  2000000000 then 0 
                 else M_RETRIES_BATCH_SIZE end as SCANNER_ENGINES_RETRY_TIME,
            case when isnull(SCR.M_RETRIES_THRESHOLD,-1)= -1 then 0 else M_RETRIES_THRESHOLD end as SCANNER_RETRIES_THRESHOLD,
            case when  A.M_DATAHIS = 0 then 'ONE DATA SET'
                 when A.M_DATAHIS = 1 then 'ONE DATA SET PER DAY'
                 when A.M_DATAHIS = 2 then 'ONE DATA SET PER RUN' 
                 else convert(varchar(20),A.M_DATAHIS) end as "HISTORISATION",
            rtrim(BT.M_LABEL) as "FEEDER",
            rtrim(BT.M_DESC) as "FEEDER_DESC",
            rtrim(TBL.M_OUTPUT) as "DM_TABLE_NAME",
            ECF.M_CH_VALUE as "FILTER",
            EDF1.M_EXP_VAL as "FILTER_EXP1" ,
            EDF2.M_EXP_VAL as "FILTER_EXP2",
            DF.M_FILTER_REF,
            DF.M_LABEL AS M_FILTER_LABEL,
            GFT_DT.COMPUTING_DATES
            from 
                ACT_BAT_DBF BT 
                left outer join ACT_SETREP_DBF CT on BT.M_REF= CT.M_REFBAT 
                left outer join ACT_DYN_DBF TBL on BT.M_REF = TBL.M_REF
                left outer join ACT_SET_DBF A on CT.M_REFSET =A.M_REF 
                left outer join SCANNERCFG_DBF SCR on A.M_SCNTMPL = SCR.M_REFERENCE 
                left outer join
                (
                    select 
                    M_LABEL,
                    M_FILTER_REF 
                    from DAPFILTER_DBF 
                    where rtrim(M_LABEL) IS NOT NULL
                ) DF on A.M_FLTTEMP = DF.M_LABEL
                left outer join 
                (
                    select 
                    M_FILTER_REF, 
                    str_replace(MUREXDB.ExpValList(M_FILTER_REF),CHAR(10),' ') as M_EXP_VAL 
                    from   DAPFLT_EXP_DBF  
                    where M_EXP_TYPE =1 
                    group by M_FILTER_REF
                )EDF1 on DF.M_FILTER_REF = EDF1.M_FILTER_REF
                left outer join
                (
                    select 
                    M_FILTER_REF, 
                    str_replace(MUREXDB.ExpValList(M_FILTER_REF),CHAR(10),' ') as M_EXP_VAL 
                    from   DAPFLT_EXP_DBF  
                    where M_EXP_TYPE =2 group by M_FILTER_REF 
                ) EDF2 on DF.M_FILTER_REF = EDF2.M_FILTER_REF
                left outer join
                (
                select 
                M_FILTER_REF, 
                MUREXDB.ChValueList(M_FILTER_REF) as M_CH_VALUE 
                from   DAPFLT_CH_DBF  
                where M_CH_VALUE IS NOT NULL group by M_FILTER_REF
                ) ECF  on DF.M_FILTER_REF =ECF.M_FILTER_REF
                left outer join
                (
                select 
                DAT0.M_FILTER_REF, 
                  (case when 	DAT0.M_TYPE	 = 	0	then	'NS'
                        when	DAT0.M_TYPE	 = 	1	then	'Contextual Today'
                        when	DAT0.M_TYPE	 = 	2	then	'Contextual Yesterday'
                        when	DAT0.M_TYPE	 = 	7	then	' User Defined Date'
                        when	DAT0.M_TYPE	 = 	19	then	 'Date Shifter'
                        when	DAT0.M_TYPE	 = 	23	then	 'Reporting Date'
                        when	DAT0.M_TYPE	 = 	24	then	 'Reporting Shifter Date' 
                        else	convert(varchar(20),DAT0.M_TYPE) end)||' '||rtrim(DAT0.M_SHIFTER)||','||
                  (case when 	DAT1.M_TYPE	 = 	0	then	'NS'
                        when	DAT1.M_TYPE	 = 	1	then	'Contextual Today'
                        when	DAT1.M_TYPE	 = 	2	then	'Contextual Yesterday'
                        when	DAT1.M_TYPE	 = 	7	then	' User Defined Date'
                        when	DAT1.M_TYPE	 = 	19	then	 'Date Shifter'
                        when	DAT1.M_TYPE	 = 	23	then	 'Reporting Date'
                        when	DAT1.M_TYPE	 = 	24	then	 'Reporting Shifter Date' 
                        else	convert(varchar(20),DAT1.M_TYPE) end)||' '||rtrim(DAT1.M_SHIFTER)||','||
                  (case when 	DAT2.M_TYPE	 = 	0	then	'NS'
                        when	DAT2.M_TYPE	 = 	1	then	'Contextual Today'
                        when	DAT2.M_TYPE	 = 	2	then	'Contextual Yesterday'
                        when	DAT2.M_TYPE	 = 	7	then	' User Defined Date'
                        when	DAT2.M_TYPE	 = 	19	then	 'Date Shifter'
                        when	DAT2.M_TYPE	 = 	23	then	 'Reporting Date'
                        when	DAT2.M_TYPE	 = 	24	then	 'Reporting Shifter Date' 
                        else	convert(varchar(20),DAT2.M_TYPE) end)||' '||rtrim(DAT2.M_SHIFTER) AS "COMPUTING_DATES"
                from DAPFLT_DAT_DBF DAT0, DAPFLT_DAT_DBF DAT1, DAPFLT_DAT_DBF DAT2
                 WHERE DAT0.M_FILTER_REF=DAT1.M_FILTER_REF AND DAT0.M_FILTER_REF=DAT2.M_FILTER_REF 
                      AND DAT0.M_INDEX=0 AND  DAT1.M_INDEX=1 AND  DAT2.M_INDEX=2
                )
                GFT_DT on DF.M_FILTER_REF =GFT_DT.M_FILTER_REF
                where BT.M_EXECTX in (5,7,8)
        ) TBL on DN.DM_TABLE_NAME =TBL.DM_TABLE_NAME
        left outer join
        /* Query to fetch the list of Processing scripts with the underlying batches */
            (
                select T1.M_NAME as "PS_NAME",
                T2.M_ORDER as PS_STEP,
                rtrim(T2.M_PARAM_LAB2) as "BATCH_NAME", 
                case when rtrim(M_UNIT) = 'REP_BATCHES_FEED' then 'FEEDERS'
                     when rtrim(M_UNIT) = 'REP_BATCHES_EXT' then 'EXTRACTIONS'
                     when  rtrim(M_UNIT) = 'REP_BATCHES_PROC' then 'PROCEDURES' end as "M_UNIT",
                M_PARAM_LAB3 as "PS_BATCH_FDR_ENTITY"
                from PROCESS#PS_SCRPT_DBF T1, PROCESS#PS_ITEM_DBF T2 
                where T1.M_REF=T2.M_REF 
                and rtrim(M_UNIT) in ('REP_BATCHES_FEED','REP_BATCHES_EXT','REP_BATCHES_PROC') 
            )PS on TBL.BATCH_NAME = PS.BATCH_NAME


        left outer join
        /*Query lists the batches with the last execution time in minutes*/

        /*Query is used for Batches*/
        (
            select
			rtrim(JOB1.M_BATCH) "BATCH_NAME",
			JOB1.M_OWNER as "BAT_USER",
			convert(varchar(8), dateadd(SECOND, M_ENDTIME-M_TIME, '1970-01-01'), 108) "EXECUTION_TIME",
			M_DATE "EXECUTION_DATE"
			from ACT_JOB_DBF JOB1,
			(
				select 
				M_BATCH,
				M_OWNER,
				MAX(M_IDJOB) M_IDJOB 
				from ACT_JOB_DBF 
				where upper(M_STATUS) ='DONE' 
				group by M_BATCH,M_OWNER
			) JOB2
		where JOB1.M_IDJOB=JOB2.M_IDJOB 
		and M_CTX in ('BF','BE','BP') 
        ) BAT1 on TBL.BATCH_NAME= BAT1.BATCH_NAME
        left outer join
        /*Query is used for Single Objects */
        (
            select 
            rtrim(JOB1.M_BATCH) "BATCH_NAME",
            JOB1.M_OWNER as "BAT_USER",
            convert(varchar(8), dateadd(SECOND, M_ENDTIME-M_TIME, '1970-01-01'), 108) "EXECUTION_TIME",
            M_DATE "EXECUTION_DATE" 
            from ACT_JOB_DBF JOB1,
            (
                select 
                M_BATCH,
                M_OWNER,
                MAX(M_IDJOB) M_IDJOB 
                from ACT_JOB_DBF 
                where upper(M_STATUS) ='DONE' 
                group by M_BATCH,M_OWNER 
            ) JOB2
            where JOB1.M_IDJOB=JOB2.M_IDJOB 
            and M_CTX in ('F','E','P') 
        ) BAT2 on TBL.FEEDER=BAT2.BATCH_NAME
order by TBL.DM_TABLE_NAME
