[![Build Status](https://travis-ci.org/riquellopes/bom-negocio-talk.svg)](https://travis-ci.org/riquellopes/bom-negocio-talk)
Olx Talk:
=========

Integra o gtalk ao site de classificados olx.


O objectivo desse projeto é unir duas das ferramentas que eu utilizo quase todos os dias.


Configuração:
--------------

```python
bot = OlxBot()
bot.setState('available', "escreva aqui o seu status.")
bot.start('user@gmail.com', 'password')
```

Como executar:
--------------
```sh
python talk.py
Digite seu gmail: user@gmail.com
Digite sua senha: ************
```

Como realizar uma busca:
--------------
![alt text](https://raw.githubusercontent.com/riquellopes/bom-negocio-talk/master/adium.png "Tela do Adium")

Observação:
----------

Nessa primeira versão, apenas as buscas para instrumentos musicais vão funcionar.
