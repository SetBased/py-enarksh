insert into ENK_NODE_TYPE( ntp_name
,                          ntp_label )
values( 'schedule'
,       'ENK_NTP_SCHEDULE' )
,     ( 'command job'
,       'ENK_NTP_COMMAND_JOB' )
,     ( 'compound job'
,       'ENK_NTP_COMPOUND_JOB' )
,     ( 'manual trigger'
,       'ENK_NTP_MANUAL_TRIGGER' )
,     ( 'terminator'
,       'ENK_NTP_TERMINATOR' )
,     ( 'dynamic job'
,       'ENK_NTP_DYNAMIC_JOB' )
,     ( 'dynamic outer worker'
,       'ENK_NTP_DYNAMIC_OUTER_WORKER' )
,     ( 'dynamic inner worker'
,       'ENK_NTP_DYNAMIC_INNER_WORKER' )
;

commit;
