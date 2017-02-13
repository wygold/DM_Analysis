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
decode(M_CLASS_TYPE,NULL,'SQL',0, M_CLASS ,1,'Accounting',2,'Copy Creation',6,'Accounting (Reporting)',3,'External',4,'Payments',5,'Definition report',6,'Accounting report',7,'Cash balances',8,'Simulation',9,'PL VAR',11,'Data Dictionary (Market Data Loader)',16,'Deliverable Cash',17,'Deliverable nostro cash',19,'Trade version audit',20,'Navigation templates', 31,'Liquidation Positions',32,'Classification tree',46,'Corporate actions static data',47,'Hedge',50,'MLC', 21, 'Collateral', 41, 'MRA', nvl(to_char(M_CLASS_TYPE), ' ')) as DYN_TYPE
from DYNDBF1#TRN_DYND_DBF 
union  
select 2 as M_TYPE  ,  M_CREATION,
decode(M_CLASS_TYPE,NULL,'SQL',0, M_CLASS ,1,'Accounting',2,'Copy Creation',6,'Accounting (Reporting)',3,'External',4,'Payments',5,'Definition report',6,'Accounting report',7,'Cash balances',8,'Simulation',9,'PL VAR',11,'Data Dictionary (Market Data Loader)',16,'Deliverable Cash',17,'Deliverable nostro cash',19,'Trade version audit',20,'Navigation templates', 31,'Liquidation Positions',32,'Classification tree',46,'Corporate actions static data',47,'Hedge',50,'MLC', 21, 'Collateral', 41, 'MRA', nvl(to_char(M_CLASS_TYPE), ' ')) as DYN_TYPE
from DYNDBF2#TRN_DYND_DBF 
union  
select 1 as M_TYPE  ,  M_CREATION,
decode(M_CLASS_TYPE,NULL,'SQL',0, M_CLASS ,1,'Accounting',2,'Copy Creation',6,'Accounting (Reporting)',3,'External',4,'Payments',5,'Definition report',6,'Accounting report',7,'Cash balances',8,'Simulation',9,'PL VAR',11,'Data Dictionary (Market Data Loader)',16,'Deliverable Cash',17,'Deliverable nostro cash',19,'Trade version audit',20,'Navigation templates', 31,'Liquidation Positions',32,'Classification tree',46,'Corporate actions static data',47,'Hedge',50,'MLC', 21, 'Collateral', 41, 'MRA', nvl(to_char(M_CLASS_TYPE), ' ')) as DYN_TYPE
from DYNDBF3#TRN_DYND_DBF 
union 
select 3 AS M_TYPE,  M_CREATION,
decode(M_CLASS_TYPE,NULL,'SQL',0, M_CLASS ,1,'Accounting',2,'Copy Creation',6,'Accounting (Reporting)',3,'External',4,'Payments',5,'Definition report',6,'Accounting report',7,'Cash balances',8,'Simulation',9,'PL VAR',11,'Data Dictionary (Market Data Loader)',16,'Deliverable Cash',17,'Deliverable nostro cash',19,'Trade version audit',20,'Navigation templates', 31,'Liquidation Positions',32,'Classification tree',46,'Corporate actions static data',47,'Hedge',50,'MLC', 21, 'Collateral', 41, 'MRA', nvl(to_char(M_CLASS_TYPE), ' ')) as DYN_TYPE
from DYNDBF4#TRN_DYND_DBF) T4
WHERE T2.M_REFERENCE=T1.M_RPO_DMSETUP_TABLE_REF and T2.M_REFERENCE=T3.M_REFERENCE and T3.M_DYN_TABLE=T4.M_CREATION(+) and T3.M_DYN_TABLE_DIR_TYPE=T4.M_TYPE(+)
and T1.M_LABEL NOT IN ('MX_REF_JOB','IDENTITY','REF_DATA','TIMESTAMP')