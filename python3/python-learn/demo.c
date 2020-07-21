#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv){
    int _size = 1;
    void* ptr = NULL;
    while (1)
    {
        _size = _size << 1;
        if (_size > 0X7FFFFFFFFFFFFFFF)
            _size = 1;
        ptr = malloc(_size);
    }
    return 0;
}
