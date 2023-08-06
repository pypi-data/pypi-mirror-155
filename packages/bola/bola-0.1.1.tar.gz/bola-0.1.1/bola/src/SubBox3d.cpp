#include "SubBox3d.h"

SubBox3d::SubBox3d(double l)
    : l(l)
{
}

const SubBox& SubBox3d::Get(int id) const
{
    return boxes[id];
}


SubBox& SubBox3d::Get(int id)
{
    return boxes[id];
}

int SubBox3d::Id(int i, int j, int k) const
{
    return i * ngrids * ngrids + j * ngrids + k;
}

int SubBox3d::Idk(double x) const
{
    return static_cast<int>(x * ngrids / l);
}


void SubBox3d::Resize(int n)
{
    if (n > 200)
        throw std::runtime_error("n (" + std::to_string(n) + ") > 200. Too big.");
    ngrids = n;
    boxes.clear();
    boxes.resize(n * n * n);
}

int SubBox3d::OptimalNGrids(double r) const
{
    return static_cast<int>(l / (2. * r));
}

std::array<int, 3> SubBox3d::IJK(int id) const
{
    int i = id / (ngrids * ngrids);
    id -= i * ngrids * ngrids;
    int j = id / ngrids;
    int k = id % ngrids;
    return {{i, j, k}};
}
