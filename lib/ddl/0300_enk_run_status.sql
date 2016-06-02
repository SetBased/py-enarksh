insert into ENK_RUN_STATUS( rst_name
,                           rst_label
,                           rst_weight )
values( 'waiting'
,       'ENK_RST_ID_WAITING'
,       1 )
,     ( 'running'
,       'ENK_RST_ID_RUNNING'
,       2 )
,     ( 'completed'
,       'ENK_RST_ID_COMPLETED'
,       3 )
,     ( 'error'
,       'ENK_RST_ID_ERROR'
,       4 )
,     ( 'queued'
,       'ENK_RST_ID_QUEUED'
,       5 )
;

commit;
