class Queue:
    def __init__(self, limit) -> None:
        self.print_mode = False
        self.que = []
        self.limit = limit
        self.front = None
        self.rear = None
        self.size = 0
        
    def is_empty(self):
        return self.size <= 0
    
    def enqueue(self, item):
        if self.size >= self.limit:
            print('Queue overflow!')
            return
        else:
            self.que.append(item)
            
        if self.front is None:
            self.front = self.rear = 0
        else:
            self.rear = self.size
        
        self.size += 1
        
        if self.print_mode:
            print('Queue after enqueue', self.que)
        
    def dequeue(self):
        if self.size <= 0:
            print('Queue underflow!')
            return 0
        else:
            ret = self.que.pop()
            self.size -= 1
            if self.size == 0:
                self.front = self.rear = None
            else:
                self.rear = self.size - 1
                
            if self.print_mode:
                print('Queue after dequeue', self.que)
                
            return ret
            
    def queue_rear(self):
        if self.rear is None:
            print('Sorry, the queue is empty!')
            raise IndexError
        return self.que[self.rear]
            
    def queue_front(self):
        if self.front is None:
            print('Sorry, the queue is empty!')
            raise IndexError
        return self.que[self.front]
    
    def get_size(self):
        return self.size
    
if __name__ == '__main__':
    que = Queue(5)
    que.enqueue('first')
    print('Front: %s' % que.queue_front())
    print('Rear: %s' % que.queue_rear())
    que.enqueue('second')
    print('Front: %s' % que.queue_front())
    print('Rear: %s' % que.queue_rear())
    que.enqueue('third')
    print('Front: %s' % que.queue_front())
    print('Rear: %s' % que.queue_rear())
    que.dequeue()
    print('Front: %s' % que.queue_front())
    print('Rear: %s' % que.queue_rear())
    que.dequeue()
    print('Front: %s' % que.queue_front())
    print('Rear: %s' % que.queue_rear())