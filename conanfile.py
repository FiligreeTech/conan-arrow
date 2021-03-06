from conans import ConanFile, CMake, tools

class ArrowConan(ConanFile):
    name = "arrow"
    version = "0.15.1"
    license = "Apache-2.0"
    url = "https://arrow.apache.org/"
    description = "Apache arrow"
    topics = ("apache", "arrow")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires="boost/1.71.0@conan/stable"

    def source(self):
        if self.settings.os == "Linux":
            self.run("sudo apt update && sudo apt install -y flex bison")
        self.run("git clone https://github.com/apache/arrow.git")
        self.run("cd arrow && git checkout apache-arrow-" + ArrowConan.version)

        tools.replace_in_file("arrow/cpp/CMakeLists.txt",
                              'project(arrow VERSION "${ARROW_BASE_VERSION}")',
                              '''project(arrow VERSION "${ARROW_BASE_VERSION}")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        tools.replace_in_file("arrow/cpp/cmake_modules/SetupCxxFlags.cmake",
                              'set(CXX_COMMON_FLAGS "${CXX_COMMON_FLAGS} -Wall -Wextra -Wdocumentation',
                              'set(CXX_COMMON_FLAGS "${CXX_COMMON_FLAGS} -Wall -Wextra')

    def configure_cmake(self):
        generator = "Ninja" if self.settings.os == "Windows" else None
        cmake = CMake(self, generator=generator)
        cmake.vebose = True
        cmake.definitions["ARROW_JEMALLOC"]="OFF"
        cmake.definitions["ARROW_BUILD_STATIC"]="ON"
        if self.settings.os == "Linux":
            cmake.definitions["ARROW_PARQUET"]="ON"
        cmake.definitions["ARROW_BUILD_SHARED"]="OFF"
        cmake.definitions["ARROW_BUILD_TESTS"]="OFF"
        cmake.definitions["ARROW_BOOST_USE_SHARED"]="OFF"
        cmake.definitions["ARROW_COMPUTE"]="OFF"
        cmake.definitions["ARROW_IPC"]="OFF"
        cmake.definitions["ARROW_HDFS"]="OFF"
        cmake.definitions["ARROW_BUILD_UTILITIES"]="OFF"
        cmake.definitions["ARROW_WITH_BROTLI"]="OFF"
        cmake.definitions["ARROW_WITH_LZ4"]="OFF"
        cmake.definitions["ARROW_WITH_SNAPPY"]="OFF"
        cmake.definitions["ARROW_WITH_ZLIB"]="OFF"
        cmake.definitions["ARROW_WITH_ZSTD"]="OFF"
        cmake.definitions["ARROW_USE_GLOG"]="OFF"
        if self.settings.os == "Windows":
            cmake.definitions["CMAKE_BUILD_TYPE"]=str(self.settings.build_type)

        cmake.configure(source_folder="arrow/cpp")
        return cmake

    def build(self):
        self.configure_cmake().build()

    def package(self):
        self.configure_cmake().install()

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["arrow_static"]
        else:
            self.cpp_info.libs = ["arrow"]
