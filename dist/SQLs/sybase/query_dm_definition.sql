select T1.M_LABEL AS TABLE_FIELD, ' | ',
T1.M_MAX_LENGTH AS LENGTH, ' | ',
T1.M_DECIMAL AS DEC, ' | ',
CASE WHEN T1.M_TYPE = 78 THEN 'Numeric'
WHEN T1.M_TYPE = 84 THEN 'Timestamp'
WHEN T1.M_TYPE = 68 THEN 'Date'
WHEN T1.M_TYPE = 71 THEN 'Numeric'
WHEN T1.M_TYPE = 67 THEN 'Char'
WHEN T1.M_TYPE = 73 THEN 'Numeric'
WHEN T1.M_TYPE = 65 THEN 'American' end as FIELD_TYPE, ' | ',
T2.M_LABEL AS DM_TABLE_NAME, ' | ',
T3.M_DYN_TABLE AS DYN_TABLE_NAME, ' | ',
CASE WHEN T3.M_DYN_TABLE_DIR_TYPE=0 then 'Murex'
 WHEN T3.M_DYN_TABLE_DIR_TYPE=1 then 'Murex Additional'
 WHEN T3.M_DYN_TABLE_DIR_TYPE=2 then 'User'
 WHEN T3.M_DYN_TABLE_DIR_TYPE=3 then 'User Additional' end AS DYN_TABLE_CATEGORY, ' | ',
T4.DYN_TYPE
from RPO_DMSETUP_COLUMN_DBF T1, RPO_DMSETUP_TABLE_DBF T2, RPO_DMSETUP_DYN_TABLE_DBF T3,
(select 0 as M_TYPE ,  M_CREATION,
 case when	isnull(M_CLASS_TYPE,1) = 1 then 'SQL'			
when	M_CLASS_TYPE = 	0	 then 	 M_CLASS 
when	M_CLASS_TYPE = 	1	 then 	'Accounting'
when	M_CLASS_TYPE = 	2	 then 	'Copy Creation'
when	M_CLASS_TYPE = 	6	 then 	'Accounting (Reporting)'
when	M_CLASS_TYPE = 	3	 then 	'External'
when	M_CLASS_TYPE = 	4	 then 	'Payments'
when	M_CLASS_TYPE = 	5	 then 	'Definition report'
when	M_CLASS_TYPE = 	7	 then 	'Cash balances'
when	M_CLASS_TYPE = 	8	 then 	'Simulation'
when	M_CLASS_TYPE = 	9	 then 	'PL VAR'
when	M_CLASS_TYPE = 	11	 then 	'Data Dictionary (Market Data Loader)'
when	M_CLASS_TYPE = 	16	 then 	'Deliverable Cash'
when	M_CLASS_TYPE = 	17	 then 	'Deliverable nostro cash'
when	M_CLASS_TYPE = 	19	 then 	'Trade version audit'
when	M_CLASS_TYPE = 	20	 then 	'Navigation templates'
when	M_CLASS_TYPE = 	31	 then 	'Liquidation Positions'
when	M_CLASS_TYPE = 	32	 then 	'Classification tree'
when	M_CLASS_TYPE = 	46	 then 	'Corporate actions static data'
when	M_CLASS_TYPE = 	47	 then 	'Hedge'
when	M_CLASS_TYPE = 	50	 then 	'MLC'
when	M_CLASS_TYPE = 	21	 then 	 'Collateral'
when	M_CLASS_TYPE = 	41	 then 	 'MRA'
when	M_CLASS_TYPE = 	34	 then 	 'VAR'
when	M_CLASS_TYPE = 	51	 then 	 'Collateral Exchange'
when	M_CLASS_TYPE = 	55	 then 	 'Collateral Interest'
else	convert(varchar(20), M_CLASS_TYPE)	end as DYN_TYPE
from DYNDBF1#TRN_DYND_DBF 
union  
select 2 as M_TYPE  ,  M_CREATION,
case when	isnull(M_CLASS_TYPE,1) = 1 then 'SQL'			
when	M_CLASS_TYPE = 	0	 then 	 M_CLASS 
when	M_CLASS_TYPE = 	1	 then 	'Accounting'
when	M_CLASS_TYPE = 	2	 then 	'Copy Creation'
when	M_CLASS_TYPE = 	6	 then 	'Accounting (Reporting)'
when	M_CLASS_TYPE = 	3	 then 	'External'
when	M_CLASS_TYPE = 	4	 then 	'Payments'
when	M_CLASS_TYPE = 	5	 then 	'Definition report'
when	M_CLASS_TYPE = 	7	 then 	'Cash balances'
when	M_CLASS_TYPE = 	8	 then 	'Simulation'
when	M_CLASS_TYPE = 	9	 then 	'PL VAR'
when	M_CLASS_TYPE = 	11	 then 	'Data Dictionary (Market Data Loader)'
when	M_CLASS_TYPE = 	16	 then 	'Deliverable Cash'
when	M_CLASS_TYPE = 	17	 then 	'Deliverable nostro cash'
when	M_CLASS_TYPE = 	19	 then 	'Trade version audit'
when	M_CLASS_TYPE = 	20	 then 	'Navigation templates'
when	M_CLASS_TYPE = 	31	 then 	'Liquidation Positions'
when	M_CLASS_TYPE = 	32	 then 	'Classification tree'
when	M_CLASS_TYPE = 	46	 then 	'Corporate actions static data'
when	M_CLASS_TYPE = 	47	 then 	'Hedge'
when	M_CLASS_TYPE = 	50	 then 	'MLC'
when	M_CLASS_TYPE = 	21	 then 	 'Collateral'
when	M_CLASS_TYPE = 	41	 then 	 'MRA'
when	M_CLASS_TYPE = 	34	 then 	 'VAR'
when	M_CLASS_TYPE = 	51	 then 	 'Collateral Exchange'
when	M_CLASS_TYPE = 	55	 then 	 'Collateral Interest'
else	convert(varchar(20), M_CLASS_TYPE)	end as DYN_TYPE
from DYNDBF2#TRN_DYND_DBF 
union  
select 1 as M_TYPE  ,  M_CREATION,
case when	isnull(M_CLASS_TYPE,1) = 1 then 'SQL'			
when	M_CLASS_TYPE = 	0	 then 	 M_CLASS 
when	M_CLASS_TYPE = 	1	 then 	'Accounting'
when	M_CLASS_TYPE = 	2	 then 	'Copy Creation'
when	M_CLASS_TYPE = 	6	 then 	'Accounting (Reporting)'
when	M_CLASS_TYPE = 	3	 then 	'External'
when	M_CLASS_TYPE = 	4	 then 	'Payments'
when	M_CLASS_TYPE = 	5	 then 	'Definition report'
when	M_CLASS_TYPE = 	7	 then 	'Cash balances'
when	M_CLASS_TYPE = 	8	 then 	'Simulation'
when	M_CLASS_TYPE = 	9	 then 	'PL VAR'
when	M_CLASS_TYPE = 	11	 then 	'Data Dictionary (Market Data Loader)'
when	M_CLASS_TYPE = 	16	 then 	'Deliverable Cash'
when	M_CLASS_TYPE = 	17	 then 	'Deliverable nostro cash'
when	M_CLASS_TYPE = 	19	 then 	'Trade version audit'
when	M_CLASS_TYPE = 	20	 then 	'Navigation templates'
when	M_CLASS_TYPE = 	31	 then 	'Liquidation Positions'
when	M_CLASS_TYPE = 	32	 then 	'Classification tree'
when	M_CLASS_TYPE = 	46	 then 	'Corporate actions static data'
when	M_CLASS_TYPE = 	47	 then 	'Hedge'
when	M_CLASS_TYPE = 	50	 then 	'MLC'
when	M_CLASS_TYPE = 	21	 then 	 'Collateral'
when	M_CLASS_TYPE = 	41	 then 	 'MRA'
when	M_CLASS_TYPE = 	34	 then 	 'VAR'
when	M_CLASS_TYPE = 	51	 then 	 'Collateral Exchange'
when	M_CLASS_TYPE = 	55	 then 	 'Collateral Interest'
else	convert(varchar(20), M_CLASS_TYPE)	end as DYN_TYPE
from DYNDBF3#TRN_DYND_DBF 
union 
select 3 AS M_TYPE,  M_CREATION,
case when	isnull(M_CLASS_TYPE,1) = 1 then 'SQL'			
when	M_CLASS_TYPE = 	0	 then 	 M_CLASS 
when	M_CLASS_TYPE = 	1	 then 	'Accounting'
when	M_CLASS_TYPE = 	2	 then 	'Copy Creation'
when	M_CLASS_TYPE = 	6	 then 	'Accounting (Reporting)'
when	M_CLASS_TYPE = 	3	 then 	'External'
when	M_CLASS_TYPE = 	4	 then 	'Payments'
when	M_CLASS_TYPE = 	5	 then 	'Definition report'
when	M_CLASS_TYPE = 	7	 then 	'Cash balances'
when	M_CLASS_TYPE = 	8	 then 	'Simulation'
when	M_CLASS_TYPE = 	9	 then 	'PL VAR'
when	M_CLASS_TYPE = 	11	 then 	'Data Dictionary (Market Data Loader)'
when	M_CLASS_TYPE = 	16	 then 	'Deliverable Cash'
when	M_CLASS_TYPE = 	17	 then 	'Deliverable nostro cash'
when	M_CLASS_TYPE = 	19	 then 	'Trade version audit'
when	M_CLASS_TYPE = 	20	 then 	'Navigation templates'
when	M_CLASS_TYPE = 	31	 then 	'Liquidation Positions'
when	M_CLASS_TYPE = 	32	 then 	'Classification tree'
when	M_CLASS_TYPE = 	46	 then 	'Corporate actions static data'
when	M_CLASS_TYPE = 	47	 then 	'Hedge'
when	M_CLASS_TYPE = 	50	 then 	'MLC'
when	M_CLASS_TYPE = 	21	 then 	 'Collateral'
when	M_CLASS_TYPE = 	41	 then 	 'MRA'
when	M_CLASS_TYPE = 	34	 then 	 'VAR'
when	M_CLASS_TYPE = 	51	 then 	 'Collateral Exchange'
when	M_CLASS_TYPE = 	55	 then 	 'Collateral Interest'
else	convert(varchar(20), M_CLASS_TYPE)	end as DYN_TYPE
from DYNDBF4#TRN_DYND_DBF) T4
WHERE T2.M_REFERENCE=T1.M_RPO_DMSETUP_TABLE_REF and T2.M_REFERENCE=T3.M_REFERENCE and T3.M_DYN_TABLE*=T4.M_CREATION and T3.M_DYN_TABLE_DIR_TYPE*=T4.M_TYPE
and T1.M_LABEL NOT IN ('MX_REF_JOB','IDENTITY','REF_DATA','TIMESTAMP')

