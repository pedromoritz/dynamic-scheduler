FROM php:7.2-apache
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
RUN echo "memory_limit = 1G" >> "$PHP_INI_DIR/php.ini"
COPY index.php /var/www/html/