%define _requires_exceptions tcsh

Summary:	A version control system
Name:		cvs
Version:	1.12.13
Release:	%mkrel 6
License:	GPL
Group:		Development/Other
URL:		http://www.nongnu.org/cvs/
Source0:	http://ftp.gnu.org/non-gnu/cvs/source/stable/%{version}/cvs-%{version}.tar.bz2
Source1:	http://ftp.gnu.org/non-gnu/cvs/source/stable/%{version}/cvs-%{version}.tar.bz2.sig
Source2: 	cvspserver
Source3: 	cvs.conf
Source4: 	cvs-xinetd
Patch0:		cvs-1.11.19-varargs.patch
Patch2: 	cvs-1.12.13-errno.patch
Patch4:		cvs-1.11.1-newline.patch
Patch5:		cvs-1.11.4-first-login.patch
Patch6:		cvs-1.11.19-cvsbug.patch
# Patch from cvs of cvs: 
# http://savannah.nongnu.org/bugs/?func=detailitem&item_id=14840
Patch7:     cvs-zlib-read.patch
Requires:	openssh-clients
Requires(post):	info-install
Requires(preun): info-install
BuildRequires:	autoconf2.5
BuildRequires:	krb5-devel
BuildRequires:	tcsh
BuildRequires:	texinfo
BuildRequires:	zlib-devel
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips
BuildRequires:	groff
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%build
export SENDMAIL="%{_sbindir}/sendmail"

%serverbuild

export CFLAGS="%(echo %optflags | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')"
export CXXFLAGS="${CFLAGS}"
export CCFLAGS="${CFLAGS}"

%configure2_5x \
    --with-tmpdir=/tmp

%make

pushd doc
    make ps
    make info
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_sysconfdir}/cvs
install -d %{buildroot}%{_sbindir}

%makeinstall

install -m0755 %{SOURCE2} %{buildroot}%{_sbindir}/
install -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/cvs
install -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xinetd.d/%{name}

bzip2 -f doc/*.ps

# %check
# Disabling currently
# make check

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_install_info %{name}.info
%_install_info cvsclient.info

%preun
%_remove_install_info %{name}.info

%_remove_install_info cvsclient.info

%files
%defattr(-,root,root)
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README
%doc doc/*.ps.bz2
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



%{_sysconfdir}/cvs/cvs.conf.

* Fri Mar 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.10.7-5mdk
- group fix.

* Thu Nov 11 1999 Jeff Garzik <jgarzik@mandrakesoft.com>
- ...but keep experimental mmap patch in cooker

* Thu Nov 11 1999 Jeff Garzik <jgarzik@mandrakesoft.com>
- Build release, without experimental mmap patch

* Mon Oct 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch from Jeff <jgarzik@mandrakesoft.com> :
	src/client.c, src/import.c, src/filesubr.c, src/logmsg.c, src/server.c:
	* mmap support for local file read
	configure.in:
	* AC_PROG_CC handles AC_C_CROSS in modern autoconf, remove it
	* check for mmap()
	src/add.c, src/buffer.c, src/lock.c, src/modules.c, src/rcs.c,
	src/update.c, src/server.c:
	* zero variable to avoid [common, but sometimes spurious] compiler
	warning about an uninitialized variable
	src/client.c:
	* remove BROKEN_READWRITE_CONVERSION, dead feature.  The code used
	fread() to read file data not fgets(), so linefeeds were never
	translated anyway.
	src/cvs.h:
	* conditionally include sys/mman.h for mmap
	src/filesubr.c:
	* mmap support for local file read
	* optimize compare case where file sizes differ (do not open files at
	all)
	src/server.c:
	* update read_and_gzip() call
	src/server.h:
	* update read_and_gzip() prototype
	src/zlib.c:
	* update read_and_gzip() to optionally support reading from an input
	buffer instead of a file
	zlib/*.c:
	* const-ify input data pointer.  smart compilers can use this to further
	optimize
	

* Mon Aug 16 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 1.10.7

* Tue Jul 20 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- add french description from Gregus <gregus@etudiant.net>

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Merging with Redhat :
	* Wed Jul 14 1999 Jim Kingdon <http://developer.redhat.com>
	- add the patch to make 1.10.6 usable
  	(http://www.cyclic.com/cvs/dev-known.html).
	

* Wed May 19 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Fix several .spec bugs
- Update to 1.10.6

* Tue May 18 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Bzipped info files.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptations

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.5.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.4.

* Tue Oct 20 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.3.

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.2.

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- remove trailing characters from rcs2log mktemp args

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.1

* Mon Aug 31 1998 Jeff Johnson <jbj@redhat.com>
- fix race conditions in cvsbug/rcs2log

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.30.

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun  8 1998 Jeff Johnson <jbj@redhat.com>
- build root
- update to 1.9.28

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 29 1997 Otto Hammersmith <otto@redhat.com>
- added install-info stuff
- added changelog section
