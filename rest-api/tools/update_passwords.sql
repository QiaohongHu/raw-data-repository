ALTER USER '${READONLY_DB_USER}'@'%' IDENTIFIED BY '${READONLY_PASSWORD}';
ALTER USER '${RDR_DB_USER}'@'%' IDENTIFIED BY '${RDR_PASSWORD}';
ALTER USER '${ALEMBIC_DB_USER}'@'%' IDENTIFIED BY '${RDR_PASSWORD}';
