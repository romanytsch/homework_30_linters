cat >> /var/lib/postgresql/data/postgresql.conf << EOF
log_destination = 'stderr'
logging_collector = on
log_directory = 'pg_log'
EOF
