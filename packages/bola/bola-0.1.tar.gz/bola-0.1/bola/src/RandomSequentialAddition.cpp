#include "Simulation.h"
#include <iostream>
#include <random>

struct Cells : public SubBox3d
{
    Cells(double l)
        : SubBox3d(l)
    {
    }

    //! Adds the sphere at `s` with id `i`.
    void AddSphere(Eigen::Vector4d s, int i)
    {
        for (int id : Ids(s))
            boxes.at(id).Add(i);
    }


    //! Returns the cell ids of the cells intersected by sphere `s`.
    std::vector<int> Ids(Eigen::Vector4d s)
    {
        const int xs = Idk(s.x() - s[3]);
        const int ys = Idk(s.y() - s[3]);
        const int zs = Idk(s.z() - s[3]);

        const int xe = Idk(s.x() + s[3]);
        const int ye = Idk(s.y() + s[3]);
        const int ze = Idk(s.z() + s[3]);

        std::vector<int> ids;
        for (int x = xs; x <= xe; ++x)
            for (int y = ys; y <= ye; ++y)
                for (int z = zs; z <= ze; ++z)
                    ids.push_back(Id(x, y, z));
        return ids;
    }

    //! Resizes the subboxes by the radius of sphere `i`. This can involve refilling all subboxes which needs all the
    //! spheres positions and radii.
    void ResizeByRadius(const Eigen::MatrixX4d& spheres, int i)
    {
        int n = OptimalNGrids(spheres(i, 3));
        if (n != ngrids)
        {
            Resize(n);
            for (int j = 0; j < i; ++j)
                AddSphere(spheres.row(j), j);
        }
    }

    //! Performs an overlap check of sphere `i` with all surrounding ones.
    bool Overlaps(const Eigen::MatrixX4d& spheres, int i)
    {
        for (int id : Ids(spheres.row(i)))
        {
            for (int j : Get(id).Entries())
            {
                double d2 = (spheres.block<1, 3>(i, 0) - spheres.block<1, 3>(j, 0)).squaredNorm();
                double dr = spheres(i, 3) + spheres(j, 3);
                if (d2 < dr * dr)
                    return true;
            }
        }
        return false;
    }
};


std::pair<Eigen::MatrixX4d, Eigen::VectorXi> RSA(Eigen::VectorXd radii, const Box& box, int seed, int maxTries,
                                                 bool progress)
{
    std::mt19937 rng(seed);
    Cells cells(box.l.maxCoeff());

    const int N = radii.rows();

    Eigen::VectorXi tries = Eigen::VectorXi::Zero(N);
    Eigen::MatrixX4d spheres(N, 4);

    for (int i = 0; i < N; ++i)
    {
        double r = radii[i];
        spheres(i, 3) = r;
        cells.ResizeByRadius(spheres, i);

        do
        {
            tries[i]++;
            spheres.block<1, 3>(i, 0) = box.PositionInside(r, rng);

            if (tries[i] > maxTries)
                throw std::runtime_error("Could not find empty random spot after " + std::to_string(maxTries) +
                                         " overlap checks.");

        } while (cells.Overlaps(spheres, i));
        cells.AddSphere(spheres.row(i), i);

        const int barWidth = 60;
        if (progress)
        {
            int pos = i * barWidth / N;
            for (int j = 0; j < barWidth; ++j)
            {
                if (j < pos)
                    std::cout << "#";
                else if (j == pos)
                    std::cout << ">";
                else
                    std::cout << " ";
            }
            std::cout << "| " << int(100. * i / N) << " %\r";
            std::cout.flush();
        }
    }
    return {spheres, tries};
}

