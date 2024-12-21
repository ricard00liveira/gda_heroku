# Gerenciador de Denúncias Ambientais

Um sistema para gerenciamento de denúncias ambientais desenvolvido com Django e Django Rest Framework (DRF).

## **Pré-requisitos**

- Python 3.10 ou superior
- Banco de Dados PostgreSQL

## **Instalação**

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/ricard00liveira/gda_heroku.git
   cd gda_heroku
   ```

2. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados no arquivo `settings.py`:**
   Atualize as informações de conexão com o banco de dados PostgreSQL.

   Exemplo:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'nome_do_banco',
           'USER': 'usuario',
           'PASSWORD': 'senha',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Aplique as migrações:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crie um superusuário:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

## **Uso**

- Acesse o sistema em: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- Utilize as credenciais do superusuário criado para acessar o painel administrativo.

---

## Endpoints

### Comarcas

- **Listar Comarcas**  
  `GET /api/comarcas/`  
  Lista todas as comarcas cadastradas.

- **Criar Comarca**  
  `POST /api/comarcas/create/`  
  Permite criar uma nova comarca.

- **Visualizar Comarca**  
  `GET /api/comarcas/<int:comarca_id>/`  
  Visualiza os detalhes de uma comarca específica.

- **Atualizar Comarca**  
  `PUT /api/comarcas/<int:comarca_id>/update/`  
  Atualiza uma comarca específica.

- **Excluir Comarca**  
  `DELETE /api/comarcas/<int:comarca_id>/delete/`  
  Exclui uma comarca específica.

### Denúncias

- **Criar Denúncia**  
  `POST /api/denuncias/create/`  
  Permite criar uma nova denúncia.

- **Listar Denúncias**  
  `GET /api/denuncias/`  
  Lista todas as denúncias disponíveis.

- **Visualizar Denúncia**  
  `GET /api/denuncias/read/<int:denuncia_id>/`  
  Visualiza os detalhes de uma denúncia específica.

- **Atualizar Denúncia**  
  `PATCH /api/denuncias/update/<int:denuncia_id>/`  
  Atualiza uma denúncia específica.

- **Excluir Denúncia**  
  `DELETE /api/denuncias/delete/<int:denuncia_id>/`  
  Exclui uma denúncia específica.

### Logradouros

- **Listar Logradouros**  
  `GET /api/logradouros/<int:municipio_id>/`  
  Lista os logradouros de um município. Se uma `query` for fornecida, retorna os logradouros correspondentes ao filtro; caso contrário, retorna o número total de logradouros do município.

- **Criar Logradouro**  
  `POST /api/logradouros/<int:municipio_id>/create/`  
  Permite criar um novo logradouro associado a um município.

- **Visualizar Logradouro**  
  `GET /api/logradouros/<int:logradouro_id>/`  
  Visualiza os detalhes de um logradouro específico.

- **Atualizar Logradouro**  
  `PATCH /api/logradouros/<int:logradouro_id>/update/`  
  Atualiza os dados de um logradouro específico.

- **Excluir Logradouro**  
  `DELETE /api/logradouros/<int:logradouro_id>/delete/`  
  Exclui um logradouro específico.

### Municípios

- **Listar Municípios**  
  `GET /api/municipios/`  
  Lista todos os municípios cadastrados.

- **Criar Município**  
  `POST /api/municipios/create/`  
  Permite criar um novo município.

- **Visualizar Município**  
  `GET /api/municipios/<int:municipio_id>/`  
  Visualiza os detalhes de um município específico.

- **Atualizar Município**  
  `PUT /api/municipios/<int:municipio_id>/update/`  
  Atualiza os dados de um município específico.

- **Excluir Município**  
  `DELETE /api/municipios/<int:municipio_id>/delete/`  
  Exclui um município específico.

### Fatos

- **Listar Fatos**  
  `GET /api/fatos/`  
  Lista todos os fatos cadastrados.

- **Criar Fato**  
  `POST /api/fatos/create/`  
  Permite criar um novo fato.

- **Visualizar Fato**  
  `GET /api/fatos/<int:fato_id>/`  
  Visualiza os detalhes de um fato específico.

- **Atualizar Fato**  
  `PUT /api/fatos/<int:fato_id>/update/`  
  Atualiza um fato específico.

- **Excluir Fato**  
  `DELETE /api/fatos/<int:fato_id>/delete/`  
  Exclui um fato específico.

### Subfatos

- **Listar Subfatos de um Fato**  
  `GET /api/fatos/<int:fato_id>/subfatos/`  
  Lista todos os subfatos relacionados a um fato específico.

- **Criar Subfato**  
  `POST /api/fatos/<int:fato_id>/subfatos/create/`  
  Permite criar um novo subfato relacionado a um fato específico.

- **Visualizar Subfato**  
  `GET /api/subfatos/<int:subfato_id>/`  
  Visualiza os detalhes de um subfato específico.

- **Atualizar Subfato**  
  `PATCH /api/subfatos/<int:subfato_id>/update/`  
  Atualiza um subfato específico.

- **Excluir Subfato**  
  `DELETE /api/subfatos/<int:subfato_id>/delete/`  
  Exclui um subfato específico.

### Usuários

- **Listar Usuários**  
  `GET /api/usuarios/`

  - **Parâmetros opcionais de query**:
    - `q` (string): Permite buscar usuários pelo nome, email ou CPF.  
       - Deve conter pelo menos 3 caracteres.
      Lista todos os usuários cadastrados.

- **Criar Usuário**  
  `POST /api/usuarios/create/`  
  Permite criar um novo usuário.

- **Visualizar Usuário**  
  `GET /api/usuarios/<str:cpf>/`  
  Visualiza os detalhes de um usuário específico.

- **Atualizar Usuário**  
  `PATCH /api/usuarios/<str:cpf>/update/`  
  Atualiza um usuário específico.

- **Excluir Usuário**  
  `DELETE /api/usuarios/<str:cpf>/delete/`  
  Exclui um usuário específico.

- **Obter Perfil**  
  `GET /api/profile/`  
  Retorna informações sobre o perfil do usuário logado.

---

## Gerando Token de Acesso

### Para acessar os endpoints protegidos, você precisa de um token de acesso. Siga os passos abaixo para gerar o token:

- Passo 1: Abra o navegador ou um cliente como Postman e faça uma requisição POST para:

`http://127.0.0.1:8000/api/token/`

- Passo 2: Digite suas credenciais nos campos específicos, o CPF e senha do usuário.

- Passo 3: Obtenha o Token. Se as credenciais estiverem corretas, você receberá uma resposta como esta:

```bash
{
  "access": "seu_token_de_acesso",
  "refresh": "seu_token_de_refresh"
}
```

**Use o valor de "access" como seu token para autenticação.**

- Passo 4: Use o Token de Acesso, para acessar as APIs protegidas, inclua o token de acesso no cabeçalho da requisição:

```bash
Exemplo de Cabeçalho:
Authorization: Bearer {seu_token_de_acesso}
```

---

## Usando na prática

#### Após criar o super usuário do django, precisamos incluir primeiramente uma comarca e posterior um município.

- Com servidor rodando, abra o programa Postman.
- Importe o arquivo `API DJANGO.postman_collection.json` para mostrar a coleção de requisições.
- Primeiramente precisaremos criar uma comarca e depois um município nela, usaremos o `LOCAL > Enderecos > Comarcas > Criar_Comarca`, em `Body > raw` digite o nome da comarca:

```bash
{
"nome":"Pelotas" //Nome da comarca
}
```

- Após a mensagem de sucesso, iremos incluir um munícipio em `LOCAL > Enderecos >  Municipios > Create_Municipios`, neste `Body > raw` incluiremos o id da comarca inserida.

```bash
{
    "comarca":1, //Id da Comarca existente (1 = Pelotas)
    "nome":"Capão do Leão" //Nome do município
}
```

- Agora iremos inserir um logradouro para ser vinculado a denúncia, `LOCAL > Enderecos > Logradouros > Criar_Logradouro`, atribuindo o id do munícipio criado.

```bash
{
    "cidade":1,
    "nome":"AVENIDA PRINCIPAL"
}
```

- Obtendo êxito na inserção do logradouro, podemos inserir uma denúncia através `LOCAL > Denuncias > Create_denuncia`, em `Body > raw` digite o dados da denúncia:

**Completa:**

```bash
{
    "denunciante": 1,                   // ID do usuário denunciante (Opcional)
    "anonima": false,                   // Indica se a denúncia é anônima (Opcional)
    "descricao": "Descrição da denúncia detalhada",
    "endereco": 1,                      // ID do logradouro relacionado
    "nr_endereco": "123",               // Número do endereço (Opcional)
    "ponto_referencia": "Próximo à escola", //(Opcional)
    "status": "analise",                // Status inicial (Opcional)
    "municipio": 1,                     // ID do município relacionado
    "fato": 1,                          // ID do fato relacionado
    "subfato": 1,                       // ID do subfato relacionado
    "responsavel": 2,                   // ID do responsável inicial (Opcional)
    "is_deleted": false,                // Define se a denúncia está marcada como excluída (Opcional)
    "infrator": "Nome do infrator",     // Nome do infrator (Opcional)
    "prioridade": "media",              // Prioridade da denúncia (Opcional)
    "localizacao": {                    // Coordenadas (em caso de uso com JSONField) (Opcional)
        "latitude": -23.55052,
        "longitude": -46.633308
    }
}
```

**Simples:**

```bash
{
    "descricao": "Descrição da denúncia detalhada",
    "endereco": 1,                      // ID do logradouro relacionado
    "nr_endereco": "123",               // Número do endereço (Opcional)
    "municipio": 1,                     // ID do município relacionado
    "fato": 1,                          // ID do fato relacionado
    "subfato": 1,                       // ID do subfato relacionado
}
```

## Não finalizado! (working...)
