#ifndef QUEUE_H
#define QUEUE_H

class Click_Queue {
private:
public:
  std::vector<int> row = {};
  std::vector<int> col = {};
  Click_Queue() {};
  void enqueue(int row_, int col_);
  void print();
};

extern Click_Queue Queue;

#endif // QUEUE_H
