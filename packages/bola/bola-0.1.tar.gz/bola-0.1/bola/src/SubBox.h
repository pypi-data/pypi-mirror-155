#pragma once

#include <vector>
#include <algorithm>

class SubBox
{

public:
    void Add(int value)
    {
        auto it = std::lower_bound(data.begin(), data.end(), value);
        if (it == data.end() || value < *it)
            data.insert(it, value);
    }

    void Remove(int value)
    {
        auto range = std::equal_range(data.begin(), data.end(), value);
        data.erase(range.first, range.second);
    }

    bool Contains(int value) const
    {
        auto range = std::equal_range(data.begin(), data.end(), value);
        return range.first != range.second;
    }

    int Size() const
    {
        return data.size();
    }

    const std::vector<int>& Entries() const
    {
        return data;
    }

private:
    std::vector<int> data;
};
