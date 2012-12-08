Summary: A text formatting package based on SGML
Name: linuxdoc-tools
Obsoletes: linuxdoc-sgml
Version: 0.9.21
Release: %mkrel 15
License: Freely distributable
Group: Publishing
Source: http://people.debian.org/~sano/linuxdoc-tools/archives/%{name}_%{version}.tar.bz2
Patch0: linuxdoc-tools-0.9.21-letter.patch
Patch1: linuxdoc-tools-0.9.20-strip.patch
Patch2: linuxdoc-tools-ifpdf.patch
Requires: jade
Requires: docbook-utils
#gw needed by sgml2info
Requires: texinfo
Url: http://people.debian.org/~sano/linuxdoc-tools/
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires:	flex
BuildRequires:	openjade
BuildRequires:	sgml-common
BuildRequires:	groff-for-man
Requires: tetex-latex gawk groff
Provides: sgml-tools
Provides: linuxdoc-sgml

%description
Linuxdoc-tools is a text formatting suite based on SGML (Standard
Generalized Markup Language), using the LinuxDoc document type.
Linuxdoc-tools allows you to produce LaTeX, HTML, GNU info, LyX, RTF,
plain text (via groff), and other format outputs from a single SGML
source.  Linuxdoc-tools is intended for writing technical software
documentation.

%prep
%setup -q
%patch0 -p1 -b .letter
%patch1 -p1 -b .strip
%patch2 -p1 -b .ifpdf

%build
%configure2_5x --with-installed-nsgmls --with-installed-iso-entities
# Packaging brain-damage
( cd entity-map
  autoconf
  %configure2_5x
)
%make OPTIMIZE="%{optflags}"
perl -pi -e 's,\$main::prefix/share/sgml/iso-entities-8879.1986/iso-entities.cat,/usr/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           lib/LinuxDocTools.pm

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mv %{buildroot}%{_docdir}/%{name} %{buildroot}%{_docdir}/%{name}-%{version}
perl -pi -e 's,/usr/share/sgml/iso-entities-8879.1986/iso-entities.cat,\$main::prefix/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           %{buildroot}%{_datadir}/%{name}/LinuxDocTools.pm

# Some files need moving around.
rm -f %{buildroot}%{_datadir}/%{name}/epsf.*
rm -f %{buildroot}%{_datadir}/%{name}/url.sty
install -d %{buildroot}%{_datadir}/texmf/tex/latex/misc
mv %{buildroot}%{_datadir}/%{name}/*.sty \
	%{buildroot}%{_datadir}/texmf/tex/latex/misc

# Move perl modules to perl_vendorlib
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Text
mv $RPM_BUILD_ROOT%{_libdir}/perl5/Text/EntityMap.pm \
	$RPM_BUILD_ROOT%{perl_vendorlib}/Text/

cat > doc/COPYRIGHT <<EOF
(C) International Organization for Standardization 1986
Permission to copy in any form is granted for use with
conforming SGML systems and applications as defined in
ISO 8879, provided this notice is included in all copies.
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -x %{_bindir}/texhash ] && /usr/bin/env - %{_bindir}/texhash > /dev/null 2>&1
exit 0

%postun
[ -x %{_bindir}/texhash ] && /usr/bin/env - %{_bindir}/texhash > /dev/null 2>&1
exit 0

%files
%defattr (-,root,root)
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/entity-map
%{_datadir}/texmf/tex/latex/misc/*.sty
%{perl_vendorlib}/Text/*.pm
%{_mandir}/*/*



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.21-14mdv2011.0
+ Revision: 666081
- mass rebuild

* Thu Jul 22 2010 Funda Wang <fwang@mandriva.org> 0.9.21-13mdv2011.0
+ Revision: 557031
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.21-12mdv2010.1
+ Revision: 520143
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.9.21-11mdv2010.0
+ Revision: 425981
- rebuild

* Fri Apr 10 2009 Funda Wang <fwang@mandriva.org> 0.9.21-10mdv2009.1
+ Revision: 365706
- use configure2_5x
- rediff letter patch

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.9.21-9mdv2009.0
+ Revision: 223115
- rebuild

* Mon Jan 21 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.9.21-8mdv2008.1
+ Revision: 155506
- add missing dep on texinfo

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.9.21-7mdv2008.1
+ Revision: 152855
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sat Jan 28 2006 Olivier Blin <oblin@mandriva.com> 0.9.21-5mdk
- buildrequires groff-for-man or else sgml2txt is likely to be unusable
  (and can for example break pam build)

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.9.21-4mdk
- Rebuild

* Wed Mar 23 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.9.21-3mdk
- Added Patch2, for having pdflatex detection more robust.

* Tue Oct 26 2004 Camille Begnis <camille@mandrakesoft.com> 0.9.21-2mdk
- Rebuild
- Source URL is broken, can't find any.

* Fri Aug 08 2003 <camille@ke.mandrakesoft.com> 0.9.21-1mdk
- 0.9.21
- removed Obsoletes: sgml-tools
- added Requires: docbook-utils

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.9.20-5mdk
- rebuild

