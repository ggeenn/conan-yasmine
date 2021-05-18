from conans import ConanFile, CMake
from conans.tools import replace_in_file
import os

class sqlpp11Conan(ConanFile):
    name = 'yasmine'
    version = '1.0'
    license = 'BSD'
    author = 'Gennadii Marianychenko<argent.genesis@gmail.com>'
    url = 'https://github.com/ggeenn/conan-yasmine.git'
    description = 'Conan recipie for  SeadexGmbH/yasmine'
    generators = 'cmake'
    settings = 'os', 'compiler', 'build_type', 'arch'
    short_paths = True
    requires = "boost/1.74.0", "rapidjson/cci.20200410"

    def source(self):
        self.run('git clone -b "v1.4.1" --single-branch https://github.com/SeadexGmbH/yasmine.git')
        replace_in_file(
            'yasmine/CMakeLists.txt',
            'project(yasmine)',
            '''
project(yasmine)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(SX_BOOST_LIB_INCLUDE ${CONAN_INCLUDE_DIRS_BOOST})
set(SX_RAPIDJSON ${CONAN_INCLUDE_DIRS_RAPIDJSON})
'''
        )
        replace_in_file('yasmine/CMakeLists.txt',
                        'add_subdirectory(examples)', '')
        replace_in_file('yasmine/CMakeLists.txt',
                        'add_subdirectory(ygen)', '')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="yasmine")
        cmake.build()

    def package(self):
        dest = os.getenv("CONAN_IMPORT_PATH", "bin")
        print("IMPORT : " + dest)
        #self.copy('*', dst='scripts', src='sqlpp11/scripts')
        self.copy('*.hpp', dst='include/yasmine', src='yasmine/libyasmine/include')

        self.copy('*.hpp', dst='include/essentials', src='yasmine/externals/essentials/source/essentials/include/essentials')
        self.copy('*.hpp', dst='include/essentials/compatibility', src='yasmine/externals/essentials/source/essentials/include/essentials/compatibility')

        self.copy('*.hpp', dst='include/hermes', src='yasmine/externals/hermes/source/hermes/include/hermes')

        self.copy('*.so*', dst='lib', src='lib')
        self.copy('*', dst='bin', src='bin')

    def package_info(self):
        self.cpp_info.libs = ['yasmine']