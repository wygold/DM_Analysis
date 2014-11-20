select 
nvl(PS.PS_NAME, ' ') as PS_NAME,' | ',
nvl(to_char(PS_STEP),' ') as PS_STEP,' | ',
nvl(TBL.BATCH_NAME,' ') as BATCH_NAME ,' | ',
nvl(BAT1.EXECUTION_TIME, ' ') as LAST_EXECUTION_TIME,' | ',
nvl(to_char(BAT1.EXECUTION_DATE), ' ') as LAST_EXECUTION_DATE,' | ',
nvl(BAT1.BAT_USER, ' ') as USER_EXECUTED,' | ',
nvl(TBL.COMPUTING_DATES,' ') as GFILTER_DATES,' | ',
nvl(TBL.FILTER,' ') as "GLOBAL_FILTER",' | ',
nvl(TBL.FILTER_EXP1,' ') as "GLOBAL_FILTER_EXP1",' | ',
nvl(TBL.FILTER_EXP2,' ') as "GLOBAL_FILTER_EXP2" ,' | ',
nvl(TBL.HISTORISATION, ' ') as "HISTORISATION",' | ',
nvl(TBL.M_SERIALIZED,' ') as "COMPUTED BY SEVERAL BATCHES",' | ',
nvl(to_char(TBL.SCANNER_ENGINES), ' ') as "SCANNER_ENGINES",' | ',
nvl(TBL.DATA_TYPE,' ') as DATA_TYPE,' | ',
nvl(TBL.LABEL_OF_DATA,' ') as LABEL_OF_DATA,' | ',
nvl(TBL.FEEDER,' ') as "SINGLE OBJECTS",' | ',
nvl(BAT2.EXECUTION_TIME,' ') as LAST_EXECUTION_TIME_SOBJ,' | ',
nvl(to_char(BAT2.EXECUTION_DATE), ' ') as LAST_EXECUTION_DATE,' | ',
nvl(BAT2.BAT_USER, ' ') as USER_EXECUTED,' | ',
nvl(DN.INDEXES,' ') as "INDEXES",' | ',
nvl(DM_SQL1,' ') as "SQL QUERY1",' | ',
nvl(DM_SQL2,' ') as "SQL QUERY2",' | ',
nvl(DM_SQL3,' ') as "SQL QUERY3",' | ',
nvl(TBL.M_UNIT,' ') as "OBJECT_TYPES",' | ',
DN.DM_TABLE_NAME,' | ',
DN.FLDSCNT,' | ',
nvl(DN.DYN_TBL_NAME,' ') as "DYNAMIC_TABLE",' | ',
nvl(M_TYPE, 0) AS "DYNAMIC_TABLE_CATEGORY",' | ',
decode(DN.TYPE,NULL,'SQL',0,DN.CLSTYPE,1,'Accounting',2,'Copy Creation',6,'Accounting (Reporting)',3,'External',4,'Payments',5,'Definition report',6,'Accounting report',7,'Cash balances',8,'Simulation',9,'PL VAR',11,'Data Dictionary (Market Data Loader)',16,'Deliverable Cash',17,'Deliverable nostro cash',19,'Trade version audit',20,'Navigation templates', 31,'Liquidation Positions',32,'Classification tree',46,'Corporate actions static data',47,'Hedge',nvl(to_char(DN.TYPE), ' ')) as "DYN_TYPE", ' | ',
nvl(to_char(DN.FIELDS_COUNT),' ') as DYN_FIELDS_COUNT,' | ',
nvl(to_char(DN.TOTAL_HFIELDS_COUNT),' ') as TOTAL_HORIZONTAL_FIELDS,' | ',
nvl(to_char(DN.HFIELDS_DBFCOUNT),' ') as DB_HORIZONTAL_FIELDS,' | ',
DN.DISABLECOMPUTE_FLAG,' | ',
DN.DYNBUILT,' | ',
nvl(trim(decode(M_DT_TYPE0, 0 ,'NS',  1,'Contextual Today', 2,'Contextual Yesterday', 7,' User Defined Date', 19, 'Date Shifter', 23, 'Reporting Date', 24, 'Reporting Shifter Date',M_DT_TYPE0) ||' '||M_DT_SHIFT0),' ') as "DYN_FILTER_DATE0", ' | ',
nvl(trim(decode(M_DT_TYPE1, 0 ,'NS',  1,'Contextual Today', 2,'Contextual Yesterday', 7,' User Defined Date', 19, 'Date Shifter', 23, 'Reporting Date', 24, 'Reporting Shifter Date',M_DT_TYPE1) ||' '||M_DT_SHIFT1),' ') as "DYN_FILTER_DATE1",' | ',
nvl(trim(decode(M_DT_TYPE2, 0 ,'NS',  1,'Contextual Today', 2,'Contextual Yesterday', 7,' User Defined Date', 19, 'Date Shifter', 23, 'Reporting Date', 24, 'Reporting Shifter Date',M_DT_TYPE2) ||' '||M_DT_SHIFT2),' ') as "DYN_FILTER_DATE2" ,' | ',
nvl(DYN_FILTER4,' ') as DYN_PREFILTER1, ' | ',
nvl(DYN_FILTER1,' ') as DYN_PREFILTER2, ' | ',
nvl(DYN_FILTER2,' ') as DYN_PREFILTER3, ' | ',
nvl(TYPOLOGY_FILTER,' ') as DYN_TYPOLOGY, ' | ',
nvl(DYN_FILTER3,' ') as DYN_POSTFILTER, ' | ',
nvl(VIEWER_NAME,' ') as VIEWER_NAME
from
/*This Query lists the Datamart tables, underlying Dynamic tables (with types and filters), SQL, Indexes*/
(
        select 
        trim(A.M_LABEL) as "DM_TABLE_NAME", 
        DYN.M_TYPE, DYN.M_DYN_TABLE as "DYN_TBL_NAME", 
        DYN.M_CLASS_TYPE as "TYPE", 
        DYN.M_CLASS as "CLSTYPE", 
        DYN.M_VIEW as "VIEWER_NAME",
        B.COLUMNS_COUNT as "FLDSCNT", 
        replace(M_FLDNAME,CHR(10),' ') as "DYN_FILTER4",
        replace(M_FORMULA1,CHR(10),' ') as "DYN_FILTER1",
        replace(M_FORMULA2,CHR(10),' ') as "DYN_FILTER2", 
        replace(M_FORMULA3,CHR(10),' ') as "DYN_FILTER3",
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
		decode(M_F_SELPFL,0, 'Detailed DBF',1 ,'Consolidated DBF',2, 'Stored Results',nvl(to_char(M_F_SELPFL), ' ')) as "DYNBUILT",
        decode(M_F_CMPNO,0, 'N',1 ,'Y',nvl(to_char(M_F_CMPNO), ' ')) as "DISABLECOMPUTE_FLAG"
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
            trim(upper(replace(replace(replace(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.substr(M_REQUEST,2000,1)), CHR(9), ' '), CHR(10), ' '), CHR(13))))||
            trim(upper(replace(replace(replace(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.substr(M_REQUEST,2000,2001)), CHR(9), ' '), CHR(10), ' '), CHR(13)))) as DM_SQL1,
            trim(upper(replace(replace(replace(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.substr(M_REQUEST,2000,4001)), CHR(9), ' '), CHR(10), ' '), CHR(13))))||
            trim(upper(replace(replace(replace(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.substr(M_REQUEST,2000,6001)), CHR(9), ' '), CHR(10), ' '), CHR(13)))) as DM_SQL2,
            trim(upper(replace(replace(replace(UTL_RAW.CAST_TO_VARCHAR2(DBMS_LOB.substr(M_REQUEST,2000,8001)), CHR(9), ' '), CHR(10), ' '), CHR(13)))) as DM_SQL3 
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
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA1 
			from   DYNDBF1#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA1 
			from   DYNDBF2#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            1 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA1 
			from   DYNDBF3#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            3 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA1 
			from   DYNDBF4#TRN_DYNO_DBF  
			where M_USAGE =0 
			group by M_CREATION
        )DYNE0 on DYN.M_DYN_TABLE=DYNE0.DYN_TBL_NAME
            AND DYN.M_TYPE=DYNE0.M_TYPE
        left outer join
        (
            select M_CREATION "DYN_TBL_NAME",
            0 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA2 
			from   DYNDBF1#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA2 
			from   DYNDBF2#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
            union
            select M_CREATION "DYN_TBL_NAME", 
            1 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA2 
			from   DYNDBF3#TRN_DYNO_DBF  
			where M_USAGE =1 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            3 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA2 
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
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA3 
			from   DYNDBF1#TRN_DYNO_DBF  
			where M_USAGE =2 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME",
            2 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA3 
			from   DYNDBF2#TRN_DYNO_DBF  
			where M_USAGE =2 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME", 
            1 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA3 
			from   DYNDBF3#TRN_DYNO_DBF 
			where M_USAGE =2 
			group by M_CREATION
            union
            select 
			M_CREATION "DYN_TBL_NAME", 
            3 as M_TYPE,
			LISTAGG(M_FORMULA, '') WITHIN group (order by M_OFFSET) as M_FORMULA3 
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
			LISTAGG(trim(M_FLDNAME), ',') WITHIN group (order by M_FLDNAME) as M_FLDNAME 
			from   DYNDBF1#TRN_DYNC_DBF   
			group by M_VALUE
            union
            select 
			M_VALUE "DYN_TBL_NAME",
            2 as M_TYPE,
			LISTAGG(trim(M_FLDNAME), ',') WITHIN group (order by M_FLDNAME) as M_FLDNAME 
			from   DYNDBF2#TRN_DYNC_DBF   
			group by M_VALUE
            union
            select 
			M_VALUE "DYN_TBL_NAME",
            1 as M_TYPE,
			LISTAGG(trim(M_FLDNAME), ',') WITHIN group (order by M_FLDNAME) as M_FLDNAME 
			from   DYNDBF3#TRN_DYNC_DBF   
			group by M_VALUE
            union
            select 
			M_VALUE "DYN_TBL_NAME",
            3 as M_TYPE,
			LISTAGG(trim(M_FLDNAME), ',') WITHIN group (order by M_FLDNAME) as M_FLDNAME 
			from   DYNDBF4#TRN_DYNC_DBF   
			group by M_VALUE
        )DYNF on DYN.M_DYN_TABLE= DYNF.DYN_TBL_NAME
        AND DYN.M_TYPE=DYNF.M_TYPE
        left outer join
        (
            select 
			CREQ.M_REFERENCE, 
			LISTAGG(trim(TYPO.M_LABEL), ',') WITHIN group (order by TYPO.M_LABEL) as "TYPOLOGY_FILTER" 
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
				REGEXP_COUNT( M_DUP_DEF0, 'TBLFIELD') "OCCURANCE",
				REGEXP_COUNT( M_DUP_DEF0, 'TABLE{\(}') "OCCURANCE1"
                from DYNDBF1#TRN_DYNU_DBF 
                union ALL
                select 
				M_CREATION,
                2 as M_TYPE,
				REGEXP_COUNT( M_DUP_DEF0, 'TBLFIELD') "OCCURANCE",
				REGEXP_COUNT( M_DUP_DEF0, 'TABLE{\(}') "OCCURANCE1"
                from DYNDBF2#TRN_DYNU_DBF 
                union ALL
                select 
				M_CREATION,
                1 as M_TYPE,
				REGEXP_COUNT( M_DUP_DEF0, 'TBLFIELD') "OCCURANCE",
				REGEXP_COUNT( M_DUP_DEF0, 'TABLE{\(}') "OCCURANCE1"
                from DYNDBF3#TRN_DYNU_DBF 
                union ALL
                select 
				M_CREATION,
                3 as M_TYPE,
				REGEXP_COUNT( M_DUP_DEF0, 'TBLFIELD') "OCCURANCE",
				REGEXP_COUNT( M_DUP_DEF0, 'TABLE{\(}') "OCCURANCE1"
                from DYNDBF4#TRN_DYNU_DBF 
            )group by M_CREATION,M_TYPE
        ) DYNHF1 on DYN.M_DYN_TABLE=DYNHF1.DYN_TBL_NAME 
         AND DYN.M_TYPE=DYNHF1.M_TYPE

        left outer join
        /*Lists the names and columns of the indexes defined on the Datamart tables from Murex*/
        (
            select 
			M_RPO_DMSETUP_TABLE_REF,
			LISTAGG(trim(INDEXES), ',') WITHIN group (order by INDEXES) "INDEXES" 
			from
            (
                select 
				T1.M_RPO_DMSETUP_TABLE_REF,
				trim(T2.M_LABEL)||'('|| LISTAGG(trim(T1.M_LABEL), ',') WITHIN group (order by T1.M_LABEL)||')' "INDEXES" 
                from RPO_DMSETUP_COLUMN_DBF T1 ,RPO_DMSETUP_COLUMN_INDEX_DBF T2
                where T1. M_REFERENCE = T2. M_RPO_DMSETUP_COLUMN_REF 
                group by T1.M_RPO_DMSETUP_TABLE_REF,T2.M_LABEL
            ) group by M_RPO_DMSETUP_TABLE_REF
        ) DM_IND on A.M_REFERENCE= DM_IND.M_RPO_DMSETUP_TABLE_REF

        where A.M_TYPE in (0,4) 
       -- and A.M_MUREX=0 
       ) DN 

        left outer join
        /* Query to fetch the list of  Batches with the underlying single objects along with the Global Filter conditions used in case of Batches 
        Since there is an outer join this also lists the single objects that are not attached to any Batches may be used for Intraday Reports */
        (
            select
            trim(A.M_LABEL) as "BATCH_NAME",
            decode(trim(BT.M_EXECTX),'5','FEEDERS','7','EXTRACTIONS','8','PROCEDURES') as "M_UNIT", A.M_TAGDATA as "LABEL_OF_DATA",
            A.M_DATACOMP,
            decode(A.M_DATASHARED,'Y','DATA PUBLISHED','N','PRIVATE',A.M_DATASHARED) as "DATA_TYPE",
            A.M_SERIALIZED,
            decode( A.M_SCNTMPL,0,'N','Y')as M_SCNTMPL,
            nvl(SCR.M_PROCESS_NB, 0) as SCANNER_ENGINES,
            decode(A.M_DATAHIS,0,'ONE DATA SET',1,'ONE DATA SET PER DAY',2,'ONE DATA SET PER RUN',A.M_DATAHIS) as "HISTORISATION",
            trim(BT.M_LABEL) as "FEEDER",
            trim(TBL.M_OUTPUT) as "DM_TABLE_NAME",
            ECF.M_CH_VALUE as "FILTER",
            EDF1.M_EXP_VAL as "FILTER_EXP1" ,
            EDF2.M_EXP_VAL as "FILTER_EXP2",
            DF.M_FILTER_REF,
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
                    where trim(M_LABEL) IS NOT NULL
                ) DF on A.M_FLTTEMP = DF.M_LABEL
                left outer join 
                (
                    select 
                    M_FILTER_REF, 
                    replace(LISTAGG(M_EXP_VAL, '') WITHIN group (order by M_EXP_IND),CHR(10),' ') as M_EXP_VAL 
                    from   DAPFLT_EXP_DBF  
                    where M_EXP_TYPE =1 
                    group by M_FILTER_REF
                )EDF1 on DF.M_FILTER_REF = EDF1.M_FILTER_REF
                left outer join
                (
                    select 
                    M_FILTER_REF, 
                    replace(LISTAGG(M_EXP_VAL, '') WITHIN group (order by M_EXP_IND),CHR(10),' ') as M_EXP_VAL 
                    from   DAPFLT_EXP_DBF  
                    where M_EXP_TYPE =2 group by M_FILTER_REF 
                ) EDF2 on DF.M_FILTER_REF = EDF2.M_FILTER_REF
                left outer join
                (
                select 
                M_FILTER_REF, 
                LISTAGG(trim(M_CH_VALUE), ',') WITHIN group (order by M_CH_VALUE) as M_CH_VALUE 
                from   DAPFLT_CH_DBF  
                where M_CH_VALUE IS NOT NULL group by M_FILTER_REF
                ) ECF  on DF.M_FILTER_REF =ECF.M_FILTER_REF
                left outer join
                (
                select 
                M_FILTER_REF, 
                LISTAGG(decode(M_TYPE, 0 ,'NS',  1,'Contextual Today', 2,'Contextual Yesterday', 7,' User Defined Date', 19, 'Date Shifter', 23, 'Reporting Date', 24, 'Reporting Shifter Date',trim(M_TYPE))||' '||trim(M_SHIFTER),',')WITHIN group (order by M_INDEX) "COMPUTING_DATES"
                from DAPFLT_DAT_DBF 
                group by M_FILTER_REF 
                )
                GFT_DT on DF.M_FILTER_REF =GFT_DT.M_FILTER_REF
                where BT.M_EXECTX in ('5','7','8')
        ) TBL on DN.DM_TABLE_NAME =TBL.DM_TABLE_NAME
        left outer join
        /* Query to fetch the list of Processing scripts with the underlying batches */
            (
                select T1.M_NAME as "PS_NAME",
                T2.M_ORDER as PS_STEP,
                trim(T2.M_PARAM_LAB2) as "BATCH_NAME", 
                decode(trim(M_UNIT),'REP_BATCHES_FEED','FEEDERS','REP_BATCHES_EXT','EXTRACTIONS','REP_BATCHES_PROC','PROCEDURES') as "M_UNIT" 
                from PROCESS#PS_SCRPT_DBF T1, PROCESS#PS_ITEM_DBF T2 
                where T1.M_REF=T2.M_REF 
                and trim(M_UNIT) in ('REP_BATCHES_FEED','REP_BATCHES_EXT','REP_BATCHES_PROC') 
            )PS on TBL.BATCH_NAME = PS.BATCH_NAME


        left outer join
        /*Query lists the batches with the last execution time in minutes*/

        /*Query is used for Batches*/
        (
            select
			trim(JOB1.M_BATCH) "BATCH_NAME",
			JOB1.M_OWNER as "BAT_USER",
			extract (hour from NUMTODSINTERVAL(trunc((M_ENDTIME - M_TIME)/60,2), 'MINUTE')) ||' HRS:'||extract (minute from NUMTODSINTERVAL(trunc((M_ENDTIME - M_TIME)/60,2), 'MINUTE'))||' MINS :'||extract (second from NUMTODSINTERVAL(trunc((M_ENDTIME - M_TIME)/60,2), 'MINUTE'))||' SECS' "EXECUTION_TIME", 
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
            trim(JOB1.M_BATCH) "BATCH_NAME",
            JOB1.M_OWNER as "BAT_USER",
            extract (hour from NUMTODSINTERVAL(trunc((M_ENDTIME - M_TIME)/60,2), 'MINUTE')) ||' HRS:'||extract (minute from NUMTODSINTERVAL(trunc((M_ENDTIME - M_TIME)/60,2), 'MINUTE'))||' MINS :'||extract (second from NUMTODSINTERVAL(trunc((M_ENDTIME - M_TIME)/60,2), 'MINUTE'))||' SECS' "EXECUTION_TIME",
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