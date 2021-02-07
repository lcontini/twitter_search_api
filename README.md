# twitter-search-api

Este projeto destina-se a utilizar as APIs do Twitter para buscar os ultimos 100 tweets baseados em hashtags predefinidas, afim de disponibilizar APIs REST que provenham as seguintes informações:

1. Dentre os usuários dos tweets buscados, os 5 (cinco) que possuem mais seguidores;
2. O total de postagens, agrupadas por hora do dia (independentemente da hashtag);
3. O total de postagens para cada uma das hashtags por idioma/país do usuário que postou 

Para consumir as informações do twitter, foi utilizada a biblioteca ![tweepy 3.10.0](https://docs.tweepy.org/en/v3.10.0/api.html)