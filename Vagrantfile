# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

Vagrant.configure(2) do |config|
  config.vm.box = "torchbox/wagtail-stretch64"
  config.vm.box_version = "~> 1.0"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision :shell, :path => "vagrant/provision.sh", :args => "timetracker"
  config.ssh.forward_agent = true
end
