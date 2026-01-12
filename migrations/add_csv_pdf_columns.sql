-- Adicionar colunas para armazenar nomes de arquivos CSV e PDF

ALTER TABLE cursos ADD COLUMN csv_file VARCHAR(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL AFTER parceiro_logo;
ALTER TABLE cursos ADD COLUMN pdf_file VARCHAR(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL AFTER csv_file;
