select ob.name as table_name,' | ',st.rowcnt as num_rows
from sysobjects ob, systabstats st 
where ob.type='U' 
and st.id=ob.id 
order by ob.name