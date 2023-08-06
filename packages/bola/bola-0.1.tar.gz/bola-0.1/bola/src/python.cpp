#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Simulation.h"
#include "Velocity.h"

namespace py = pybind11;

PYBIND11_MODULE(_cpp, m)
{
    m.doc() = R"pbdoc(
        EDMD - Flying, growing and colliding spheres. 
        -----------------------
    )pbdoc";

    py::class_<Event> event(m, "Event");
    event.def_readonly("t", &Event::time);
    event.def_readonly("i", &Event::i);
    event.def_readonly("j", &Event::j);
    event.def_readonly("type", &Event::type);

    py::enum_<Event::Type>(event, "Type")
            .value("Sphere", Event::Type::SPHERE)
            .value("Wall", Event::Type::WALL)
            .value("Transfer", Event::Type::TRANSFER)
            .value("None", Event::Type::NONE)
            .value("Resize", Event::Type::RESIZE_GRID);

    py::class_<Box> box(m, "Box");
    box.def("predict_collision", &Box::PredictCollision);
    box.def("perform_collision", &Box::PerformCollision);
    box.def("volume", &Box::Volume);

    py::class_<Cube, Box> cube(m, "Cube");
    cube.def(py::init<double, double, double>());
    cube.def_readonly("l", &Cube::l);

    py::class_<Sphere> sphere(m, "Sphere");
    sphere.def(py::init<>());
    sphere.def_readwrite("x", &Sphere::x);
    sphere.def_readwrite("r", &Sphere::r);
    sphere.def_readwrite("v", &Sphere::v);
    sphere.def_readwrite("gr", &Sphere::gr);
    sphere.def_readwrite("m", &Sphere::m);
    sphere.def_readonly("id", &Sphere::id);

    sphere.def("predict_collision", &Sphere::PredictCollision);
    sphere.def("perform_collision", &Sphere::PerformCollision);
    sphere.def("update", &Sphere::Update);

    py::class_<Stats> stats(m, "Stats");
    stats.def_readonly("n_events", &Stats::n_events);
    stats.def_readonly("n_collisions", &Stats::n_collisions);
    stats.def_readonly("n_transfers", &Stats::n_transfers);
    stats.def_readonly("n_checks", &Stats::n_checks);
    stats.def_readonly("pf", &Stats::pf);
    stats.def_readonly("energy", &Stats::energy);
    stats.def_readonly("energychange", &Stats::energychange);
    stats.def_readonly("pressure", &Stats::pressure);
    stats.def_readonly("collisionrate", &Stats::collisionrate);

    py::class_<Simulation> simulation(m, "Simulation");
    simulation.def(py::init<const Box&, std::vector<Sphere>>());
    simulation.def(py::init<const Box&, Eigen::MatrixX4d, Eigen::MatrixX3d, Eigen::VectorXd, Eigen::VectorXd>());
    simulation.def("process", &Simulation::Process);
    simulation.def("process_event", &Simulation::ProcessEvent);
    simulation.def("synchronize", &Simulation::Synchronize);
    simulation.def("spheres", &Simulation::Spheres);
    simulation.def("t", &Simulation::T);

    simulation.def_readonly("stats", &Simulation::stats);

    simulation.def_readwrite("show_resize", &Simulation::showResize);
    simulation.def_readwrite("show_events", &Simulation::showEvents);

    py::class_<MaxwellBoltzmann> maxBoltz(m, "MaxwellBoltzmann");
    maxBoltz.def(py::init<int>());
    maxBoltz.def("component", &MaxwellBoltzmann::Component);
    maxBoltz.def("__call__", &MaxwellBoltzmann::Vector);

    m.def("rsa", &RSA);
}
