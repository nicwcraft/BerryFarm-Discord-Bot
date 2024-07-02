# BerryFarm-Discord-Bot
O BerryFarm Bot é um bot para Discord que simula uma fazenda de morangos. Os usuários podem plantar, colher, vender morangos, produzir receitas e vender essas receitas. O bot também possui um sistema de banco para armazenar o dinheiro dos usuários e um sistema de ranking para mostrar quem tem mais dinheiro.

# Funcionalidades

Comandos Principais
f!plantar [quantidade]
Planta a quantidade especificada de morangos. Se não especificar, planta 1 por padrão.
f!colher [quantidade]
Colhe a quantidade especificada de morangos. Se não especificar, colhe 1 por padrão.
f!vender [quantidade]
Vende a quantidade especificada de morangos. Se não especificar, vende todos por padrão.
f!inventario
Mostra quantos morangos você tem no inventário.
f!saldo
Mostra o saldo de dinheiro no banco.
f!list
Apresenta a lista completa das receitas disponíveis.
f!mre
Mostra suas receitas armazenadas.
f!vre [numero]
Vende uma receita específica pelo número correspondente.
f!receita [numero]
Cozinha uma receita específica pelo número correspondente.
f!ranking
Mostra o ranking de membros com mais dinheiro.

# Sistema de Receitas
Os usuários podem criar diversas receitas utilizando morangos. Cada receita requer uma quantidade específica de morangos e tem um valor de venda correspondente.
As receitas são numeradas para facilitar a produção e a venda.
Ao produzir uma receita, o bot envia uma mensagem em embed notificando o sucesso da produção.

# Sistema de Banco
Os morangos colhidos podem ser vendidos para ganhar dinheiro.
O saldo de dinheiro de cada usuário é armazenado em um arquivo banco.json.
O bot possui um comando de ranking que mostra os membros com mais dinheiro no banco.

# Exemplos de Receitas
Bolo de Morango
Morangos Necessários: 5
Valor de Venda: 20
Torta de Morango
Morangos Necessários: 10
Valor de Venda: 40
Sorvete de Morango
Morangos Necessários: 8
Valor de Venda: 30

# Estrutura do Projeto
bot.py: Arquivo principal que configura o bot e carrega os cogs.
cogs: Diretório que contém todos os cogs do bot (ajuda, banco, fazenda, receitas, loja).
ajuda.py: Comandos relacionados à ajuda e descrição dos comandos.
bank.py: Comandos relacionados ao banco e saldo dos usuários.
farm.py: Comandos relacionados ao plantio e colheita de morangos.
recipes.py: Comandos relacionados à produção e venda de receitas.
shop.py: Comandos relacionados à loja (futuras expansões).

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

