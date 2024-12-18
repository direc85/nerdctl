#
# spec file for package nerdctl
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


%global provider_prefix github.com/containerd/nerdctl
%global import_path     %{provider_prefix}

Name:           nerdctl
Version:        1.7.7
Release:        1
Summary:        Docker-compatible CLI for containerd
License:        Apache-2.0
URL:            https://github.com/containerd/nerdctl
Source:         %{name}-%{version}.tar.gz
Source1:        vendor.tar.gz
#BuildRequires:  golang(API) >= 1.21
BuildRequires:  golang(API) >= 1.23
Requires:       buildkit
Requires:       cni-plugins
Requires:       containerd
Requires:       iptables
Requires:       rootlesskit >= 1.0.0
Requires:       slirp4netns >= 0.4.0

%description
nerdctl is a Docker-compatible CLI for containerd.

%prep
%autosetup -a1 -n %{name}-%{version}/%{name}

%build
CGO_ENABLED=0
go build -mod=vendor -buildmode=pie -o _output/nerdctl %{provider_prefix}/cmd/nerdctl

%install
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 _output/nerdctl %{buildroot}%{_bindir}/nerdctl
install -m 0755 extras/rootless/containerd-rootless-setuptool.sh %{buildroot}%{_bindir}/containerd-rootless-setuptool.sh
install -m 0755 extras/rootless/containerd-rootless.sh %{buildroot}%{_bindir}/containerd-rootless.sh

%files
%license LICENSE
%doc docs/*.md
%{_bindir}/nerdctl
%{_bindir}/containerd-rootless-setuptool.sh
%{_bindir}/containerd-rootless.sh
