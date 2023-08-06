#include "Box.h"

Box::Box(double lx, double ly, double lz)
    : l(lx, ly, lz)
{
}

Cube::Cube(double lx, double ly, double lz)
    : Box(lx, ly, lz)
{
}

double Cube::Volume() const
{
    return l.prod();
}

void Cube::PerformCollision(Sphere& s, int k) const
{
    const double directed_gr = std::copysign(s.gr, s.v[k]);
    s.v[k] = -s.v[k] - 4. * directed_gr;
}

Event Cube::PredictCollision(const Sphere& s) const
{
    Event e(dblINF, s.id, Event::Type::NONE);
    for (int k : {0, 1, 2})
        if (s.v[k] > 0) // wall collision right
        {
            const double t = (l[k] - (s.x[k] + s.R(s.lutime))) / (s.v[k] + s.gr);
            e = std::min(e, Event(t + s.lutime, s.id, Event::Type::WALL, k));
        }
        else if (s.v[k] < 0) // wall collision left
        {
            const double t = -(s.x[k] - s.R(s.lutime)) / (s.v[k] - s.gr);
            e = std::min(e, Event(t + s.lutime, s.id, Event::Type::WALL, k));
        }
    return e;
}

Eigen::Vector3d Cube::PositionInside(double r, std::mt19937& rng) const
{
    double x = std::uniform_real_distribution<double>(r, l[0] - r)(rng);
    double y = std::uniform_real_distribution<double>(r, l[1] - r)(rng);
    double z = std::uniform_real_distribution<double>(r, l[2] - r)(rng);
    return {x, y, z};
}
