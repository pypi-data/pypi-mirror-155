#include "Sphere.h"

#include <limits>

Sphere::Sphere(Eigen::Vector3d x_i, double r_i)
    : x(x_i)
    , r(r_i)
{
}

Sphere::Sphere(Eigen::Vector3d x_i, Eigen::Vector3d v_i, double r_i, double gr_i, double m_i)
    : x(x_i)
    , v(v_i)
    , r(r_i)
    , gr(gr_i)
    , m(m_i)
{
}

void Sphere::Update(double gtime)
{
    x += v * (gtime - lutime);
    lutime = gtime;
}

double Sphere::PerformCollision(Sphere& sj)
{
    assert(lutime == sj.lutime);
    Sphere& si = *this;

    // Check to see if a diameter apart
    double r_sum = si.R(lutime) + sj.R(lutime);
    double distance = (si.x - sj.x).squaredNorm() - r_sum * r_sum;
    if (distance > 10. * std::numeric_limits<double>::epsilon())
    {
        std::runtime_error("[PerformCollision] Spheres " + std::to_string(si.id) + " and " + std::to_string(sj.id) +
                           " are overlapping at t = " + std::to_string(lutime) +
                           ".\n Distance = " + std::to_string(distance));
    }

    // make unit vector out of displacement vector
    Eigen::Vector3d dhat = si.x - sj.x;
    double dhatmagnitude = dhat.norm();
    dhat /= dhatmagnitude;

    Eigen::Vector3d vipar = dhat * si.v.dot(dhat);
    Eigen::Vector3d vjpar = dhat * sj.v.dot(dhat);
    Eigen::Vector3d viperp = si.v - vipar;
    Eigen::Vector3d vjperp = sj.v - vjpar;

    si.v = vjpar + dhat * (si.gr + sj.gr) * 2 + viperp;
    sj.v = vipar - dhat * (si.gr + sj.gr) * 2 + vjperp;

    // momentum exchange
    double xvelocity = (si.v - sj.v).dot(dhat) - (si.gr + sj.gr);
    return xvelocity * dhatmagnitude * si.m * sj.m * 2 / (si.m + sj.m);
}

Event Sphere::PredictCollision(const Sphere& sj) const
{
    const Sphere& si = *this;

    const double t_ref = std::max(si.lutime, sj.lutime);

    const auto dx = si.x + si.v * (t_ref - si.lutime) - sj.x - sj.v * (t_ref - sj.lutime);
    const auto dv = si.v - sj.v;

    const double dr = si.R(t_ref) + sj.R(t_ref);
    const double dgr = si.gr + sj.gr;

    const double a = dv.squaredNorm() - dgr * dgr;
    const double b = dx.dot(dv) - dgr * dr;
    const double c = dx.squaredNorm() - dr * dr;

    if (c < -100. * std::numeric_limits<double>::epsilon())
    {
        std::runtime_error("[PredictCollision] Spheres " + std::to_string(si.id) + " and " + std::to_string(sj.id) +
                           " are overlapping at t = " + std::to_string(t_ref) + ".\n A = " + std::to_string(a) +
                           " B = " + std::to_string(b) + " C = " + std::to_string(c));
    }
    double det = b * b - a * c;

    if (det < -10. * std::numeric_limits<double>::epsilon())
        return Event::NoEvent(si.id);

    if (b < 0.)
    {
        det = std::max(det, 0.);
        return Event::SphereEvent(t_ref + c / (-b + std::sqrt(det)), si.id, sj.id);
    }

    if (a < 0.)
    {
        det = std::max(det, 0.);
        return Event::SphereEvent(t_ref - (b + std::sqrt(det)) / a, si.id, sj.id);
    }

    return Event::NoEvent(si.id);
}
