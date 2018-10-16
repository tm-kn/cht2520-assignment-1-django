# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

Vagrant.configure(2) do |config|
  config.vm.box = "torchbox/wagtail-jessie64"
  config.vm.box_version = "~> 2.0"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true
  config.vm.provision :shell, :path => "vagrant/provision.sh", :args => "timetracker"
  config.ssh.forward_agent = true
end
