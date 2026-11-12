#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	CFF table subroutinizer for FontTools
Summary(pl.UTF-8):	Generator podprocedur tablic CFF dla FontTools
Name:		python3-compreffor
Version:	0.6.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/compreffor/
Source0:	https://files.pythonhosted.org/packages/source/c/compreffor/compreffor-%{version}.tar.gz
# Source0-md5:	f8e33a2735018eab3bdbd93b5c8e1d02
Patch0:		compreffor-fonttools-glyphset.patch
URL:		https://pypi.org/project/compreffor/
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	python3-Cython >= 0.29.24
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
BuildRequires:	python3-setuptools_git_ls_files
%if %{with tests}
BuildRequires:	python3-fonttools >= 4
BuildRequires:	python3-pytest >= 2.8
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CFF table subroutinizer for FontTools.

%description -l pl.UTF-8
Generator podprocedur tablic CFF dla FontTools.

%prep
%setup -q -n compreffor-%{version}
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest --pyargs compreffor
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/compreffor
%dir %{py3_sitedir}/compreffor
%attr(755,root,root) %{py3_sitedir}/compreffor/_compreffor.cpython-*.so
%{py3_sitedir}/compreffor/*.py
%{py3_sitedir}/compreffor/__pycache__
# compreffor --check imports compreffor.test.util
%{py3_sitedir}/compreffor/test
%{py3_sitedir}/compreffor-%{version}-py*.egg-info
