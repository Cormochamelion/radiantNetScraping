(use-modules (guix packages)
             (guix download)
             (guix git-download)
             (guix hg-download)
             (guix build-system r)
             (guix build-system python)
             (guix build-system pyproject)
             (guix licenses))

(define-public r-unigd
  (package
    (name "r-unigd")
    (version "0.1.1")
    (source (origin
              (method url-fetch)
              (uri (cran-uri "unigd" version))
              (sha256
               (base32
                "0q6nix6pqjg7adfyisg6zn7hzwkdmz1dhd34c6a58dsg2yq1qh1a"))))
    (properties `((upstream-name . "unigd")))
    (build-system r-build-system)
    (inputs (list (specification->package "cairo")
                  (specification->package "fontconfig")
                  (specification->package "freetype")
                  (specification->package "libpng")
                  (specification->package "zlib")))
    (propagated-inputs (list (specification->package "r-cpp11")
                             (specification->package "r-systemfonts")))
    (native-inputs (list (specification->package "pkg-config")
                         (specification->package "r-knitr")))
    (home-page "https://github.com/nx10/unigd")
    (synopsis "Universal Graphics Device")
    (description
     "This package provides a unified R graphics backend.  Render R graphics fast and
easy to many common file formats.  Provides a thread safe C interface for
asynchronous rendering of R graphics.")
    (license gpl2+)))

(define-public r-asioheaders
  (package
    (name "r-asioheaders")
    (version "1.22.1-2")
    (source (origin
              (method url-fetch)
              (uri (cran-uri "AsioHeaders" version))
              (sha256
               (base32
                "192qxayrpvi02wrqq2h5cjc92aaxrsgw7z32r8qk5imqg3mc0a8n"))))
    (properties `((upstream-name . "AsioHeaders")))
    (build-system r-build-system)
    (home-page "https://github.com/eddelbuettel/asioheaders")
    (synopsis "'Asio' C++ Header Files")
    (description
     "Asio is a cross-platform C++ library for network and low-level I/O programming
that provides developers with a consistent asynchronous model using a modern C++
approach.  It is also included in Boost but requires linking when used with
Boost.  Standalone it can be used header-only (provided a recent compiler).
Asio is written and maintained by Christopher M. Kohlhoff, and released under
the Boost Software License', Version 1.0.")
    (license (fsdg-compatible "BSL-1.0"))))

(define-public r-httpgd
  (package
    (name "r-httpgd")
    (version "2.0.1")
    (source (origin
              (method url-fetch)
              (uri (cran-uri "httpgd" version))
              (sha256
               (base32
                "14i358r0pix6xl0i3byarasa6sry3qcajj6p49rlk7p4gw4lh85c"))))
    (properties `((upstream-name . "httpgd")))
    (build-system r-build-system)
    (propagated-inputs (list r-asioheaders
                             r-unigd
                             (specification->package "r-cpp11")))
    (native-inputs (list (specification->package "r-knitr")))
    (home-page "https://github.com/nx10/httpgd")
    (synopsis "'HTTP' Server Graphics Device")
    (description
     "This package provides a graphics device for R that is accessible via network
protocols.  This package was created to make it easier to embed live R graphics
in integrated development environments and other applications.  The included
HTML/JavaScript client (plot viewer) aims to provide a better overall user
experience when dealing with R graphics.  The device asynchronously serves
graphics via HTTP and WebSockets'.")
    (license gpl2+)))

(define r-vscdebugger
  (let ((commit "c44a5393ae4b2682eb72c7f45458ec269fe9da56")
        (revision "1"))
    (package
      (name "r-vscdebugger")
      (version (git-version "0.5.3" revision commit))
      (source (origin
                (method git-fetch)
                (uri (git-reference
                      (url "https://github.com/ManuelHentschel/vscDebugger")
                      (commit commit)))
                (file-name (git-file-name name version))
                (sha256
                 (base32
                  "08ic9mr4n9n0grsil1lx51j6w61lcfydmqnfmb8y230faiink0xv"))))
      (properties `((upstream-name . "vscDebugger")))
      (build-system r-build-system)
      (propagated-inputs (list (specification->package "r-jsonlite")
                               (specification->package "r-r6")))
      (native-inputs (list (specification->package "r-knitr")))
      (home-page "https://github.com/ManuelHentschel/vscDebugger")
      (synopsis "Support for Visual Studio Code Debugger")
      (description
       "This package provides support for a visual studio code debugger")
      (license expat))))

(packages->manifest
  (append
    (list r-unigd
          r-httpgd
          r-vscdebugger)
    (map specification->package
      (list "r-jsonlite"
            "r-languageserver"
            "r-styler"))))