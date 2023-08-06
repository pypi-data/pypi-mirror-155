#include "SubBoxes.h"

SubBoxes::SubBoxes(Eigen::Vector3d l)
    : SubBox3d(l.maxCoeff())
{
}

void SubBoxes::AddSphere(Sphere& s)
{
    s.cellId = Id(Idk(s.x[0]), Idk(s.x[1]), Idk(s.x[2]));
    for (int cell : SurroundingCells(s.cellId))
        Get(cell).Add(s.id);
}

const std::vector<int>& SubBoxes::SurroundingCells(int cellId)
{
    auto cell = IJK(cellId);

    int xs = std::max(cell[0] - 1, 0);
    int ys = std::max(cell[1] - 1, 0);
    int zs = std::max(cell[2] - 1, 0);

    int xe = std::min(cell[0] + 1, ngrids - 1);
    int ye = std::min(cell[1] + 1, ngrids - 1);
    int ze = std::min(cell[2] + 1, ngrids - 1);

    v.clear();
    for (int x = xs; x <= xe; ++x)
        for (int y = ys; y <= ye; ++y)
            for (int z = zs; z <= ze; ++z)
                v.push_back(Id(x, y, z));
    return v;
}


void SubBoxes::PerformTransfer(Sphere& s, int k)
{
    if (boxes.size() <= 1)
        return;

    const int direction = std::copysign(1, s.v[k]);

    for (int cell : SurroundingCells(s.cellId))
        Get(cell).Remove(s.id);

    auto c = IJK(s.cellId);
    c[k] += direction;
    s.cellId = Id(c[0], c[1], c[2]);

    // AddSphere(s);
    for (int cell : SurroundingCells(s.cellId))
        Get(cell).Add(s.id);
}

Event SubBoxes::PredictTransfer(const Sphere& s) const
{
    Event e(dblINF, s.id, Event::Type::NONE);
    const auto cell = IJK(s.cellId);
    for (int k : {0, 1, 2})
        if (s.v[k] > 0) // subbox transfer right
        {
            const double x_wall = (cell[k] + 1) * l / ngrids;
            const double t = (x_wall - s.x[k]) / s.v[k];
            e = std::min(e, Event(t + s.lutime, s.id, Event::Type::TRANSFER, k));
        }
        else if (s.v[k] < 0) // subbox transfer left
        {
            const double x_wall = cell[k] * l / ngrids;
            const double t = (x_wall - s.x[k]) / s.v[k];
            e = std::min(e, Event(t + s.lutime, s.id, Event::Type::TRANSFER, k));
        }
    return e;
}

Event SubBoxes::PredictOutgrow(const Sphere& s) const
{
    if (s.gr == 0.)
        return Event::NoEvent(s.id);

    double outgrowtime = (.5 * l / ngrids - s.R(s.lutime)) / s.gr + s.lutime;
    return Event(outgrowtime, s.id, Event::Type::RESIZE_GRID);
}

const std::vector<int>& SubBoxes::Neighbors(const Sphere& s) const
{
    return Get(s.cellId).Entries();
}
