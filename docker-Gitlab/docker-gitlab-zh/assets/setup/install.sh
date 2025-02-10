#!/bin/bash
set -e

GEM_CACHE_DIR="${SETUP_DIR}/cache"

# rebuild apt cache
apt-get update

# install build dependencies for gem installation
apt-get install -y gcc g++ make patch pkg-config cmake \
  libc6-dev ruby2.1-dev \
  libmysqlclient-dev libpq-dev zlib1g-dev libyaml-dev libssl-dev \
  libgdbm-dev libreadline-dev libncurses5-dev libffi-dev \
  libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev

# remove the host keys generated during openssh-server installation
rm -rf /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub

# add ${GITLAB_USER} user
adduser --disabled-login --gecos 'GitLab' ${GITLAB_USER}
passwd -d ${GITLAB_USER}

# set PATH (fixes cron job PATH issues)
cat >> ${GITLAB_HOME}/.profile <<EOF
PATH=/usr/local/sbin:/usr/local/bin:\$PATH
EOF

rm -rf ${GITLAB_HOME}/.ssh
sudo -HEu ${GITLAB_USER} mkdir -p ${GITLAB_DATA_DIR}/.ssh
sudo -HEu ${GITLAB_USER} ln -s ${GITLAB_DATA_DIR}/.ssh ${GITLAB_HOME}/.ssh

# create the data store
sudo -HEu ${GITLAB_USER} mkdir -p ${GITLAB_DATA_DIR}

# configure git for the 'git' user
sudo -HEu ${GITLAB_USER} git config --global core.autocrlf input

# install gitlab-shell
echo "Cloning gitlab-shell v.${GITLAB_SHELL_VERSION}..."
sudo -u git -H git clone -q -b v${GITLAB_SHELL_VERSION} --depth 1 \
  https://git.coding.net/khan/gitlab-shell.git ${GITLAB_SHELL_INSTALL_DIR}

cd ${GITLAB_SHELL_INSTALL_DIR}
sudo -u git -H cp -a config.yml.example config.yml
sudo -u git -H ./bin/install

# shallow clone gitlab-ce
echo "Cloning gitlab-ce v.${GITLAB_VERSION}..."
sudo -HEu ${GITLAB_USER} git clone -q -b v${GITLAB_VERSION} --depth 1 \
  https://gitcafe.com/larryli/gitlab.git ${GITLAB_INSTALL_DIR}

cd ${GITLAB_INSTALL_DIR}

# remove HSTS config from the default headers, we configure it in nginx
sed "/headers\['Strict-Transport-Security'\]/d" -i app/controllers/application_controller.rb

# copy default configurations
cp lib/support/nginx/gitlab /etc/nginx/sites-enabled/gitlab
sudo -HEu ${GITLAB_USER} cp config/gitlab.yml.example config/gitlab.yml
sudo -HEu ${GITLAB_USER} cp config/resque.yml.example config/resque.yml
sudo -HEu ${GITLAB_USER} cp config/database.yml.mysql config/database.yml
sudo -HEu ${GITLAB_USER} cp config/unicorn.rb.example config/unicorn.rb
sudo -HEu ${GITLAB_USER} cp config/initializers/rack_attack.rb.example config/initializers/rack_attack.rb
sudo -HEu ${GITLAB_USER} cp config/initializers/smtp_settings.rb.sample config/initializers/smtp_settings.rb

# symlink log -> ${GITLAB_LOG_DIR}/gitlab
rm -rf log
ln -sf ${GITLAB_LOG_DIR}/gitlab log

# create required tmp directories
sudo -HEu ${GITLAB_USER} mkdir -p tmp/pids/ tmp/sockets/
chmod -R u+rwX tmp

# create symlink to assets in tmp/cache
rm -rf tmp/cache
sudo -HEu ${GITLAB_USER} ln -s ${GITLAB_DATA_DIR}/tmp/cache tmp/cache

# create symlink to assets in public/assets
rm -rf public/assets
sudo -HEu ${GITLAB_USER} ln -s ${GITLAB_DATA_DIR}/tmp/public/assets public/assets

# create symlink to uploads directory
rm -rf public/uploads
sudo -HEu ${GITLAB_USER} ln -s ${GITLAB_DATA_DIR}/uploads public/uploads

# create symlink to .secret in GITLAB_DATA_DIR
rm -rf .secret
sudo -HEu ${GITLAB_USER} ln -sf ${GITLAB_DATA_DIR}/.secret

# install gems required by gitlab, use local cache if available
if [[ -d ${GEM_CACHE_DIR} ]]; then
  mv ${GEM_CACHE_DIR} vendor/
  chown -R ${GITLAB_USER}:${GITLAB_USER} vendor/cache
fi
sudo -HEu ${GITLAB_USER} bundle install -j$(nproc) --deployment --without development test aws

# make sure everything in ${GITLAB_HOME} is owned by the git user
chown -R ${GITLAB_USER}:${GITLAB_USER} ${GITLAB_HOME}/

# install gitlab bootscript
cp lib/support/init.d/gitlab /etc/init.d/gitlab
chmod +x /etc/init.d/gitlab

# disable default nginx configuration and enable gitlab's nginx configuration
rm -f /etc/nginx/sites-enabled/default

# disable pam authentication for sshd
sed 's/UsePAM yes/UsePAM no/' -i /etc/ssh/sshd_config
sed 's/UsePrivilegeSeparation yes/UsePrivilegeSeparation no/' -i /etc/ssh/sshd_config
echo "UseDNS no" >> /etc/ssh/sshd_config

# permit password login
sed 's/#PasswordAuthentication yes/PasswordAuthentication no/' -i /etc/ssh/sshd_config

# configure verbose logging for sshd
sed 's/LogLevel INFO/LogLevel VERBOSE/' -i /etc/ssh/sshd_config

# move supervisord.log file to ${GITLAB_LOG_DIR}/supervisor/
sed 's|^logfile=.*|logfile='"${GITLAB_LOG_DIR}"'/supervisor/supervisord.log ;|' -i /etc/supervisor/supervisord.conf

# move nginx logs to ${GITLAB_LOG_DIR}/nginx
sed 's|access_log /var/log/nginx/access.log;|access_log '"${GITLAB_LOG_DIR}"'/nginx/access.log;|' -i /etc/nginx/nginx.conf
sed 's|error_log /var/log/nginx/error.log;|error_log '"${GITLAB_LOG_DIR}"'/nginx/error.log;|' -i /etc/nginx/nginx.conf

# configure supervisord log rotation
cat > /etc/logrotate.d/supervisord <<EOF
${GITLAB_LOG_DIR}/supervisor/*.log {
  weekly
  missingok
  rotate 52
  compress
  delaycompress
  notifempty
  copytruncate
}
EOF

# configure gitlab log rotation
cat > /etc/logrotate.d/gitlab <<EOF
${GITLAB_LOG_DIR}/gitlab/*.log {
  weekly
  missingok
  rotate 52
  compress
  delaycompress
  notifempty
  copytruncate
}
EOF

# configure gitlab-shell log rotation
cat > /etc/logrotate.d/gitlab-shell <<EOF
${GITLAB_LOG_DIR}/gitlab-shell/*.log {
  weekly
  missingok
  rotate 52
  compress
  delaycompress
  notifempty
  copytruncate
}
EOF

# configure gitlab vhost log rotation
cat > /etc/logrotate.d/gitlab-nginx <<EOF
${GITLAB_LOG_DIR}/nginx/*.log {
  weekly
  missingok
  rotate 52
  compress
  delaycompress
  notifempty
  copytruncate
}
EOF

# configure supervisord to start unicorn
cat > /etc/supervisor/conf.d/unicorn.conf <<EOF
[program:unicorn]
priority=10
directory=${GITLAB_INSTALL_DIR}
environment=HOME=${GITLAB_HOME}
command=bundle exec unicorn_rails -c ${GITLAB_INSTALL_DIR}/config/unicorn.rb -E ${RAILS_ENV}
user=git
autostart=true
autorestart=true
stopsignal=QUIT
stdout_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
stderr_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
EOF

# configure supervisord to start sidekiq
cat > /etc/supervisor/conf.d/sidekiq.conf <<EOF
[program:sidekiq]
priority=10
directory=${GITLAB_INSTALL_DIR}
environment=HOME=${GITLAB_HOME}
command=bundle exec sidekiq -c {{SIDEKIQ_CONCURRENCY}}
  -q post_receive
  -q mailer
  -q archive_repo
  -q system_hook
  -q project_web_hook
  -q gitlab_shell
  -q common
  -q default
  -e ${RAILS_ENV}
  -t {{SIDEKIQ_SHUTDOWN_TIMEOUT}}
  -P ${GITLAB_INSTALL_DIR}/tmp/pids/sidekiq.pid
  -L ${GITLAB_INSTALL_DIR}/log/sidekiq.log
user=git
autostart=true
autorestart=true
stdout_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
stderr_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
EOF

# configure supervisor to start sshd
mkdir -p /var/run/sshd
cat > /etc/supervisor/conf.d/sshd.conf <<EOF
[program:sshd]
directory=/
command=/usr/sbin/sshd -D -E ${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
user=root
autostart=true
autorestart=true
stdout_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
stderr_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
EOF

# configure supervisord to start nginx
cat > /etc/supervisor/conf.d/nginx.conf <<EOF
[program:nginx]
priority=20
directory=/tmp
command=/usr/sbin/nginx -g "daemon off;"
user=root
autostart=true
autorestart=true
stdout_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
stderr_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
EOF

# configure supervisord to start crond
cat > /etc/supervisor/conf.d/cron.conf <<EOF
[program:cron]
priority=20
directory=/tmp
command=/usr/sbin/cron -f
user=root
autostart=true
autorestart=true
stdout_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
stderr_logfile=${GITLAB_LOG_DIR}/supervisor/%(program_name)s.log
EOF

# purge build dependencies
apt-get purge -y --auto-remove gcc g++ make patch pkg-config cmake \
  libc6-dev ruby2.1-dev \
  libmysqlclient-dev libpq-dev zlib1g-dev libyaml-dev libssl-dev \
  libgdbm-dev libreadline-dev libncurses5-dev libffi-dev \
  libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev

# cleanup
rm -rf /var/lib/apt/lists/*
