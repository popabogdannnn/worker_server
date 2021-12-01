sudo mkdir -p /sys/fs/cgroup/cpuacct/ia-sandbox/
sudo mkdir -p /sys/fs/cgroup/memory/ia-sandbox/
sudo mkdir -p /sys/fs/cgroup/pids/ia-sandbox/

sudo chown -R bogdan:bogdan /sys/fs/cgroup/cpuacct/ia-sandbox
sudo chown -R bogdan:bogdan /sys/fs/cgroup/memory/ia-sandbox
sudo chown -R bogdan:bogdan /sys/fs/cgroup/pids/ia-sandbox

mkdir eval/jail/
sudo mount -t tmpfs -o size=1024m swap eval/jail

echo "0" | sudo tee /sys/kernel/mm/transparent_hugepage/khugepaged/defrag
echo "madvise" | sudo tee /sys/kernel/mm/transparent_hugepage/defrag
echo "madvise" | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

sudo sysctl kernel.randomize_va_space=0
sudo swapoff -a