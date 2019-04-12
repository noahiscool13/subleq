//
// Created by Noah Jadoenathmisier on 3/20/2019.
//

#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>


int main(int argc, const char *argv[]) {
    int value;
    char buf;
    std::vector<int> script_vec;

    FILE *file = fopen(argv[1], "r");

    if (file == NULL) {
        std::cout << "no such file.\n";
        return 0;
    }

    while (fscanf(file, "%d", &value) == 1) // While file can be read in ( You can increase numbers in text
    {
        script_vec.push_back(value);
    }

    int *memory = &script_vec[0];

    int pc = 0;

    while (pc >= 0) {
        if (memory[pc] == -1) {
            char buf;
            fgets(&buf, 1, stdin);
            //std::cin >> buf;
            memory[memory[pc + 1]] = (int) buf;
        } else if (memory[pc + 1] == -1) {
            std::cout << (char) memory[memory[pc]];
        } else {
            memory[memory[pc + 1]] -= memory[memory[pc]];
            if (memory[memory[pc + 1]] <= 0) {
                pc = memory[pc + 2];
                continue;
            }
        }
        pc += 3;
    }

    return 0;
}
