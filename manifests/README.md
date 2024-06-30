# Analytix Scrapy Cluster Configuration/Setup

## Cluster Setup
High availability MicroK8s cluster with OpenEBS provisioning
and failure-aware domains 

Install Microk8s/enable SSH, then establish master node and join leaf nodes

NOTE: Ensure each node has unique hostname

```commandline
sudo hostnamectl set-hostname <unique hostname>
sudo reboot
```

Enable the following addons:
* ArgoCD
* CoreDNS
* Ingress
* Docker registry
* Mayastor (production-ready OpenEBS volume provisoning)

Enable high availability cluster settings

## Application Installation:
helm install scrapy . -n scrapy --create-namespace
