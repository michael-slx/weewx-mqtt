Vagrant.configure("2") do |config|
  config.vm.box = "michael-slx/arch64-develop"

  config.vm.hostname = "vm-weewx-mqtt-test"
  config.vm.network "forwarded_port", guest: 1883, host: 1883
  config.vm.network "forwarded_port", guest: 9001, host: 9001

  config.vm.provider "virtualbox" do |v|
    v.memory = 8192
    v.cpus = 8
  end

  config.vm.provision :shell, path: "vm/provision.sh", privileged: false, keep_color: true
end
