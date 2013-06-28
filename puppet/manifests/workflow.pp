class workflow {

  file { "/home/vagrant/.bash_login":
    content => "cd /home/vagrant/workflow",
  }

  package{ "packages":
      name => [
        "git-core",
      ],
      ensure    => "latest",
  }

  file{ "ssh-config":
    ensure => "file",
    path => "/home/vagrant/.ssh/config",
    owner => "vagrant",
    group => "vagrant",
    content => "StrictHostKeyChecking no",
  }

  file{ "ssh-private":
    ensure => "file",
    path => "/home/vagrant/.ssh/id_rsa",
    owner => "vagrant",
    group => "vagrant",
    mode => 0600,
    content => "-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2Ydn3iYRgR4zwwLG6m+LEX6mn/MFPF6hMJNvuHAjuu9Ps0/d
qacyqq8QkWfXScrSWuV6Bg98urLLmiGDsfXTd1zSghHKokZ1Nb3wapVNnazx+nh3
R/qcrvwKBDm21BPwlntP8cUSc6tFaH8sRspQus93cZTWsXwJsgOPwQvL7tOlada2
M81ysGdVygPsD+P2kgnqaEFyKakyyiDx2lNHvr0PxUDZgJTAQVn7TTOT4VbZot3L
g0zuf9dELyX1OZ+s/MErmOcqHTkqmTQ6x1uiOlZyH4rZgfNI1XaFZ7L9pd/jpjXL
rRIBZwlWHheRpHHtkepQaPgtZbq/vqZ13kgrFQIDAQABAoIBACzgEj1x/Qp2AJeq
av7SJA5n4lf8+oeJvhcXU2TpPXXDCN4lC8WECJ/Nnc1hbrh6bwrxbErzxvd9CyOw
5kpAPG/TZloO8Y6ommWL2Z0jT+/HTeQuFe1zdf9jX22fumfl9SwWJFfsH/Jc0uTL
14aDFkRzqGB2JBRZUma29WEN3fRWs9KkU8KAKpK/bQIs2lywIBlomzd58oIdPtx5
4iArNaLI9Q0FqdJ9uREDvIzfy4IPItpLwWisMkPY56pLmFy+fp01ijkH7P74eSMz
ETChOKkP8p0qMh9dCPbZyppbWTRB5xHPu4r+J+uva4VxGJ8Yhm96/JtIocgtDGgq
fRcwD8ECgYEA8mZ8pMoBDq83555sMux/wv1YCX7zTuRib+U+CqTDPYETreGRdWps
7KJrQoOQCi99W++b4SRbeYtlJg2Kg0BsCHNdlM1AspomtXVxiWMKaN+5OMA1BJv0
s7MUJrb4EH6rbp2TcFUp7b299A9GMKjv0exmR4VE7f6Rw5e+MGIBSi8CgYEA5buz
BEG7yIgdj3clRTo3ujeFjxxoTl2Ei9/fmNsHS7fH1TQRuRBBqYiS+LNKAaGXWmDh
DNMFjEgnXzTvUH12/MdquCXkKAGa8DkKG6kLEJATKCiPaEIcHWRghkykIxZU9lOj
nmWotAsC1uhn/GWFo4X7K+n2j15lfWqjtAiZwfsCgYAguOMUn8xavh6O3tz+Vty8
ZtTOm1ufB8eeEVU5vJo6oEUW0P+A2TgRDa/rD7WPGnASzBq/3teWZdHmvCc5pqWu
0lwMrVSRh6u4DT2hbURHegQX/CJsF92FsKQEwehk2aSszwrLPEPnuxh8bN9tzDBr
pzz7ZKs0cYwd2ksrXt+LswKBgH3pDOmFWXVD3Oe3hm7VxJtEOOhByo1AxhefgL4X
NX1zYYvhuOD0HvjbCKpUIXiZZwm61T2hHoZPOXz91zgHO8K5TS1WXyDqGFAXAwo7
8PuH62f0Kv0aVqxpSlnxAXjVkYVcO+3hi7/51PmScQOtZLxF/26HEYJsWzWMz+Ip
YJQnAoGBAMc7MFibP9H3i4tlPIQ+z0fvHC4QQhKsbdS1VFLWHg77pxnc0ZvcAjmY
YtIDwO5A1cpIDd6oSea3C6wfNbhu41Gne6ELsdeuSTA6keMTjCGdAfPJAkCw5+Fk
wQJ7/RaQGgXdhrAKCDTOl3stAvXTUTx3YAGsxRo5EWzJnRk4DuxB
-----END RSA PRIVATE KEY-----
"
  }

  file{ "ssh-public":
    ensure => "file",
    path => "/home/vagrant/.ssh/id_rsa.pub",
    owner => "vagrant",
    group => "vagrant",
    content => "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZh2feJhGBHjPDAsbqb4sRfqaf8wU8XqEwk2+4cCO670+zT92ppzKqrxCRZ9dJytJa5XoGD3y6ssuaIYOx9dN3XNKCEcqiRnU1vfBqlU2drPH6eHdH+pyu/AoEObbUE/CWe0/xxRJzq0VofyxGylC6z3dxlNaxfAmyA4/BC8vu06Vp1rYzzXKwZ1XKA+wP4/aSCepoQXIpqTLKIPHaU0e+vQ/FQNmAlMBBWftNM5PhVtmi3cuDTO5/10QvJfU5n6z8wSuY5yodOSqZNDrHW6I6VnIfitmB80jVdoVnsv2l3+OmNcutEgFnCVYeF5Gkce2R6lBo+C1lur++pnXeSCsV vagrant@workflow
"
  }

  exec { "permissions_home":
    command => "/bin/chmod 777 /home",
  }

  exec{ "workflow_test":
      command   => "/usr/bin/git clone git@github.com:h-nuschke/workflow_test.git /home/workflow_test",
      cwd => "/home",
      user  => "vagrant",
      creates => "/home/workflow_test",
      require => [
        Package['packages'],
        File['ssh-config'],
        File['ssh-private'],
        File['ssh-public'],
        Exec['permissions_home'],
      ],
  }

}

class { "workflow": }
