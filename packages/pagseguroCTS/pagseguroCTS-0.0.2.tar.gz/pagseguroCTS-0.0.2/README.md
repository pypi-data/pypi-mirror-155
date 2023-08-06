# pagseguroCTS
SDK Pagseguro

#### Dependencias
You need Python 2 or later to use **pagseguroCTS**.

If you have pip, just run:
```
pip install pagseguroCTS
```
## Como usar

Defina sandbox True caso for usar neste ambiente. 
config = {'sandbox': True}

Instancie a classe usando as credenciais.
pg = PagSeguro(email="seuemail@dominio.com", token="ABCDEFGHIJKLMNO", config=config)


O seu config também pode fazer override de algumas váriaveis pré-definidas na classe de Config padrão. 
São elas:

- CURRENCY - Moeda utilizada. Valor padrão: `'BRL'`
- DATETIME_FORMAT - Formato de Data/Hora. Valor Padrão: `'%Y-%m-%dT%H:%M:%S'`
- REFERENCE_PREFIX - Formato do valor de referência do produto. Valor Padrão: `'REF%s'` Obs: Nesse caso, sempre é necessário deixar o `%s` ao final do prefixo para que o mesmo seja preenchido automaticamente
- USE_SHIPPING - User endereço de entrega. Valor padrão: `True`

Para mais informações: `https://pypi.org/project/pagseguro/`
