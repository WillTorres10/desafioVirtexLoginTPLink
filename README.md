## Objetivo do desafio

Realizar login e alterar a senha do Roteador WR840N (ou modelos da TP-Link) via
Script (em qualquer linguagem).

## Equipamento usado

Devido a não ter acesso ao dispositivo dado como preferêncial, o teste foi realizado um roteador da mesma fabricante porém do seguinte modelo: **WR841N**

## Antes do código

Diante o desafio, tive como primeiro passo, antes de fazer em o código em si, pesquisar as seguintes coisas:

- Qual protocolo usar?
- Como funciona a autenticação no roteador?
- Como efetuar os comandos?

### Qual protocolo usar?

Como já tive experiências com acesso a servidores tanto Linux (ssh) e Windows (RPD), descidi procurar qual o protocoloca de acesso eu poderia usar. Em uma busca geral, em alguns fóruns, encontrei postagens dizendo para tentar o ssh ou telnet.

No entanto, as tentativas de conexão com o roteador utilizando esses protocolos não foi bem sucedida. Tendo como resultado o seguinte:

**Com ssh:**

_Comando_

    ssh 192.168.0.1

_Resposta_

    ssh: connect to host 192.168.0.1 port 22: Connection refused

**Com telnet**

_Comando_

    telnet 192.168.0.1

_Resposta_

    Trying 192.168.0.1...
    telnet: Unable to connect to remote host: Connection refused

Após esses testes, descidi então analisar como que o painel de administração do próprio roteador funcionava. Por usar a web, já sabia que seria o HTTP, porém faltava uma coisa, qual é a rota e como autenticar?

### Como funciona a autenticação no roteador?

Com o monitoramento de rede aberto no console de desenvolvedor no navegador, acesso a página de adminsitração do roteador e monitoro as requisições feitas. Ao analisar os cabeçalhos das requisições noto que ele utiliza um campo chamando Authentication.

Em uma rápida pesquisa no google, em uma [postagem em um forúm](https://www.mentebinaria.com.br/forums/topic/480-tools-router-brute-script-em-python-para-realizar-brute-force-em-roteadores-tp-links/ "Tools Router Brute - Script em Python para realizar brute force em roteadores TP-LINKs") vejo que seu valor é o encode em base64 do usuário e senha no formado `usuario:senha`.

Após descobrir qual protocolo usar e como é feita a autenticação, falta uma coisa. Como efetuar os comandos?

### Como efetuar os comandos?

Continuando no monitoramento de rede no console de desenvolvedor, afim de saber como que se dava a requisição para a atualização da senha, manualmente, alterei a senha e monitorei as requisições feitas.

Diferente do que imaginava, ao executar a alteração da senha, diferente do comum que é um PATCH ou um POST, a requisição enviada para o roteador foi um GET. Ao analisar, vejo que todos os parâmetros eram de configuração eram enviados como query.

Pronto, agora já sei qual protocolo usar, como autênticar e como efetuar um comando. Vamos agora para o código.

## O código

Devido a esperiência que já tenho, descido usar o python para fazer o script. Ao procurar por algum script que faça algo semenhante ao que eu queria, me deparado com uma postagem no [Stack Overflow](https://stackoverflow.com/questions/15386582/how-to-control-a-tplink-router-with-a-python-script "How to control a TPLINK router with a python script") que o tópico era justamente como controlar um roteador TP-Link utilizando python.

No exemplo dado na primeira resposta, ao executar o script, ele reiniciar o roteador. Apesar de não ser exatamente o que procurava, ele já me deu a faca e o quejo nas mãos. Analisando o código, identifiquei qual parte do script eu alteraria para que servisse ao que me foi proposto no desafio.

Na parte de declaração de constantes do código, a variável `url_template` era justamente o comando enviado para o roteador. As contates que eram:

    tplink = '192.168.0.1'
    user = 'admin'
    password = 'admin'
    url_template = 'http://{}/userRpm/SysRebootRpm.htm?Reboot=Reboot'

Após minhas modificações, ficaram assim:

    tplink = "192.168.0.1"
    user = "USER_ACCESS_PANEL"
    password = "PASSWORD_ACCESS_PANEL"
    url_template = "http://{}/userRpm/WlanSecurityRpm.htm?secType=3&pskSecOpt=3&pskCipher=3&pskSecret={}&interval=0&wpaSecOpt=3&wpaCipher=1&radiusIp=&radiusPort=1812&radiusSecret=&intervalWpa=0&wepSecOpt=3&keytype=1&keynum=1&key1=&length1=0&key2=&length2=0&key3=&length3=0&key4=&length4=0&Save=Salvar"
    novaSenha = "NEW_PASSWORD_WIFI"

Além da troca do valor da constante `url_template`, foi adicionado uma nova constant`novaSenha`, nela é onde é informada a nova senha do roteador.

_Atenção, alterações por questão da segurança:_

- `USER_ACCESS_PANEL` é o usuário usado para autenticar no painel do roteador.

- `PASSWORD_ACCESS_PANEL` é a senha do usuário usado para autenticar no painel do roteador

- `NEW_PASSWORD_WIFI` senha a ser configurada no wifi.

Na `url_template`, onde estão os `{}` o python substituirá pelo ip do roteador no primeiro e no segundo, a nova senha do wifi.

Pronto, script finalizado, agora só executar:

    python script.py

Pronto, senha alterada.
