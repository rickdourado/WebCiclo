import re
with open('/home/ssdlinux/Documents/dev/WebCiclo/migrations/legacy_sql/cursoscarioca_dados.sql', 'r', encoding='utf-8') as f:
    sql_commands = f.read()

pattern = re.compile(r"INSERT INTO[^;]+?\);", re.DOTALL)
matches = list(pattern.finditer(sql_commands))
print(f"Found {len(matches)} matches.")
for i, m in enumerate(matches):
    print(f"Match {i}: Starts with: {m.group(0)[:50]}... Ends with: ...{m.group(0)[-50:]}")
