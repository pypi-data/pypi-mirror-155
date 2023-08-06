#pragma once

#include <Eigen/Core>

#include "Event.h"

class Sphere
{
public:
    Sphere() = default;

    Sphere(Eigen::Vector3d x_i, double r_i);

    //! @brief initialize physical members, user defined
    Sphere(Eigen::Vector3d x_i, Eigen::Vector3d v_i, double r_i, double gr_i, double m_i);
    void Update(double gtime);

    double R(double gtime) const
    {
        return r + gr * gtime;
    }

    double PerformCollision(Sphere& sj);

    Event PredictCollision(const Sphere& sj) const;

    // variables
    int cellId;
    int id;
    double lutime = 0; // last update time
    Eigen::Vector3d x; // position
    Eigen::Vector3d v; // velocity
    double r = 0.; // Sphere radius
    double gr = 0.; // Sphere growth rate
    double m = 1.; // Sphere mass
};
