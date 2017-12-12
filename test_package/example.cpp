#include <iostream>
#include <jemalloc/jemalloc.h>

int main() {
    std::cout << JEMALLOC_VERSION << '\n';
    return 0;
}
