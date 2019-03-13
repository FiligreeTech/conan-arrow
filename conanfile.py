from conans import ConanFile, CMake, tools


class ArrowConan(ConanFile):
    name = "arrow"
    version = "0.11.1"
    license = "Apache-2.0"
    url = "https://arrow.apache.org/"
    description = "Apache arrow"
    topics = ("apache", "arrow")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires="boost/1.68.0@conan/stable"

    def source(self):
        self.run("git clone https://github.com/apache/arrow.git")
        self.run("cd arrow && git checkout apache-arrow-0.11.1")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly

        tools.replace_in_file("arrow/cpp/CMakeLists.txt", 'project(arrow VERSION "${ARROW_BASE_VERSION}")',
                              '''project(arrow VERSION "${ARROW_BASE_VERSION}")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.vebose = True
        cmake.definitions["ARROW_BUILD_STATIC"]="ON"
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
        cmake.configure(source_folder="arrow/cpp")
        return cmake

    def build(self):
        self.configure_cmake().build()

    def package(self):
        self.configure_cmake().install()

    def package_info(self):
        self.cpp_info.libs = ["arrow"]


