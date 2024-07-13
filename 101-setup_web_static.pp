# Define variables
$USER = 'ubuntu'
$GROUP = 'ubuntu'

# Install nginx if not installed
package { 'nginx':
  ensure => installed,
}

# Allow Nginx HTTP traffic
exec { 'allow_nginx_http':
  command => 'sudo ufw allow "Nginx HTTP"',
  unless  => 'sudo ufw status | grep "Nginx HTTP" | grep "ALLOW"',
}

# Ensure Nginx service is running
service { 'nginx':
  ensure => running,
  enable => true,
  require => Package['nginx'],
}

# Ensure directories are created
['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test'].each |$dir| {
  file { $dir:
    ensure => directory,
    owner  => $USER,
    group  => $GROUP,
    mode   => '0755',
  }
}

# Deploy index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "Hello World!, I'm deploying static content.\n",
  owner   => $USER,
  group   => $GROUP,
  mode    => '0644',
}

# Manage current symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => $USER,
  group  => $GROUP,
}

# Set ownership recursively
file { '/data':
  ensure  => 'directory',
  recurse => true,
  owner   => $USER,
  group   => $GROUP,
}

# Modify Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => template('your_module/nginx_config.erb'), # Use a template file for configuration
  require => Service['nginx'],
  notify  => Service['nginx'],
}

# Restart Nginx after configuration changes
exec { 'restart_nginx':
  command     => 'sudo service nginx restart',
  refreshonly => true,
  subscribe   => File['/etc/nginx/sites-available/default'],
}
