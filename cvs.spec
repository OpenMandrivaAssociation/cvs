%define __requires_exceptions tcsh\\|/bin/csh
%global __requires_exclude_from ^/usr/share/cvs/contrib/
%define debug_package %nil

%define _disable_lto 1

Summary:	A version control system
Name:		cvs
Version:	1.12.13
Release:	33
License:	GPL
Group:		Development/Other
Url:		http://www.nongnu.org/cvs/
Source0:	http://ftp.gnu.org/non-gnu/cvs/source/feature/%{version}/%{name}-%{version}.tar.bz2
Source1:	http://ftp.gnu.org/non-gnu/cvs/source/feature/%{version}/%{name}-%{version}.tar.bz2.sig
Source2: 	cvspserver
Source3: 	cvs.conf
Source4: 	cvs-xinetd
Source5:	cvs.rpmlintrc
Patch0:		cvs-1.11.19-varargs.patch
Patch2: 	cvs-1.12.13-errno.patch
Patch4:		cvs-1.11.1-newline.patch
Patch5:		cvs-1.11.4-first-login.patch
Patch6:		cvs-1.11.19-cvsbug.patch
# Patch from cvs of cvs: 
# http://savannah.nongnu.org/bugs/?func=detailitem&item_id=14840
Patch7:		cvs-zlib-read.patch
Patch8:		cvs-1.12.13-format_not_a_string_literal_and_no_format_arguments.diff
Patch9:		cvs-1.12.13-CVE-2012-0804.diff
Patch10:	cvs-aarch64-detection.patch

BuildRequires:	groff
BuildRequires:	tcsh
BuildRequires:	vim-minimal
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	gettext-devel
Requires:	openssh-clients

%description
CVS means Concurrent Version System; it is a version control
system which can record the history of your files (usually,
but not always, source code). CVS only stores the differences
between versions, instead of every version of every file
you've ever created. CVS also keeps a log of who, when and
why changes occurred, among other aspects.

CVS is very helpful for managing releases and controlling
the concurrent editing of source files among multiple
authors. Instead of providing version control for a
collection of files in a single directory, CVS provides
version control for a hierarchical collection of
directories consisting of revision controlled files.

These directories and files can then be combined together
to form a software release.

Install the cvs package if you need to use a version
control system.

%prep
%setup -q

%patch0 -p1 -b .varargs
%patch2 -p1 -b .errno
%patch4 -p1 -b .newline
%patch5 -p1 -b .first-login
%patch6 -p1 -b .cvsbug
%patch7 -p0 -b .zlib-read
%patch8 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch9 -p0 -b .CVE-2012-0804
%patch10 -p1 -b .aarch64

# make autoreconf happy
sed -i -e 's/AM_GNU_GETTEXT_VERSION.*/AM_GNU_GETTEXT_REQUIRE_VERSION(\[0.18.0\])/' configure.in
sed -i -e 's/gl_AC_TYPE_LONG_LONG/AC_TYPE_LONG_LONG_INT/' m4/* configure.in

%build
# http://qa.mandriva.com/show_bug.cgi?id=31848
%define _fortify_cflags %{nil}

export SENDMAIL="%{_sbindir}/sendmail"

%serverbuild

export CXXFLAGS="${CFLAGS}"
export CCFLAGS="${CFLAGS}"

# to recognize aarch64
autoreconf -vfi

%configure \
	--with-tmpdir=/tmp \
	--with-external-zlib \
	--with-editor=vim

%make_build

%install
install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_sysconfdir}/cvs
install -d %{buildroot}%{_sbindir}

%make_install

install -m0755 %{SOURCE2} %{buildroot}%{_sbindir}/
install -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/cvs
install -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xinetd.d/%{name}

%files
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%dir %{_sysconfdir}/cvs
%config(noreplace) %{_sysconfdir}/cvs/cvs.conf
%{_bindir}/cvs
%{_bindir}/cvsbug
%{_bindir}/rcs2log
%{_sbindir}/cvspserver
%{_infodir}/cvs*
%{_datadir}/cvs
%{_mandir}/man1/cvs.1*
%{_mandir}/man5/cvs.5*
%{_mandir}/man8/cvsbug.8*
