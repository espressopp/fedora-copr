Name:           espressopp
Version:        2.0.2
Release:        1%{?dist}
Summary:        Parallel simulation software for soft matter research
License:        GPLv3+
Url:            http://www.espresso-pp.de/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  fftw-devel
BuildRequires:  python2-numpy
BuildRequires:  python2-devel
BuildRequires:  boost-devel
BuildRequires:  gromacs-devel
BuildRequires:  mpich-devel
BuildRequires:  boost-mpich-devel
BuildRequires:  openmpi-devel
BuildRequires:  boost-openmpi-devel
%if 0%{?fedora} >= 29
BuildRequires:  boost-python2-devel
%else
BuildRequires:  boost-python-devel
%endif
Requires:       python2-h5py
BuildRequires:  python2-h5py

%description
ESPResSo++ is an extensible, flexible, parallel simulation software
for soft matter research. It is a software package for the
scientific simulation and analysis of coarse-grained atomistic or bead-spring
models as they are used in soft matter research. ESPResSo and ESPResSo++ have
common roots and share parts of the developer/user community. However, their
development is independent and they are different software packages.

%package -n python2-%{name}-openmpi
Summary:        Parallel simulation software for soft matter research, Open MPI version
Requires:       openmpi
BuildRequires:  python2-mpi4py-openmpi
Requires:       python2-mpi4py-openmpi
%{?python_provide:%python_provide python2-%{name}-openmpi}
%description -n python2-%{name}-openmpi
ESPResSo++ is an extensible, flexible, parallel simulation software
for soft matter research. It is a software package for the
scientific simulation and analysis of coarse-grained atomistic or bead-spring
models as they are used in soft matter research. ESPResSo and ESPResSo++ have
common roots and share parts of the developer/user community. However, their
development is independent and they are different software packages.

This package contains %{name} compiled against Open MPI.

%package -n python2-%{name}-mpich
Summary:        Parallel simulation software for soft matter research, MPICH version
Requires:       mpich
BuildRequires:  python2-mpi4py-mpich
Requires:       python2-mpi4py-mpich
%{?python_provide:%python_provide python2-%{name}-mpich}
%description -n python2-%{name}-mpich
ESPResSo++ is an extensible, flexible, parallel simulation software
for soft matter research. It is a software package for the
scientific simulation and analysis of coarse-grained atomistic or bead-spring
models as they are used in soft matter research. ESPResSo and ESPResSo++ have
common roots and share parts of the developer/user community. However, their
development is independent and they are different software packages.

This package contains %{name} compiled against MPICH.

%prep
%setup -q

# Remove bundled libs
rm -rf contrib/boost contrib/mpi4py

%build
mkdir openmpi mpich

pushd openmpi
%{_openmpi_load}
%{cmake3} -DWITH_RC_FILES=OFF -DEXTERNAL_BOOST=ON -DEXTERNAL_MPI4PY=ON -DWITH_XTC=ON -DPYTHON_INSTDIR=${MPI_PYTHON2_SITEARCH} ..
%make_build
%{_openmpi_unload}
popd

pushd mpich
%{_mpich_load}
%{cmake3} -DWITH_RC_FILES=OFF -DEXTERNAL_BOOST=ON -DEXTERNAL_MPI4PY=ON -DWITH_XTC=ON -DPYTHON_INSTDIR=${MPI_PYTHON2_SITEARCH} ..
%make_build
%{_mpich_unload}
popd

%install
%make_install -C openmpi
%make_install -C mpich

%check
%if 0%{?fedora} < 29
%ifarch %ix86
# roundoff error in old numpy on i386
%global testargs ARGS='-E \\(MTSAdResS\\|dump_xtc\\)'
%endif
%endif

%{_openmpi_load}
make -C openmpi test CTEST_OUTPUT_ON_FAILURE=1 %{?testargs}
%{_openmpi_unload}
%{_mpich_load}
make -C mpich test CTEST_OUTPUT_ON_FAILURE=1 %{?testargs}
%{_mpich_unload}

%files -n python2-%{name}-openmpi
%doc AUTHORS NEWS README.md COPYING
%{python2_sitearch}/openmpi/%{name}
%{python2_sitearch}/openmpi/_%{name}.so

%files -n python2-%{name}-mpich
%doc AUTHORS NEWS README.md COPYING
%{python2_sitearch}/mpich/%{name}
%{python2_sitearch}/mpich/_%{name}.so

%changelog
* Wed Mar 13 2019 Christoph Junghans <junghans@votca.org> - 2.0.2-1
- version bump to v2.0.2

* Thu Feb 21 2019 Christoph Junghans <junghans@votca.org> - 2.0.1-0
- initial import
