"""insert cursoscarioca dados

Revision ID: 44e829b482c2
Revises: 8848a6de01ce
Create Date: 2026-02-26 14:02:45.727964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44e829b482c2'
down_revision: Union[str, Sequence[str], None] = '8848a6de01ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


import os
import re

def upgrade() -> None:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sql_file_path = os.path.join(current_dir, '..', 'legacy_sql', 'cursoscarioca_dados.sql')
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_commands = f.read()
        
    current_statement = []
    in_insert = False
    
    for line in sql_commands.split('\n'):
        # Check if we are starting a new INSERT statement
        if line.startswith('INSERT INTO'):
            in_insert = True
            
        if in_insert:
            current_statement.append(line)
            # Find the end of the INSERT statement (ends with );)
            if line.strip().endswith(');'):
                stmt = '\n'.join(current_statement)
                op.execute(sa.text(stmt))
                current_statement = []
                in_insert = False


def downgrade() -> None:
    # To downgrade, we would delete the inserted records. 
    # Since these are initial records, we can clear the tables.
    # However, to be safe and avoid wiping user data generated later,
    # we'll use a simple DELETE for the IDs we know were inserted, or just truncate if requested.
    # A safe approach is to just pass or delete the explicit IDs.
    pass
