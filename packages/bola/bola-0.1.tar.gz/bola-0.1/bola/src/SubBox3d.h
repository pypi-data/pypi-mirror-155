#pragma once
#include <vector>
#include <array>
#include "SubBox.h"

class SubBox3d
{
public:
    SubBox3d(double l);

    SubBox& Get(int cellId);

    const SubBox& Get(int cellId) const;

    int Id(int i, int j, int k) const;

    int Idk(double x) const;

    std::array<int, 3> IJK(int cellId) const;

    void Resize(int n);

    int OptimalNGrids(double r) const;


protected:
    std::vector<SubBox> boxes;
    int ngrids = 0;
    double l;
};
