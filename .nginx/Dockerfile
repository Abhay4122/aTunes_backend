FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY ./.nginx/nginx.conf /etc/nginx/conf.d
# COPY fullchain.pem /etc/letsencrypt/live/api.domain.com/fullchain.pem
# COPY privkey.pem /etc/letsencrypt/live/api.domain.com/privkey.pem
# COPY options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
# COPY ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem