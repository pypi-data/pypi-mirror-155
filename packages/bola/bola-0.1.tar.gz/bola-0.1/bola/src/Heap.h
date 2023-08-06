//---------------------------------------------------------------------------
// Event Heap maker
//---------------------------------------------------------------------------
#pragma once

#include <vector>

class Event;
class Heap
{

public:
    // constructor and destructor
    Heap(const std::vector<Event>& nextevents);

    // variables
    int maxsize; // max allowed number of events
    int N; // current number of events
    std::vector<int> a;
    const std::vector<Event>& nextevents;
    std::vector<int> index; // array of indices for each sphere
    // event minevent;


    // functions which operate on a binary Heap

    void upheap(int k);
    void downheap(int k);
    void insert(int i);
    int extractmax();
    void print();
    void checkindex();

private:
    int Swap(int a, int b);
};
