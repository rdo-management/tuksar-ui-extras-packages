%global srcname tuskar-ui-extras

Name:           openstack-tuskar-ui-extras
Version:        XXX
Release:        XXX{?dist}
Summary:        Additional plugins for Tuskar-ui

License:        ASL 2.0
# URL:            https://github.com/stackforge/%{srcname}/
# FIXME: tarball generated (the one provided by github fails to build)
# git clone https://github.com/stackforge/tuskar-ui-extras
# make source
# Source0:        %{srcname}-%{version}.tar.gz
URL:            https://github.com/rdo-management/%{srcname}
Source0:        https://github.com/rdo-management/%{srcname}/archive/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
Requires:       openstack-tuskar-ui
Requires:       python-oauthlib
Requires:       python-requests-oauthlib


%description
Additional plugins for Tuskar-ui
- Tuskar-UI Boxes is a plugin for the Tuskar-UI application
that improves the looks of the deployment overview page, by
visualising the nodes to be deployed in a form of small colored boxes.

- Tuskar-UI Sat6 is a plugin for the Tuskar-UI application
that adds integration with Red Hat's Satellite 6 service.7

%prep
%setup -q -n %{srcname}-%{upstream_version}
rm requirements.txt test-requirements.txt


%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
install -d -m 0755 %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
install -d -m 0755 %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
cp _60_tuskar_boxes.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_60_tuskar_boxes.py
cp _60_tuskar_sat_ui.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_60_tuskar_sat_ui.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_60_tuskar_boxes.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_tuskar_boxes.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_60_tuskar_sat_ui.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_tuskar_sat_ui.py

# Move static files to horizon. These require that you compile them again
# post install { python manage.py compress }
# This might be possible to replace with "python %{buildroot}%{_datadir}/openstack-dashboard/manage.py collectstatic --noinput"
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/static/tuskar_boxes
cp -r tuskar_ui_extras/tuskar_boxes/static/tuskar_boxes/* %{buildroot}%{_datadir}/openstack-dashboard/static/tuskar_boxes/

# Compress static files
%{__python2} %{buildroot}%{_datadir}/openstack-dashboard/manage.py compress --force

%files
%doc README.rst ChangeLog
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{python2_sitelib}/*
%{_sysconfdir}/openstack-dashboard/enabled/_60_tuskar_boxes.py*
%{_sysconfdir}/openstack-dashboard/enabled/_60_tuskar_sat_ui.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_tuskar_boxes.py
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_tuskar_sat_ui.py



%changelog
* Mon Mar 16 2015 Jiri Tomasek <jtomasek@redhat.com> - 0.0.1-1
- Initial package
