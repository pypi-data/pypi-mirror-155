#include <random>
#include <array>

class MaxwellBoltzmann
{
public:
    MaxwellBoltzmann(int seed = 0)
        : rng(seed)
        , uniform(-.5, .5)
    {
    }

    double Component(double T)
    {
        /* Taken from the original code... */
        if (T == 0)
            return 0;

        const double sigma_squared = T;
        const double sigma = std::sqrt(T);
        double dv = sigma / 1000.;

        double v = 0;
        double p = 0;

        double rnd = uniform(rng);
        if (rnd < 0)
        {
            rnd = -rnd;
            dv = -dv;
        }

        while (std::abs(p) < rnd)
        {
            p += dv * 0.39894228 * std::exp(-v * v / (2 * sigma_squared)) / sigma;
            v += dv;
        }
        return v;
    }

    std::array<double, 3> Vector(double T)
    {
        return {Component(T), Component(T), Component(T)};
    }

private:
    std::mt19937 rng;
    std::uniform_real_distribution<double> uniform;
};
