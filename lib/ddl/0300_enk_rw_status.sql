insert into ENK_RW_STATUS( rws_name
,                          rws_label )
values( '-'
,       'ENK_RWS_ID_NONE' )
,     ( 'read'
,       'ENK_RWS_ID_READ' )
,     ( 'write'
,       'ENK_RWS_ID_WRITE' )
;

commit;
