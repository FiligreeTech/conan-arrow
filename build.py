from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(archs=["x86_64"])
    #For c projects set pure_c to True to avoid building verisons for both libstdc++ and libc++
    builder.add_common_builds(pure_c=False)
    builder.remove_build_if(lambda build: build.settings.get("compiler.runtime") == "MT")
    builder.remove_build_if(lambda build: build.settings.get("compiler.runtime") == "MTd")
    builder.remove_build_if(lambda build: build.settings.get("compiler.version") == "14")
    builder.remove_build_if(lambda build: build.options.get("arrow:shared") == True)
    builder.run()
