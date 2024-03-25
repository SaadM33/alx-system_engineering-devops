#create school file
file{'school':
    ensure  => present,
    path    => '/tmp',
    content => 'I love Puppet',
    owner   => 'www-data',
    group   => 'www-data',
    mode    => '0744',
}