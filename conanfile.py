import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class JemallocConan(ConanFile):
    name = "jemalloc"
    sha256 = "4814781d395b0ef093b21a08e8e6e0bd3dab8762f9935bbfb71679b0dea7c3e9"

    version = "5.0.1"
    license = "BSD"
    url = "https://github.com/ess-dmsc/conan-jemalloc"
    description = ("jemalloc is a general purpose malloc(3) implementation "
                   "that emphasizes fragmentation avoidance and scalable "
                   "concurrency support")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    folder_name = "{}-{}".format(name, version)
    archive_name = "{}.tar.bz2".format(folder_name)

    def source(self):
        tools.download(
            "https://github.com/jemalloc/jemalloc/releases/download/{}/{}".format(
                self.version,
                self.archive_name
            ),
            self.archive_name
        )
        tools.check_sha256(self.archive_name, self.sha256)
        tools.unzip(self.archive_name)
        os.unlink(self.archive_name)

    def build(self):
        configure_args = [
            "--prefix="
        ]

        if self.settings.build_type == "Debug":
            configure_args.append("--enable-debug")

        env_build = AutoToolsBuildEnvironment(self)
        env_build.configure(
            configure_dir=self.folder_name,
            args=configure_args
        )

        env_build.make()

        os.mkdir("install")
        cwd = os.getcwd()
        destdir = os.path.join(cwd, "install")
        env_build.make(args=["install_bin", "DESTDIR="+destdir])
        env_build.make(args=["install_include", "DESTDIR="+destdir])
        if self.options.shared:
            env_build.make(args=["install_lib_shared", "DESTDIR="+destdir])
        else:
            env_build.make(args=["install_lib_static", "DESTDIR="+destdir])

        os.chdir(self.folder_name)
        os.rename("COPYING", "LICENSE.jemalloc")
        os.chdir(cwd)

    def package(self):
        self.copy("*", dst="bin", src="install/bin")
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="lib", src="install/lib")
        self.copy("LICENSE.*", src=self.folder_name)
        self.copy("CHANGES.*", src=self.folder_name)

    def package_info(self):
        self.cpp_info.libs = ["jemalloc"]
