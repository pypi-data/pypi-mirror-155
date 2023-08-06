#pragma once

#include "SubBox3d.h"
#include "Sphere.h"

class SubBoxes : public SubBox3d
{
public:
    SubBoxes(Eigen::Vector3d l);

    void AddSphere(Sphere& s);

    Event PredictTransfer(const Sphere& s) const;

    Event PredictOutgrow(const Sphere& s) const;

    void PerformTransfer(Sphere& s, int k);

    const std::vector<int>& Neighbors(const Sphere& s) const;

private:
    const std::vector<int>& SurroundingCells(int id);

    std::vector<int> v; // avoid reallocation in this.SurroundingCells()
};
