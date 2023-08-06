#!/bin/sh

# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


sudo snap install microk8s --classic --channel=1.21/stable
sudo usermod -a -G microk8s $USER
newgrp microk8s
sudo chown -f -R $USER ~/.kube
microk8s enable dns storage ingress metallb:10.64.140.43-10.64.140.49
microk8s status --wait-ready
sudo snap install juju --classic
juju bootstrap microk8s --agent-version="2.9.22"
juju add-model kubeflow
juju deploy kubeflow-lite --trust
juju config dex-auth public-url=http://10.64.140.43.nip.io
juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io
read -p 'Username: ' uservar
read -sp 'Password: ' passvar
juju config dex-auth static-username= $uservar
juju config dex-auth static-password= $passvar
echo "http://10.64.140.43.nip.io"
