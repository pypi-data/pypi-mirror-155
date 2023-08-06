/*
   Packing of hard spheres via molecular dynamics
   Developed by Monica Skoge, 2006, Princeton University
   Contact: Aleksandar Donev (adonev@math.princeton.edu) with questions
   This code may be used, modified and distributed freely.
   Please cite:

   "Packing Hyperspheres in High-Dimensional Euclidean Spaces"
        M. Skoge, A. Donev, F. H. Stillinger and S. Torquato, 2006

   if you use these codes.
*/

//-----------------------------------------------------------------------------
// Simulation maker
//---------------------------------------------------------------------------
#pragma once

#include <Eigen/Core>
#include <vector>

#include "Box.h"
#include "Event.h"
#include "Heap.h"
#include "Sphere.h"
#include "SubBoxes.h"

struct Stats
{
    int n_events = 0;
    int n_collisions = 0;
    int n_transfers = 0;
    int n_checks = 0;

    double energy = 0;
    double energychange = 0;
    double pf = 0;
    double pressure = 0;
    double collisionrate = 0;
};

class Simulation
{
public:
    // constructor and destructor
    Simulation(const Box& box, std::vector<Sphere> spheres);

    Simulation(const Box& box, Eigen::MatrixX4d sphereMatrix, Eigen::MatrixX3d velocities, Eigen::VectorXd growthRates,
               Eigen::VectorXd masses);

    // Creating configurations
    void SetInitialEvents();
    void AssignCells();

    // Predicting next Event
    Event PredictSphereVsWall(int i);

    void SetNextEvent(int i);
    void CollisionChecker(Event c);
    Event FindNextCollision(int i);

    // Processing an Event
    void Process(int n);
    void ProcessEvent();
    void ProcessSphereVsSphere(Event e);
    void ProcessSphereVsWall(Event e);
    void Synchronize(bool rescale);
    void ChangeNgrids(int newNGrids);

    // Debugging
    Eigen::MatrixX4d Spheres();
    void OutputEvents();
    void GetInfo();

    // Statistics
    double Energy();
    double PackingFraction();
    // variables

    double T()
    {
        return gtime + rtime;
    }

    const int N; // number of spheres
    const Box& box;

    int ngrids; // number of cells in one direction
    double gtime = 0; // this is global clock
    double rtime = 0; // reset time, total time = rtime + gtime

    // statistics
    double xmomentum = 0; // exchanged momentum
    Stats stats;

    // arrays
    std::vector<Sphere> s; // array of spheres
    std::vector<Event> nextevents;
    SubBoxes cells; // array that keeps track of spheres in each cell
    Heap h; // Event heap

    bool showResize = false;
    bool showEvents = false;
};

//! RSA algorithm implemented in RandomSequentialAddition.cpp
std::pair<Eigen::MatrixX4d, Eigen::VectorXi> RSA(Eigen::VectorXd radii, const Box& box, int seed, int maxTries,
                                                 bool progress);
