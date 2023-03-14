FROM centos:7.6.1810
MAINTAINER "Pedro Moritz de Carvalho Neto" <pmoritz@yahoo.com>
ENV container docker

COPY start-all /etc/init.d/start-all

RUN \
yum clean all && \
yum -y upgrade && \
yum -y install epel-release yum-utils && \
yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm && \
yum-config-manager --enable remi-php73 && \
yum-config-manager --disable remi-php54 && \
yum -y install --nogpgcheck --setopt=tsflags=nodocs httpd mod_ssl openssl net-tools php php-common php-ldap php-cli php-mysqlnd php-zip php-devel php-gd php-mcrypt php-mbstring php-curl php-xml php-pear php-bcmath php-json php-pecl-apcu php-pdo php-mysqlnd php-gd mariadb-libs && \
chmod -v +x /etc/init.d/start-all && \
rm -rf /var/cache/yum && \
rm -f /etc/httpd/conf/httpd.conf && \
rm -rf /tmp/* /var/tmp/*

EXPOSE 443

COPY index.html /var/www/html/
COPY php-on-html-files.conf /etc/httpd/conf.d/
COPY httpd.conf /etc/httpd/conf/httpd.conf
COPY custom.conf /etc/httpd/conf.d/

CMD /etc/init.d/start-all