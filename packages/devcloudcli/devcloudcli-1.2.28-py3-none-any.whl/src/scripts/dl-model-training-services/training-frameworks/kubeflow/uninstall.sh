#!/bin/sh

# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

kubectl delete namespace kubeflow
microk8s reset
microk8s.disable dashboard dns
sudo snap remove microk8s

