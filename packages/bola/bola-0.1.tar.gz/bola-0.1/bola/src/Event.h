#pragma once

#include <Eigen/Core>
#include <ostream>
#define dblINF 100000000.

class Event
{
public:
    enum Type
    {
        SPHERE,
        WALL,
        TRANSFER,
        RESIZE_GRID,
        NONE
    };

    Event(double time_i, int i_i, Type type_i, int j_i = -1)
        : time(time_i)
        , type(type_i)
        , i(i_i)
        , j(j_i)
    {
    }

    static Event SphereEvent(double t, int i, int j)
    {
        return Event(t, i, Event::Type::SPHERE, j);
    }

    static Event NoEvent(int i)
    {
        return Event(dblINF, i, Event::Type::NONE, -i);
    }

    Event() = default;

    bool operator<(const Event& e) const
    {
        return time < e.time;
    }

    friend std::ostream& operator<<(std::ostream& out, Event e)
    {
        out << "(t, i, j) = (" << e.time << " " << e.i << " " << e.j << "): ";
        out << e.TypeString();
        return out;
    }

    std::string TypeString() const
    {
        switch (type)
        {
        case Event::Type::SPHERE:
            return "SPHERE";
        case Event::Type::RESIZE_GRID:
            return "RESIZE";
        case Event::Type::TRANSFER:
            return "TRANSFER";
        case Event::Type::WALL:
            return "WALL";
        case Event::Type::NONE:
            return "NONE";
        }
        return ""; // mimimi reaches end of non-void function
    }

    // variables

    double time; // time of next collision
    Type type;
    int i; // always a sphere index. 0 <= i <  N
    int j; // meaning depends on type:
    /* SPHERE:
     * 0 <= j < N   collision between spheres i and j
     *
     *  WALL:
     * j = k        wall collision
     *
     * TRANSFER: f
     * j = k        transfer from one subbox to another
     *
     * RESIZE_GRID:
     * j = ?        i outgrows the subbox size
     *
     * NONE:
     * j = ?        event that only indicates that a new event for i
     *              has to be calculated.
     *              Events are set to NONE
     *                  - at the start of the simulation
     *                  - after a sphere collision of i and j for nextevent(j).j
     *                  - after rescaling the velocities
     *
     */
};
