# Desafio b2bflow - Desenvolvimento Python

Script em Python que consome dados de contatos cadastrados no Supabase e dispara mensagens padronizadas no WhatsApp utilizando a Z-API. 

**Diferencial técnico aplicado:** Utilização da API REST nativa do Supabase (via `requests`) ao invés do SDK padrão, visando evitar gargalos de *deadlock* com HTTP/2 e garantindo maior estabilidade no consumo dos dados.

---

## 🛠️ 1. Setup da Tabela (Supabase)

No painel do seu Supabase, acesse o **SQL Editor** e execute o script abaixo para criar a tabela, desativar o RLS (para facilitar os testes) e inserir dados de exemplo:

```sql
-- 1. Cria a tabela
CREATE TABLE contatos (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL
);

-- 2. Desativa o RLS para permitir leitura via API de forma simplificada
ALTER TABLE contatos DISABLE ROW LEVEL SECURITY;

-- 3. Insere dados de teste (Substitua pelos seus números reais)
INSERT INTO contatos (nome, telefone) VALUES 
('Marcelo', '5511999999999'),
('João', '5511988888888'),
('Maria', '5511977777777');
```

---

## ⚙️ 2. Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto e preencha com as suas credenciais:

```env
SUPABASE_URL=[https://seu-projeto.supabase.co](https://seu-projeto.supabase.co)
SUPABASE_KEY=sua-chave-anon-public
ZAPI_INSTANCE=sua-instancia-zapi
ZAPI_TOKEN=seu-token-zapi
```
*(Nota: O arquivo `.env` está no `.gitignore` por boas práticas de segurança e não foi comitado no repositório).*

---

## 🚀 3. Como Rodar o Projeto

Siga os passos abaixo no seu terminal:

1. **Clone este repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
   cd SEU_REPOSITORIO
   ```

2. **Crie e ative um ambiente virtual (Recomendado):**
   ```bash
   # No Windows:
   python -m venv venv
   .\venv\Scripts\activate

   # No Linux/Mac:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o script principal:**
   ```bash
   python main.py
   ```
