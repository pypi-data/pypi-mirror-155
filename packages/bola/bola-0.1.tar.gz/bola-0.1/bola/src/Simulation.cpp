/*
   "Packing Hyperspheres in High-Dimensional Euclidean Spaces"
        M. Skoge, A. Donev, F. H. Stillinger and S. Torquato, 2006
*/

#include "Simulation.h"

#include <cmath>
#include <iostream>

Simulation::Simulation(const Box& box, std::vector<Sphere> spheres)
    : N(spheres.size())
    , box(box)
    , s(spheres)
    , nextevents(N)
    , cells(box.l)
    , h(nextevents)
{

    for (int i = 0; i < N; i++)
    {
        auto Error = [i](std::string msg, double value) {
            throw std::runtime_error("Sphere " + std::to_string(i) + ": " + msg + std::to_string(value));
        };
        if (s[i].r <= 0)
            Error("Radius must be > 0, not ", s[i].r);
        if (s[i].gr < 0)
            Error("Growth rate must be >) 0, not ", s[i].gr);
        if (s[i].m <= 0)
            Error("Mass must be > 0, not ", s[i].m);

        s[i].id = i;
    }

    ngrids = cells.OptimalNGrids(s.front().r);
    cells.Resize(ngrids);
    std::cout << ngrids << std::endl;

    AssignCells();
    SetInitialEvents();
}

std::vector<Sphere> ToSphereVector(Eigen::MatrixX4d sphereMatrix, Eigen::MatrixX3d velocities,
                                   Eigen::VectorXd growthRates, Eigen::VectorXd masses)
{
    const int N = sphereMatrix.rows();
    std::vector<Sphere> spheres(N);
    for (int i = 0; i < N; ++i)
    {
        auto& s = spheres[i];
        s.id = i;
        s.x = sphereMatrix.block<1, 3>(i, 0);
        s.r = sphereMatrix(i, 3);
        s.v = velocities.row(i);
        s.gr = growthRates[i];
        s.m = masses[i];
    }
    return spheres;
}

Simulation::Simulation(const Box& box, Eigen::MatrixX4d sphereMatrix, Eigen::MatrixX3d velocities,
                       Eigen::VectorXd growthRates, Eigen::VectorXd masses)
    : Simulation(box, ToSphereVector(sphereMatrix, velocities, growthRates, masses))
{
}


void Simulation::AssignCells()
{
    for (int i = 0; i < N; i++)
        cells.AddSphere(s[i]);
}

Event Simulation::PredictSphereVsWall(int i)
{
    return std::min(box.PredictCollision(s[i]), cells.PredictTransfer(s[i]));
}

void Simulation::SetInitialEvents()
{
    for (int i = 0; i < N; i++)
    {
        nextevents[i] = Event(gtime, i, Event::Type::NONE);
        h.insert(i);
    }
}

void Simulation::SetNextEvent(int i)
{
    Event o = cells.PredictOutgrow(s[i]);
    Event t = PredictSphereVsWall(i);
    Event c = FindNextCollision(i);

    Event e = std::min({o, t, c});
    e.time = std::max(e.time, gtime);

    if (e.type == Event::Type::SPHERE)
        CollisionChecker(e);

    nextevents[i] = e;
    h.downheap(1);
}

void Simulation::CollisionChecker(Event c)
{
    int i = c.i;
    int j = c.j;

    // j should have NO Event before collision with i!
    assert(c.time < nextevents[j].time);

    if (nextevents[j].type == Event::Type::SPHERE)
    {
        // j's next Event was collision so invalidate his collision partner
        int k = nextevents[j].j;
        nextevents[k].type = Event::Type::NONE;
    }

    // give collision cj to j
    nextevents[j] = Event(c.time, j, Event::Type::SPHERE, i);
    h.upheap(h.index[j]);
}

Event Simulation::FindNextCollision(int i)
{
    Event e(dblINF, i, Event::Type::NONE);
    for (int j : cells.Neighbors(s[i]))
    {
        if (i == j)
            continue;
        Event f = s[i].PredictCollision(s[j]);
        if (f.time < nextevents[j].time)
            e = std::min(e, f);
    }
    return e;
}

void Simulation::ProcessEvent()
{
    stats.n_events++;
    // Extract first Event from heap
    int i = h.extractmax(); // heap at (1)
    Event e = nextevents[i]; // current Event

    if (showEvents)
        std::cout << "[ProcessEvent]: " << e << "\n";

    switch (e.type)
    {
    case Event::Type::SPHERE:
        stats.n_collisions++;
        ProcessSphereVsSphere(e);
        SetNextEvent(i);

        // make sure collision was symmetric and invalidate j
        assert(nextevents[e.j].j == i and nextevents[e.j].time == gtime);
        nextevents[e.j].type = Event::Type::NONE;

        break;
    case Event::Type::NONE:
        stats.n_checks++;
        SetNextEvent(i);
        break;
    case Event::Type::RESIZE_GRID:
        gtime = e.time;
        Synchronize(false);
        ngrids = ngrids - 1;
        if (showResize)
            std::cout << "[ProcessEvent] Reduce  ngrids to " << ngrids << ".\n";
        ChangeNgrids(ngrids);
        h.downheap(1);
        break;
    case Event::Type::TRANSFER:
    case Event::Type::WALL:
        stats.n_transfers++;
        ProcessSphereVsWall(e);
        SetNextEvent(i);
        break;
    }
}

void Simulation::ProcessSphereVsSphere(Event e)
{
    gtime = e.time;
    s[e.i].Update(gtime);
    s[e.j].Update(gtime);
    xmomentum += s[e.i].PerformCollision(s[e.j]);
}

void Simulation::ProcessSphereVsWall(Event e)
{
    gtime = e.time;
    s[e.i].Update(gtime);

    if (e.type == Event::Type::TRANSFER)
        cells.PerformTransfer(s[e.i], e.j);
    else
        box.PerformCollision(s[e.i], e.j);
}

void Simulation::OutputEvents()
{
    std::cout << "== EVENTS == at t = " << gtime << " \n";
    h.print();
}

Eigen::MatrixX4d Simulation::Spheres()
{
    Eigen::MatrixX4d spheres(N, 4);
    for (int i = 0; i < N; i++)
    {
        spheres.block<1, 3>(i, 0) = s[i].x + s[i].v * (gtime - s[i].lutime);
        spheres(i, 3) = s[i].R(gtime);
    }
    return spheres;
}

double Simulation::Energy()
{
    double E = 0;
    for (const Sphere& si : s)
        E += 0.5 * si.m * si.v.squaredNorm();

    return E / N;
}

double Simulation::PackingFraction()
{
    double rfactor = 0.;
    for (const Sphere& si : s)
        rfactor += std::pow(si.R(gtime), 3);

    double v = rfactor * 4. / 3. * M_PI;
    return v / box.Volume();
}

void Simulation::ChangeNgrids(int newNGrids)
{
    cells.Resize(newNGrids);
    AssignCells();
    for (int i = 0; i < N; i++)
        nextevents[i] = Event(0., i, Event::Type::NONE);
    Process(N);
}

void Simulation::Process(int n)
{
    int n_collisions = stats.n_collisions;

    const double t = gtime;
    for (int i = 0; i < n; i++)
        ProcessEvent();

    int d_collisions = stats.n_collisions - n_collisions;

    stats.pf = PackingFraction(); // packing fraction

    double oldenergy = stats.energy;
    stats.energy = Energy(); // kinetic energy

    stats.energychange = ((oldenergy - stats.energy) / oldenergy);

    const double deltat = gtime - t;
    if (deltat != 0.)
    {
        stats.pressure = 1 + xmomentum / (2. * stats.energy * N * deltat);
        stats.collisionrate = d_collisions / deltat;
    }

    // reset to 0
    xmomentum = 0.;
}

void Simulation::Synchronize(bool rescale)
{
    double vavg = std::sqrt(2. * stats.energy);

    for (int i = 0; i < N; i++)
    {
        s[i].Update(gtime);
        s[i].r = s[i].R(gtime);
        s[i].lutime = 0.;
        nextevents[i].time -= gtime;

        assert(nextevents[i].time >= 0.);

        if (rescale)
        {
            nextevents[i] = Event(0., i, Event::Type::NONE);
            s[i].v /= vavg;
        }
    }

    rtime += gtime;
    gtime = 0.;

    if (rescale)
        // All events set to NONE. Processing N times will
        // find the next events for each sphere.
        Process(N);
}
