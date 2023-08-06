#include "Heap.h"
#include "Event.h"
#include <iostream>

Heap::Heap(const std::vector<Event>& nextevents)
    : maxsize(nextevents.size() + 1)
    , N(0)
    , nextevents(nextevents)
{
    a.resize(maxsize);
    index.resize(maxsize);
}

int Heap::Swap(int i, int j)
{
    a[i] = a[j];
    index[a[j]] = i;
    return j;
}

void Heap::upheap(int k)
{
    int i = a[k];
    while (k > 1)
    {
        const int parent = k / 2;
        if (nextevents[a[parent]].time <= nextevents[i].time)
            break;
        k = Swap(k, parent);
    }
    a[k] = i;
    index[i] = k;
}

void Heap::downheap(int k)
{
    int i = a[k];
    while (k <= N / 2)
    {
        // find smaller child (junior)
        // left would be right -1
        const int right = 2 * k + 1;
        const bool cond = right <= N && nextevents[a[right - 1]].time > nextevents[a[right]].time;
        const int jr = right - !cond;

        if (nextevents[i].time <= nextevents[a[jr]].time)
            break;
        k = Swap(k, jr);
    }
    a[k] = i;
    index[i] = k;
}

void Heap::insert(int i)
{
    if (N >= maxsize)
        std::runtime_error("error, N >= maxsize, cannot insert another event");
    N++;
    a[N] = i;
    index[i] = N;
    upheap(N);
}

int Heap::extractmax()
{
    return a[1];
}

void Heap::print()
{
    auto PrintEvent = [](Event e) {
        std::string type = "";
        if (e.type == Event::Type::SPHERE)
            type = "sphere";
        if (e.type == Event::Type::NONE)
            type = "none";
        if (e.type == Event::Type::TRANSFER)
            type = "transfer";
        if (e.type == Event::Type::WALL)
            type = "wall";
        std::cout << e.i << " " << e.j << " " << e.time << " " << type;
    };
    for (int k = 1; k <= N; k++)
    {
        std::cout << k << " ";
        PrintEvent(nextevents[a[k]]);
        std::cout << std::endl;
    }
}

void Heap::checkindex()
{
    for (int k = 1; k <= N; k++)
        if (k != index[a[k]])
            std::cout << "Index error for k = " << k << " " << a[k] << " " << index[a[k]] << std::endl;
}
