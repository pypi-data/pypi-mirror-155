#pragma once

#include "Sphere.h"
#include <random>

class Box
{
public:
    Box(double lx, double ly, double lz);

    virtual ~Box() = default;

    virtual double Volume() const = 0;

    virtual Event PredictCollision(const Sphere& s) const = 0;

    virtual void PerformCollision(Sphere& s, int k) const = 0;

    virtual Eigen::Vector3d PositionInside(double r, std::mt19937& rng) const = 0;

    Eigen::Vector3d l;
};

class Cube : public Box
{
public:
    Cube(double lx, double ly, double lz);

    double Volume() const override;

    void PerformCollision(Sphere& s, int k) const override;

    Event PredictCollision(const Sphere& s) const override;

    Eigen::Vector3d PositionInside(double r, std::mt19937& rng) const override;
};
