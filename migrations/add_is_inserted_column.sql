-- ========================================
-- MIGRATION: Adicionar coluna is_inserted
-- Data: 2025-11-25
-- Descrição: Adiciona coluna para rastrear se curso foi inserido no sistema
-- ========================================

USE cursoscarioca;

-- Adicionar coluna is_inserted
ALTER TABLE cursos 
ADD COLUMN is_inserted ENUM('sim', 'nao') DEFAULT 'nao' 
AFTER status;

-- Verificar se a coluna foi criada
DESCRIBE cursos;

-- Mostrar alguns registros para confirmar
SELECT id, titulo, status, is_inserted FROM cursos LIMIT 5;
