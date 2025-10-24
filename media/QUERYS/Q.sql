--USERS INFO
SELECT * FROM public.users

--DOCUMENTOS METADATA
SELECT * FROM public.source_documents
LIMIT 100

--CONTENIDO DOC
SELECT * FROM public.document_chunks

--CONSULTAS Y RESPUESTAS
SELECT * FROM public.rag_query_logs
WHERE conversation_id = 6

